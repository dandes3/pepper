#
# Created by Don Andes
#

# Define needed base values
baseString = ("BEGIN:VCALENDAR\nCALSCALE:GREGORIAN\nVERSION\nX-WR-CALNAME:Schedule\nBEGIN:VTIMEZONE\nTZID:America/New_York\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0500\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nDTSTART:20070311T020000\nTZNAME:EDT\nTZOFFSETTO:-0400\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0400\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nDTSTART:20071104T020000\nTZNAME:EST\nTZOFFSETTO:-0500\nEND:STANDARD\nEND:VTIMEZONE\n")
workLoc = ("300 Monticello Ave\, Macarthur Center\, Norfolk\, VA 23510")
uidList = []
eventList = []

uidCount = 0;
eventCount = 0;


print("\n")
print("Welcome to pepper.\n")
fileMod = input("Please enter the name of the file to be changed: ")

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

if uidCount > eventCount:
	uidList.pop(0)
	uidCount-=1

print("\n")
print("UIDs scraped are: ")
print(uidList)
print("Number of UIDs are: ")
print(uidCount)
print("Events scraped are: ")
print(eventList)
print("Number of events are: ")
print(eventCount)


		


newFile.write(baseString)


# Clean up work
oldFile.close()
newFile.close()

