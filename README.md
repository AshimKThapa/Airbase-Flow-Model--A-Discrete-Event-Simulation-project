Term Simulation Project for OR635 - Discrete Event Simulation

The first thing to do before running the code is making sure all the dependencies are installed. We do this by running:
pip install -r requirements.txt

Next, double check all files are stored in the same directory. These files include:
1. doe.py: script to run the entire doe setup
2. main.py: script to run a single case. If you wish to change the parameters, you can change them in the airbase instantiation in this file.
3. env_vars.py: holds all variables the model will run. This is where you can change things like number of reps run, time of simulation, and various average times to run processes. 
4. airbase.py: The meat of the code is in this file. It is an airbase class which holds everything the airbase needs to function. For instance, we define the mission requests, runway requests, refuel requests and maintenance requests.
5. resources.py: This file contains classes with the different resource objects. Things like missions, planes, runways and the priority logic for each of these objects.

Once everything is set up, all you need to do is run the main.py script or the doe.py script. This can be done using an IDE, or directly from the terminal. For example, we can run the script from the Anaconda terminal by navigating to the directory with the code and then run following command:
python main.py        OR        python doe.py
If running the main.py script, the simulation will print out key metrics for each rep including refueling crew utilization, maintenance crew utilization, average time waiting for refueling station, runways utilization, average runway delay, and average deterrence mission delay time. 
If running the doe.py script, the terminal will print out the status of the runs by case. There are 434 cases and it takes approximately 2 hours for the entire DOE to run (depending on your computer). 
There is one more set of files pertaining to the output analysis of the data. We saved the doe run as a csv file and did some statistical analysis on that. The csv file along with a jupyter notebook live in the output_analysis folder. 
If there are any questions about the code, please contact us at:
hghayoom@gmu.edu, athapa26@gmu.edu, ghulsey@gmu.edu, or kvierra@gmu.edu
