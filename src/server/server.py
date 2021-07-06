import logging
import telebot
import time
import json
from base64 import b64decode
from flask import Flask, request, abort, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from src.common.settings import TG_URL_PATH, WORKER_URL_PATH, MS_ANS_PATH, DEBUG, EXTERNAL_HOST, SETUP_PATH, \
    SETUP_PASSWORD
from src.common.utils import get_ngrok_url
from src.server.bot import ms_ans, deadline_kick
from src.server.setuper import Setuper

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SetupForm(FlaskForm):
    greetings = StringField("Приветствие:",
                            default="@{username}, добро пожаловать! Для нахождения в чате необходимо пройти регистрацию. Для начала, отправь свою почту в следующем формате:\\\" /mail iiivanov@edu.hse.ru\\\".")
    same_mail = StringField("Есть другой user_id с такой почтой:", default="Кто-то уже использует эту почту.")
    another_mail = StringField("User уже зареган по другой почте:",
                               default="Ты уже зарегистрирован по другой почте.")
    register = StringField("Проверяем почту (обязательно нужен {link}):",
                           default="@{username}, пожалуйста, авторизируйся по рабочей почте: {link}")
    no_mail = StringField("/mail без почты:",
                          default="Не увидел твою почту. отправь свою почту в следующем формате:\\\" /mail iiivanov@edu.hse.ru\\\".")
    oauth_good = StringField("OAUTH сказал, что всё хорошо:", default="Регистрация прошла успешно.")
    oauth_bad = StringField("OAUTH сказал, что всё плохо:",
                            default="@{username}, во время регистрации что-то пошло не так. Еще раз отправь свою почту в формате:\\\" /mail iiivanov@edu.hse.ru\\\" и пройди регистрацию.")
    kick = StringField("Вышло время регистрации:", default="@{username} не зарегистрировался.")
    rights = StringField("/ban, /ignore, /unban отправил не админ:", default="У @{username} недостаточно прав.")
    went_wrong = StringField("C /ban, /ignore, /unban что-то сломалось:", default="Что-то пошло не так  ̄\_(ツ)_/ ̄.")
    ban = StringField("Cлучился /ban @username:", default="Пользователь был забанен.")
    unban = StringField("Cлучился /unban @username:", default="Пользователь был разбанен.")
    ignore = StringField("Cлучился /ignore @username:", default="Успешно.")
    banned = StringField("Забаненый юзер зашел в чат или написал сообщение:", default="@{username} в бане.")
    deadline = StringField("Время, через которое пользователь будет удален (в минутах)", default="1")
    check = StringField("Пользователь не прошел проверку:",
                        default="@{username}, для нахождения в чате необходимо пройти регистрацию. Для начала, отправь свою почту в следующем формате:\\\" /mail iiivanov@edu.hse.ru\\\".")
    password = StringField("Ключ для подтверждения:")
    switch = RadioField("Проверять все сообщения пользователей:", choices=[(True, "Да"), (False, "Нет")], default=False)
    submit = SubmitField("Submit")


class Server(Flask):
    def __init__(self, name: str, tg_bot: telebot.TeleBot, setuper: Setuper):
        super().__init__(name)
        self._tg_bot = tg_bot
        self._setuper = setuper
        urls = [
            (TG_URL_PATH, self.handle_tg, {'methods': ['POST']}),
            (WORKER_URL_PATH, self.trigger, {'methods': ['GET']}),
            (MS_ANS_PATH, self.ms_ans, {'methods': ['POST']}),
            (SETUP_PATH, self.setup, {'methods': ['GET', 'POST']})
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def handle_tg(self):
        if request.headers.get('content-type') == 'application/json':
            logger.debug(request.get_json())
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            self._tg_bot.process_new_updates([update])
            return ''
        else:
            abort(403)

    def trigger(self):
        deadline_kick()
        return 'Well done!'

    def ms_ans(self):
        req = json.loads(b64decode(request.get_json()['data']).decode('ascii'))
        if req["status"] == '1':
            ms_ans(req["mail"], req["user_id"], req["chat_id"], 1)
        else:
            ms_ans(req["mail"], req["user_id"], req["chat_id"], 0)
        return 'Well done!'

    def setup(self):
        form = SetupForm()
        if form.validate_on_submit():
            if str(form.password.data) == SETUP_PASSWORD:
                self._setuper._greetings = form.greetings.data
                self._setuper._same_mail = form.same_mail.data
                self._setuper._another_mail = form.another_mail.data
                self._setuper._register = form.register.data
                self._setuper._no_mail = form.no_mail.data
                self._setuper._oauth_good = form.oauth_good.data
                self._setuper._oauth_bad = form.oauth_bad.data
                self._setuper._kick = form.kick.data
                self._setuper._rights = form.rights.data
                self._setuper._went_wrong = form.went_wrong.data
                self._setuper._ban = form.ban.data
                self._setuper._unban = form.unban.data
                self._setuper._ignore = form.ignore.data
                self._setuper._banned = form.banned.data
                self._setuper._check = form.check.data
                self._setuper._deadline = form.deadline.data
                self._setuper._switch = form.switch.data
                print(self._setuper._switch)
            form.password.data = ""

        return render_template('index.html', form=form, setuper=self._setuper)

    def run_server(self):
        if DEBUG.find('ngrok') != -1:
            # Comment all lines up to `app.run` in case you ran it at least once
            # for one ngrok server_dir to avoid setting same link as telegram webhook

            ngrok_url = get_ngrok_url() + TG_URL_PATH
            wh_info = self._tg_bot.get_webhook_info()
            logger.debug(wh_info)
            if wh_info.url != ngrok_url:
                assert self._tg_bot.remove_webhook()
                time.sleep(1)
                assert self._tg_bot.set_webhook(ngrok_url)
            logger.debug(self._tg_bot.get_webhook_info())
            super().run(host='0.0.0.0', port=8000, debug=True)

        else:
            url = 'https://' + EXTERNAL_HOST + TG_URL_PATH
            wh_info = self._tg_bot.get_webhook_info()
            logger.debug(wh_info)
            if wh_info.url != url:
                assert self._tg_bot.remove_webhook()
                # logger.debug('public url = %s', url)
                time.sleep(1)
                assert self._tg_bot.set_webhook(url)
            logger.debug(self._tg_bot.get_webhook_info())
            if DEBUG:
                super().run(host='0.0.0.0', port=8000, debug=True)
            else:
                super().run(host='0.0.0.0', port=8000)
