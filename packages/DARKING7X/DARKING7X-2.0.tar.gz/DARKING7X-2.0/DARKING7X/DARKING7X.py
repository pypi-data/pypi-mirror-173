from LegendsLIB import *
from gdolib import *
from VENOMgetREST import *
def HITS(email):
	if('@gmail.com')in email:
		check = check_email.instagram(email)
		if check['status']=='Success':
			check = mails.gmail(email)
			if check==True:
				return True
			else:
				return False
		else:
			return False
	elif('@hotmail.com')in email:
		check = check_email.instagram(email)
		if check['status']=='Success':
			check = mails.hotmail(email)
			if check==True:
				return True
			else:
				return False
		else:
			return False
	elif('@yahoo.com')in email:
		check = check_email.instagram(email)
		if check['status']=='Success':
			check = mails.yahoo(email)
			if check==True:
				return True
			else:
				return False
		else:
			return False
	elif('@aol.com')in email:
		check = check_email.instagram(email)
		if check['status']=='Success':
			check = mails.aol(email)
			if check==True:
				return True
			else:
				return False
		else:
			return False
	elif('@outlook.com')in email:
		check = check_email.instagram(email)
		if check['status']=='Success':
			check = mails.outlook(email)
			if check==True:
				return True
			else:
				return False
		else:
			return False
def info(email):
				user = email.split('@')[0]
				info = A7X.info(user)
				name=info["Name"]
				user=info["User"]
				folwing=info["Followers"]
				folowers=info["Followors"]
				ID=info["ID"]
				privet=info["Privacy"]
				rest=VENOM.get_rest(user)
				date=info["Date"]
				bio=info["Bio"]
				X=f'''
 🌀𝗡𝗔𝗠𝗘:{name} 
 ❄𝗨𝗦𝗘𝗥:{user} 
 ⛈️𝗠𝗔𝗜𝗟:{email} 
 🍀𝗙𝗢𝗟𝗟𝗢𝗪𝗜𝗡𝗚: {folowing}
  🔭𝗙𝗢𝗟𝗟𝗢𝗪𝗘𝗥𝗦: {folowers} 
 🆔 𝗜𝗗:{ID} 
 🌇𝗥𝗘𝗦𝗧:{rest} 
 ☢️𝗣𝗥𝗜𝗩𝗔𝗧𝗘:{privet} 
 🧾𝗗𝗔𝗧𝗘:{date} 
 ☣️𝗕𝗜𝗢:{bio} 𖢒
 '''
				return X