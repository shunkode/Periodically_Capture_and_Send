# What's this?
This program periodically takes pictures and transfers data to Dropbox.  
You can execute this by command of "python main.py"  
Also, you can change config like width, height, framerate, interval of capture, etc.   

It works well, but is not yet organized.  
If you have any questions, feel free to ask.

# Features of v7
This program is dedicated to video recording using a raspberry pi, USB camera and opencv.  
It introduces multiprocessing and Queue, and uses separate cores for acquiring frames and saving frames in video format (plus data transfer).  
This solves the problem of not getting the specified frame rate when shooting video using the raspberry pi.



