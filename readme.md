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
- Get appropriate version of chrome driver from http://chromedriver.storage.googleapis.com/index.html
- Unzip the chromedriver.zip
- Move the file to /usr/bin directory sudo mv chromedriver /usr/bin
- Go to /usr/bin directory and you would need to run "chmod a+x chromedriver" to mark it executable. 

```
browser = webdriver.Chrome()
browser.get("http://localhost:8000")
```

http://stackoverflow.com/questions/22130109/cant-use-chrome-driver-for-selenium
