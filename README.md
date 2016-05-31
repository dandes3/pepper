# Pepper
An ICS file modifier and parser with a GUI for learning purposes.

# Environment
This program is packaged and bundle with the application Platypus to utilize the default python version on the given OSX system. It runs under the assumption that python 2 is the current system version, and it is not inside a virtualEnv. 

# Description
This program presents a GUI box prompting the user to select a .ics file downloaded from myPage, which it then parses, stripping the start and end times of every work event. It creates a new .ics file that includes additional information for each event. The final .ics file will be named modified.ics, and will be placed in the directory that Pepper was placed in. The final .ics will include the following additional information for each work event: event name changed to “work,” address for the Apple Store Macarthur center added in location field, time zone changed to EST, alert set to when user needs to leave to arrive on time, description set to “work schedule,” and URL for myPage placed in the URL field. 

# Usage
Copy Pepper into any folder (Downloads, Desktop, etc.) Double click, and click the button to select .ics file downloaded from myPage. Pepper will then create a file called “modified.ics” in the same folder you put Pepper in. Double click “modified.ics” to add your work schedule to your calendar!