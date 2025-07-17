
---


## Account locking

As we saw with the last lab, one way to prevent attackers from brute-forcing into an account is by blocking them from attempting to login. Locking an account works the same. The attacker will not be able to login into the victim's account even after waiting. However, this method of protection is useless when is comes to logging into a random user.

We can have a list of potential usernames and a short list of passwords. No matte how many attempts we do, we will get valid credentials eventually.

Account locking also fails to protect against credential stuffing attacks. This involves using a massive dictionary of `username:password` pairs, composed of genuine login credentials stolen in data breaches. Credential stuffing relies on the fact that many people reuse the same username and password on multiple websites and, therefore, there is a chance that some of the compromised credentials in the dictionary are also valid on the target website. Account locking does not protect against credential stuffing because each username is only being attempted once.

---

## Lab: Username enumeration via account lock

This lab is vulnerable to username enumeration. It uses account locking, but this contains a logic flaw. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Unfortunately, this lab requires us to have the professional edition of BurpSuite since the Brute-force attack is too long and will take too much time. 

If we have the professional edition, this is how we can solve this lab.

If we try to login with any username and password multiple times, we see that the account doesn't get blocked. This makes perfect sense, since we need to attempt to login using a valid username to get this account blocked.

We will capture a POST request trying to login and send it to Intruder. We will choose the cluster bomb attack type. We will put a payload mark in the username field. In the password field, we will put two empty payload marks with any random password behind them, so the password field should look like this: password=test§§. In the first payload, we will put the list of usernames. The second payload will make it null payloads with 5 payloads to generate. 
This will make BurpSuite to try the same password five times with each username.

We will notice that one of the usernames gave us a different message, telling us that we are blocked for 1 minute.

This is a valid username.

To solve this lab, we simply need to brute-force the password against this username.

Indeed, we will get blocked with most of our attempts. However, for one of the attempts, we will get a response with no message at all. This is our password.