import dash
import dash_bootstrap_components as dbc

# some kwargs are needed for it to work with zappa - otherwise get js loading errors, DashRenderer not found, etc...
zappa_kwargs = {
    "compress": False,
    #'requests_pathname_prefix': '/production/', # this is needed if deployed without a domain mapping
    "serve_locally": False,
}

app = dash.Dash(
    __name__,
    title="Sour Scouse",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],  # to improve mobile views
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    **zappa_kwargs,
)
