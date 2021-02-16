import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from helper_funcs import ani_us_map


title = 'COVID-19 in the US'
layout = html.Div(children=[
	dbc.Row([dbc.Col(html.H1('COVID-19 in the US'),width={'size':'auto', 'offset':5})]),
	html.Br(),
	dbc.Col(dcc.Graph(id="animation_us_map", figure=ani_us_map)
	)])