# War Game

simple war simulation, it is divided in regions of the words:
- africa
- europe
- middle east
- asia
- oceania se asia
- north america
- south america
this regions fight with each other in the simulation. The world is represented
in a grid like the following:
```
[[1 1 1 1 1 1 1 1 1 1]
 [1 1 1 1 1 1 1 1 1 1]
 [1 1 2 2 2 2 2 2 2 2]
 [2 2 2 2 2 2 2 2 2 2]
 [2 2 3 3 3 4 4 4 4 4]
 [4 4 4 5 5 5 5 5 5 5]
 [5 5 5 5 5 5 5 5 6 6]
 [6 6 6 6 6 6 6 6 6 6]
 [6 6 6 6 6 6 6 7 7 7]
 [7 7 7 7 7 7 7 7 7 7]]
```
each number represent a region.

as the day pass in the sim, you can see how diff numbers grow while other
diminish, this is happening because there are war breaking out.

# set up
you'll need python3 installed in your systems, then you can easily do
```
pip install -r requirements.txt
```
then you'll be ready to go.

NOTE: since we use numpy and so on, I recommend using a virtual enviorment
for you to not have problems with your versions and all that.

# run the sim

okay, so the project is broken down in 3 sections: data, sim and visualisation.
Each section has its directory with all the necessary files to run the
simulation. The compilation of data, or to just see the output.

if you just want to run the simulation, you can go to the sim directory
and do:
```
python sim.py
```
by default, it will print the grid with the countries each day, it has a
sleep of 1 second for you to check the map every iteration.
