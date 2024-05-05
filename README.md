# ELEC3907A3-F-Ball-Balancing-Platform
Code for the Carleton University Department of Electronics 3rd year project of group 3-F, the Ball Balancing Platform

Team Members:
Noah Connell, Tristan Laliberte, Ciaran McDonald-Jensen, Ayooluwa Owolabi, Ibrahim Shah

Date: Winter Semester 2024, (January-April 2024)

Project Description:
This project involved making a ball balancing platform, a platform that can change it's angle to balance a ball on top of it. The original intention was to use a camera to provide position feedback to control the servos, automatically balancing the ball, there was a scope switch to instead turn it into a game, controlling the angle of the platform using a joystick. With another couple weeks the camera would be working and the table self-balancing.

What is in this repository:
Ball Balancer folder - Camera Calibration code and files
PlatformMotionSimulation - MATLAB code that simulates our platform
*Demo.py files - files intended to run on the raspberry pi, they use the other python files


Main files that are intended to be run:
- platformDemo.py - shows off pretty platform movement, does not require camera or joystick
- joystickDemo.py - controls platform using joystick, pushing button moves platform to higher level, releasing lowers again, joystick can be used to balance ball, does not require camera
- cameraControlLoopDemo.py - balances ball in center of platform (not functioning at current time as camera did not work), does not require joystick