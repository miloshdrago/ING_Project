# Possible Adjustments:
* [ ] Now we download all files, can we narrow that down to the selected simulation based on the name?  
* [ ] Introduce different types of errors
    1. [ ] Error where connection between servers is severed  
    2. [ ] Infinite loop  
    3. [ ] Connection break  
    4. [x] A faulty patch, anomaly processed within 10 seconds at the place of 1 seconds after update.  
* [x] Finalise plotly drop down selection  
* [ ] Add latency and kind servers to logs
    * [X] Add latency to visualisation
    * [X] Color network graph based on server kind
    * [X] Add filtering on server kind to plotly
    * [X] Take mean for all servers of a specific kind
    * [X] Use INFO to filter graphs
    * [X] Plot occurences of errors in plotly graph
* [ ] Add crash and restart when memory overload  
* [x] Add timeout error (with appropriate logger level)
    * [x] Move message code out of Subprocess (see test_simulation/simulation_seasonality_error.py for inspiration)
* [ ] Add error introduction (with seperate logger (see Manual_Error_Log.csv))  
* [x] Different routes for request type  
    * [x] Backend
    * [ ] Frontend
* [ ] Visual interface (see java modelling tool and Areana? for inspiration)
* [x] Release server requests appropriately
* [x] add description to filename
* [x] Reformat Subprocess to property include timeout

# Implementation:
* [ ] Create API documentation (low priority, can be done after report is written)  
* [ ] Test diffent scenarios for possible results in powerpoint/poster

# Bugs:
* [x] Simulation only prints out 21 lines of log (both from frontend and command line)  
* [x] Frontend fails if most recent file is not in correct format (fixed by filtering logs by filenames)
## relative paths
* OutlierDetection.py:  
    * [x] 15: OUT_DIR  
* Logger.py:  
    * [x] defaults: directory="logs"
* LogProcessing.py:  
    * [x] LOG_PATH = 'logs'  
    * [x] logs/Manual_Log_Filtered.csv  
* Processor.py
    * [x] Fix no load when returning to same server


# Defined variables/distributions/proposed changes:  
## lib folder  
* Envoirment.py: None  
* Logger.py:  
    * [x] defaults: directory="logs", level = 20 (20 is level INFO)  
* LogProcessing.py:
    * [x] LOG_PATH (change to relative to file)
    * [x] 172: add "latency" to metrics
    * [ ] 173: num_std_dev = 3
* Middleware.py: None  
* MultiServers.py: None
    * [X] 17: moving_average:  
     35: detect_outliers: n=3, default: 3 (maybe a bit small for this large amount of records)  -> Changed to n=10
    * [X] 68: outlier_writer: delimiter=',' (rest of csv have ";" delimiter)  
* Process.py:  
## main app2 folder  
* routes.py  
    * [ ] Abstract simulation to separate module  
    * [X] 181: wrong format log_filenames  
    * [X] 187: fixed filename seasonality, change to default  
    * [x] 187: make max_volume flexible  
    * [x] 224: Replace complicated most recent file search to more default functions  
    * [x] 272: Replace complicated most recent file search to more default functions  
    * [ ] 306: Only save files of selected simulation  
    * [ ] 315: name logs based on simulation run number  

## sample code:  
### first most recent file matchting a certain condition:  
```
import glob, os
list_of_files = glob.glob('log_*.csv')
latest_file = max(list_of_files, key=os.path.getctime))
```

### Set relative paths to script location  
```
file_dir = os.path.dirname(__file__)  
location_logs = os.path.join(file_dir, "Logs")  
```
