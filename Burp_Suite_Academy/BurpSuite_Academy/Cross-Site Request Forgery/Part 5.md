
---

## CSRF token is tied to a non-session cookie

In a variation on the preceding vulnerability, some applications do tie the CSRF token to a cookie, but not to the same cookie that is used to track sessions. This can easily occur when an application employs two different frameworks, one for session handling and one for CSRF protection, which are not integrated together:

```
POST /email/change HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 68
Cookie: session=pSJYSScWKpmC60LpFOAHKixuFuM4uXWF; csrfKey=rZHCnSzEp8dbI6atzagGoSYyqJqTz5dv 

csrf=RhV7yQDO0xcq9gLEah2WVbmuFqyOq7tY&email=wiener@normal-user.com
```

This situation is harder to exploit but is still vulnerable. If the website contains any behavior that allows an attacker to set a cookie in a victim's browser, then an attack is possible. The attacker can log in to the application using their own account, obtain a valid token and associated cookie, leverage the cookie-setting behavior to place their cookie into the victim's browser, and feed their token to the victim in their CSRF attack.

---
## Lab: CSRF where token is tied to non-session cookie

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.

To solve the lab, we will use our exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

We have two accounts on the application that we can use to help design our attack. The credentials are as follows:
- `wiener:peter`
- `carlos:montoya`

We will need to login as both users and will make carlos act as the attacker and wiener as the victim. 

After capturing an update email request for the victim, we will notice a CSRF token and a CSRFKey as a cookie. 

We will test if both of these values are tied to each other. 

We will first submit an invalid CSRF token while keeping the original CSRFKey. This will result in an error message saying that invalid CSRF token. We will do the same with the CSRFKey while keeping the original CSRF token. Again, we will get an invalid CSRF token error. Now, we know that these values are related to each other.

Another test we will do is that we will submit a session value of our user instead of the session value of the victim. In order to get a new session value for our user carlos, we will open a new incognito tab and login as carlos and we will capture the update email request. We will take the Cookie session value and put it instead of the victim session value and we will send the request as the victim user. This will work. That means the CSRF token and the CSRFKey values are not related to the session value. 

In order for us to perform this vulnerability, we need to perform two things: 
1. Inject a CSRFKey Cookie in the user's session (HTTP Header injection).
2. Send a CSRF attack to the victim with a known CSRF token.

That needs to be done in one step.

We will need to find a place to put our malicious HTTP Header injection in.

We will notice a search bar in the Home page.

We will search for a random word like hat. After searching, a new Cookie value will be added in the response: LastSearchTerm=hat.

We will send the search request to Repeater to begin our HTTP Header injection attack. The payload will look like this: `GET /?search=hat%0d%0aSet-Cookie:%20csrfKey=abQVvk1C68mdJ0FKnSZLeHU6U7e2PYbe%3b%20SameSite=None`

If we sent this, we will get a 200 OK response with the csrfKey Cookie value changed to the one that we specified.

Now, back to the victim update email request, we will create the PoC. We will replace the CSRF token value with ours. 

Since we don't just want to automatically submit the request, we will replace the submission part which is going to be between two `<script>` tags with the following: `<img src="https://0a30003203ebc49880bead9f002e00a6.web-security-academy.net/?search=hat%0d%0aSet-Cookie:%20csrfKey=(our csrfKey value)%3b%20SameSite=None" onerror="document.forms[0].submit()"/>`

We also change the value of the csrf in the form to our csrf token value.

Note that we also want `SameSite=None` in there to have the browser send the cookie, regardless if the request originated from the same site or a separate, third-party site. Otherwise it won’t work

If we deliver this exploit to the victim, we will solve the lab.









victime:1asAkpzKS86dYPIrjHOu9Lwx6R5HiAEL

attacker: csrfKey:abQVvk1C68mdJ0FKnSZLeHU6U7e2PYbe
csrf:QxMSDzfZ1IDObVXiN0BrZAgP9iJdCOrH

