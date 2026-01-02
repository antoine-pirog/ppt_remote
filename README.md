# ppt_remote

Webapp to turn your phone into a simple -and somewhat secure against interference - remote control for PowerPoint presentations.

It was originally written to use my smartphone as a remote control via the local network for the lessons I was taching with a PowerPoint presentation. To prevent snooping from my students and any voluntary interference with my lesson, I randomized everything I could on the app : port, page name, and callbacks.

## First steps

Launch the app with main.py, and scan the qr code in the console to access the webapp. Make sure to have both devices on the same network. 

## Under the hood

Sends keyboard input to your computer running PowerPoint from a webapp on your smartphone. 
Python/Flask backend.


