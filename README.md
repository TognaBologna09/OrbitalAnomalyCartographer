# OrbitalAnomalyCartographer
This is a program written for an assignment in an Orbital Dynamics course.
For extra credit, we were challenged to turn the orbits from 2d to 3d. This part of the project was not completed before the due date, but I added it to this repository anyway to show how close I got.  

# Background
The goal of this script is to translate between three angles used to represent the position of an object throughout its orbit: the true anomaly, the eccentric anomaly, and the mean anomaly. The true anomaly is a measure of the actual position, while the mean anomaly is a measure of the 'time' in an orbit (when m = pi/2, you are 1/4 of the way through the orbit). The eccentric anomaly is an angle used to relate the other angles. While this script translates between the anomalies, it also plots the output using the "AnomalyCartographer" function. Other functions specific to assignment credit have been commented out. 

### How to Run
This script was written to be used in the Spyder IDE and offers prompts to the user in the console. The user is meant to follow the prompts in the console and input the values directly, and once the program concludes the graph(s) will appear.

### Example Output
![Alt text](https://github.com/TognaBologna09/OrbitalAnomalyCartographer/blob/main/OrbitalAngleConsoleExample.png)
![Alt text](https://github.com/TognaBologna09/OrbitalAnomalyCartographer/blob/main/AnomalyCartographerExample.png)
