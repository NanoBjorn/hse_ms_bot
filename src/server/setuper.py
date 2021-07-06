from src.common.settings import DEADLINE_TIME

class Setuper:
    def __init__(self):
        self._greetings = "@{username}, добро пожаловать! Для нахождения в чате необходимо пройти регистрацию. Для начала, отправь свою почту в следующем формате:\" /mail iiivanov@edu.hse.ru\"."
        self._same_mail = "Кто-то уже использует эту почту."
        self._another_mail = "Ты уже зарегистрирован по другой почте."
        self._register = "@{username}, пожалуйста, авторизируйся по рабочей почте: {link}"
        self._no_mail = "Не увидел твою почту. отправь свою почту в следующем формате:\" /mail iiivanov@edu.hse.ru\"."
        self._oauth_bad = "@{username}, во время регистрации что-то пошло не так. Еще раз отправь свою почту в формате:\" /mail iiivanov@edu.hse.ru\" и пройди регистрацию."
        self._oauth_good = "Регистрация прошла успешно."
        self._kick = "@{username} не зарегистрировался."
        self._rights = "У @{username} недостаточно прав."
        self._went_wrong = "Что-то пошло не так  ̄\_(ツ)_/ ̄."
        self._ban = "Пользователь был забанен."
        self._unban = "Пользователь был разбанен."
        self._ignore = "Успешно."
        self._banned = "@{username} в бане."
        self._check = "@{username}, для нахождения в чате необходимо пройти регистрацию. Для начала, отправь свою почту в следующем формате:\" /mail iiivanov@edu.hse.ru\"."
        self._deadline = DEADLINE_TIME

    def greetings(self, username, first_name, last_name):
        return eval("f\"" + self._greetings + "\"")

    def same_mail(self, username, first_name, last_name):
        return eval("f\"" + self._same_mail + "\"")

    def another_mail(self, username, first_name, last_name):
        return eval("f\"" + self._another_mail + "\"")

    def register(self, username, first_name, last_name, link):
        return eval("f\"" + self._register + "\"")

    def no_mail(self, username, first_name, last_name):
        return eval("f\"" + self._no_mail + "\"")

    def oauth_bad(self, username, first_name, last_name):
        return eval("f\"" + self._oauth_bad + "\"")

    def oauth_good(self, username, first_name, last_name):
        return eval("f\"" + self._oauth_good + "\"")

    def kick(self, username, first_name, last_name):
        return eval("f\"" + self._kick + "\"")

    def rights(self, username, first_name, last_name):
        return eval("f\"" + self._rights + "\"")

    def went_wrong(self, username, first_name, last_name):
        return eval("f\"" + self._went_wrong + "\"")

    def ban(self, username, first_name, last_name):
        return eval("f\"" + self._ban + "\"")

    def unban(self, username, first_name, last_name):
        return eval("f\"" + self._unban + "\"")

    def ignore(self, username, first_name, last_name):
        return eval("f\"" + self._ignore + "\"")

    def banned(self, username, first_name, last_name):
        return eval("f\"" + self._banned + "\"")

    def check(self, username, first_name, last_name):
        return eval("f\"" + self._check + "\"")

    def int_deadline(self):
        return int(self._deadline)