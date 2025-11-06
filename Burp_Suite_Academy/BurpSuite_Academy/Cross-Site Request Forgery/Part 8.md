
---

## Bypassing SameSite restrictions using on-site gadgets

If a cookie is set with the `SameSite=Strict` attribute, browsers won't include it in any cross-site requests. We may be able to get around this limitation if we can find a gadget that results in a secondary request within the same site.

One possible gadget is a client-side redirect that dynamically constructs the redirection target using attacker-controllable input like URL parameters.

As far as browsers are concerned, these client-side redirects aren't really redirects at all; the resulting request is just treated as an ordinary, standalone request. Most importantly, this is a same-site request and, as such, will include all cookies related to the site, regardless of any restrictions that are in place.

If we can manipulate this gadget to elicit a malicious secondary request, this can enable us to bypass any SameSite cookie restrictions completely.

Note that the equivalent attack is not possible with server-side redirects. In this case, browsers recognize that the request to follow the redirect resulted from a cross-site request initially, so they still apply the appropriate cookie restrictions.

---
## Lab: SameSite Strict bypass via client-side redirect

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. We should use the provided exploit server to host our attack.

We can log in to our own account using the following credentials: `wiener:peter`

We will capture the login request and we can see that the response has the SameSite is set to Strict. That means we have to find a page in the website that redirects the user. If we put our malicious code in the redirecting mechanism so that the email of the user will change, the SameSite Strict option is going to be useless in that case.

The page that redirects the user to another page is when the user submits a comment on post. After submitting a comment, the user will get redirected back to the post. If we captured this process, we will get this: `GET /post/comment/confirmation?postId=4` . Since it uses GET method, we can easily change the redirecting page instead of the postId value.

We also need to capture updating email request. We will get this:  `POST /my-account/change-email` with values: email=example@email.com and submit=1. Since this request doesn't have CSRF token, we can easily change the email without providing a random generated token.

Now, we need to figure a way to change the email of the user with these findings. We can try to redirect the user to the change email page using the comment posting process: `/post/comment/confirmation?postId=4/../../my-account/change-email`. If we put this in the URL, we will trigger the change email process as we will get an error page telling us the submit value is missing. That means this website also has page traversal vulnerability. 

Now, we will put everything together to craft our malicious code and send it to the user :
```html
<script>
window.location="https://0ac900fb049c36d8802e03a600ca00ef.web-security-academy.net/post/comment/confirmation?postId=4/../../my-account/change-email?email=pen%40pen.com%26submit=1"
</script>
```

