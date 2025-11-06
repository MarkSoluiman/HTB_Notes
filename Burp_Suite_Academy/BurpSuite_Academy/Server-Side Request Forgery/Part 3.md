
---

## SSRF with blacklist-based input filters

ome applications block input containing hostnames like `127.0.0.1` and `localhost`, or sensitive URLs like `/admin`. In this situation, you can often circumvent the filter using the following techniques:

- Use an alternative IP representation of `127.0.0.1`, such as `2130706433`, `017700000001`, or `127.1`.
- Register our own domain name that resolves to `127.0.0.1`. We can use `spoofed.burpcollaborator.net` for this purpose.
- Obfuscate blocked strings using URL encoding or case variation.
- Provide a URL that we control, which redirects to the target URL. Try using different redirect codes, as well as different protocols for the target URL. For example, switching from an `http:` to `https:` URL during the redirect has been shown to bypass some anti-SSRF filters.

---

## Lab: SSRF with blacklist-based input filter

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at `http://localhost/admin` and delete the user `carlos`.

The developer has deployed two weak anti-SSRF defenses that we will need to bypass.

The key for this lab is to find what triggers the anti-SSRF. 

As usual, we will capture the checking stock request and send it to Repeater. We will try to access the admin's page. We will get this message: "External stock check blocked for security reasons".

We will try to change the localhost to one of these alternatives: `2130706433`, `017700000001`, or `127.1`. We will still get the same message.

We will try to obfuscate our input be encoding it using URL. We will still get the same error.

Finally, we will try to change the letters case in admin and in localhost like so: `http://localHost/Admin`. This will give us access to the admin panel. Now, we know what triggers the anti-SSRF. 

We will delete the user carlos: `http://localHost/Admin/delete?username=carlos`

