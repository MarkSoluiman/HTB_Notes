
---
## Prototype pollution via the constructor

So far, we've looked exclusively at how you can get a reference to prototype objects via the special `__proto__` accessor property. As this is the classic technique for prototype pollution, a common defense is to strip any properties with the key `__proto__` from user-controlled objects before merging them. This approach is flawed as there are alternative ways to reference `Object.prototype` without relying on the `__proto__` string at all.

Unless its prototype is set to `null`, every JavaScript object has a `constructor` property, which contains a reference to the constructor function that was used to create it. For example, we can create a new object either using literal syntax or by explicitly invoking the `Object()` constructor as follows:

```js
let myObjectLiteral = {};
let myObject = new Object();
```

We can then reference the `Object()` constructor via the built-in `constructor` property:
```js
myObjectLiteral.constructor // function Object(){...}
myObject.constructor // function Object(){...}
```

Remember that functions are also just objects under the hood. Each constructor function has a `prototype` property, which points to the prototype that will be assigned to any objects that are created by this constructor. As a result, we can also access any object's prototype as follows:

```js
myObject.constructor.prototype // Object.prototype 
myString.constructor.prototype // String.prototype 
myArray.constructor.prototype // Array.prototype
```

As `myObject.constructor.prototype` is equivalent to `myObject.__proto__`, this provides an alternative vector for prototype pollution.

## Bypassing flawed key sanitization

An obvious way in which websites attempt to prevent prototype pollution is by sanitizing property keys before merging them into an existing object. However, a common mistake is failing to recursively sanitize the input string. For example, consider the following URL: `vulnerable-website.com/?__pro__proto__to__.gadget=payload`

If the sanitization process just strips the string `__proto__` without repeating this process more than once, this would result in the following URL, which is a potentially valid prototype pollution source: `vulnerable-website.com/?__proto__.gadget=payload`

## Lab: Client-side prototype pollution via flawed sanitization

The only thing that is different about this lab is this part of the code that we are going to find in the file: searchLoggerFiltered.js: 
```js

function sanitizeKey(key) {
    let badProperties = ['constructor','__proto__','prototype'];
    for(let badProperty of badProperties) {
        key = key.replaceAll(badProperty, '');
    }
    return key;
}
```
This code goes through the URL and filters three words that can cause prototype pollution attack on the website. However, the loop checks only once for each bad word that can cause property pollution. For example, if our input has something like this: construc`constructor`tor, the code will identify the constructor word that is between the other divided constructor word and removes it. It will then check for the words `__proto__` and prototype. So, our input will still have the word constructor. 

In the same file, we will see this other vulnerable code that will allow JS code to be executed if we passed it to the URL:
```js
async function searchLogger() {
    let config = {params: deparam(new URL(location).searchParams.toString())};
    if(config.transport_url) {
        let script = document.createElement('script');
        script.src = config.transport_url;
        document.body.appendChild(script);
    }
    if(config.params && config.params.search) {
        await logQuery('/logger', config.params);
    }
}
```

The transport_url is what we are after.

In the URL, we will do the following:`/?construcconstructortor[protoprototypetype][transport_url]=data:,alert()` 