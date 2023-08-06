#!/usr/bin/env python3
"""Pass information container."""
import json
from dataclasses import dataclass
from difflib import get_close_matches
from typing import get_args
from typing import get_origin
from typing import Optional
from typing import Union

import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from numpy.typing import NDArray
from plotly import graph_objects as go
from tinydb import Query
from tinydb import TinyDB

from .quaeldich import DB_LOC
from .quaeldich import PASS_DB
from .quaeldich import PASS_NAME_DB
from .tools import decompose_digit

PASS_DB_LOC = DB_LOC + PASS_DB
PASS_NAME_DB_LOC = DB_LOC + PASS_NAME_DB

GRAD_TO_COLOR = np.asarray(
    [
        "#a43074",
        "#80225c",
        "#5f1547",
        "#4e1d52",
        "#2e2048",
        "#102747",
        "#1d406b",
        "#11507c",
        "#34759d",
        "#7db5d5",
        "#aadff7",
        "#79d0f2",
        "#55c0da",
        "#1ab2cc",
        "#14b1b3",
        "#1bb195",
        "#24b065",
        "#20ae50",
        "#49b54e",
        "#78bf4b",
        "#ACE186",
        "#ACE186",
        "#ACE186",
        "#C7E383",
        "#E2F080",
        "#FDFE7B",
        "#FFEA75",
        "#FFD671",
        "#FFBE6D",
        "#FFA668",
        "#FF8B64",
        "#FF7260",
        "#F75B5B",
        "#DB5757",
        "#BA5353",
        "#9A4F4F",
        "#8E4D4D",
        "#824B4B",
        "#774A4A",
        "#6A4848",
        "#5E4747",
    ]
)

GRAD_MAX: float = 30.0
GRAD_MIN: float = -30.0


@dataclass
class Pass:

    name: str
    """Name of pass."""
    coord: list[float]
    """coordinate of pass."""
    alt: str
    """Alternative name if exists"""
    country: str
    """Pass country"""
    region: str
    """Pass region."""
    height: int
    """Height of the pass in meter."""
    total_distance: list[float]
    """Total distance of each paths."""
    total_elevation: list[int]
    """Total elevation of each paths."""
    avg_grad: list[float]
    """Average gradient of each paths."""
    max_distance: float
    """Max distance among the paths"""
    min_distance: float
    """Min distance among the paths"""
    max_elevation: int
    """Max elevation among the paths"""
    min_elevation: int
    """Min elevation among the paths"""
    url: str
    """URL of the pass"""
    gpts: dict
    """Geographical coordinate information. Latitude, Longitude, Elevation, Distance."""

    def __call__(self):
        if len(self.gpts) > 0:

            self.geo_log = get_gpt_data(self.gpts)

            # Process gradients
            self.grad_process()
        return self

    @property
    def is_valid(self) -> bool:
        """Check whether Pass information contains valid path data."""

        return self.max_distance > 0

    @property
    def map_bound(self) -> list[float]:

        sf = np.asarray(self.starts_from, dtype=np.float64)
        pass_coord = np.asarray(self.coord, dtype=np.float64)

        if len(sf) == 1:
            coord_delta = pass_coord - sf[0]
            return [
                (pass_coord - coord_delta).tolist(),
                (pass_coord + coord_delta).tolist(),
            ]
        else:
            coord_delta_dist = np.sqrt(((pass_coord - sf) ** 2).sum(axis=1))
            path_idx = np.argmax(coord_delta_dist)
            coord_delta = pass_coord - sf[path_idx]

            return [
                (pass_coord - coord_delta).tolist(),
                (pass_coord + coord_delta).tolist(),
            ]

    @property
    def num_pathes(self) -> int:
        """Number pathes to the top."""
        return len(self.total_distance)

    @property
    def starts_from(self) -> list[list[float]]:

        return [geo[0, :2].tolist() for geo in self.geo_log if geo is not None]

    @property
    def path_names(self) -> list[str]:

        return [self.gpts[pid]["name"] for pid in self.gpts]

    @property
    def grad_max(self) -> list[float]:
        """Maximum gradient measured."""
        return self._grad_max

    @property
    def grad_min(self) -> list[float]:
        """Minimum gradient measured."""
        return self._grad_min

    @property
    def flat(self) -> list[float]:
        """Measured flat section in km. If the gradient is +- 2%, it is regarded as the flat section."""
        return self._flat

    @property
    def descend(self) -> list[float]:
        """Measured descending section in km."""
        return self._descend

    @property
    def grad(self) -> list[NDArray[np.float64]]:
        """Computed gradient. Interpolated every 100 meter from 50 meter."""
        return self._grad

    @property
    def grad_bin(self) -> list[NDArray[np.float64]]:
        """Coordinate for the gradients."""
        return self._grad_bin

    @property
    def grad_color(self) -> list[NDArray[np.unicode_]]:
        """Converted gradient to color code."""
        return self._grad_color

    @property
    def distance(self) -> list[NDArray[np.float64]]:
        """Distance to the top of the Pass in km."""

        return self._distance

    @property
    def elev(self) -> list[NDArray[np.float64]]:
        """Elevlation interpolated to grad_bin."""
        return self._elev_interp

    @property
    def elev_lower(self) -> list[float]:
        """Lower limit of the elevation."""
        return self._elev_lower

    @property
    def elev_upper(self) -> list[float]:
        """Upper limit of the elevation."""
        return self._elev_upper

    @property
    def up(self) -> list[float]:
        return self._up

    @property
    def down(self) -> list[float]:
        return self._down

    def grad_process(self) -> None:
        """Compute average gradient of every 100m."""

        self._grad_max = []
        self._grad_min = []
        self._flat = []
        self._descend = []
        self._up = []
        self._down = []

        self._grad = []
        self._grad_bin = []
        self._grad_color = []
        self._elev_interp = []

        self._distance = []

        # For plot bounds
        self._elev_lower = []
        self._elev_upper = []

        for geo in self.geo_log:

            if geo is not None:

                dist = geo[:, 3] * 1000  # in meter
                self._distance.append(dist / 1000)
                height = geo[:, 2]  # in meter
                # Altitude cannot be zero?
                dist = dist[height > 0.0]
                height = height[height > 0.0]  # remove zero

                self._elev_lower.append(decompose_digit(height[0], -2)[0])
                self._elev_upper.append(decompose_digit(height[-1], 2)[0])

                (
                    grad_interp,
                    grad_bin,
                    elev_interp,
                    profile_data,
                ) = _compute_grad(dist, height)

                self._descend.append(profile_data["descend"])
                self._flat.append(profile_data["flat"])
                self._up.append(profile_data["up"])
                self._down.append(profile_data["down"])
                # Min-max gradient measured
                self._grad_max.append(min((grad_interp).max(), GRAD_MAX))
                self._grad_min.append(max((grad_interp).min(), GRAD_MIN))

                self._grad.append(grad_interp)
                self._grad_bin.append(grad_bin)
                self._elev_interp.append(elev_interp)

                self._grad_color.append(grad_to_color(grad_interp))

    def plot_gradient(self, idx: int) -> go.Figure:
        """Plot gradient profile."""

        # WIP
        fig = None

        dist = self.grad_bin[idx] / 1000
        elev = self.elev[idx]
        color = self.grad_color[idx]
        elev_diff = elev[-1] - elev[0]
        base = elev[0] - elev_diff * 0.1
        upper = elev_diff * 0.1 + elev[-1]
        num_patch = dist.shape[0] - 1

        fig = go.Figure()
        fig.update_xaxes(range=[dist[0], dist[-1]], zeroline=False)
        fig.update_yaxes(range=[base, upper], zeroline=False)
        for i in range(num_patch):

            fig.add_shape(
                {
                    "type": "path",
                    "path": f"M{dist[i]},{base} L{dist[i]},{elev[i]} L{dist[i+1]},{elev[i+1]}, L{dist[i+1]},{base} Z",
                },
                fillcolor=color[i],
                line_color="rgba(255, 255, 255, 0)",
            )
        fig.update_layout(
            xaxis_title="distance [km]", yaxis_title="elevation [m]"
        )

        return fig

    def plot_heatmap(self) -> go.Figure:

        fig = go.Figure()

        z = []
        c_scale = []
        min_grad = 0
        dc = 1 / 40
        for i, c in enumerate(GRAD_TO_COLOR):
            z.append(i - 20)
            c_scale.append([min_grad + i * dc, c])

        fig.add_trace(go.Heatmap(z=[z], colorscale=c_scale))
        fig.update_traces(showscale=False)
        fig.update_layout(
            autosize=False,
            width=700,
            height=200,
            xaxis={
                "tickvals": [0, 10, 20, 30, 40],
                "ticktext": ["-20", "-10", "0", "10", "20"],
            },
            yaxis={"visible": False},
        )

        return fig


def _compute_grad(
    dist: NDArray[np.float64], height: NDArray[np.float64]
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
    dict[str, float],
]:
    """Compute averaged gradient over every 100m."""

    # Substract by the initial height
    last = dist[-1]  # in meter
    # Find the nearest 100th meter
    last_rounded = int(np.round((last - 50) / 100)) + 1

    grad = np.zeros(last_rounded)
    lng = np.zeros(last_rounded)
    mheight = np.zeros(last_rounded)

    start: float = 0.0

    flat: float = 0.0
    descend: float = 0.0
    up: float = 0.0
    down: float = 0.0

    for idx in range(last_rounded):

        lng[idx] = start
        add_dist = []
        add_height = []

        if idx == last_rounded - 1:
            for d, h in zip(dist, height):
                if d > lng[idx - 1] + 50:
                    add_height.append(h)
                    add_dist.append(d)
        else:
            for d, h in zip(dist, height):
                if d > start - 50 and d <= start + 50:
                    add_height.append(h)
                    add_dist.append(d)

        if len(add_dist) == 0:
            hdist = 0.0
            grad[idx] = 0.0
            if idx == 0:
                ddist = 50
                mheight[idx] = height[0]
            else:
                ddist = 100
                mheight[idx] = mheight[idx - 1]
        elif len(add_dist) == 1:
            if idx == 0:
                ddist = 50
                hdist = add_height[0] - height[0]
                grad[idx] = hdist / ddist * 100
            else:
                ddist = add_dist[0] - lng[idx - 1]
                hdist = add_height[0] - mheight[idx - 1]
                grad[idx] = hdist / ddist * 100
            mheight[idx] = add_height[0]
        else:
            dist_array = np.asarray(add_dist, dtype=np.float64)
            ddist = (dist_array - dist_array[0]).sum()

            height_array = np.asarray(add_height, dtype=np.float64)
            hmean = height_array.mean()
            hdist = (height_array - height_array[0]).sum()

            grad[idx] = hdist / ddist * 100
            mheight[idx] = hmean

        start += 100
        if grad[idx] > -2 and grad[idx] < 2:
            flat += ddist
        elif grad[idx] <= -2:
            descend += ddist
            down += hdist
        else:
            up += hdist

    lng[-1] = last

    return (
        grad,
        lng,
        mheight,
        {"flat": flat, "descend": descend, "down": down, "up": up},
    )


def grad_to_color(grad: NDArray[np.float64]) -> NDArray[np.unicode_]:
    """Convert gradient to the color code. Min-max cut-off is [-20, 20] %."""

    idx = np.round(grad).astype(np.int64) + 20
    idx[idx < 0] = 0
    idx[idx > 40] = 40

    return GRAD_TO_COLOR[idx]


def latlng2m(
    latlng1: NDArray[np.float64], latlng2: NDArray[np.float64]
) -> float:
    """Convert latitude, longitude data to distance. Compute using the Haversine formula.

    Args:
        latlng1 (NDArray[np.float64]): the first point
        latlng2 (NDArray[np.float64]): the second point

    Returns:
        float: distance to be computed
    """

    radius = 6371e3  # Earch radius in meter
    dlat = deg2rad(latlng2[0] - latlng1[0])
    dlng = deg2rad(latlng2[1] - latlng1[1])

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(deg2rad(latlng1[0]))
        * np.cos(deg2rad(latlng2[0]))
        * np.sin(dlng / 2) ** 2
    )

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return radius * c


def deg2rad(deg: float) -> float:
    """Convert degree to radian."""
    return deg * np.pi / 180


def search_pass_by_distance(distance: list[float], db_loc: str) -> list[Pass]:

    pass_db_loc = db_loc + PASS_DB
    db = TinyDB(pass_db_loc)

    # Sanity check
    _sanity_check_list_input(distance)

    from_db = db.search(
        (
            (Query().min_distance >= distance[0])
            & (Query().min_distance <= distance[1])
        )
        | (
            (Query().max_distance >= distance[0])
            & (Query().max_distance <= distance[1])  # type: ignore
        )
    )

    searched_pass = []

    for data in from_db:
        dist_list = np.asarray(data["total_distance"])
        indicies = np.argwhere(
            np.logical_and(dist_list >= distance[0], dist_list <= distance[1])
        )
        searched_pass.append(Pass(**_update_list_data(data, indicies)))

    if len(searched_pass) == 0:
        raise RuntimeError(
            f"Pass: No pass data searched matching distance range: {distance}"
        )

    return searched_pass


def search_pass_by_elevation(
    elevation: list[float], db_loc: str
) -> list[Pass]:

    pass_db_loc = db_loc + PASS_DB
    db = TinyDB(pass_db_loc)

    # Sanity check
    _sanity_check_list_input(elevation)

    from_db = db.search(
        (
            (Query().min_elevation >= elevation[0])
            & (Query().min_elevation <= elevation[1])
        )
        | (
            (Query().max_elevation >= elevation[0])
            & (Query().max_elevation <= elevation[1])  # type: ignore
        )
    )

    searched_pass = []

    for data in from_db:
        dist_list = np.asarray(data["total_elevation"])
        indicies = np.argwhere(
            np.logical_and(
                dist_list >= elevation[0], dist_list <= elevation[1]
            )
        )

        searched_pass.append(Pass(**_update_list_data(data, indicies)))

    if len(searched_pass) == 0:
        raise RuntimeError(
            f"Pass: No pass data searched matching elevation range: {elevation}"
        )

    return searched_pass


def search_pass_by_height(height: list[float], db_loc: str) -> list[Pass]:
    """Search pass by its height (heightest point).

    Args:
        elevation (list[int]): lower and upper bound of passes to be searched.

    Returns:
        list[Pass]: list of searched passes.
    """

    pass_db_loc = db_loc + PASS_DB
    db = TinyDB(pass_db_loc)

    _sanity_check_list_input(height)

    from_db = db.search(
        (Query().height > height[0]) & (Query().height < height[1])
    )

    searched_pass = [Pass(**data) for data in from_db]

    if len(searched_pass) == 0:
        raise RuntimeError(
            f"Pass: No pass data searched matching height range: {height}"
        )

    return searched_pass


def search_pass_by_region(region: str, db_loc: str) -> list[Pass]:

    region = region.lower()

    pass_db_loc = db_loc + PASS_DB
    db = TinyDB(pass_db_loc)

    from_db = db.search(Query().region == region)

    searched_pass = [Pass(**data) for data in from_db]

    if len(searched_pass) == 0:

        raise RuntimeError(
            f"Pass: No pass data searched matching region: {region}"
        )

    return searched_pass


def search_pass_by_country(country: str, db_loc: str) -> list[Pass]:

    country = country.lower()

    pass_db_loc = db_loc + PASS_DB
    db = TinyDB(pass_db_loc)

    from_db = db.search(Query().country == country)

    searched_pass = [Pass(**data) for data in from_db]

    if len(searched_pass) == 0:

        raise RuntimeError(
            f"Pass: No pass data searched matching country: {country}"
        )

    return searched_pass


def search_pass_by_name(name: str, db_loc: str) -> list[Pass]:
    """Search pass by its name. First, it searches `db.names`. In the case of no matching name is found, check `db.alts` instead. Also, if there is a typo in the given name input, this function will return non-empty list contains name suggestions. Suggestion is made by using `difflib.get_close_mathces`.

    Args:
        name (str): name of a pass

    Returns:
        list[Pass]: searched pass. If there is no matching name, return None and non-empty name suggestion.
    """

    pass_db_loc = db_loc + PASS_DB
    pass_name_db_loc = db_loc + PASS_NAME_DB

    db = TinyDB(pass_db_loc)
    db_names = TinyDB(pass_name_db_loc)

    # There should be only one pass corresponding to the given name.
    from_db = db.get(Query().name == name)

    if from_db is None:

        # Try with alternative name
        from_db = db.get(Query().alt == name)

        if from_db is None:
            # Check levenstein distance of pass names
            all_names = db_names.all()[0]["alts"] + db_names.all()[0]["names"]
            suggested = get_close_matches(name, all_names)

            raise NameError(
                f"The given name ({name}) is not in our database. Did you mean {suggested}?"
            )

        else:
            pass_searched = [Pass(**from_db)()]

    else:
        pass_searched = [Pass(**from_db)()]

    return pass_searched


PASS_SEARCH_TYPE = [
    "name",
    "height",
    "elevation",
    "distance",
    "region",
    "country",
]

SEARCH_FACTORIES = {
    "name": {"func": search_pass_by_name, "key_type": str},
    "height": {"func": search_pass_by_height, "key_type": Union[list, tuple]},
    "distance": {
        "func": search_pass_by_distance,
        "key_type": Union[list, tuple],
    },
    "elevation": {
        "func": search_pass_by_elevation,
        "key_type": Union[list, tuple],
    },
    "region": {"func": search_pass_by_region, "key_type": str},
    "country": {"func": search_pass_by_country, "key_type": str},
}


@dataclass
class PassDB:

    db_loc: str = DB_LOC
    """Database location"""

    def search(
        self, key: Union[str, list[int], list[float]], search_type: str
    ) -> list[Pass]:

        search_type = search_type.lower()

        if search_type in PASS_SEARCH_TYPE:

            search_func = SEARCH_FACTORIES[search_type]["func"]
            input_type = SEARCH_FACTORIES[search_type]["key_type"]

            if (
                isinstance(key, get_args(input_type))
                and get_origin(input_type) is Union
            ) or isinstance(key, input_type):

                pass_searched = search_func(key, self.db_loc)

            else:
                raise TypeError(
                    f"PassDB: Non-supporting input type: {type(key)}. Should be {input_type}."
                )

        else:

            raise TypeError(
                f"PassDB: Non-supporting search type: {search_type}. Should be one of {PASS_SEARCH_TYPE}."
            )

        return pass_searched


def _update_list_data(data: dict, indicies: NDArray[np.int64]) -> dict:

    gpts = dict()
    total_distance: list[float] = []
    total_elevation: list[int] = []
    avg_grad: list[float] = []

    # Indices is 2D array. Therefore need to be accessed with zero index.
    for i, idx in enumerate(indicies):
        gpts.update({str(i): data["gpts"][str(idx[0])]})
        total_distance.append(data["total_distance"][idx[0]])
        total_elevation.append(data["total_elevation"][idx[0]])
        avg_grad.append(data["avg_grad"][idx[0]])

    max_distance = max(total_distance)
    min_distance = min(total_distance)
    max_elevation = max(total_elevation)
    min_elevation = min(total_elevation)

    data["gpts"] = gpts
    data["total_distance"] = total_distance
    data["total_elevation"] = total_elevation
    data["max_distance"] = max_distance
    data["min_distance"] = min_distance
    data["max_elevation"] = max_elevation
    data["min_elevation"] = min_elevation
    data["avg_grad"] = avg_grad

    return data


def _sanity_check_list_input(inputs: Union[list[float], list[int]]) -> None:

    # Sanity check
    assert (
        len(inputs) == 2
    ), "Pass: length of the input should be 2 -> [lower, upper]."

    assert (
        inputs[1] > inputs[0]
    ), "Pass: bounds should be increasing order -> [lower, upper]."


def get_gpt_data(
    gpts: dict[str, dict[str, str]]
) -> list[Optional[NDArray[np.float64]]]:
    """Obtain latitude, longitude, height, and distance information (GPT data) from the path ids.

    Args:
        path_ids (list[str]): path ids

    Returns:
        list[NDarray[np.float64]]: resulting gpt data
    """
    gpt_data_string = [
        json.loads(
            bs(requests.get(gpts[pid]["gpt"]).text, "lxml").text.replace(
                ";", ","
            )
        )
        for pid in gpts
    ]

    # Convert string to number
    # Since json cannot serialize numpy ndarray, convert to list.
    gpt_data = []
    for gpt in gpt_data_string:

        try:
            gpt_data.append(
                np.asarray(
                    [
                        np.array(line.split(","), dtype=np.float64)
                        for line in gpt
                    ],
                    dtype=np.float64,
                )
            )
        except ValueError:
            gpt_data.append(None)

    return gpt_data
