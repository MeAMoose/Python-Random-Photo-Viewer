#Imports Libraries
import os
import time
import random
import json
from tkinter import *  
from PIL import ImageTk,Image

#Assigns Base Values
numberList = []
imageList = []
quitVal = False
checkFalse = True
configMissing = False
failCount = 0

root = Tk()                                                                                                             #Links the "tk" function to "root"
root.configure(bg="black")                                                                                              #Makes background black
root.title("Image Randomizer")                                                                                          #Changes program title to "Image Randomizer"

#Default Config --DO NOT CHANGE--
defaultConfig = {"settings":[{"imageLibrary": "", "imageDelay": "", "debug": ""}]}                                      #Default config template, called on if config is missing.

#Config Loader/Compiler (builds base config if missing)
try:                                                                                                                    #Attempts to read config.
    with open("config.json") as json_file:
        data = (json.load(json_file))["settings"][0]                                                                    #Assigns data in file to a variable.

except FileNotFoundError:                                                                                               #If config is missing, generates config using default template
    with open('config.json', 'w') as outFile:
        json.dump(defaultConfig, outFile, indent=4)
        configMissing = True


#Configurable Values (errors if config not filled in/newly generated)
try:                                                                                                                    #Attempts to read data from variable (data from config)
    imageLibrary = data["imageLibrary"]
    imageDelay = float(data["imageDelay"]) 
    debug = bool(data["debug"])
except (NameError, ValueError):                                                                                         #If config has invalid features
    if configMissing == True:                                                                                           #If the config was originally missing, prompts user that the config has been generated and needs configuring.
        print("Config Missing or Invalid, please configure then retry")
        input()
        quit()
    else:                                                                                                               #Else, will display standard invalid message and prompt user to re-configure their config.
        print("Config Invalid, please reconfigure then retry")
        input()
        quit()

#Generates a list of images from the "ImageLibrary" folder
for q in range(len(os.listdir(imageLibrary))):
    checkValue = (os.path.splitext(os.listdir(imageLibrary)[q]))[1]                                                     #Takes the files extention
    if checkValue == ".png" or checkValue == ".jpg" or checkValue == ".jpeg" or checkValue == ".gif":                   #Checks the files extention if it matches a valid image format.
        imageList.append(imageLibrary+"\\"+os.listdir(imageLibrary)[q])                                                 #Adds file directory to list.
    elif debug == True:
        print("Invalid Detected, skipping")                                                                             #Skips any files with invalid extentions (.int, .exe etc...)
print(f"Image List Size: {len(imageList)}")


# Seed Generator
def seedGen():                                                                                                          #Generates a seed of valid length, with each number being unique.
    global checkFalse

    if debug == True:
        print("Generating Seed.")
    numberList.clear()
    while len(numberList) != (len(imageList)):                                                                          #Loops for length of the imageList (x amount of images in a folder)
        randomizer = random.randint(1,(len(imageList)))                                                                 #Generates a random number between 1 and the imageList length (highest value of images)
        for q in range(len(numberList)):                                                                                #Loops for the number of numbers in the numberList that correlate to the imageList
            if randomizer == numberList[q]:                                                                             #If the randomly generated number is already in the list, skips number and re-generates it.
                randomizer = random.randint(1,(len(imageList)))
                checkFalse = False
                break
        if checkFalse != False:
            numberList.append(randomizer)                                                                               #If random number is unique, add it to numberList
        checkFalse = True
    if debug == True:
        print(f"Seed Successfully Generated\n{numberList}")

seedGen()
#Loops Indefinately
while quitVal != True:                                                                                                  #Loops indefinately.
    for n in range(0,len(imageList)):                                                                                   #Repeats for length of the imageList (number of images)
        #Opens the image
        try:                                                                                                            #Attempts to parse and display image.
            im = Image.open(rf"{imageList[numberList[n]-1]}")
            if im.size[0] >= root.winfo_screenwidth() or im.size[1] >= root.winfo_screenheight():
                im.thumbnail((root.winfo_screenwidth(),root.winfo_screenheight()))
            myimg = ImageTk.PhotoImage(im)
            myLabel = Label(image=myimg,bg="black")
        except IndexError:                                                                                              #Failsafe incase invalid indexing occurs.
            print("IndexError has Occured\n")                                                                           #Basic debug information.
            print("ImageList: ",imageList)
            print("NumberList: ",numberList)
            print("For 'n' Number",n)
            input()
            quit()
        while failCount != 1:                                                                                           #Only runs once.
            windowWidth = im.size[0]
            windowHeight = im.size[1]
 
            positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
            positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

            root.geometry('%dx%d+%d+%d' % (im.size[0],im.size[1],positionRight,positionDown))                           #Designates the size of the starter window.
            failCount = 1
        root.update()                                                                                                   #Updates the tkinter menu.
        for q in range(round(80*imageDelay)):                                                                           #Cycles the tkinter window at a rate of 80 * config(imageDelay)
            try:                                                                                                        #Attempts to dynamically change padding to suit screen and window resolution.
                myLabel.grid(row=0,column=0,columnspan=3,padx=((root.winfo_width()-im.size[0])/2),pady=((root.winfo_height()-im.size[1])/2))
            except:
                try:
                    myLabel.grid(row=0,column=0,padx=((root.winfo_width()-im.size[0])/2),pady=0)
                except:
                    try:
                        myLabel.grid(row=0,column=0,padx=0,pady=((2-im.size[1])/2))
                    except:
                        myLabel.grid(row=0,column=0,padx=0,pady=0)
            time.sleep(1/120)                                                                                           #Program pauses 1/120 of a second.
            root.update()
        myLabel.grid_forget()                                                                                      #After cycle, removes previous image from grid.
    #Resets the list once all numbers have been successfully cycled through.
    if len(imageList) == len(numberList):                                                                               #If all numbers in list have been cycles, regenerate seed.
        if debug == True:
            print("List At Maximum Capacity, Resetting")
        seedGen()                                                                                                       #Regenerates the seed.

#TODO
#
#1. Change the window size from relative to fixed (when changing images)        [DONE]
#2. Center the image to the center of the window regardless of window size/location.        [DONE]
#3. Increase the window refresh rate to work without lag input (replace time.sleep with a deltatime system)     [DONE]
#
#FUTURE: Repurpose this program from images to music (mp3 and mp4) files.