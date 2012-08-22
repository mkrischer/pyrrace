# car.py

import pygame, random, math
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

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
	#print "fuege ", obj ,"hinzu"
	images[i] = pygame.image.load(obj).convert_alpha()
	i+=5

#paint field
tribune = 50	#spaceused by tribune (map specific)


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


startx1 = 525 
starty1 = 664

startx2 = 495
starty2 = 700

#start position
carx = startx1		#map specific
cary = starty1		#map specific
angle = 0			#0 = facing east
car = images[angle]		#load 0 image
screen.blit(car,[carx,cary])	#paint car



reaction = 70		#steering wheel
max_kmh = 230		#max kmh shown on speedometer (all steps will be calculated with)

speed = 0		#start speed
max_speed = 4.0		#max speed
max_backward = -1	#max backward speed
bumper=5		#how much feedback from walls
crash_brake = 0.5	#how much speed is lost on hitting the wall
brake = 0.2		#force for brakes
acc   = 0.1		#force for acceleration
slowdown = 0.005	#speed lost if not acc

damage = 0		#start damage level
max_damage = 10		#max damage level
crash_damage = 0.4	#damage added per crash

laps = 0		#laps gone
time = 0		#timer

pygame.key.set_repeat(reaction, 25)	#keyboard multiply strokerate

#speedometer
speedfont = pygame.font.Font("lcdb.ttf", 30)

#carpos
carposfont = pygame.font.Font(None, 14)

#status
statusfont = pygame.font.Font(None, 16)

xfont = pygame.font.Font("lcdb.ttf", 30)

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
	
	# securing the outer edges
	if carx <= 0:
		carx  = 0 + bumper
		speed = speed - crash_brake
	if carx >= screenx - (car_width/2):
		carx = screenx - (car_width/2) - bumper
		speed = speed - crash_brake
        if cary <= 0:
		cary = 0 + bumper
		speed = speed - crash_brake
	if cary >= screeny - (car_width/2) - tribune:
		cary = screeny - (car_width/2) - tribune - bumper
		speed = speed - crash_brake
	
	checkpoints = True
	
	#initial lap count
	if cary > 635 and cary < 735:
		#print "startziel gerade"
		if int(carx) == 590:
			laps = laps + 1

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
		speed = max_speed/4
		
	elif bw_racearray[int(carx)][int(cary)] == bw_racefield.map_rgb((255,255,255)):
		#strasse
		status = "Runde %d - (Piste)" % (laps)
	else:
		#sand
		status = "Runde %d - (Bunker)" % (laps)
		speed = max_speed/5
	
	#render status
	statustext = statusfont.render(status, True, (255,255,0))

	time = time + clock.get_time()/100
	xt = xfont.render(str(round(time,22)), True, (255,255,0))
	#paint all stuff
        screen.blit(racefield,[0,0])
	screen.blit(car,[carx-35,cary-35])
        screen.blit(speedtext, (screenx-150, screeny-50))        
	screen.blit(carpostext, (50, screeny-50))  
	screen.blit(statustext, (50, 50))
	screen.blit(xt, (50, screeny-50))


	pygame.display.update();
	clock.tick(100)
pygame.quit()
