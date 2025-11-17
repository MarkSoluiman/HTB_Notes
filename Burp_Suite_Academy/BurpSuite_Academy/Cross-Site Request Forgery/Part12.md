## Validation of Referer can be circumvented

Some applications validate the `Referer` header in a naive way that can be bypassed. For example, if the application validates that the domain in the `Referer` starts with the expected value, then the attacker can place this as a subdomain of their own domain: `http://vulnerable-website.com.attacker-website.com/csrf-attack`

Likewise, if the application simply validates that the `Referer` contains its own domain name, then the attacker can place the required value elsewhere in the URL: `http://attacker-website.com/csrf-attack?vulnerable-website.com`

#### Note

Although we may be able to identify this behavior using Burp, we will often find that this approach no longer works when we go to test our proof-of-concept in a browser. In an attempt to reduce the risk of sensitive data being leaked in this way, many browsers now strip the query string from the `Referer` header by default.

We can override this behavior by making sure that the response containing our exploit has the `Referrer-Policy: unsafe-url` header set (note that `Referrer` is spelled correctly in this case, just to make sure we're paying attention!). This ensures that the full URL will be sent, including the query string.

## Lab: CSRF with broken Referer validation

This lab's email change functionality is vulnerable to CSRF. It attempts to detect and block cross domain requests, but the detection mechanism can be bypassed.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

First, we will try to redo the same attack as we did in the previous lab but we need to remove this part: `<meta name="referrer" content="never">` so we can see the Referer header in the exploit request when we capture it.

If we tried to send the exploit to the victim, we will get this error message: "Invalid referer header". 

We will take a look at our exploit request Referer header. The header will have a value like this: `https://exploit-0a41003b036af88a80cd0cd5016700ac.exploit-server.net/`

The website checks if the part of the Referer header matches the actual website domain which is: `LAB-ID.web-security-academy.net`

We will send the exploit request to Repeater and will make this change to the Referer header: `https://LAB-ID.web-security-academy.net.exploit-LAB-ID.exploit-server.net/`

This header is basically the website domain+our exploit domain.

We will send this request using Repeater. We manged to change the email address of our victim. 

Now, to solve the lab, we need to use the exploit server and not BurpSuite.

In the exploit server File field we will add this: `/LAB-ID.web-security-academy.net/my-account/change-email`

We will add this to the Header field: Referrer-Policy: unsafe-url.

This will send the whole URL in the Referer header. 

The body field will have this simple malicious code: 
```html
<form action="https://LAB-ID.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="pwned2@evil-user.net" />
    </form>
    <script>
      document.forms[0].submit();
    </script>

```

Now, the URL of our request is: `https://0a6f00950312f8e180e80da3001100c3.web-security-academy.net/my-account/change-email` and the Referer header is: `https://exploit-LAB-ID.exploit-server.net/LAB-ID.web-security-academy.net/my-account/change-email`

Since part of the Referer header has the same domain as the website, the Referer validation will go through and we will be able to change the victim's email address.

