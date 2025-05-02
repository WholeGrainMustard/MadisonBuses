This folder contains the suite of python scripts and requisite folder structure used to collect the bus data. To set up the process yourself, you will need to change the config.txt file to contain your API key from the City of Madison and the proper home folder location for the entire suite. You would then need to run the processController.py file and the combineContoller.py file to begin collecting and collating data. The use of each file is explained below:

The combineContoller.py file will run continuously once initiated. This script looks for saved JSON responses from the processController.py script and combines them into a csv file for each bus destination each day. It will check every 20 minutes for new JSON files, and sleep for longer periods after no files are found.

The combineFiles.py script holds the functions used by the combineController.py file. These functions do the actual file manipulation. 

The config.py file holds code for a config object that is used to read in the config file within the controller scripts.

The config.txt file holds the actual configuration information for the processes preformed by the other scripts. 

The downtimeCheck.py file contains a function to check if there is bus data coming in or not and to sleep the processes collecting data if no data is coming in, i.e. at night.

The getData.py file contains functions to make the API requests to Madison Metro and to write the response to a JSON file.

The grabWeather.py file contains methods to scrap the weather.gov website for the Madison area and retrieve the time of the request, the temperature, the relative humidity, the weather field, and the windchill and save the data to a csv.

The metroClasses.py file contains code of classes and methods to contain the data collected from the Madison Metro API.

The processController.py file will run continuously until interrupted, once initiated. This file attempts to collect bus data every 10 seconds and weather data every 50 seconds, while data is coming in. 