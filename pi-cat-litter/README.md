# Intro
This is the code related to my [home project to build a motion activated fan for my cat's litter box](https://xinxindai.medium.com/build-a-ventilated-cat-litter-box-with-pi-zero-ce943d55b446). In the original post, the database is running on the same Pi Zero that is connected with the motion sensor. The project is now moved to a MQTT based strcture so you could potentially running the database somewhere else.

# Note
You'd need to create a `.service` file to run the `motion_detection_storage.py` as well. This file is missing since it contains the username & password I use, but should be fairly simply to build yourself. Enjoy!