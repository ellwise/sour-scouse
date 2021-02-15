import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from components import inputs, outputs

col_kwargs = {"xs": 12, "sm": 12, "md": 12, "lg": 6, "xl": 6}


def make_layout():
    return dbc.Container(
        children=[
            html.Header(
                dbc.Row(
                    className="mb-3",
                    children=dbc.Col(
                        html.H2(
                            "The Sour Scouse's Calculator",
                            style={"textAlign": "center"},
                        )
                    ),
                )
            ),
            dbc.Row([dbc.Col(inputs, **col_kwargs), dbc.Col(outputs, **col_kwargs)]),
            dcc.Store(id="store"),
        ]
    )
