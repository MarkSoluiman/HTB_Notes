
---

## API Recon

To start API testing, we need to find out as much information about the API as possible, to discover its attack surface.

To begin, we should identify API endpoints. These are locations where an API receives requests about a specific resource on its server. For example, consider the following GET request:

```
GET /api/books HTTP/1.1
Host: example.com
```
The API endpoint for this request is /api/books. This results in an interaction with the API to retrieve a list of books from a library. Another API endpoint might be, for example, `/api/books/mystery`, which would retrieve a list of mystery books.

Once we have identified the endpoints, we need to determine how to interact with them. This enables us to construct valid HTTP requests to test the API. For example, we should find out information about the following:
- The input data the API processes, including both compulsory and optional parameters.
- The types of requests the API accepts, including supported HTTP methods and media formats.
- Rate limits and authentication mechanisms.

## API Documentation

APIs are usually documented so that developers know how to use and integrate with them.

Documentation can be in both human-readable and machine-readable forms. Human-readable documentation is designed for developers to understand how to use the API. It may include detailed explanations, examples, and usage scenarios. Machine-readable documentation is designed to be processed by software for automating tasks like API integrating and validation. It's written in structured formats like JSON or XML.

API documentation is often publicly available, particularly if the API is for use by external developers. If this is the case, always start the recon by reviewing the documentation.

## Discovering API Documentation

Even if API documentation isn't openly available, we may still be able to access it by browsing applications that use the API. 

To do this, we can use Burp Scanner to crawl the API. We can also browse applications manually using Burp's browser. Look for endpoints that may refer to API documentation, for example:
- /api
- /swagger/index.html
- /openai.json

If we identify an endpoint for a resource, we need to make sure to investigate the base path. For example, if we identify the resource endpoint `/api/swagger/v1/users/123`, then we should investigate the following paths:
- /api/swagger/v1
- /api/swagger/
- /api

We can also use a list of common paths to find documentation using Intruder.

---

## Lab: Exploiting an API endpoint using documentation


To solve the lab, find the exposed API documentation and delete `carlos`. You can log in to your own account using the following credentials: `wiener:peter`.

#### Required knowledge

To solve this lab, you'll need to know:

- What API documentation is.
- How API documentation may be useful to an attacker.
- How to discover API documentation.

To solve this lab, we will try this URL:/api. This will lead us to the API documentation. This API can GET, DELETE, and PATCH users.
The endpoint for deleting a user is: `/user/[username:string]`. That means in order to delete the user carlos, we will need to send a DELETE request followed with: /user/carlos.

Since we have captured the request to visit the /api URL and sent it to the Repeater, we will change the GET to DELETE and the URL to: /api/users/carlos. We will get a text input that will allow us to put the username that we want to delete. If we click send, the user carlos will be deleted. 