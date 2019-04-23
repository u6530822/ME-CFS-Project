import GUI_bk

class LoginCheck:
	def __init__(self, uname, pswd):
		self.uname = uname
		self.pswd = pswd

	def check_login(self):
		if (self.uname == "test" and self.pswd == "test"):
			return 1
		else:
			return 0
