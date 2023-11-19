import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

chunks = [0,0,0,0,0,0,0,0,0,0]
global motions1
global motions2
global minMot

motions1 = 0
motions2 = 0
minMot = 0

lastChunk = 0
significance = 0 #0 = no singificant motion detected, 1 = significant motion detected
lastingSignificance = 0

inBed = 0 #0 = no, 1 = yes
state = 0 #1 = deep sleep, 2 = light sleep, 3 = restless, 4 = other activities

schro = 0 #0 = definitive inBed, 1 = unsure inBed
timPas = 0 #How much time has passed since last polling period
moveObs = 0 #How much minor movement has been observed since last polling period
expect = 0 #The state of sleep expected from the single time block
restCount = 0 #The number of continuous uninterupted rest conclusions

def callback(channel):
        global motions1
        global motions2
        global minMot

        minMot = minMot + 1
        if GPIO.input(channel):
                print("Movement 1 Detected!")
                motions1 = motions1 + 1
        else:
                print("Movement 2 Detected!")
                motions2 = motions2 + 1

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=50)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

file1 = open("vibLog.txt", "w")
file1.write("start\n")
file1.close 

# infinite loop
while True:
        #print(GPIO.input(channel))
        for x in range(30):
                time.sleep(2)
                if (minMot == 0):
                        lastChunk = 0
                        chunks[0] = chunks[0] + 1
                elif (minMot < 5):
                        lastChunk = 1
                        chunks[1] = chunks[1] + 1
                elif (minMot < 10):
                        lastChunk = 2
                        chunks[2] = chunks[2] + 1
                elif (minMot < 15):
                        lastChunk = 3
                        chunks[3] = chunks[3] + 1
                elif (minMot < 20):
                        if (lastChunk >= 4):
                                significance = 1
                        lastChunk = 4
                        chunks[4] = chunks[4] + 1
                elif (minMot < 25):
                        significance = 1
                        lastChunk = 5
                        chunks[5] = chunks[5] + 1
                elif (minMot < 30):
                        significance = 1
                        lastChunk = 6
                        chunks[6] = chunks[6] + 1
                elif (minMot < 35):
                        significance = 1
                        lastChunk = 7
                        chunks[7] = chunks[7] + 1
                elif (minMot < 40):
                        significance = 1
                        lastChunk = 8
                        chunks[8] = chunks[8] + 1
                else:
                        lastChunk = 9
                        chunks[9] = chunks[9] + 1
                minMot = 0
                
        
        #Drawing conclusions
        
        if (significance > 0):        
                lastingSignificance = lastingSignificance + 1
        significance = 0
                
        if (lastingSignificance > 0):
                expect = 4
                if (lastingSignificance > 2):
                        state = 4
        else:
                if (motions1 <= 4 and motions2 <= 2):
                        expect = 1
                elif (chunks[2] == 0 and chunks [3] == 0 and chunks[4] == 0):
                        expect = 2
                else:
                        expect = 3
        
        if (expect == 4):
                if (state != 4):
                        schro = 1
                        inBed = 1
                
                        state = 3
                timPas = 0
                moveObs = 0
        else:
                timPas = timPas + 1
                if (expect > 1):
                        moveObs = moveObs + 1
                if (inBed == 0): #Previously though the bed was empty
                        if (expect == 0):
                                #eveything is as normal. Run a line to fill the block
                                moveObs = moveObs
                        elif (expect == 1): #Potential movement
                                schro = 1
                                timPas = 0
                                moveObs = 0
                        else: #person-recognized motion occured when the bed was thought to be empty
                                inBed = 1
                                state = expect
                if (inBed == 1):
                        if (state == 1):
                                if (expect == 3):
                                        state = 2
                                        restCount = 0
                                        timPas = 0
                                        moveObs = 0
                                if (timPas >= 30): #every 30 blocks
                                        if (moveObs > 2):
                                                state = 2
                                                restCount = 0
                                        timPas = 0
                                        moveObs = 0
                        if (state == 2):
                                if (timPas >= 10): #every 10 blocks
                                        if (moveObs < 1):
                                                restCount = restCount + 1
                                        else:
                                                restCount = 0
                                        if (moveObs > 3):
                                                state = 3
                                        if (restCount > 3): #If the rest has been continous
                                                state = 1
                                        timPas = 0
                                        moveObs = 0
                        if (state == 3):
                                if (timPas >= 10): #every 10 blocks
                                        if (moveObs < 2):
                                                state = 2
                                                restCount = 0
                                        timPas = 0
                                        moveObs = 0
                        if (schro > 0):
                                if (timPas >= 5):
                                        if (moveObs < 2):
                                                inBed = 0
                                                state = 0
                                        schro = 0
                                
        
        #Recording data
                
        file1 = open("vibLog.txt", "a") 
        file1.write("Motion 1: " + str(motions1) + "\n")
        file1.write("Motion 2: " + str(motions2) + "\n")
        for x in range(9):
                file1.write("Chunk " + str(x) + ": " + str(chunks[x]) + "\n")
                chunks[x] = 0
        file1.write("---------------------------------\n")
        motions1 = 0
        motions2 = 0
        minMot = 0
        file1.close
        file1 = open("vibLog.txt", "a") 
        file1.close
        print("wrote an entry")
        
