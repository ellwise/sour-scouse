from dash import Dash
import dash_bootstrap_components as dbc

# A value for `requests_pathname_prefix` is not needed locally nor when a
# custom domain name is configured through API Gateway. However, it is
# required if to run the app directly via the default AWS domain name given to
# the REST API on deployment. If not used there, then the app will display a
# "Layout not found" error.
# requests_pathname_prefix = "/sour-scouse/"

app = Dash(
    __name__,
    title="Sour Scouse",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],  # to improve mobile views
    external_stylesheets=[dbc.themes.FLATLY],
)
