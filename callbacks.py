from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd

from app import app


@app.callback(
    Output("div-ingredients", "children"),
    Input("dropdown-ingredients", "value"),
    [State("dropdown-ingredients", "options"), State("div-ingredients", "children")],
)
def add_ingredient(values, options, children):

    if values is None:
        raise PreventUpdate

    # drop removed children
    if len(children) > 0:
        children = [
            child for child in children if child["props"]["id"]["index"] in values
        ]

    # add new children
    labels = {x["value"]: x["label"] for x in options}
    ids = [child["props"]["id"]["index"] for child in children]
    for value in values:
        if value not in ids:
            label = labels[value]
            name = dbc.InputGroupAddon(
                children=label,
                addon_type="prepend",
                id={"type": "input-name", "index": value},
            )
            if value == "egg":
                input_count = dbc.Input(
                    type="number",
                    id="input-eggcount",
                )
                input_size = dcc.Dropdown(
                    id="input-eggsize",
                    style={
                        "flexGrow": 1,
                        "borderTopLeftRadius": 0,
                        "borderBottomLeftRadius": 0,
                        "borderTopRightRadius": 0,
                        "borderBottomRightRadius": 0,
                    },
                    options=[
                        {"value": "small", "label": "Small"},
                        {"value": "medium", "label": "Medium"},
                        {"value": "large", "label": "Large"},
                        {"value": "extra-large", "label": "Extra-large"},
                    ],
                    placeholder="Select size...",
                )
                units = dbc.InputGroupAddon(
                    children="eggs",
                    addon_type="append",
                )
                hidden_input = dbc.Input(
                    className="d-none",
                    id={"type": "input", "index": value},
                )
                hidden_units = html.Div(
                    className="d-none",
                    id={"type": "inputgroupaddon-units", "index": value},
                )
                child = dbc.InputGroup(
                    id={"type": "inputgroup-ingredients", "index": value},
                    children=[
                        name,
                        hidden_input,
                        input_count,
                        input_size,
                        hidden_units,
                        units,
                    ],
                    className="mb-2",
                )
            else:
                input = dbc.Input(
                    type="number",
                    id={"type": "input", "index": value},
                )
                units = dbc.InputGroupAddon(
                    id={"type": "inputgroupaddon-units", "index": value},
                    addon_type="append",
                )
                child = dbc.InputGroup(
                    id={"type": "inputgroup-ingredients", "index": value},
                    children=[name, input, units],
                    className="mb-2",
                )
            children.append(child)

    return children


@app.callback(Output("div-weight", "className"), Input("radio-units", "value"))
def hide_weights(value):
    if not value:
        raise PreventUpdate
    return "d-none" if value == "weight" else "percentage"


@app.callback(
    Output({"type": "inputgroupaddon-units", "index": ALL}, "children"),
    Input("radio-units", "value"),
    State("dropdown-ingredients", "value"),
)
def set_units(radio_value, dropdown_values):
    if not radio_value:
        raise PreventUpdate
    n = len(dropdown_values)
    units = "g" if radio_value == "weight" else "%"
    return [units] * n


@app.callback(
    Output({"type": "input", "index": "egg"}, "value"),
    [Input("input-eggcount", "value"), Input("input-eggsize", "value")],
)
def set_count_inputs(number, size):
    if not number or not size:
        raise PreventUpdate
    egg_weights = {
        "small": 40,
        "medium": 50,
        "large": 60,
        "extra-large": 80,
    }
    return number * egg_weights[size]


@app.callback(
    Output("cardbody-convertedweights", "children"),
    [Input("store", "data"), Input("radio-units", "value")],
)
def convert_weights(data, units):

    txt = "Converted weights\n"
    if not data:
        return txt

    df = pd.DataFrame.from_dict(data)

    # calculate percentages given grams
    if units == "weight":
        mask = df["percentages"].notna()
        txt += "\n".join(
            f"{row['percentages']:3.0f}% is {row['names']}"
            for _, row in df[mask].iterrows()
        )

    # calculate grams given percentages
    elif units == "percentage":
        mask = df["weights"].notna()
        txt += "\n".join(
            f"{row['weights']:.0f}g is {row['names']}" for _, row in df[mask].iterrows()
        )

    return txt


@app.callback(
    Output("cardbody-calculatedhydration", "children"),
    Input("store", "data"),
)
def calculate_hydration(data):

    txt = "Hydration\n"
    if not data:
        return txt

    df = pd.DataFrame.from_dict(data)
    mask = df[["hydration_percentages", "hydration_weights"]].notna().all(axis=1)
    txt += "\n".join(
        f"{row['hydration_percentages']:3.0f}% ({row['hydration_weights']:.0f}g) from {row['names']}"
        for _, row in df[mask].iterrows()
    )

    return txt


@app.callback(
    Output("store", "data"),
    [
        Input({"type": "input", "index": ALL}, "value"),
        Input("radio-units", "value"),
        Input("input-itemno", "value"),
        Input("input-itemweight", "value"),
    ],
    [
        State({"type": "input", "index": ALL}, "id"),
        State({"type": "input-name", "index": ALL}, "children"),
    ],
)
def update_store(values, units, item_no, item_weight, ids, names):

    # add ingredients
    indices = [id["index"] for id in ids]
    df = pd.DataFrame(
        {
            "indices": indices,
            "names": names,
        }
    )

    # add weights
    if units == "weight":
        df["weights"] = values
        flour_mask = df["indices"].isin(["flour1", "flour2", "flour3", "flour4"])
        flour_weight = df.loc[flour_mask, "weights"].sum()
        df["percentages"] = [100 * v / flour_weight if v else None for v in values]
    elif units == "percentage":
        df["percentages"] = values
        if not item_no or not item_weight:
            df["weights"] = None
        else:
            dough_weight = item_no * item_weight
            df["weights"] = df["percentages"] / df["percentages"].sum() * dough_weight

    # calculate hydration
    df["hydration_indices"] = df["indices"].map(
        {
            "butter": 15,
            "egg": 70,
            "milk": 88,
            "wet": 10,
            "water": 100,
        }
    )
    flour_mask = df["indices"].isin(["flour1", "flour2", "flour3", "flour4"])
    flour_weight = df.loc[flour_mask, "weights"].sum()
    if flour_weight > 0:
        df["hydration_percentages"] = (
            df["weights"] * df["hydration_indices"] / flour_weight
        )
    else:
        df["hydration_percentages"] = None
    df["hydration_weights"] = df["weights"] * df["hydration_indices"] / 100

    return df.to_dict("records")
