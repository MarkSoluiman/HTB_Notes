import hashlib
import base64

## read the file of passwords and turn into md5 hash
cookie_key="carlos:"
hashes=[]
with open ('passwords.txt','r') as file:
	for password in file:
		password=password.strip()
		md5_hash=hashlib.md5(password.encode()).hexdigest()
		hashes.append(md5_hash)
		

##create the cookie for carlos
for h in hashes:

	cookie=cookie_key+h

	#Convert the string into bytes and encode it

	encoded_cookie=base64.b64encode(cookie.encode('utf-8'))

	#Turn the bytes into a normal string:
	cookie=encoded_cookie.decode("utf-8")

	print (cookie)







