Google Calendar Display - for pygame
====================================

Cloned originally from https://github.com/course-hero/google-calendar-display

A very simple pygame app to display conference room status outside the room. Useful to indicate which rooms are free or booked. 

The service written in Python, using pyGame to generate the UI locally on a tablet. The tablet could be mounted on the wall or window outside a room.

Screen Shots:

![](https://github.com/barneyman/gcalMeetingRoom/blob/master/Free.PNG)
![](https://github.com/barneyman/gcalMeetingRoom/blob/master/Soon.PNG)
![](https://github.com/barneyman/gcalMeetingRoom/blob/master/busy.PNG)


Installation
-------------
Install Pygame and the Google client libraries via pip:

RPI

```
$ sudo apt-get update
$ sudo apt-get install python-pip
$ sudo pip install --upgrade google-api-python-client python-gflags python-dateutil pytz pygame
```

Windows

Install Python 2
```
pip install --upgrade google-api-python-client python-gflags python-dateutil pytz pygame
```
pip will be in the python scripts directory


Preparation
-------------
1. In Google Developer Console, create a project, create an API key (with no key restriction), and OAuth2 Client ID
2. GCAL
	2a. The GCAL you wish to show should be in the list of calendars available to the "authorising google account" OR
	2b. where i work, we've set up a google room resource - no idea how that was done - IT faeries!
3. Enable the Calendar API for your project (Library / Google Calendar API / Enable)


Configuration
-------------
1. Open the file calendar_config.py and enter your Google API client ID, client secret, developer (API) key.
2. Enter the CALENDAR name with the name of the calendar, or room name - the app downloads all calendar names it can 'see' after authorisation, to calendars.json - have a look in there
3. Enter the TIMEZONE for the room https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones

Basic Usage
-------------

local pygame version
```
$ python local.py
```

The first time you run it, it will provide an URL you will have to visit to authorise the application


Hardware
-------------

* RPI3 - http://au.element14.com/raspberry-pi/raspberrypi-modb-1gb/raspberry-pi-3-model-b/dp/2525226
* Screen - http://au.element14.com/raspberry-pi/raspberrypi-display/raspberry-pi-7inch-touchscreen/dp/2473872?MER=sy-me-pd-mi-acce
* Case - http://au.element14.com/multicomp/cbrpp-ts-blk-wht/raspberry-pi-touchscreen-enclosure/dp/2494691?MER=bn_level5_5NP_EngagementRecSingleItem_1



