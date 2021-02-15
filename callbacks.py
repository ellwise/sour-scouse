from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd

from app import app
from components import make_single_input


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
            child = make_single_input(value, label)
            children.append(child)

    return children


@app.callback(Output("div-weight", "className"), Input("radio-units", "value"))
def hide_weights(value):
    if not value:
        raise PreventUpdate
    return "d-none" if value == "weight" else "percentage"


@app.callback(
    [
        Output({"type": "input-eggsize", "index": "egg"}, "className"),
        Output({"type": "input-eggsize", "index": "egg"}, "style"),
    ],
    Input("radio-units", "value"),
    State({"type": "input-eggsize", "index": "egg"}, "style"),
)
def hide_style_eggsize(units, style):
    class_name = "d-none" if units == "percentage" else "d-block"
    style["flexGrow"] = 1 if units == "weight" else 0
    return class_name, style


@app.callback(
    Output({"type": "inputgroupaddon-units", "index": ALL}, "children"),
    Input("radio-units", "value"),
    State("dropdown-ingredients", "value"),
)
def set_units(radio_value, dropdown_values):
    if not radio_value:
        raise PreventUpdate
    units = [
        "eggs"
        if radio_value == "weight" and v == "egg"
        else "g"
        if radio_value == "weight"
        else "%"
        for v in dropdown_values
    ]
    return units


@app.callback(
    Output({"type": "input", "index": ALL}, "invalid"),
    [Input({"type": "input", "index": ALL}, "value"), Input("radio-units", "value")],
    State("dropdown-ingredients", "value"),
)
def validate_flour_percentages(values, units, ids):
    if units == "weight":
        return [None for v in values]
    elif units == "percentage":
        flour_ids = ["flour1", "flour2", "flour3", "flour4"]
        total = sum(x for x, id in zip(values, ids) if x and id in flour_ids)
        invalid = abs(100 - total) > 0.01
        return [invalid if id in flour_ids else None for id in ids]


@app.callback(
    Output("pre-convertedweights", "children"),
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
        width = df.loc[mask, "percentages"].apply(lambda x: len(str(int(x)))).max()
        txt += "\n".join(
            "{num:{width}.0f}% {name}".format(
                num=row["percentages"], width=width, name=row["names"]
            )
            for _, row in df[mask].iterrows()
        )

    # calculate grams given percentages
    elif units == "percentage":
        mask = df["weights"].notna()
        width = df.loc[mask, "weights"].apply(lambda x: len(str(int(x)))).max()
        txt += "\n".join(
            "{num:{width}.0f}g {name}".format(
                num=row["weights"], width=width, name=row["names"]
            )
            for _, row in df[mask].iterrows()
        )

    return txt


@app.callback(
    Output("pre-calculatedhydration", "children"),
    Input("store", "data"),
)
def calculate_hydration(data):

    txt = "Hydration\n"
    if not data:
        return txt

    df = pd.DataFrame.from_dict(data)
    mask = df[["hydration_percentages", "hydration_weights"]].notna().all(axis=1)
    width = (
        df.loc[mask, "hydration_percentages"].apply(lambda x: len(str(int(x)))).max()
    )
    txt += "\n".join(
        "{num1:{width}.0f}% ({num2:.0f}g) {name}".format(
            num1=row["hydration_percentages"],
            width=width,
            num2=row["hydration_weights"],
            name=row["names"],
        )
        for _, row in df[mask].iterrows()
    )

    return txt


@app.callback(
    Output("store", "data"),
    [
        Input({"type": "input", "index": ALL}, "value"),
        Input({"type": "input-eggsize", "index": ALL}, "value"),
        Input("radio-units", "value"),
        Input("input-itemno", "value"),
        Input("input-itemweight", "value"),
    ],
    [
        State({"type": "input", "index": ALL}, "id"),
        State({"type": "input-name", "index": ALL}, "children"),
    ],
)
def update_store(values, egg_sizes, units, item_no, item_weight, ids, names):

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
        if egg_sizes:
            egg_mask = df["indices"] == "egg"
            df["egg_sizes"] = None
            df.loc[egg_mask, "egg_sizes"] = egg_sizes
            egg_weights = {
                "small": 40,
                "medium": 50,
                "large": 60,
                "extra-large": 80,
            }
            df.loc[egg_mask, "weights"] = df[egg_mask].apply(
                lambda row: row["weights"] * egg_weights[row["egg_sizes"]]
                if row["egg_sizes"]
                else None,
                axis=1,
            )
        flour_mask = df["indices"].isin(["flour1", "flour2", "flour3", "flour4"])
        flour_weight = df.loc[flour_mask, "weights"].sum()
        df["percentages"] = df["weights"].apply(
            lambda v: 100 * v / flour_weight if v and flour_weight > 0 else None
        )
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
