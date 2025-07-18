
---

## User rate limiting

Another way websites try to prevent brute-force attacks is through user rate limiting. In this case, making too many login requests within a short period of time causes your IP address to be blocked. Typically, the IP can only be unblocked in one of the following ways:

- Automatically after a certain period of time has elapsed
- Manually by an administrator
- Manually by the user after successfully completing a CAPTCHA

As the limit is based on the rate of HTTP requests sent from the user's IP address, it is sometimes also possible to bypass this defense if we can work out how to guess multiple passwords with a single request.


---

## HTTP basic authentication

Although fairly old, we might sometimes see HTTP basic authentication being used since it is easy to be implemented.

In HTTP basic authentication, the client receives an authentication token from the server, which is constructed by concatenating the username and password, and encoding it in Base64. This token is stored and managed by the browser, which automatically adds it to the Authorization header of every subsequent request as follows: `Authorization: Basic base64(username:password)`

This is not secure for multiple reasons. Firstly, it involves repeatedly sending the user's credentials with every request. Unless the website also implements HSTS, user credentials are open to being captured in a man-in-the-middle attack.

In addition, implementations of HTTP basic authentication often don't support brute-force protection. As the token consists exclusively of static values, this can leave it vulnerable to being brute-forced.

HTTP basic authentication is also particularly vulnerable to session-related exploits, notably CSRF, against which it offers no protection on its own.

In some cases, exploiting vulnerable HTTP basic authentication might only grant an attacker access to a seemingly uninteresting page. However, in addition to providing a further attack surface, the credentials exposed in this way might be reused in other, more confidential contexts.

---

## Vulnerabilities in multi-factor authentication

Verifying biometric factors is impractical for most websites. However, it is increasingly common to see both mandatory and optional two-factor authentication (2FA) based on **something you know** and **something you have**. This usually requires users to enter both a traditional password and a temporary verification code from an out-of-band physical device in their possession.

If 2FA is poorly implemented, it can be beaten or bypassed entirely just as single-factor authentication can.

---
## Two-factor authentication tokens

Verification codes are usually read by the user from a physical device. Many high-security websites now provide users with a dedicated device for this purpose, such as the RSA token or keypad device that a user might use to access their online banking or work laptop. It is also common for websites to use a dedicated mobile app such as Google Authentication for the same reason.

On the other hand, some websites send verification codes to a user's mobile phone as a text message. While this is technically still verifying the factor of "something you have", it is open to abuse. Firstly, the code is being transmitted via SMS rather than being generated by the device itself. This creates the potential for the code to be intercepted. There is also a risk of SIM swapping, whereby an attacker fraudulently obtains a SIM card with the victim's phone number. The attacker would then receive all SMS messages sent to the victim, including the one containing their verification code.

---

## Bypassing two-factor authentication

If the user is first prompt to enter a password, and then prompted to enter a verification code on a separate page, the user is effectively in a "logged in" state even before they have entered the verification code. In this case, we can test to see if we can directly skip to "logged-in only" pages after completing the first authentication step. Occasionally, we will find that a website doesn't actually check whether or not we completed the second step before loading the page.

---

## Lab: 2FA simple bypass


This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.

- Your credentials: `wiener:peter`
- Victim's credentials `carlos:montoya`

To solve this lab, we need to login with our credentials and observe how the website reacts. 

We will login with our credentials first. The website will ask us to provide 4 digit code as 2FA. We can obtain this code if we clicked on user Email button. We will see our email inbox with the 2FA code that we need to provide. After providing the 2FA code, we will be logged in to our user account. We notice something interesting, when we are logged in, the end of the URL is this: "/my-account?id=wiener" .  What if we try to change the user name with our victim username after using the victims credentials.  

This works. We are logged in to our victim's account without providing the 2FA code that was sent to the victim's email inbox
