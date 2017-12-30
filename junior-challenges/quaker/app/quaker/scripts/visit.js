var system = require('system');
var page = require('webpage').create();
var timeout = 3000;

if (system.args.length !== 3) {
        console.log('args: url sessionid');
        phantom.exit(1);
} else {
    session = system.args[1];
    url = system.args[2];
}
phantom.addCookie({
    'name': 'flag',
    'value': 'You are close. Keep digging, the admin has stored his flag somewhere in his profile!',
    'domain': '127.0.0.1',
    'path': '/',
    'httponly': false
});

phantom.addCookie({
    'name': 'flag',
    'value': 'You are close. Keep digging, the admin has stored his flag somewhere in his profile!',
    'domain': 'localhost',
    'path': '/',
    'httponly': false
});

phantom.addCookie({
    'name': 'flag',
    'value': 'You are close. Keep digging, the admin has stored his flag somewhere in his profile!',
    'domain': '78.46.224.80',
    'path': '/',
    'httponly': false
});

phantom.addCookie({
    'name': 'sessionid',
    'value': session,
    'domain': '127.0.0.1',
    'path': '/',
    'httponly': false
});

phantom.addCookie({
    'name': 'sessionid',
    'value': session,
    'domain': 'localhost',
    'path': '/',
    'httponly': false
});

phantom.addCookie({
    'name': 'sessionid',
    'value': session,
    'domain': '78.46.224.80',
    'path': '/',
    'httponly': false
});
 
page.onNavigationRequested = function(url, type, willNavigate, main) {
    console.log("[phantom][URL] URL="+url);  
    //console.log(page.content);
    //console.log("[SESSION] sessionid="+session);  
};

page.onResourceRequested = function(requestData, networkRequest) {
    console.log("[phantom][Resource requested] URL="+requestData.url);  
    //console.log("Resource requested: "+JSON.stringify(requestData));  
};

page.onResourceReceived = function(response) {
  //console.log('Response (#' + response.id + ', stage "' + response.stage + '"): ' + JSON.stringify(response));
};

page.onConsoleMessage = function(msg) {
      console.log(msg);
};

 
page.settings.resourceTimeout = timeout;
page.onResourceTimeout = function(e) {
    setTimeout(function(){
        console.log("[phantom][INFO] Timeout")
        phantom.exit();
    }, 2000);
};

 
page.open(url, function(status) {
    console.log("[phantom][INFO] rendered page");
    //console.log(page.content);
    //console.log("\n\n\n\n");
    setTimeout(function(){
        phantom.exit();
    }, 2000);
});
