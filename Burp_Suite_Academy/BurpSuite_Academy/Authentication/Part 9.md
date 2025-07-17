
---

## Take care with user credentials


Even the most robust authentication mechanisms are ineffective if we unwittingly disclose a valid set of login credentials to an attacker. It should go without saying that we should never send any login data over unencrypted connections. Although we may have implemented HTTPS for our login requests, we need to make sure that we enforce this by redirecting any attempted HTTP requests to HTTPS as well.

We should also audit your website to make sure that no username or email addresses are disclosed either through publicly accessible profiles or reflected in HTTP responses, for example.

## Don't count on users for security

Strict authentication measures often require some additional effort from our users. Human nature makes it all but inevitable that some users will find ways to save themselves this effort. Therefore, we need to enforce secure behavior wherever possible.

The most obvious example is to implement an effective password policy. Some of the more traditional policies fall down because people crowbar their own predictable passwords into the policy. Instead, it can be more effective to implement a simple password checker of some kind, which allows users to experiment with passwords and provides feedback about their strength in real time. A popular example is the JavaScript library `zxcvbn`, which was developed by Dropbox. By only allowing passwords which are rated highly by the password checker, we can enforce the use of secure passwords more effectively than we can with traditional policies.

## Prevent username enumeration

It is considerably easier for an attacker to break our authentication mechanisms if we reveal that a user exists on the system. There are even certain situations where, due to the nature of the website, the knowledge that a particular person has an account is sensitive information in itself.

Regardless of whether an attempted username is valid, it is important to use identical, generic error messages, and make sure they really are identical. We should always return the same HTTP status code with each login request and, finally, make the response times in different scenarios as indistinguishable as possible.

## Implement robust brute-force protection

Given how simple constructing a brute-force attack can be, it is vital to ensure that we take steps to prevent, or at least disrupt, any attempts to brute-force logins.

One of the more effective methods is to implement strict, IP-based user rate limiting. This should involve measures to prevent attackers from manipulating their apparent IP address. Ideally, we should require the user to complete a CAPTCHA test with every login attempt after a certain limit is reached.

## Triple-check verification logic

As demonstrated by the labs, it is easy for simple logic flaws to creep into code which, in the case of authentication, have the potential to completely compromise our website and users. Auditing any verification or validation logic thoroughly to eliminate flaws is absolutely key to robust authentication. A check that can be bypassed is, ultimately, not much better than no check at all.

## Don't forget supplementary functionality

We must be sure not to just focus on the central login pages and overlook additional functionality related to authentication. This is particularly important in cases where the attacker is free to register their own account and explore this functionality. We need to remember that a password reset or change is just as valid an attack surface as the main login mechanism and, consequently, must be equally as robust.

## Implement proper multi-factor authentication

While multi-factor authentication may not be practical for every website, when done properly it is much more secure than password-based login alone. Verifying multiple instances of the same factor is not true multi-factor authentication. Sending verification codes via email is essentially just a more long-winded form of single-factor authentication.

SMS-based 2FA is technically verifying two factors (something you know and something you have). However, the potential for abuse through SIM swapping, for example, means that this system can be unreliable.

Ideally, 2FA should be implemented using a dedicated device or app that generates the verification code directly. As they are purpose-built to provide security, these are typically more secure.

Finally, just as with the main authentication logic, we need to make sure that the logic in our 2FA checks is sound so that it cannot be easily bypassed.