#  ----------------------
# | Created by Don Andes |
#  ----------------------
#
# ----------------------------------------------------------------------------------------------------------------------
#
# This program accepts an ICS calender file and scrapes events from it. It then re-writes these events
# into a nicely re-formatted new ICS file that includes additional information such as address
# for work, appropriate name, and URL to login to time site. 
# This software is provided FOR EDUCATIONAL USE ONLY, the writer assumes no risk or fault if you are late to your job.
# That is your own fault. 
#
# This is not configured to run in a standalone environment, it assumes it is being run as a packaged app. 
#
# If you're reading this I hope you know what you're doing, or at least think you do. 
#
# ----------------------------------------------------------------------------------------------------------------------


# For directory movements and termination
import os
import sys

# Imports modified for python 2 compatibility
from Tkinter import *
import tkFileDialog
import tkSimpleDialog

# TODO: Unbork this
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
string5a = ("\nLOCATION:")
string5b = ("")
string5c = ("\nDESCRIPTION:Work Schedule\nURL;VALUE=URI:https://mypage.apple.com\nEND:VEVENT\n")
string6 = ("END:VCALENDAR\n")
uidList = []
eventList = []

uidCount = 0;
eventCount = 0;

eventName = ""
storeNum = ""

# Test for config file, prompt for event name and create if doesn't exist
try:
	with open('config.txt', 'r') as configFile:
		eventName = configFile.readline()
		storeNum = configFile.readline()

except IOError as e:
	window = Toplevel(master)
	window.attributes('-topmost', True)
	window.title("Setup")
	window.configure(background='grey')
	window.minsize(width=250, height=200)
	window.maxsize(width=250, height=200)

	def babyNuke():
		window.destroy()
		nuke()

	window.protocol("WM_DELETE_WINDOW", babyNuke)

	doc1 = Label(window, text="\nEnter the name for parsed events", background='grey')
	doc1.pack()
	v = StringVar()
	e = Entry(window, textvariable=v)
	e.pack()
	v.set("Work")
	
	doc2 = Label(window, text="\nSelect your store number", background='grey')
	doc2.pack()

	v2 = StringVar(window)
	v2.set("R211") # initial value

	option = OptionMenu(window, v2, "R211", "R614")
	option.pack()

	goNow = False

	def setupDone():
		goNow = True
		eventName = v.get()
		storeNum = v2.get()

		if eventName == '' or eventName == ' ':
			nuke()

		configFile = open("config.txt", "w")

		configFile.write(eventName)
		configFile.write("\n")
		configFile.write(storeNum)
		configFile.close()

		window.destroy()



	doc3 = Label(window, text="\n", background='grey')
	doc3.pack()

	button = Button(window, text="Enter", command=setupDone)
	button.pack()


# Build new append string with event name from user
string4 = string4a+eventName.rstrip("\n")+string4c
cleanStoreNum = storeNum.rstrip("\n")

# Address builder
if cleanStoreNum == "R211":
	string5b = ("300 Monticello Ave\, Macarthur Center\, Norfolk\, VA 23510")

elif cleanStoreNum == "R614":
	string5b = ("701 Lynnhaven Parkway\, Virginia Beach\, VA 23452")


string5 = string5a+string5b+string5c

def callback():
	''' Creates button that throws a file selecton box to the user. Selected file will be old file to parse through.'''
	global fileMod # Quick and dirty fix for encapsulaton of tk button functions
	fileMod = tkFileDialog.askopenfilename() # Line modified for python 2 compatibility
	master.quit()

# Create and pack in dialog and button. Enter loop awaiting user file selection
label1 = Label(master, text="                      Welcome                      \n\nClick the button below to select your downloaded\n.ics file from myPage. Modified file will be\nsaved onto your desktop. \n", background='grey')
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

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

os.chdir(desktop)

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


