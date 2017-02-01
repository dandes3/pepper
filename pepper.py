#
# Created by Don Andes
#

# This program accepts an ICS calender file and scrapes events from it. It then re-writes these events
# into a nicely re-formatted new ICS file that includes additional information such as address
# for work, appropriate name, and URL to login to time site. 
# This software is provided FOR EDUCATIONAL USE ONLY, the writer assumes no risk or fault if you are late to your job.
# That is your own fault. 

# This should never be run outside of the packaged application in standalone mode.


# For directory movements and termination
import os
import sys

# Imports modified for python 2 compatibility
from Tkinter import *
import tkFileDialog
import tkSimpleDialog

# Pushes all Python windows to front in OS X 
#os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

# Anchor for GUI window using TKinter. 
master = Tk()
master.wm_title("Pepper")
master.configure(background='grey')
master.minsize(width=350, height=140)
master.maxsize(width=350, height=140)

def nuke():
	''' Assures when the program is exited prematurely, no files are written. '''
	sys.exit()
	master.destroy()

# Assigns closing function to behaviour of master window
master.protocol("WM_DELETE_WINDOW", nuke)

# Define needed base values (They're chunky and they know it)
baseString = ("BEGIN:VCALENDAR\nCALSCALE:GREGORIAN\nVERSION\nX-WR-CALNAME:Schedule\nBEGIN:VTIMEZONE\nTZID:America/New_York\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0500\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nDTSTART:20070311T020000\nTZNAME:EDT\nTZOFFSETTO:-0400\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0400\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nDTSTART:20071104T020000\nTZNAME:EST\nTZOFFSETTO:-0500\nEND:STANDARD\nEND:VTIMEZONE\n")
string2 = ("BEGIN:VEVENT\nUID:")
string3 = ("\nDTEND;TZID=America/New_York:")
string4a = ("\nTRANSP:OPAQUE\nX-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\nSUMMARY:")
string4c = ("\nDTSTART;TZID=America/New_York:")
string5 = ("\nLOCATION:300 Monticello Ave\, Macarthur Center\, Norfolk\, VA 23510\nDESCRIPTION:Work Schedule\nURL;VALUE=URI:https://mypage.apple.com\nEND:VEVENT\n")
string6 = ("END:VCALENDAR\n")
uidList = []
eventList = []

uidCount = 0;
eventCount = 0;

# Test for config file, prompt for event name and create if doesn't exist
try:
    configFileTester = open('config.txt')
    configFileTester.close()
except IOError as e:
	eventName = tkSimpleDialog.askstring("Initial Configuration", "Enter the name you want for the events")
	if eventName == '':
		nuke()
	if eventName == ' ':
		nuke()
	configFile = open("config.txt", "w")
	configFile.write(eventName)
	configFile.close()

# Pull name from config file
with open('config.txt', 'r') as configFile:
    eventName = configFile.readline()

# Build new append string with event name from user
string4 = string4a+eventName.rstrip("\n")+string4c


def callback():
	''' Creates button that throws a file selecton box to the user. Selected file will be old file to parse through.'''
	global fileMod # Quick and dirty fix for encapsulaton of tk button functions
	fileMod = tkFileDialog.askopenfilename() # Line modified for python 2 compatibility
	master.quit()

# Create and pack in dialog and button. Enter loop awaiting user file selection
#T = Text(master, height=7, width=50)
#T.pack()
#T.configure(state='normal')
label1 = Label(master, text="                      Welcome                      \n\nClick the button below to select your downloaded\n.ics file from myPage. Modified file will be\nsaved into the folder you put Pepper in. \n", background='grey')
#T.insert(END, "//////////////// Welcome to Pepper ///////////////\n\nClick the button below to select your downloaded\n.ics file from myPage. Modified file will be\nsaved into the folder you put Pepper in. ")
#T.configure(state='disabled')
label1.pack()
b = Button(master, text="Click to select file", command=callback)
b.pack()
mainloop()

try:
	# Open up given file and create new
	oldFile = open(fileMod, "r+")

except NameError:
	# TODO: make exit silent at this point for debugging purposes. Causes no issues with packaged app.
	nuke()

# Quick and dirty directory movement up and out of application bundle into parent directory
# os.chdir("..")
# os.chdir("..")
# os.chdir("..")

newFile = open("modified.ics", "w") 

# Parse file to find UIDs and start/end time pairs, adds UIDs to array and groups start/end into arrays and appends to larger array
oldIter = iter(oldFile)
for line in oldIter:
	filler = []
	if line[:4] == "UID:":
		uidScratch, uidVal = line.split(":")
		uidList.append(uidVal.rstrip("\n"))
		uidCount+=1

	elif line[:8] == "DTSTART:":
		line2 = next(oldIter)
		if line2[:6] == "DTEND:":
			startScratch, startVal = line.split(":")
			filler.append(startVal.rstrip("\n"))
			endScratch, endVal = line2.split(":")
			filler.append(endVal.rstrip("\n"))
			eventList.append(filler)
			eventCount+=1

# Correction for occasional extra first UID
if uidCount > eventCount:
	uidList.pop(0)
	uidCount-=1

# Close file and re-open as append mode for safety
newFile.write(baseString)
newFile.close()

newFile = open("modified.ics", "a+")

# Constuct strings to write to file out of pre-made strings and scraped values
for i in range(len(uidList)):
	temp1 = string2+uidList[i]
	temp2 = string3+eventList[i][1]
	temp3 = string4+eventList[i][0]+string5
	newFile.write(temp1+temp2+temp3)

# Ends ics file
newFile.write(string6)

# Clean up work
newFile.close()
oldFile.close()


