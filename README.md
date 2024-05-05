· A project title: Magic Pong

· Nevan Mukherjee, Ian Garrison

· A description of the desired functionality for the project/project (goals):
We are making the basic pong game using pygame, and then adding some cool features. We are using computer vision to 
use our hands to control the paddles, as opposed to a throttle or button. Furthermore, we are planning
to use our simulation knowledge to add other features like different difficulty, and power ups. We may also
incorporate the M5 as a remote controller in some way. 


A description of what was actually completed in the project:
We successfully made classic pong, with using our hands to move the paddles. The simulation
has all the bells and whistles of the original pong: effective ball movement physics, smooth
vertical paddle movement, a running scoreboard, a user-friendly game window, and
an end game screen. We also implemented power ups, specifically one that speeds up the ball
and one that makes the user's paddle bigger. We use MQTT wireless communication to use our
M5 sticks as controllers, so when a player has a power up, they can click the M5's button
to activate it. For the computer vision, the computer tracks the players' hands as they
move them up and down to control the vertical paddle movement. Furthermore, when one of the 
player wins (first to 3 points) and the game is over, one of the players can make a fist
which will reset the game. This lab effectively utilizes communication, simulation,
computer vision, and human-computer interfaces to create a fun and innovative version of the
classic game of pong.

A video demonstrating how the project works: 
Note: In the video, it may seem that my M5 is connected to Ian's laptop. It is simply
charging, it's not communicating through serial. Like Ian's M5, mine is communicating with
the game using the wireless MQTT protocol.

A description of the work completed by each group member. Only a very small portion of this can be “co-design”.
Whoever’s keys were on the keyboard for the work that gets done gets to take the credit:

I (Nevan) did most of the simulation work. Setting up pygame, building the ball, score, and
paddle classes was the start. Then testing these objects and making sure they worked as I 
wanted them to. I set up the game window dimensions, colors, constants, and basic stuff
along those lines. I built the logic behind the ball physics, making the balls bounce off
the top and bottom boundaries as well as the paddles, but increase score when colliding
with the left and right boundaries. We had some trouble getting the score to work, and
I spent a good bit of time troubleshooting that. I also spent a good chunk of time 
testing our code.

Ian did the opencv/mediapipe/computer vision part and the MQTT part. 

We both came together a few times to test the code, brainstorm solutions to issues we faced,
and make the submission video.

