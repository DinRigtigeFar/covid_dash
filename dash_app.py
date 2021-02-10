from os import environ, path, listdir

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.io as pio
from dash.dependencies import Input, Output

from graphFuncs import *

# Nice theme is nice
pio.templates.default = "plotly"


# external CSS stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

deaths = pd.read_csv("../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
cases = pd.read_csv("../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
popsizes = pd.read_csv('../COVID-19/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv')

# If province_state has a value, make that value the country_region instead
popsizes.loc[popsizes['Province_State'].isnull()==False, ['Country_Region']] = popsizes['Province_State']


def make_clean_df(to_clean):
	"""
	Small function to clean cases and deaths dataframes
	"""

	# Make some updates to the dataframe to sum Australia, Canada and China provinces as one country
	bad1 = 'Australian Capital TerritoryNew South WalesNorthern TerritoryQueenslandSouth AustraliaTasmaniaVictoriaWestern Australia'
	bad1_lat = -26.4390917
	bad1_lon = 133.281323

	bad2 = 'AlbertaBritish ColumbiaDiamond PrincessGrand PrincessManitobaNew BrunswickNewfoundland and LabradorNorthwest TerritoriesNova ScotiaNunavutOntarioPrince Edward IslandQuebecRepatriated TravellersSaskatchewanYukon'
	bad2_lat = 56.0
	bad2_lon = -96.0

	bad3 = 'AnhuiBeijingChongqingFujianGansuGuangdongGuangxiGuizhouHainanHebeiHeilongjiangHenanHong KongHubeiHunanInner MongoliaJiangsuJiangxiJilinLiaoningMacauNingxiaQinghaiShaanxiShandongShanghaiShanxiSichuanTianjinTibetXinjiangYunnanZhejiang'
	bad3_lat = 35.8592948
	bad3_lon = 104.1361118
	# Append the countries to the dataframe
	to_clean = to_clean.append(to_clean[to_clean['Country/Region']=='Australia'].sum(), ignore_index=True)
	to_clean = to_clean.append(to_clean[to_clean['Country/Region']=='Canada'].sum(), ignore_index=True)
	to_clean = to_clean.append(to_clean[to_clean['Country/Region']=='China'].sum(), ignore_index=True)
	# Find all to_clean where province/state is not NaN and update the country with that name
	to_clean.loc[to_clean['Province/State'].isnull()==False, ['Country/Region']] = to_clean['Province/State']
	# Make the lat/long and Country name the correct one for the 3 bad countries
	to_clean.loc[to_clean['Country/Region']==bad1, ['Lat']] = bad1_lat
	to_clean.loc[to_clean['Country/Region']==bad1, ['Long']] = bad1_lon
	to_clean.loc[to_clean['Country/Region']==bad1, ['Country/Region']] = 'Australia'
	to_clean.loc[to_clean['Country/Region']==bad2, ['Lat']] = bad2_lat
	to_clean.loc[to_clean['Country/Region']==bad2, ['Long']] = bad2_lon
	to_clean.loc[to_clean['Country/Region']==bad2, ['Country/Region']] = 'Canada'
	to_clean.loc[to_clean['Country/Region']==bad3, ['Lat']] = bad3_lat
	to_clean.loc[to_clean['Country/Region']==bad3, ['Long']] = bad3_lon
	to_clean.loc[to_clean['Country/Region']==bad3, ['Country/Region']] = 'China'
	# Sort the dataframe so order is by country again
	to_clean = to_clean.sort_values(by=['Country/Region'])

	return to_clean
deaths = make_clean_df(deaths)
cases = make_clean_df(cases)

# Make the date "tidy" so it can be visualized in an animation map
melted_cases = cases.melt(id_vars=['Province/State','Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Cumulative_Cases')

# Downsample the data to update on a weekly basis instead of daily
melted_cases = melted_cases.set_index(['Date'])

melted_cases.index = pd.to_datetime(melted_cases.index)

downsample = melted_cases.groupby(['Country/Region']).resample('W', origin='start').mean()
melted_cases = downsample.reset_index()
melted_cases['Date'] = melted_cases['Date'].astype(str)

# Make a static animation map
ani_map = animation_map(melted_cases)

regions = {}
reg_dir = 'regions'
# Open file with countries in both cases and popsizes
for i in listdir(reg_dir):
	name = i.split('.')[0]
	with open(path.join(reg_dir,i), 'r') as f:
		regions[name] = tuple(j.strip() for j in f)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'COVID-19 app'
app.layout = html.Div(children=[
	html.H1('COVID-19 dash app'),
	html.Br(),
	dbc.Col(dcc.Graph(id="animation_map", figure=ani_map)
	),
	html.Br(),
	dbc.Row([
		dbc.Col(html.H5('Select individual countries'), width={'size':'auto', 'offset':5}),
		dbc.Col(
			dcc.Dropdown(
				id='country_select',
    			options=[
				{'label':cases[cases['Country/Region']==i].iloc[-1]['Country/Region'], 'value': i} for i in cases['Country/Region']
				],
    			value=['China', 'US', 'Belgium', 'Italy', 'Brazil', 'Sweden', 'Germany', 'Denmark', 'United Kingdom', 'Norway', 'Russia', 'Hungary', 'Israel'],
    			multi=True
			),
			width={'size':6, 'offset':3}
		),
		dbc.Col(html.Br()),
		dbc.Col(html.H5('Select entire regions'), width={'size':'auto', 'offset':5}),
		dbc.Col(
			dcc.Dropdown(
				id='region_select',
    			options=[
				{'label': i, 'value': i} for i in sorted	(regions.keys())
				],
    			value='',
    			multi=False
			),
			width={'size':6, 'offset':3}
		),
		dbc.Col(
			dcc.Checklist(
    			options=[
        		{'label': 'Scale', 'value': 'scale'},
        		{'label': 'Log transform Y', 'value': 'transform'},
    			],
    			value=['scale'],
				id='options',
    			labelStyle={'display': 'inline'},
				inputStyle={"margin": "0 5px 0 20px"}
			),
			width={'size':'auto', 'offset':3})
	]),
	html.Br(),
	html.Div(dbc.Row([
		dbc.Col(dcc.Graph(id="scatter-plot"),
		width={'size':'auto', 'offset':1}
		),
		dbc.Col(dcc.Graph(id="day_to_day"),
		width={'size':'auto', 'offset':1}
		),
		dbc.Col(dcc.Graph(id="death-plot"),
		width={'size':'auto', 'offset':1}
			),
		dbc.Col(dcc.Graph(id="day_to_day-death"),
		width={'size':'auto', 'offset':1}
		)])),
	html.Br(),
	dbc.Row(
		dbc.Col(dcc.Graph(id="pie_chart_part"))
	),
	dbc.Col(dcc.Graph(id="map_chart")
	),
	])

@app.callback(
	Output('scatter-plot', 'figure'),
	Output('day_to_day', 'figure'),
	Output('death-plot', 'figure'),
	Output('day_to_day-death', 'figure'),
	Output('pie_chart_part', 'figure'),
	Output('map_chart', 'figure'),
	[Input('options', 'value'), Input('country_select','value'), Input('region_select','value')])
def update_bar_chart(options, dropdown_country, dropdown_region):
	countries = {i:popsizes[popsizes['Country_Region']==i]['Population'].iloc[0] for i in dropdown_country}
	if dropdown_region:
		countries = {i:popsizes[popsizes['Country_Region']==i]['Population'].iloc[0] for i in regions[dropdown_region]}
	if 'scale' in options:
		case_scat, dTd_scat = base_graph(cases, countries, 100000)
		death_scat, dTd_death_scat = base_graph(deaths, countries, 100000, death=True)
		case_pie = pie_part_chart(cases, countries, 100000)
		case_map = map_graph(cases, countries, 100000)
	else:
		case_scat, dTd_scat = base_graph(cases, countries, 1)
		death_scat, dTd_death_scat = base_graph(deaths, countries, death=True)
		case_pie = pie_part_chart(cases, countries, 1)
		case_map = map_graph(cases, countries, 1)
	if 'transform' in options:
		case_scat.update_yaxes(type='log')
		dTd_scat.update_yaxes(type='log')
		death_scat.update_yaxes(type='log')
		dTd_death_scat.update_yaxes(type='log')
	return case_scat, dTd_scat, death_scat, dTd_death_scat, case_pie, case_map


if __name__ == '__main__':
    app.run_server(debug=True)

