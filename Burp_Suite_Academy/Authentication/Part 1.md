
---

## What is authentication?

Authentication is the process of verifying the identity of a user. Since websites are exposed to anyone connected to the internet, robust auth mechanisms are a must to effective web security.

There are three types of auth:

1. Something you know, such as a password or the answer to a security question. These are sometimes called "knowledge factors".
2. Something you have, This is a physical object such as a mobile phone or security token. These are sometimes called "possession factors".
3. Something you are or do. For example, your biometrics or patterns of behavior. These are sometimes called "inherent factors".


---

## What is the difference between authentication and authorization?

Authentication is the process of verifying the identity of the user. While authorization is verifying whether the user is allowed to do something.

For example, authentication determines whether someone attempting to access a website with the username Carlos123 really is the same person who created the account.

Once Carlos123 is authenticated, their permissions determine what they are authorized to do. For example, they may be authorized to access personal information about other users, or perform actions such as deleting another user's account.

---

## Vulnerabilities in password-based login


For websites that adopt a password-based login process, users either register for an account themselves or assigned with an account by admin. This account is accessed by a unique set of credentials.

This means that the security of the website is compromised if an attacker is able to either obtain or guess the login credentials of another user.

This can be achieved in a number of ways. The following sections show how an attacker can use brute-force attacks, and some of the flaws in brute-force protection. We'll also learn about the vulnerabilities in HTTP basic authentication.

### Brute-Force Attack:

A brute-force attack is when an attacker uses a system of trial and error to guess valid user credentials. These attacks are typically automated using wordlists of usernames and passwords. Automating this process, especially using dedicated tools, potentially enables an attacker to make vast numbers of login attempts at high speed.

### Brute-forcing usernames:

Usernames are easy to guess especially if they are related to a recognizable pattern, an email address for an example. It is very common to see businesses logins in the format of firstname.lastname@companyname.com. However, even if there is no obvious pattern, sometimes even high-privileged accounts are created using predictable usernames, such as admin or administrator.

During auditing, we check whether the website shows potential usernames publicly. For example, Are we able to access user profiles without logging in? Even if the actual content of the profiles is hidden, the name used in the profile is sometimes the same as the login username. We should also check for HTTP responses to see if any email address is shown.

### Username enumeration:

Username enumeration is when an attacker is able to observe changes in the websites behavior in order to identify whether a given username is valid.

For example, in login forms, if we entered a valid username but incorrect password, or a in registration forms, if we entered an already taken username, the website will let us know. This greatly reduces the time and effort required to brute-force a login because the attacker is able to quickly generate a shortlist of valid usernames.

While attempting to brute-force a login page, we should pay attention to any differences in :

Status codes: During a brute-force attack, the returned HTTP status code is likely to be the same for the vast majority of guesses because most of them will be wrong. If a guess returns a different status code, this is a strong indication that the username was correct. It is best practice for websites to always return the same status code regardless of the outcome, but this practice is not always followed.

Error messages: Sometimes the returned error message is different depending on whether both the username AND password are incorrect or only the password was incorrect. It is best practice for websites to use identical, generic messages in both cases, but small typing errors sometimes creep in. Just one character out of place makes the two messages distinct, even in cases where the character is not visible on the rendered page.


Response times: If most of the requests were handled with a similar response time, any that deviate from this suggest that something different was happening behind the scenes. This is another indication that the guessed username might be correct. For example, a website might only check whether the password is correct if the username is valid. This extra step might cause a slight increase in the response time. This may be subtle, but an attacker can make this delay more obvious by entering an excessively long password that the website takes noticeably longer to handle.

---

## LAB - Username enumeration via different responses

**This lab is vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

**Candidate usernames
Candidate passwords
To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.**

In order to solve this lab, we will use BurpSuite.

Also, we will use both of the wordlists provided for us:

We will try to login using any username and password and capture the POST request.

We will send the request to Intruder to start the Brute-force attack.

We will replace the username and password with a payload marker while choosing cluster bomb attack type. In the payloads tab, we will add the list of both of the wordlists in their respectful places. Then, we press Attack.

After a while, we will notice a different response with credentials: athena:123456.

If we try to login using these credentials, we will find that these are the right credentials.

