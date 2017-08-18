from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

import httplib2

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow

from datetime import datetime
from datetime import timedelta
import pytz
import dateutil.parser
import sys
import os
import json

import pyScreen
import pygame

import time

import signal
import sys, getopt

def handler(signum, frame):
	print "Told to die ..."
	sys.exit()

signal.signal(signal.SIGTERM, handler)

print "Current PID ", os.getpid()

import calendar_config

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
FLOW = OAuth2WebServerFlow(
    client_id=calendar_config.CLIENT_ID,
    client_secret=calendar_config.CLIENT_SECRET,
    scope=calendar_config.SCOPE,
    user_agent=calendar_config.USER_AGENT)


# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run_flow(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http(timeout=30)
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.

foundServer=False

while not foundServer:
	try:
		service = build(serviceName='calendar', version='v3', http=http,developerKey=calendar_config.DEVELOPER_KEY)
		foundServer=True
		print 'service built'
	except Exception as e:
		print "could not build, retrying ..."
		print 'exception - ',e
		time.sleep(5)
		foundServer=False
	

la = pytz.timezone(calendar_config.TIMEZONE)

def create_time_string(dt):
    if not dt:
        return None
    hours, remainder = divmod(dt.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    minutes=minutes+1
    h = 'hours'
    m = 'minutes'
    if hours == 1:
        h = 'hour'
    if minutes == 1:
        m = 'minute'
    if hours == 0:
       return '%s %s' % (minutes, m)
    else:
        return '%s %s and %s %s' % (hours, h, minutes, m)


def get_events(room_name):
	items = []
	now = datetime.utcnow()

	la_offset = la.utcoffset(datetime.utcnow())
	now = now + la_offset

	start_time = datetime(year=now.year, month=now.month, day=now.day, tzinfo=la)
	end_time = start_time + timedelta(days=1)

	print "Running at", now.strftime("%A %d %B %Y, %I:%M%p"),
	print " - ", room_name

	if not os.path.isfile('calendars.json'):
		# this is duplicated from the calendars() method
		calendars = {}
		calendar_list = service.calendarList().list().execute()
		for calendar_list_entry in calendar_list['items']:
			#if calendar_list_entry['id'] not in calendar_config.EXCLUSIONS:
			calendars[calendar_list_entry['id']] = calendar_list_entry['summary']

        # store this to a local file
		with open('calendars.json', mode='w') as calendar_file:
			json.dump({value: key for key, value in calendars.items()}, calendar_file)

	with open('calendars.json', 'r') as f:
		calendars = json.load(f)

	if room_name not in calendars:
		return { 
		'roomState' : pyScreen.roomState.notFound,
		'events' : {},
		'status' : '!Error!', 
        'now': now.strftime("%A %d %B %Y, %I:%M%p")
		}


	room_id = calendars[room_name]

	print '	execute',
	events = service.events().list(
		calendarId=room_id,
		orderBy='startTime',
		singleEvents=True,
		timeMin=start_time.isoformat(),
		timeMax=end_time.isoformat()
	).execute()
	print 'out'


	currentEventId=None
	next_start = None
	next_end = None
	status = "FREE"
	roomCurrentState = pyScreen.roomState.free

	for event in events['items']:

		#DEBUG
		#print event
		#print '----------------------------------------'

		# if this is an all day event it has a 'date' for start and end, not a 'dateTime'


		if not 'dateTime' in event['start']:
			start = dateutil.parser.parse(event['start']['date']).replace(tzinfo=None)
		else:
			start = dateutil.parser.parse(event['start']['dateTime']).replace(tzinfo=None)


		if not 'dateTime' in event['end']:
			end = dateutil.parser.parse(event['end']['date']).replace(tzinfo=None)
		else:
			end = dateutil.parser.parse(event['end']['dateTime']).replace(tzinfo=None)


		if not 'displayName' in event['creator']:
			event['creator']['displayName']=event['creator']['email']

		if not 'summary' in event:
			event['summary']="(no title)"

		# if we are before it ends, add it to the list of upcoming	
		if now <= end:
			items.append({'name': event['summary'], 
				'creator': event['creator']['displayName'], 
                'start': start.strftime("%I:%M%p"), 
                'end': end.strftime("%I:%M%p"),
				'eventid' : event['id']
                })
 
			# if it's currently running ...
			if start < now and end > now:
				if 'hangoutLink' in event:
					status = "OnAir"
					roomCurrentState = pyScreen.roomState.busyHangout
				else:
					status = "BUSY"
					roomCurrentState = pyScreen.roomState.busy
					
				currentEventId=event['id']
				next_end = (end - now)

			if start > now and not next_start:
				next_start = (start - now)


	next_start_str = create_time_string(next_start)
	next_end_str = create_time_string(next_end)

	if roomCurrentState == pyScreen.roomState.free and next_start and next_start < timedelta(minutes=15):
		roomCurrentState = pyScreen.roomState.soonBusy
		status = "SOON"

	print 'status ', status, 'start in ', next_start_str, 'end in ',next_end_str
	print '============================================='

	return {'room': events['summary'], 
		'serviceEngine' : service,
		'roomState' : roomCurrentState,
		'currentEventId':currentEventId,
        'status': status, 
        'now': now.strftime("%A %d %B %Y, %I:%M%p"), 
		'calendarid' : room_id,
        'events': items, 
        'next_start_str': next_start_str, 
        'next_end_str': next_end_str}

		
		
		

		
		


# build a screen  
cs=pyScreen.calenderScreen()

rn=calendar_config.CALENDAR

exceptionsCaught=0

while True:

	try:
		print 'get_events',
		events=get_events(rn)
		print 'out'
		print 'Consume',
		cs.Consume(rn,events)
		print 'out'

		# reset exceptions caught
		exceptionsCaught=0
	except Exception as e:
		print 'exception - ',e
		exceptionsCaught=exceptionsCaught+1
		if exceptionsCaught>10:
			os.system('sudo shutdown -r')
			break

	print 'ui',
	cs.UserInteraction(45)
	print 'out'




	
