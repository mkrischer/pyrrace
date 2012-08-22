# car.py

import pygame, random, math
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

debug = False

screenx = 1200
screeny = 800

car_length = 70
car_width = 70

screen = pygame.display.set_mode([1200,800])
pygame.display.set_caption("Car Race")

bkcol=[200,200,200]

#read all car images into object dictionary
i=0
images = {}
while i < 360:
	obj = "images/car"+str(i)+".png"
	images[i] = pygame.image.load(obj).convert_alpha()
	i+=5

#paint field
tribune = 50	#space used by tribune (map specific)

#b/w map edition for easier collision detection
bw_field = pygame.image.load("images/racefield_bw.png")
bw_racefield = pygame.Surface((screenx,screeny))
bw_racefield.blit(bw_field,[0,0])
bw_racearray = pygame.PixelArray(bw_racefield)

#racemap image
field = pygame.image.load("images/racefield.png").convert_alpha()
racefield = pygame.Surface((screenx,screeny))
racefield.set_colorkey(bkcol)
racefield.blit(field,[0,0])

#the car
car = pygame.Surface((car_length, car_width ))
car.fill(bkcol)
car.set_colorkey(bkcol)

#the statusfield
statusfield = pygame.Surface((350,120))
statusfield.fill((200,200,200))


#first starter
startx1 = 525 
starty1 = 664

#second starter
startx2 = 495
starty2 = 700

#third starter
startx3 = 430
startx3 = 664

#fourth starter
startx4 = 380
starty4 = 700

#start position
carx = startx1		#map specific
cary = starty1		#map specific
angle = 0			#0 = facing east
car = images[angle]		#load 0 image
screen.blit(car,[carx,cary])	#paint car

#some world values
reaction = 70		#steering wheel and gas/brake delay
max_kmh = 280		#max kmh shown on speedometer (all steps will be calculated with)

speed = 0		#start speed
max_speed = 5		#max speed
grass = 4		#cut maxspeed/grass
sand  = 5		#cut maxspeed/sand
max_backward = -1	#max backward speed
bumper=5		#how much feedback from walls
crash_brake = 0.5	#how much speed is lost on hitting the wall
brake = 0.1		#force for brakes
acc   = 0.1		#force for acceleration
slowdown = 0.005	#speed lost if not acc

crash = False		#crash detection
damage = 0		#start damage level
max_damage = 10		#max damage level
crash_damage = 1	#damage added per crash

laps = 0		#laps gone
lasttime = 0		#last lap
fasttime = 0		#fastest lap
time = 0		#timer

checkpoint1 = True	#checkpoint on the road (default: True, for start)
checkpoint2 = True	#checkpoint on the road (default: True, for start)
newlap = False 		#don't add a new lap if checkpoints aren't flagged true

pygame.key.set_repeat(reaction, 25)	#keyboard multiply strokerate

#speedometer
speedfont = pygame.font.Font("lcdb.ttf", 30)

#carpos
carposfont = pygame.font.Font(None, 14)

#status
statusfont = pygame.font.Font(None, 16)

#timer
xfont = pygame.font.Font("lcdb.ttf", 20)

#msg
msgfont = pygame.font.Font(None, 60)

while True:
        #print "car at", carx, cary

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			break
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
				break
			if event.key == pygame.K_LEFT:			  
				angle = angle - 5
				if angle == -5:
					angle = 355
				car = images[angle]
			if event.key == pygame.K_RIGHT:
				angle = angle + 5
				if angle == 360:
					angle = 0
				car = images[angle]
			if event.key == pygame.K_UP:
				if speed + acc < max_speed:
					speed = speed + acc
				else:
					speed = max_speed
			if event.key == pygame.K_DOWN:
				if speed > 0 and speed - brake < 0:
					speed = 0
				if speed <= 0 :
					speed = speed - brake/5
					if speed <  max_backward:
						speed = max_backward
				else: 
					speed = speed - brake
        #else:
         #       if speed - slowdown > 0:
          #              speed = speed - slowdown
           #     if speed <= 0:
            #            speed = 0


	#check for damage
	if damage >= max_damage:
		msg = "CAR BROKEN"
		msgtext = msgfont.render(msg, True, (255,0,0), (0,0,0))
		screen.blit(msgtext, (screenx/3, screeny/2-25))
		break	

	# crashing the walls? the outer edges
	if carx <= 0:
		carx  = 0 + bumper
		crash = True
	elif carx >= screenx - (car_width/2):
		carx = screenx - (car_width/2) - bumper
		crash = True
        elif cary <= 0:
		cary = 0 + bumper
		crash = True
	elif cary >= screeny - (car_width/2) - tribune:
		cary = screeny - (car_width/2) - tribune - bumper
		crash = True
	if crash:
		speed = speed - crash_brake
		damage += speed/max_speed*crash_damage
		crash = False
	
	#mark area for checkpoint 1 
	if cary > 25 and cary < 131:
		if carx > 980 and carx < 1000 and checkpoint1 == False and newlap:
			checkpoint1 = True
			print "hit checkpoint 1"
	
	#mark area for checkpoint 2
	if carx > 45 and carx < 180:
		if cary > 350 and cary < 370 and checkpoint2 == False and checkpoint1 and newlap:
			checkpoint2 = True
			newlap = False
			print "hit checkpoint 2"

	#initial lap count
	if cary > 635 and cary < 735:
		if carx > 582 and carx < 600 and newlap == False:
			checkpoint1 = False	#reset checkpoints
			checkpoint2 = False
			newlap = True		#tell checkpoints we have a new lap
			laps = laps + 1		#inc lap no
			lasttime = time		#save time
			time = 0		#reset time
			#check if we have a fastest lap
			if lasttime > 0 and lasttime < fasttime or fasttime == 0:
				print "New time record"
				fasttime = lasttime
			print "lap" + str(laps)

        # calculate speed according to driving angle
	movx = speed * math.cos(math.radians(angle))
	movy = speed * math.sin(math.radians(angle))
	carx = carx + movx 
	cary = cary + movy

        # Render speedometer
        kmh = (speed * max_kmh) / max_speed
        if kmh < 0:
                speedometer = "R %3d km/h" % (math.fabs(int(kmh)))
        else:
                speedometer = "%3d km/h" % (int(kmh))
        speedtext = speedfont.render(str(speedometer), True, (0, 0, 0), (200, 200, 200))
	
	#render coords
	carpos = str(round(carx)) + ", " + str(round(cary))
	carpostext = carposfont.render(carpos, True, (255,255,255), (0,0,0))
		
	#check for course
	if bw_racearray[int(carx)][int(cary)] == bw_racefield.map_rgb((0,0,0)):
		#wiese
		status = "Runde %d - (Wiese)" % (laps)
		if speed >= max_speed/grass:
			speed = max_speed/grass
		
	elif bw_racearray[int(carx)][int(cary)] == bw_racefield.map_rgb((255,255,255)):
		#strasse
		status = "Runde %d - (Piste)" % (laps)
	else:
		#sand
		status = "Runde %d - (Bunker)" % (laps)
		if speed >= max_speed/sand:
			speed = max_speed/sand
	
	#render status
	statustext = statusfont.render(status, True, (255,255,0))
	
	#race clock
	if laps > 0:
		time = time + clock.get_time() 
	
	timer1 = "Letze Runde:  " + str(round(lasttime/float(1000),3))
	timer2 = "Schnellste Runde:  " + str(round(fasttime/float(1000),3))
	timer3 = "Aktuelle Zeit:  " + str(round(time/float(1000),3))
	damage = "Schaden:  " + str(damage/max_damage*100) + "/" + str(max_damage*10)

	xt1 = xfont.render(timer1, True, (0,0,0), (200,200,200)) #lastlap
	xt2 = xfont.render(timer2, True, (0,0,0), (200,200,200)) #fastestlap
	xt3 = xfont.render(timer3, True, (0,0,0), (200,200,200)) #acttime
	xt4 = xfont.render(damage, True, (0,0,0), (200,200,200)) #car damage
	
	#paint all stuff
        screen.blit(racefield,[0,0])
	screen.blit(statusfield,((screenx/2)-300, screeny-300))	
        screen.blit(speedtext, (screenx/2-100, screeny-225))        
	screen.blit(xt1, (screenx/2-290, screeny-295))
	screen.blit(xt2, (screenx/2-290, screeny-270))
	screen.blit(xt3, (screenx/2-290, screeny-245))
	screen.blit(xt4, (screenx/2-290, screeny-220))
	screen.blit(car,[carx-35,cary-35])

	if debug:
		screen.blit(carpostext, (50, screeny-50))
		screen.blit(statustext, (50, 50))

	pygame.display.update();
	clock.tick(100)
pygame.quit()
