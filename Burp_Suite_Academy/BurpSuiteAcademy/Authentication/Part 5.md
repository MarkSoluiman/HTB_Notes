
---

## Flawed two-factor verification logic

Sometimes flawed logic in two-factor authentication means that after a user has completed the initial login step, the website doesn't adequately verify that the same user is completing the second step.

For example, the user logs in with their normal credentials in the first step as follows:

`POST /login-steps/first HTTP/1.1
Host: vulnerable-website.com
...
username=carlos&password=qwerty`

They are then assigned a cookie that relates to their account, before being taken to the second step of the login process:

`HTTP/1.1 200 OK
Set-Cookie: account=carlos
GET /login-steps/second HTTP/1.1
Cookie: account=carlos`

When submitting the verification code, the request uses this cookie to determine which account the user is trying to access:
`POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=carlos
... 
verification-code=123456`


In this case, an attacker can change the cookie value to the victim's username and brute-force their way to the right verification code:
`POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=victim-user
... 
verification-code=123456`

---

## Lab: 2FA broken logic

This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`

You also have access to the email server to receive your 2FA verification code.

To solve this lab, we will need to login with our credentials and capture requests for every step that we do until we login to our user.

We will eventually capture a request that contains the cookie value which is our username and the 2FA code that we need to login to our user.

We can now send this request to intruder and simply change the cookie value to the victim's username and we will brute-force the 2FA code. 

However, before we launch our brute-force attack, we need to send a request to the website from the request in login2 page. We will send this to the Repeater and change the Cookie value from our username to the victim's username and we will also delete the session completely. This will send the victim's the 2FA code.

If we didn't do this step, we will never bypass the 2FA step.

