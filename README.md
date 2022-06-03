# War Game

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
