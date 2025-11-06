
---
## SSRF with whitelist-based input filters

Some applications only allow inputs that match, a whitelist of permitted values. The filter may look for a match at the beginning of the input, or contained within in it. We may be able to bypass this filter by exploiting inconsistencies in URL parsing.

The URL specification contains a number of features that are likely to be overlooked when URLs implement ad-hoc parsing and validation using this method:

- We can embed credentials in a URL before the hostname, using the `@` character. For example:
    
    `https://expected-host:fakepassword@evil-host`
- We can use the `#` character to indicate a URL fragment. For example:
    
    `https://evil-host#expected-host`
- We can leverage the DNS naming hierarchy to place required input into a fully-qualified DNS name that we control. For example:
    
    `https://expected-host.evil-host`
- We can URL-encode characters to confuse the URL-parsing code. This is particularly useful if the code that implements the filter handles URL-encoded characters differently than the code that performs the back-end HTTP request. We can also try double-encoding characters; some servers recursively URL-decode the input they receive, which can lead to further discrepancies.
- We can use combinations of these techniques together.

## Bypassing SSRF filters via open redirection

It is sometimes possible to bypass filter-based defenses by exploiting an open redirection vulnerability.

In the previous example, imagine the user-submitted URL is strictly validated to prevent malicious exploitation of the SSRF behavior. However, the application whose URLs are allowed contains an open redirection vulnerability. Provided the API used to make the back-end HTTP request supports redirections, we can construct a URL that satisfies the filter and results in a redirected request to the desired back-end target.

For example, the application contains an open redirection vulnerability in which the following URL:

`/product/nextProduct?currentProductId=6&path=http://evil-user.net `

returns a redirection to: `http://evil-user.net`

We can leverage the open redirection vulnerability to bypass the URL filter, and exploit the SSRF vulnerability as follows:

```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118 stockApi=http://weliketoshop.net/product/nextProduct?currentProductId=6&path=http://192.168.0.68/admin
```

This SSRF exploit works because the application first validates that the supplied `stockAPI` URL is on an allowed domain, which it is. The application then requests the supplied URL, which triggers the open redirection. It follows the redirection, and makes a request to the internal URL of the attacker's choosing.

---

## Lab: SSRF with filter bypass via open redirection vulnerability

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at `http://192.168.0.12:8080/admin` and delete the user `carlos`.

The stock checker has been restricted to only access the local application, so we will need to find an open redirect affecting the application first.

We will capture the checking stock request and send it to the Repeater. We will try to change the stockApi header to redirect us to the admin panel page using open redirection:  /product/stock/check?productId=4&storeId=1&path=`http://192.168.0.12:8080/admin`

Note(we always need to url encode the stockApi header). 

This doesn't work. 

We notice that we can toggle products when we check the stock by clicking on previous product or next product at the bottom right corner of a product's page.

We will capture the request of going to the next or prev product and send it to the Repeater as well.

We notice that the GET request has path value. We will test for the open redirection vulnerability by changing the path value to: `https:www/google.com`. That indeed works and now we know that this URL is vulnerable for open redirection.

We will copy the GET request URL and put it in the stockApi header and replace the path value to the admin panel page: /product/nextProduct?currentProductId=4&path=`http://192.168.0.12:8080/admin`

This will redirect us to the admin panel page and we can delete the carlos user.

