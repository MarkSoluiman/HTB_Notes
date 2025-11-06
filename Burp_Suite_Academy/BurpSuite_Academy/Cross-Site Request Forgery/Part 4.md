
---

## CSRF token is not tied to the user session

Some applications do not validate that the token belongs to the same session as the user who is making the request. Instead, the application maintains a global pool of tokens that it has issued and accepts any token that appears in this pool.

In this situation, the attacker can log in to the application using their own account, obtain a valid token, and then feed that token to the victim user in their CSRF attack.

---

## Lab: CSRF where token is not tied to user session

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't integrated into the site's session handling system.

To solve the lab, we will use our exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

We have two accounts on the application that we can use to help design your attack. The credentials are as follows:

- `wiener:peter`
- `carlos:montoya`

To solve this lab, we will need to capture both of the email updates logging in for both users and send them to the Repeater. We will use the CSRF token of wiener to change carlos email. (We can do this the vise-versa). We will copy the CSRF of wiener. Then, we will create the HTML CSRF attack for carlos and copy paste it to the exploit server. Before we send the exploit, we will replace the CSRF of carlos with wiener's one. This should change the email of carlos despite using the wrong CSRF.