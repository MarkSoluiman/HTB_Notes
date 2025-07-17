
---

## Server-side parameter pollution

Some systems contain internal APIs that aren't directly accessible from the internet. Server-side parameter pollution occurs when a website embeds user input in a server-side request to an internal API without enough encoding. This means that an attacker may be able to manipulate or inject parameters, which may enable them to:
- Override existing parameters.
- Modify the application behavior.
- Access unauthorized data.

We can test any user input for any kind of parameter pollution. For example, query parameters, form fields, headers, and URL path parameters may all be vulnerable.

## Testing for server-side parameter pollution in the query string

To test for server-side parameter pollution in the query string, we place query syntax characters like #, &, and = in our input and observe how the application responds.

Consider a vulnerable application that enables us to search for other users based on their username. When we search for a user, our browser makes the following request: `GET /userSearch?name=peter&back=/home`

To retrieve user information, the server queries an internal API with the following request: `GET /users/search?name=peter&publicProfile=true`

## Truncating query strings

We can use a URL-encoded # character to attempt to truncate the server-side request. To help us interpret the response, we could also add a string after the # char.

For example, we could modify the query string to: `GET /userSearch?name=peter%23foo&back=/home`. The front-end will try to access the following URL: `GET /users/search?name=peter#foo&publicProfile=true`

We review the response for clues about whether the query has been truncated. For example, if the response returns the user `peter`, the server-side query may have been truncated. If an `Invalid name` error message is returned, the application may have treated `foo` as part of the username. This suggests that the server-side request may not have been truncated.

If we're able to truncate the server-side request, this removes the requirement for the `publicProfile` field to be set to true. We may be able to exploit this to return non-public user profiles.

## Injecting invalid parameters

We can use an URL-encoded `&` character to attempt to add a second parameter to the server-side request.

For example, We could modify the query string to the following:
`GET /userSearch?name=peter%26foo=xyz&back=/home`

This results in the following server-side request to the internal API:
`GET /users/search?name=peter&foo=xyz&publicProfile=true

We review the response for clues about how the additional parameter is parsed. For example, if the response is unchanged this may indicate that the parameter was successfully injected but ignored by the application.

To build up a more complete picture, we'll need to test further.

## Injecting valid parameters

If we're able to modify the query string, you can then attempt to add a second valid parameter to the server-side request.

For example, if you've identified the `email` parameter, you could add it to the query string as follows:
`GET /userSearch?name=peter%26email=foo&back=/home`

This results in the following server-side request to the internal API:
`GET /users/search?name=peter&email=foo&publicProfile=true`

## Overriding existing parameters

To confirm whether the application is vulnerable to server-side parameter pollution, we could try to override the original parameter. We do this by injecting a second parameter with the same name.

For example, we could modify the query string to the following:
`GET /userSearch?name=peter%26name=carlos&back=/home`

This results in the following server-side request to the internal API:
`GET /users/search?name=peter&name=carlos&publicProfile=true`

The internal API interprets two `name` parameters. The impact of this depends on how the application processes the second parameter. This varies across different web technologies. For example:
- PHP parses the last parameter only. This would result in a user search for `carlos`.
- ASP.NET combines both parameters. This would result in a user search for `peter,carlos`, which might result in an `Invalid username` error message.
- Node.js / express parses the first parameter only. This would result in a user search for `peter`, giving an unchanged result.

If we're able to override the original parameter, we may be able to conduct an exploit. For example, we could add `name=administrator` to the request. This may enable us to log in as the administrator user.

---

## Lab: Exploiting server-side parameter pollution in a query string

To solve the lab, log in as the `administrator` and delete `carlos`.

To solve this lab, we will first need to know how does the forgot password page work. To do so, we will view the source code of the page using our browser. An interesting info that we see is that the reset token will be added to the URL to get the reset password page: `window.location.href = `/forgot-password?reset_token=${resetToken}`;`

Now, we need to capture a POST request when we submit the administrator username to get the token and send the request to Repeater.

At the bottom of the request, we see this part:&username=administrator. To test if we can truncate the query, we will add the # character but with URL encoding which is:%23, so our request will be &username=administrator%23. 
We will get an error message:"Field not specified". This is a clue. 

We will try to add a field called field after administrator with & character URL encoded:&username=administrator%26field=
we will try different stuff like username.
This will return the username.

We will try to get the reset token: &username=administrator%26field=reset_token.

This will indeed get us the reset token. 

We will change the URL of the page to: /forgot-password?reset_token=(reset token).

This will give us access to the reset password page.

after resetting the password. We will login as administrator and delete user carlos.

