from .dash_chalice import DashChalice
import dash_bootstrap_components as dbc


app = DashChalice(
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
