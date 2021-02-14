import dash_bootstrap_components as dbc
import dash_html_components as html
from helper_funcs import ani_us_map


title = 'COVID-19 in the US'
layout = html.Div(children=[
	html.H1('COVID-19 dash app'),
	html.Br(),
	dbc.Col(dcc.Graph(id="animation_us_map", figure=ani_us_map)
	)])