Google Calendar Display - for pygame
====================================

Cloned originally from https://github.com/course-hero/google-calendar-display

A very simple pygame app to display conference room status outside the room. Useful to indicate which rooms are free or booked. 

The service written in Python, using pyGame to generate the UI locally on a tablet. The tablet could be mounted on the wall or window outside a room. For example, here's a prototype mounted on the Superman conference room at Course Hero:

![](https://github.com/course-hero/google-calendar-display/blob/master/calendar-display.jpg)

Here's a screenshot of the app, when the room is free, and shows two upcoming events:

![](https://github.com/course-hero/google-calendar-display/blob/master/screenshot-free.png)


Installation
-------------
Install Flask, pygame and the Google client libraries via pip:

```
$ sudo apt-get update
$ sudo apt-get install python-pip
$ sudo pip install --upgrade google-api-python-client python-gflags python-dateutil Flask pytz
```

Configuration
-------------
1. Open the file calendar_config.py and enter your Google API client ID, client secret, developer key.
2. Fill the CALENDAR_IDS dictionary with mappings for the room IDs you want to use in a URL to the Google Calendar ID for each room.

Basic Usage
-------------
You can run the server in debug mode:

original http version
```
$ python server.py
```

local pygame version
```
$ python local.py
```


Using default Flask settings, you would access the app at:

```
http://<YOUR IP ADDRESS>:5000/<ROOM ID>
```

And you can see a status list for all conference rooms here:
```
http://<YOUR IP ADDRESS>:5000/calendars
```

Or you could configure it to run through a webserver, and on a different port, such as 80.
