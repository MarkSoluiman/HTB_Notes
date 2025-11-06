
---

## Validation of CSRF token depends on token being present

Some applications correctly validate the token when it is present but skip the validation if the token is omitted.

In this situation, the attacker can remove the entire parameter containing the token (not just its value) to bypass the validation and deliver a CSRF attack:

```
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 25
Cookie: session=2yQIDcpia41WrATfjPqvm9tOkDvkMvLm email=pwned@evil-user.net
```

---

## Lab: CSRF where token validation depends on token being present

This lab's email change functionality is vulnerable to CSRF.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

We can log in to our own account using the following credentials: `wiener:peter`

To solve this lab, we will capture an email update request and send it to the Repeater. Then, we will remove the :`&csrf=` part of the request then we will create the CSRF HTML code . We will copy this code to  the exploit server and we will change the email to something else then deliver the exploit to victim.



