import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
from graphFuncs import *
from helper_funcs import *

# external CSS stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

title = 'COVID-19 app'
layout = html.Div(children=[
	dbc.Row([dbc.Col(html.H1('COVID-19 tracker'),width={'size':'auto', 'offset':5})]),
	html.Br(),
	dbc.Col(dcc.Graph(id="animation_world_map", figure=ani_map)
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
		dbc.Col(html.Br())]),
	dbc.Row([
		dbc.Col(html.H5('Select entire regions'), width={'size':'auto', 'offset':5}),
		dbc.Col(
			dcc.Dropdown(
				id='region_select',
    			options=[
				{'label': i, 'value': i} for i in sorted(regions.keys())
				],
    			value='',
    			multi=False
			),
			width={'size':6, 'offset':3}
		),
		dbc.Col(html.H5('Select options:'), width={'size':'auto', 'offset':3}),
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
			width={'size':'auto', 'offset':0})
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