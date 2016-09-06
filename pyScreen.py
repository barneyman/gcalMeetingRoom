
import pygame
import os


class pySurface:

	def __init__(self, hostScreen, location=(0,0), size=(-1,-1)):
		
		self.actualScreen=hostScreen.ActualScreen()
		
		parentExtents=hostScreen.GetExtents()
		
		self.myExtents=pygame.Rect(parentExtents)
		
		self.myExtents.x=parentExtents.x+location[0]
		self.myExtents.y=parentExtents.y+location[1]
		
		self.myExtents.w=size[0]
		self.myExtents.h=size[1]
		
		if size[0]==-1:
			self.myExtents.w=parentExtents.w-location[0]
			
		if size[1]==-1:
			self.myExtents.h=parentExtents.h-location[1]
			
		self.surface=pygame.Surface((self.myExtents.w,self.myExtents.h))
		self.surface=self.surface.convert()
		
		
		
	def GetExtents(self):
		return self.myExtents
		
	def DrawCentreText(self, text,size=25, textrgb=(255,255,255)):
		scantext=self.BuildText(text,size,textrgb)
		textbox=scantext.get_rect()
		textbox.centerx = self.surface.get_rect().centerx
		self.surface.blit(scantext, textbox)
		self.ActualScreen().blit(self.surface,(self.myExtents.x,self.myExtents.y))
		return textbox
		
	def DrawLeftText(self, text,size=25, textrgb=(255,255,255),offset=(0,0)):
		scantext=self.BuildText(text,size,textrgb)
		textbox=scantext.get_rect()
		textbox.left = self.surface.get_rect().left
		textbox=textbox.move(offset)
		self.surface.blit(scantext, textbox)
		self.ActualScreen().blit(self.surface,(self.myExtents.x,self.myExtents.y))
		return textbox
		
	def BuildText(self, text,size=25, textrgb=(255,255,255)):
	
		# have a look for newlines
		lines=text.split('\n')
	
		if len(lines)==1:
			font=pygame.font.Font(None,size)
			scantext=font.render(text,1,textrgb)
			return scantext
			
		textboxes=list()
			
		for each in lines:
			textboxes.append(self.BuildText(each,size,textrgb))
			
		newSurfDims=pygame.Rect(0,0,0,0)
		for each in textboxes:
			if each.get_rect().w > newSurfDims.w:
				newSurfDims.w=each.get_rect().w
			newSurfDims.h=newSurfDims.h+each.get_rect().h
			
		textSurface=pygame.Surface((newSurfDims.w,newSurfDims.h))
		textSurface=textSurface.convert()
		
		colorkey=(128,128,128)
		textSurface.set_alpha(None)
		textSurface.set_colorkey(colorkey)
		textSurface.fill(colorkey)
		
		lineTop=0
		for each in textboxes:
			linebox=each.get_rect()
			linebox.top=lineTop
			lineTop=lineTop+linebox.h
			textSurface.blit(each,linebox)
			
		return textSurface
			
	
	
	def ActualScreen(self):
		return self.actualScreen
	

	def cls(self, rgb=(0,0,0)):
		self.surface.fill(rgb)
		self.ActualScreen().blit(self.surface,(self.myExtents.x,self.myExtents.y))
		#pygame.display.flip()
	
	
	
class pyScreen:

	def __init__(self):
#		os.environ["SDL_FBDEV"] = "/dev/fb0"
#		os.environ['SDL_VIDEODRIVER']="directfb"

		# for touch screen
#		os.environ['SDL_MOUSEDRV']='TSLIB'
#		os.environ['SDL_MOUSEDEV']='/dev/input/event0'

		pygame.init()

		if self.pyScreen_get_init():
			self.screenSize=pygame.Rect(0,0,pygame.display.Info().current_w,pygame.display.Info().current_h)
			self.screen = pygame.display.set_mode((self.screenSize.w,self.screenSize.h))
	
		pygame.mouse.set_visible(0)

	def pyScreen_get_init(self):
		return pygame.display.get_init()
		
	def ActualScreen(self):
		return self.screen

	#def Display(self, details):
	
	# the ACTUAL screen co-ords in a pygame.rect
	def GetExtents(self):
		return self.screenSize
		
		

	def cls(self, rgb=(0,0,0)):
		self.screen.fill(rgb)
		#pygame.display.flip()


	def mousey(self):

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print "quitting"
					pygame.quit()
					sys.exit()

				# print if mouse is pressed.
				# get_pressed() tells you which mouse button is pressed
				if event.type == pygame.MOUSEBUTTONDOWN:
					print 'mouse pressed ', pygame.mouse.get_pressed()
				# print if mouse is released.
				elif event.type == pygame.MOUSEBUTTONUP:
					print 'mouse released', pygame.mouse.get_pressed()
				elif event.type == pygame.MOUSEMOTION:
					print "mouse at (%d, %d)" % event.pos


					
					
					
###############################

#from enum import Enum
class roomState(object):
	free=1
	soonBusy=2
	busy=3
	busyHangout=4

class calenderScreen:

	def __init__(self):
		# main screen
		self.mainScreen=pyScreen()
		self.screensize=self.mainScreen.GetExtents()
		# left hand status
		self.mainStatusWnd=pySurface(self.mainScreen,(0,0),(self.screensize.w/2,-1))
		# free/busy window
		self.freeBusyWnd=pySurface(self.mainStatusWnd,(2,2),((self.screensize.w/2)-4,150))
		self.current=pySurface(self.mainStatusWnd,(2,152),((self.screensize.w/2)-4,25))
		self.datetime=pySurface(self.mainStatusWnd,(2,self.screensize.h-20),((self.screensize.w/2)-4,18))
		
		# right hand 
		self.mainRoomWnd=pySurface(self.mainScreen,(self.screensize.w/2,0),(self.screensize.w/2,-1))
		self.roomName=pySurface(self.mainRoomWnd,(2,2),((self.screensize.w/2)-4,250))
		self.roomEvents=pySurface(self.mainRoomWnd,(2,252),((self.screensize.w/2)-4,-1))
		
		
	def Consume(self, roomname, events):
		# first, get room status
		status=events['roomState']
		narrative='No upcoming events'
		if status==roomState.free:
			rgbback=(0,128,0)
			if events['next_start_str']:
				narrative='Next event starts in '+events['next_start_str']
		if status==roomState.busy or status==roomState.busyHangout:
			rgbback=(200,0,0)
			if events['next_end_str']:
				narrative='Current event ends in '+events['next_end_str']
		if status==roomState.soonBusy:
			rgbback=(255,165,0)
			if events['next_start_str']:
				narrative='Next event starts in '+events['next_start_str']
				
		
		self.mainScreen.cls(rgbback)
		self.mainStatusWnd.cls(rgbback)
		self.freeBusyWnd.cls(rgbback)
		self.datetime.cls(rgbback)
		self.current.cls(rgbback)


		#out = alpha * new + (1 - alpha) * old
		rgba=((int)((255*.8)+(.2*rgbback[0])),(int)((255*.8)+(.2*rgbback[1])),(int)((255*.8)+(.2*rgbback[2])))
		
		self.mainRoomWnd.cls(rgba)
		self.roomName.cls(rgba)
		self.roomEvents.cls(rgba)

		

		self.mainStatusWnd.DrawLeftText(events['status'],150,(255,255,255))
		self.current.DrawLeftText(narrative,25,(255,255,255))
		self.datetime.DrawLeftText(events['now'],25,(255,255,255))
		
		roomname=roomname.replace(' ','\n')
		
		self.roomName.DrawLeftText(roomname,100,(0,0,0))
		
		topline=0;
		for event in events['events']:
			line=event['name']+'\n'+event['creator']+'\n'+event['start']+' - '+event['end']
			topline=topline+self.roomEvents.DrawLeftText(line,25,(0,0,0),(0,topline)).h + 5
		
		pygame.display.flip()


