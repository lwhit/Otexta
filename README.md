# Otexta
ECE 4564 Assignment I   
Team: The Internet Explorers    
Contact: lwhit@vt.edu

##Client and Server Initialization
Before running the server, ensure that a previous instance of the server file (wolf359.py) is not already running. If it is running then the server will not be able to use the port number given by the "port" variable. In this case, running wolf359.py will result in the following error:  Could not open socket: [Errno 98] Address already in use

To free up the port, the previous instance of the server file will need to be ended. On the RPi, get a list of all current programs running and look for wolf359.py:  "ps aux | grep wolf359.py"    
Once you have the PID of the program, use the kill command to end it: "sudo kill -9 PID"    
Attempt to run wolf359.py again

