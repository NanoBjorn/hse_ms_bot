from src.common.settings import DEADLINE_TIME, FOR_SETUP


class Setuper:
    def __init__(self):
        self._greetings = FOR_SETUP["greetings"]
        self._same_mail = FOR_SETUP["same_mail"]
        self._another_mail = FOR_SETUP["another_mail"]
        self._register = FOR_SETUP["register"]
        self._no_mail = FOR_SETUP["no_mail"]
        self._oauth_bad = FOR_SETUP["oauth_bad"]
        self._oauth_good = FOR_SETUP["oauth_good"]
        self._kick = FOR_SETUP["kick"]
        self._rights = FOR_SETUP["rights"]
        self._went_wrong = FOR_SETUP["went_wrong"]
        self._ban = FOR_SETUP["ban"]
        self._unban = FOR_SETUP["unban"]
        self._ignore = FOR_SETUP["ignore"]
        self._banned = FOR_SETUP["banned"]
        self._check = FOR_SETUP["check"]
        self._deadline = FOR_SETUP["deadline"]
        self._switch = FOR_SETUP["switch"]

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

    def switch(self):
        return self._switch
