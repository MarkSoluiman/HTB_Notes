
---

## Bypassing SameSite Lax restrictions with newly issued cookies

Cookies with `Lax` SameSite restrictions aren't normally sent in any cross-site `POST` requests, but there are some exceptions.

As mentioned earlier, if a website doesn't include a `SameSite` attribute when setting a cookie, Chrome automatically applies `Lax` restrictions by default. However, to avoid breaking single sign-on (SSO) mechanisms, it doesn't actually enforce these restrictions for the first 120 seconds on top-level `POST` requests. As a result, there is a two-minute window in which users may be susceptible to cross-site attacks.

#### Note
This two-minute window does not apply to cookies that were explicitly set with the `SameSite=Lax` attribute.

It's somewhat impractical to try timing the attack to fall within this short window. On the other hand, if we can find a gadget on the site that enables us to force the victim to be issued a new session cookie, we can preemptively refresh their cookie before following up with the main attack. For example, completing an OAuth-based login flow may result in a new session each time as the OAuth service doesn't necessarily know whether the user is still logged in to the target site.

To trigger the cookie refresh without the victim having to manually log in again, we need to use a top-level navigation, which ensures that the cookies associated with their current OAuth session are included. This poses an additional challenge because we then need to redirect the user back to our site so that we can launch the CSRF attack.

Alternatively, we can trigger the cookie refresh from a new tab so the browser doesn't leave the page before we're able to deliver the final attack. A minor snag with this approach is that browsers block popup tabs unless they're opened via a manual interaction. For example, the following popup will be blocked by the browser by default: `window.open('https://vulnerable-website.com/login/sso');`

To get around this, you can wrap the statement in an `onclick` event handler as follows: 
```JS
window.onclick = () => { window.open('https://vulnerable-website.com/login/sso'); }
```
This way, the `window.open()` method is only invoked when the user clicks somewhere on the page.

## Lab: SameSite Lax bypass via cookie refresh

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

The lab supports OAuth-based login. You can log in via your social media account with the following credentials: `wiener:peter`

First, we will login using the credentials that we have. We will notice that we will get redirected to this page: `https://0a2600a0037e722e81d9530700390017.web-security-academy.net/social-login` . This page will ask us to provide valid credentials and will ask for our permission to access. This will provide us with a cookie session confirming that we are indeed logged in.

We will logout and try to login again. We notice that this time we weren't asked to provide any login credentials. Here comes the vulnerability that we are going to use.

We can change the email address of our victim by sending them the exploit immediately after logging in using their credentials and before the 120 seconds window passes. 

We will send them this exploit: 

```html
<form action="https://LAB-ID.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="pwned1@evil-user.net" />
    </form>
    <script>
      document.forms[0].submit();
    </script>
```


However, we can still change their email even after the 120 seconds window. 

We will force them to redirect to the login page which will reset the 120 seconds window, then we will send them the main exploit changing their email address. 

We will send this exploit: 
```js
window.onclick = () => { window.open('https://LAB-ID.web-security-academy.net/social-login'); }
```

If we sent these exploits, we will be able to change their email address.



For full explanation:https://www.youtube.com/watch?v=xWe7ey0EBZw

