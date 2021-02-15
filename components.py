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
                dbc.Col(html.Pre(id="pre-convertedweights")),
                dbc.Col(html.Pre(id="pre-calculatedhydration")),
            ]
        ),
    ]
)

def make_single_input(value, label):
    name = dbc.InputGroupAddon(
        children=label,
        addon_type="prepend",
        id={"type": "input-name", "index": value},
    )
    input = dbc.Input(
        type="number",
        id={"type": "input", "index": value},
    )
    units = dbc.InputGroupAddon(
        id={"type": "inputgroupaddon-units", "index": value},
        addon_type="append",
    )
    if value == "egg":
        input_size = dcc.Dropdown(
            id={"type": "input-eggsize", "index": value},
            style={
                "borderRadius": 0,
                "marginBottom": -1,
                "marginLeft": -1,
                "marginRight": -1,
            },
            options=[
                {"value": "small", "label": "small"},
                {"value": "medium", "label": "medium"},
                {"value": "large", "label": "large"},
                {"value": "extra-large", "label": "extra-large"},
            ],
            placeholder="Select size...",
        )
        input_group = [name, input, input_size, units]
    else:
        input_group = [name, input, units]
    return dbc.InputGroup(
        id={"type": "inputgroup-ingredients", "index": value},
        children=input_group,
        className="mb-2",
    )