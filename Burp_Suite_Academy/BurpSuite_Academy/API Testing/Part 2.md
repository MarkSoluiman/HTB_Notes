
---

## Using machine-readable documentation

We can use a range of automated tools to analyze any machine-readable API documentation that we find.

We can use Burp Scanner to crawl and audit OpenAPI documentation, or any other documentation is JSON or YAML format. We can also parse OpenAPI documentation using the OpenAPI parser BApp.

We may also be able to use a specialized tool to test the documented endpoints, such as Postman or SoapUI.

## Identifying API endpoints

We can also gather a lot of information by browsing applications that use the API. This is often worth doing even if we have access to API documentation, as sometimes documentation may be inaccurate or out of date.

We can use Burp Scanner to crawl the application, then manually investigate interesting attack surface using Burp's browser.

While browsing the application, we look for patterns that suggest API endpoints in the URL structure, such as /api/ . We also look out for JavaScript files. These can contain references to API endpoints that we haven't triggered directly via the web browser. Burp Scanner automatically extracts some endpoints during crawls, but for a more heavyweight extraction, we use the JS Link Finder BAp. We can also manually review JavaScript files in Burp.

## Interacting with API endpoints

once we have identified API endpoints, we interact with them using Burp Repeater and Intruder. This enables us to observe the API's behavior and discover additional attack surface. For example, we could investigate how the API responds to changing the HTTP method and media type.

As we interact with the API endpoints, we review error messages and other responses closely. Sometimes these include information that we can use to construct a valid HTTP request.

## Identifying supported HTTP methods

The HTTP method specifies the action to be performed on a resource. For example: 
- `GET` - Retrieves data from a resource.
- `PATCH` - Applies partial changes to a resource.
- `OPTIONS` - Retrieves information on the types of request methods that can be used on a resource.

An API endpoint may support different HTTP methods. It is important to test all potential methods when we are investigating API endpoints. This may enable us to identify additional endpoint functionality, opening up more attack surface.

For example, the endpoint /api/tasks may support the following methods:

- `GET /api/tasks` - Retrieves a list of tasks.
- `POST /api/tasks` - Creates a new task.
- `DELETE /api/tasks/1` - Deletes a task.

We can use the built-in **HTTP verbs** list in Burp Intruder to automatically cycle through a range of methods.

API endpoints often expect data in a specific format. They may therefore behave differently depending on the content type of the data provided in a request. Changing the content type may enable us to: 

- Trigger errors that disclose useful information.
- Bypass flawed defenses.
- Take advantage of differences in processing logic. For example, an API may be secure when handling JSON data but susceptible to injection attacks when dealing with XML.

To change the content type, we modify the Content-Type header, then reformat the request body accordingly, We can use the Content type converter BApp to automatically convert data submitted within requests between XML and JSON.

---


## Lab: Finding and exploiting an unused API endpoint

To solve the lab, exploit a hidden API endpoint to buy a **Lightweight l33t Leather Jacket**. You can log in to your own account using the following credentials: `wiener:peter`.

#### Required knowledge

To solve this lab, you'll need to know:

- How to use error messages to construct a valid request.
- How HTTP methods are used by RESTful APIs.
- How changing the HTTP method can reveal additional functionality.

To solve this lab, we will start the BurpSuite browser and start surfing the website. We will try to buy the item that is mentioned in the lab description. It turns out that we don't have sufficient funds for the purchase. Eventually we will get across a request with the header: `GET /api/products/1/price` 

If we replace the GET with Options, we will see that HTTP methods we can use. We can see that PATCH request is allowed. 

If we changed the method to PATCH, we will get this: 
`{
"type":"ClientError",
"code":400,
"error":"Only 'application/json' Content-Type is supported"
}`

That means we will need to add Content-Type header and set it as application/json . Then, we will be able to change the price if we put JSON code setting the price as 0. 

At the end of the request that we currently have we will add:
`

Content-Type: application/json
Content-Length:0

{
 "price":0
}
`

If we sent this, we will change the price of the item to 0. Then, we will be able to buy the item.

---

## Using Intruder to find hidden endpoints

Once we have identified some initial API points, we can use intruder to uncover hidden endpoint. For example, lets consider a scenario where we have identified the following API endpoint for updating user information: `PUT /api/user/update` 

To identify hidden endpoints, we could use Burp Intruder to find other resources with the same structure. For example, we could add a payload to the /update position of the path with a list of other common functions, such as delete and add.

When looking for a hidden endpoints, we should use wordlists based on common API naming conventions and industry terms. We also make sure to include terms that are relevant to the application, based on our initial recon.


