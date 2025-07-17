
---

## Resetting User Passwords

In practice, some people will need to reset their passwords after forgetting them. Since password-based authentication is not possible in this scenario, websites have to rely on alternative methods to authenticate the user who is trying to change their password. 

Every method has its own vulnerability.

## Sending passwords by email

It should go without saying that sending users their current password should never be possible if a website handles passwords securely in the first place. Instead, some websites generate a new password and send this to the user via email.

Generally speaking, sending persistent passwords over insecure channels is to be avoided. In this case, the security relies on either the generated password expiring after a very short period, or the user changing their password again immediately. Otherwise, this approach is highly susceptible to man-in-the-middle attacks.

Email is also generally not considered secure given that inboxes are both persistent and not really designed for secure storage of confidential information. Many users also automatically sync their inbox between multiple devices across insecure channels.

## Resetting passwords using a URL

A more robust method is to send a unique URL to users that takes them to a password reset page. Less secure implementation of this method use a URL with an easily guessable parameter to identify which account is being reset, for example:`http://vulnerable-website.com/reset-password?user=victim-user`
In this example, an attacker could change the user parameter to refer to any username they have identified. This URL will take them straight to the password reset page of that user without proper authentication. 

A better way of implementing this process is to generate a high-entropy, hard-to-guess token and create the reset URL based on that. 

When the user visits this URL, the system should check whether this token exists on the back-end and, if so, which user's password is should reset. This token should expire after a short period of time and be destroyed immediately after the password has been reset.

However, some websites fail to validate the token again when the reset form is submitted. In this case, the attacker could visit the reset form from their account, delete the token, and leverage this page to reset an known user's password.

---

## LAB (Password reset broken logic)

This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos's password then log in and access his "My account" page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`

To solve this lab, we simply need to capture the new password reset request after submitting the new password in the form.

We will first login with our user's credentials. Then, we will attempt to reset a new password and go through the process of doing so. Once we are on the new password reset page, we will start BurpSuite to capture the new password request. Once we capture the request, we will send it to the Repeater. We will just need to change the user name from wiener to carlos and click send. Since the logic of the website is broken, the user carlos password is has now been changed.

---

If the URL in the reset email is generated dynamically, this may also be vulnerable to password reset poisoning. In this case, an attacker can potentially steal another user's token and use it change their password.

## LAB (Password reset poisoning via middleware)

This lab is vulnerable to password reset poisoning. The user `carlos` will carelessly click on any links in emails that he receives. To solve the lab, log in to Carlos's account. You can log in to your own account using the following credentials: `wiener:peter`. Any emails sent to this account can be read via the email client on the exploit server.

To solve this lab, we will need to capture multiple requests and send them to the Repeater. First, we will attempt to reset new password for our target user. We will capture this request and send it to the Repeater.

This will send carlos a link to his email to reset his password. However, we will add this part to the request and send click send in Repeater: `X-Forwarded-Host: exploit-0aa000fd0487b083806c2fcc01eb003f.exploit-server.net` This will send us the temp-forgot-password-token value which is unique to the user carlos and we will be able to see this in the log of the exploit server. 

We will copy the token value.

Next, we will attempt to reset our password. We will capture the request from the reset password form and send it to the Repeater. We will replace the token value with carlo's and click send. This will change the password for carlos instead of our user.
