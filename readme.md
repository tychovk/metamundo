#Metamundo

In this 2D world, there are a lot of trivial things that are of no importance. And, there are... Blobs.

##Blobs
Blobs are jelly-like consistencies that appear here and there. They are not necessarily everywhere, but definitely present. They grow in a seemingly random pattern. What is the meaning of this?

##The App
This is a 2D simulation where so called 'blobs' grow on a grid, relatively far apart from each other. Blobs age, and thereby increase their chance of expanding. 

Plans are to:
- Allow players, who spawn on a random spot on the map, to walk around and interact with the blobs.
- Have blobs get different characteristics, either spontaneously, or by interaction with players. Characteristics can be: colour, stiffness, procreative enthusiasm, defiance or adherence towards players/their own blob-mind, hostility, and so forth.
- Have the map expand automatically as players reach the periphery (meaning blobs can spawn there too, but players as well)
- Have a visual representation for this, in a web environment as well as a smartphone app
- Have links with apps that track real-life (health) performance, e.g. steps walked, to increase player's speed / energy / blob carrying capacity (temporarily).







#Setup for testing

###Selenium
If selenium testing doesn't work for Firefox, try it for chrome:
- Install latest version of chrome "sudo apt-get install chromium-browser"
- Get appropriate version of chrome driver from http://chromedriver.storage.googleapis.com/index.html (MAKE SURE! That you have the latest version. Check on what date it was added/modified.)
- Unzip the chromedriver.zip
- Move the file to /usr/bin directory sudo mv chromedriver /usr/bin
- Go to /usr/bin directory and you would need to run "chmod a+x chromedriver" to mark it executable. 

```
browser = webdriver.Chrome()
browser.get("http://localhost:8000")
```

http://stackoverflow.com/questions/22130109/cant-use-chrome-driver-for-selenium


http://stackoverflow.com/questions/10404160/when-to-use-explicit-wait-vs-implicit-wait-in-selenium-webdriver#28067495 <-- may also be interesting in case of erraticly different test results when ran a few times consecutively.



# Django & Angular integration

```
var app = angular.module("testMetamundo", []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol(':{');
    $interpolateProvider.endSymbol('}:');
}]);

app.controller('testController', function() {
    var thing = 'hi world';
    var data = {
        'access': 42
    };
    this.thing = thing;
    this.data = data;

    this.set_data = function(name, data) {
        this.data[name] = data;
    };
});

```

Changed the interpolation (templating brackets) to `:{ <content> }:`
I have this rudimentary controller there, with data object data
and most importantly, a set function
on the flask side

 ```
 from testapp import app
from flask import render_template
import json


@app.route('/')
def index():
    options = [1, 2, 3, 4]
    #options = json.loads(options)
    return render_template('index.html', options=options)

```

all i want to do is pass this simple array object with numbers 1-4,
i initialy used JSON loads, but found it wasn't necessary - I just passed in the actual object

and that's because in `index.html`...


 ```
 <!DOCTYPE html>
<html lang='en', ng-app='testMetamundo'>
    <head>
        <script type='text/javascript' src='static/node_modules/angular/angular.min.js'></script>
        <script type='text/javascript' src='static/appjs/app.js'></script>
        <title>Hello World</title>
        <script>
            var new_data = {{ options|tojson|safe }};

            console.log(new_data)
        </script>        
    </head>


    <body>
        <h2>This is a test</h2>

        <p>Insert stuff here:

        <div ng-controller='testController as test'>
            <p>:{ test.thing }:</p>
            <input type='text' name='test-data' ng-model='test.data.access'>

            <p>:{ test.data.access }:</p>
            <p> Let there be new data!!!
                :{ test.set_data('new_data', {{ options|tojson|safe }}) }:
            </p>
            :{ test.data.new_data }:
        </div>

        </p>
    </body>
</html>

```

notice `{{ options|tojson|safe }}`

jinja2 has a built-in filter to convert said object to json on the HTML doc

what's more interesting is that I'm able to pass in this Jinja2 interpolated Python array, within a Angular interpolated controller func

so I gave this `testController` a piece of data that originated from Python

and then the controller can have functions to do shit with it


