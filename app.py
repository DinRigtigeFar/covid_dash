import dash
import dash_bootstrap_components as dbc

# external CSS stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=False, external_stylesheets=external_stylesheets)
app.title = 'COVID-19 Dash'
server = app.server
