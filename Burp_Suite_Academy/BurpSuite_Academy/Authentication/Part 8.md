
---

## Changing user passwords

Typically, changing your password involves entering your current password and then the new password twice. These pages fundamentally rely on the same process for checking that usernames and current passwords match as a normal login page does. Therefore, these pages can be vulnerable to the same techniques.

Password change functionality can be particularly dangerous if it allows an attacker to access it directly without being logged in as the victim user. For example, if the username is provided in a hidden field, an attacker might be able to edit this value in the request to target arbitrary users. This can potentially be exploited to enumerate usernames and brute-force passwords.

---

## Lab (Password brute-force via password change)


This lab's password change functionality makes it vulnerable to brute-force attacks. To solve the lab, use the list of candidate passwords to brute-force Carlos's account and access his "My account" page.

- Your credentials: `wiener:peter`
- Victim's username: `carlos`
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

To solve this lab, we will need to see how will the change the password page will act if we provided it with the wrong current password with matching new passwords. We will be logged out and prevented to login again for a minute. However, If we provided a wrong password with not matching password, we will be still logged in with a message saying that we have the wrong password. If we provided the page with the right current password with not matching passwords, we will get a different message saying that new passwords have to match.

This is the key to solve this lab. We will first capture a request trying to change the password for our current user providing the right current password with not matching new passwords.

We will send the request that we have captured to Intruder. We will change the username field to carlos, then we will brute force the current password filed. We should get a response saying that new passwords have to match when we get the right password.