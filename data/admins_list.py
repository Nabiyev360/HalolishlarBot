from loader import db


def ADMINS():
	admins = []
	for user in db.get_admins():
		admins.append(user[0])
	return admins