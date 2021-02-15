import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

options = [
    {"value": "flour1", "label": "Flour 1"},
    {"value": "flour2", "label": "Flour 2"},
    {"value": "flour3", "label": "Flour 3"},
    {"value": "flour4", "label": "Flour 4"},
    {"value": "water", "label": "Water"},
    {"value": "starter", "label": "Starter"},
    {"value": "salt", "label": "Salt"},
    {"value": "butter", "label": "Butter"},
    {"value": "egg", "label": "Egg"},
    {"value": "milk", "label": "Milk"},
    {"value": "dry", "label": "Dry (Other)"},
    {"value": "wet", "label": "Wet (Other)"},
]

inputs = html.Div(
    [
        html.H5("Inputs"),
        dbc.Form(
            dbc.FormGroup(
                [
                    dbc.Label("Measure by"),
                    dbc.RadioItems(
                        id="radio-units",
                        className="mb-2",
                        options=[
                            {"value": "weight", "label": "weight"},
                            {"value": "percentage", "label": "percentage"},
                        ],
                        value="weight",
                        inline=True,
                    ),
                ]
            )
        ),
        html.Div(
            id="div-weight",
            className="d-none",
            children=[
                dbc.InputGroup(
                    className="mb-2",
                    children=[
                        dbc.InputGroupAddon("Number of items", addon_type="prepend"),
                        dbc.Input(id="input-itemno", type="number"),
                    ],
                ),
                dbc.InputGroup(
                    className="mb-2",
                    children=[
                        dbc.InputGroupAddon("Weight per item", addon_type="prepend"),
                        dbc.Input(id="input-itemweight", type="number"),
                        dbc.InputGroupAddon("g", addon_type="append"),
                    ],
                ),
            ],
        ),
        dcc.Dropdown(
            id="dropdown-ingredients",
            className="mb-2",
            options=options,
            placeholder="Select ingredients...",
            multi=True,
        ),
        html.Div(id="div-ingredients", children=[]),
    ]
)

outputs = html.Div(
    [
        html.H5("Outputs"),
        dbc.Row(
            [
                dbc.Col(html.Pre(id="cardbody-convertedweights")),
                dbc.Col(html.Pre(id="cardbody-calculatedhydration")),
            ]
        ),
    ]
)
