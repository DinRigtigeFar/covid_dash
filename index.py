import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import dash_app, us_only


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row([
		dbc.Col(dcc.Link('World', href='/apps/dash_app')),
        dbc.Col(dcc.Link('US', href='/apps/us_only')),
    ])]),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/dash_app':
        return dash_app.layout
    if pathname == '/apps/us_only':
        return us_only.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)