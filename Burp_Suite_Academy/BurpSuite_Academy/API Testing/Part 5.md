
---

## Testing for server-side parameter pollution in REST paths

A RESTful API may place parameter names and values in the URL path, rather than the query string. For example, lets consider the following path: /api/users/123

The URL path might be broken down as follows:

- `/api` is the root API endpoint.
- `/users` represents a resource, in this case `users`.
- `/123`represents a parameter, here an identifier for the specific user.

Lets consider an application that enables us to edit user profiles based on their username. Requests are sent to the following endpoint:
`GET /edit_profile.php?name=peter`

This results in the following server-side request: 
`GET /api/private/users/peter`

An attacker may be able to manipulate server-side URL path parameters to exploit the API. To test for this vulnerability, we add path traversal sequences to modify parameters and observe how the application responds.

We could submit URL-encoded `peter/../admin` as the value of the `name` parameter: `GET /edit_profile.php?name=peter%2f..%2fadmin`

This may result in the following server-side request:
`GET /api/private/users/peter/../admin`

If the server-side client or back-end API normalize this path, it may be resolved to `/api/private/users/admin`.

## Testing for server-side parameter pollution in structured data formats

An attacker may be able to manipulate parameters to exploit vulnerabilities in the server's processing of other structured data formats, such as a JSON or XML. To test for this, we inject unexpected structured data into user inputs and see how the server responds.

Lets consider an application that enables users to edit their profile, then applies their changes with a request to a server-side API. When we edit our name, our browser makes the following request:
```
POST /myaccount
name=peter
```

This results in the following server-side request:
```
PATCH /users/7312/update
{"name":"peter"}
```

We can attempt to add the `access_level` parameter to the request as follows:
```
POST /myaccount
name=peter","access_level":"administrator
```

If the user input is added to the server-side JSON data without adequate validation or sanitization, this results in the following server-side request:
```
PATCH /users/7312/update {name="peter","access_level":"administrator"}
```

This may result in the user `peter` being given administrator access.

Lets consider a similar example, but where the client-side user input is in JSON data. When we edit our name, our browser makes the following request:
```
POST /myaccount
{"name": "peter"}
```

This results in the following server-side request:
```
PATCH /users/7312/update
{"name":"peter"}
```

We can attempt to add the `access_level` parameter to the request as follows:
```
POST /myaccount {"name": "peter\",\"access_level\":\"administrator"}
```

If the user input is decoded, then added to the server-side JSON data without adequate encoding, this results in the following server-side request:
```
PATCH /users/7312/update {"name":"peter","access_level":"administrator"}
```

Again, this may result in the user `peter` being given administrator access.

Structured format injection can also occur in responses. For example, this can occur if user input is stored securely in a database, then embedded into a JSON response from a back-end API without adequate encoding. We can usually detect and exploit structured format injection in responses in the same way we can in requests.

## Testing with automated tools

Burp includes automated tools that can help us detect server-side parameter pollution vulnerabilities.

Burp Scanner automatically detects suspicious input transformations when performing an audit. These occur when an application receives user input, transforms it in some way, then performs further processing on the result. This behavior doesn't necessarily constitute a vulnerability, so we'll need to do further testing using the manual techniques outlined above.

We  can also use the Backslash Powered Scanner BApp to identify server-side injection vulnerabilities. The scanner classifies inputs as boring, interesting, or vulnerable. We'll need to investigate interesting inputs using the manual techniques outlined above.