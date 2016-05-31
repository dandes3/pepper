#
# Created by Don Andes
#

# This program accepts an ICS calender file and scrapes events from it. It then re-writes these events
# into a nicely re-formatted new ICS file that includes additional information such as address
# for work, appropriate name, and URL to login to time site. 
# This software is provided FOR EDUCATIONAL USE ONLY, the writer assumes no risk or fault if you are late to your job.
# That is your own fault. 

import os


# TODO re-write in python 2 for backwards compatibility 

from tkinter import *   ## notice capitalized T in Tkinter 
import tkinter.filedialog
#from tkinter import *


# Define needed base values (They're chunky and they know it)
baseString = ("BEGIN:VCALENDAR\nCALSCALE:GREGORIAN\nVERSION\nX-WR-CALNAME:Schedule\nBEGIN:VTIMEZONE\nTZID:America/New_York\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0500\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nDTSTART:20070311T020000\nTZNAME:EDT\nTZOFFSETTO:-0400\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0400\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nDTSTART:20071104T020000\nTZNAME:EST\nTZOFFSETTO:-0500\nEND:STANDARD\nEND:VTIMEZONE\n")
string2 = ("BEGIN:VEVENT\nUID:")
string3 = ("\nDTEND;TZID=America/New_York:")
string4 = ("\nTRANSP:OPAQUE\nX-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\nSUMMARY:Work\nDTSTART;TZID=America/New_York:")
string5 = ("\nLOCATION:300 Monticello Ave\, Macarthur Center\, Norfolk\, VA 23510\nDESCRIPTION:Work Schedule\nURL;VALUE=URI:https://mypage.apple.com\nEND:VEVENT\n")
string6 = ("END:VCALENDAR\n")
uidList = []
eventList = []

uidCount = 0;
eventCount = 0;


# GUI window using TKinter. 
master = Tk()

def callback():
	''' Creates button that throws a file selecton box to the user. Selected file will be old file to parse through.'''
	global fileMod
	fileMod = tkinter.filedialog.askopenfilename()
	master.quit()

# Create and pack in dialog and button. Enter loop.
T = Text(master, height=5, width=50)
T.pack()
T.insert(END, "Welcome to Pepper.\n Click the below button to select your .ics\nfile from myPage. Modified file will be saved in\nthe folder you put Pepper in. ")
master.wm_title("Pepper")
b = Button(master, text="Click to select file", command=callback)
b.pack()
mainloop()


# Open up given file and create new
oldFile = open(fileMod, "r+")
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


