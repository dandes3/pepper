#
# Created by Don Andes
#

# Define needed base string
baseString = ("BEGIN:VCALENDAR\nCALSCALE:GREGORIAN\nVERSION\nX-WR-CALNAME:Schedule\nBEGIN:VTIMEZONE\nTZID:America/New_York\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0500\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nDTSTART:20070311T020000\nTZNAME:EDT\nTZOFFSETTO:-0400\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0400\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nDTSTART:20071104T020000\nTZNAME:EST\nTZOFFSETTO:-0500\nEND:STANDARD\nEND:VTIMEZONE\n")
uidList = []
startEnd = []
filler = []
uidTest = "UID:"


print("\n")
print("Welcome to pepper.\n")
fileMod = input("Please enter the name of the file to be changed: ")

# Open up given file and create new
oldFile = open(fileMod)
newFile = open("modified.ics", "w")



for line in oldFile:
	if line[:4] == uidTest:
		uidList.append(line[-17:])


newFile.write(baseString)


# Clean up work
oldFile.close()
newFile.close()

