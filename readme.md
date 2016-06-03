We're using python3.5 for this project!

Kivy and KivEnt

Kivy installation, install dependencies:
https://kivy.org/docs/installation/installation.html#ubuntu

then: 
```
sudo pip3 install kivy
```

Then for KivEnt, follow instructions:
```
git clone https://github.com/kivy/KivEnt
cd .../KivEnt/modules/core python3 setup.py build_ext install

```


install some dependencies individually for python3, e.g. pygame:

https://pypi.python.org/pypi/setuptools/3.5#installation-instructions

```
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3
```

http://www.pygame.org/wiki/CompileUbuntu?parent=Compilation

```
sudo apt-get install mercurial python3-dev python3-numpy libav-tools \
libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev

sudo apt-get install python3-opengl
```

Make sure you also have setuptools installed:
https://pypi.python.org/pypi/setuptools

Run this one too:
```
sudo apt-get install python-setuptools python3-opengl \
python-gst0.10 python3-enchant gstreamer0.10-plugins-good python-dev \
build-essential libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev
```

You should be set up now!