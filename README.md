# COVID-19 Dash app
## Explore the current pandemic through data.
### Now a very small snippet is available on [Heroku](https://covid-19-dashapp.herokuapp.com/apps/dash_app)!

### Worldwide development of COVID-19
The app contains the ability to lookup individual countries, multiple countries of your liking or entire continents at a time. The countries chosen will be presented in various graphs including a pie chart, scatter plots and a map. You also have the ability to scale the output to cases/deaths per 100K capita.<br>
Below is a gif of the animated world map.
![Showcase animated map](demo/demo.gif)

In the latest commit I made the app multipage with an US only map option.

## Prerequisites
* A mapbox token saved as an enviroment variable so it will heed the call of: `environ['MAPBOX_KEY']`.
* The token can be aquired from [mapbox](https://www.mapbox.com) after signing up (free).

## Installation
### Download app:
````
git clone https://github.com/DinRigtigeFar/covid_dash.git
````
### Create the necessary environment and activate it:
````
cd covid_dash
conda env create -f environment.yml
conda activate Dash
````
### Run the app
````
python index.py
````
Now that the app is running all you need is to open it in your [browser](http://127.0.0.1:8050/) (it may take a few seconds to spin up)!