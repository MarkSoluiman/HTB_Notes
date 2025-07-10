
---

## Flawed brute-force protection

Brute-force protection revolves around trying to make it as tricky as possible to automate a brute-force attack and slow down the rate of failed attempts. 

The two most common ways of preventing brute-force attacks are:

Locking the account that the remote user is trying to access if they make too many failed login attempts.

Blocking the remote user's IP address if they make too many login attempts in quick succession.

Neither of them is invulnerable, especially if implemented using flawed logic.

For example, we might sometimes find that our IP is blocked if we fail to log in too many times. In some implementations, the counter for the number of failed attempts resets if the IP owner logs in successfully. That means an attacker can login using their own account every few login attempts to prevent this limit from being reached.

---

## LAB - Broken brute-force protection, IP block

**This lab is vulnerable due to a logic flaw in its password brute-force protection. To solve the lab, brute-force the victim's password, then log in and access their account page.**

**Your credentials: wiener:peter
Victim's username: carlos
Use Candidate passwords**

To solve this lab, we will need to figure out first how many times we can try to login with wrong credentials before being blocked from attempting more.

We find out that after the third attempt, we are prevented from logging in and we need to wait for a minute. 

The trick is that to come up with a script to write for us our password every third word after going through the password list that we have along with writing our username every third Carlos word.

The code for this in Python: 
```
print ("The following usernames:")


for i in range (150):

	if i % 3:
		print("carlos")
	else:
		print("wiener")


print("The follwing passwords:")

with open('passwordslist.txt','r') as f:
	lines=f.readlines()

i=0

for pwd in lines:
	if i%3:
		print(pwd.strip('\n'))
		
	else:
		print("peter")
		print(pwd.strip('\n'))
		i+=1
	i+=1

#To let us know how many times we need to print both of usernames to match with our passwrods list
print("number of tries:",i)
```


We will catch a login request then send it to Intruder.  Using Pitch Fork attack, we will put two payload markers on the user name and password. In the first payload we will put the usernames list that we get. We need to put our valid username first so BurpSuite doesn't attempt to login with empty credentials. The same goes to the password.

After running the attack, we will get the right password for carlos. The response should be 302 for the username carlos.

