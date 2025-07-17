
---

## Finding hidden parameters

When we are doing API recon, we may find undocumented parameters that the API supports. We can attempt to use these to change the application's behavior. Burp includes numerous tools that can help us identify hidden parameters:
- Intruder enables us to automatically discover hidden parameters, using a wordlist of common parameter names to replace existing parameters or add new parameters. We also make sure to include names that are relevant to the application. 
- The Param miner BAPP enables us to automatically guess up to 65,536 param names per request. Param miner automatically guesses names that are relevant to the application, based on information taken from the scope.
- The Content discovery tool enables us to discover content that isn't from visible content that we can browse to, including parameters.

## Mass assignment vulnerabilities

Mass assignment (aka auto-binding) can inadvertently create hidden parameters. It occurs when software frameworks automatically bind request parameters to fields on an internal object. Mass assignment may therefore result in the application supporting parameters that were never intended to be processed by the developer. 

## Identifying hidden parameters


Since mass assignment creates parameters from object fields, we can often identify these hidden parameters by manually examining objects returned by the API.

For example, consider a `PATCH /api/users/` request, which enables users to update their username and email, and includes the following JSON:

```
{
"username": "wiener",
"email": "wiener@example.com",
}
```

A concurrent `GET /api/users/123` request returns the following JSON:

```
{ 
"id": 123,
"name": "John Doe",
"email": "john@example.com",
"isAdmin": "false"
}
```

This may indicate that the hidden id and isAdmin parameters are bound to the internal user object, alongside the updated username and email parameters.

## Testing mass assignment vulnerabilities

To test whether we can modify the enumerated isAdmin parameter value, we add it to the PATCH request:

```
{ 
"username": "wiener",
"email": "wiener@example.com",
"isAdmin": false, 
}
```

In addition, we send a PATCH request with an invalid isAdmin parameter value:

```
{
"username": "wiener",
"email": "wiener@example.com",
"isAdmin": "foo",
}
```

If the application behaves differently, this may suggest that the invalid value impacts the query logic, but the valid value doesn't. This may indicate that the parameter can be successfully updated by the user.

We can then send a PATCH request with the isAdmin parameter value set to true, to try and exploit the vulnerability:

```
{ 
"username": "wiener",
"email": "wiener@example.com",
"isAdmin": true, 
}
```

If the isAdmin value in the request is bound to the user object without enough validation and sanitization , the user wiener may be incorrectly granted admin privileges.

---

## Lab: Exploiting a mass assignment vulnerability

To solve the lab, find and exploit a mass assignment vulnerability to buy a **Lightweight l33t Leather Jacket**. You can log in to your own account using the following credentials: `wiener:peter`.

#### Required knowledge

To solve this lab, you'll need to know:

- What mass assignment is.
- Why mass assignment may result in hidden parameters.
- How to identify hidden parameters.
- How to exploit mass assignment vulnerabilities.

To solve this lab, we need to know how does the API work. We will visit the /api page. In the API page, we will see that we are allowed with two HTTP methods: GET and POST with the endpoint of /checkout. The POST method has a parameter of order which it has this JSON format
```
{ "chosen_discount": ChosenDiscount, // defaults to: {"description":null,"discount_id":null,"percentage":0} "chosen_products": [ChosenProduct] 
}
```
Since this parameter has a discount percentage, we will try to make a POST request with the percentage set to 100.

We will first need to capture a request while we are attempting to buy the jacket. This should be a GET request to /api/checkout. We send this to  the Repeater.

First, we will change the GET method to POST. Then, we will add both of the following parts at the end of the request:

```
Content-Type:application/json
Content-Length:0

{
"chosen_discount":{
"percentage":100
},"chosen_products":[{"product_id":"1","name":"Lightweight \"l33t\" Leather Jacket","quantity":2,"item_price":133700}]
}

```

If we sent this request, we will get a 201 response and we will solve the lab.

---

## Preventing vulnerabilities in APIs

When designing APIs, developers need to make sure that security is a consideration from the beginning. In particular, they need to make sure that they:
- Secure the documentation if they don't intend their API to be publicly accessible.
- Ensure their documentation is kept up to date so that legitimate testers have full visibility of the API's attack surface.
- Apply an allowlist of permitted HTTP methods.
- Validate that the content type is expected for each request or response.
- Use generic error messages to avoid giving away information that may be useful for an attacker.
- Use protective measures on all versions of your API, not just the current production version.

To prevent mass assignment vulnerabilities, allowlist the properties that can be updated by the user, and blocklist sensitive properties that shouldn't be updated by the user.