#!/usr/bin/env python3
"""Builds this home's four dashboards from Origami's parts.

Each part is read from its folder under ../dashboard, changed to this home's
entities and put into a view that fits the device. The result is one YAML file
for each dashboard, to paste into the dashboard's raw configuration editor.

    python3 my-dashboards/build.py

The home's entities are in the first half of this file, and the layout of each
device is at the end. After a change here, or after an Origami update, run the
script again and paste the files again. The script needs PyYAML.
"""

import copy
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
PARTS = HERE.parent / "dashboard"


# ---------------------------------------------------------------------------
# The home
# ---------------------------------------------------------------------------

WEATHER = "weather.openweathermap"
CALENDAR = "calendar.household"
SHOPPING = "todo.shopping_list"
VACUUM = "vacuum.kitchen_eufy_robovac"
VACUUM_BATTERY = "sensor.kitchen_eufy_robovac_battery"
TV = "media_player.living_room_55_tcl_roku_tv"
TV_REMOTE = "remote.living_room_55_tcl_roku_tv"
# The apps of the TV, with the names its source_list attribute uses
TV_APPS = ["Netflix", "YouTube", "Prime Video"]
# The toggle that opens and closes the climate table
CLIMATE_TABLE = "input_boolean.room_climate_card"
# The weather card's bar goes from 14° to 95° in Fahrenheit, and from -10° to 35° in Celsius
FAHRENHEIT = True

# The window contacts that the rooms header counts
WINDOWS = [
    "binary_sensor.couch_window_sensor_snzb_04pr2_sonoff_a4400479b6",
    "binary_sensor.front_door_window_sensor_snzb_04pr2_sonoff_a4400479af",
    "binary_sensor.stairs_window_sensor_snzb_04pr2_sonoff_a4400479b5",
    "binary_sensor.typewriter_window_sensor_snzb_04pr2_sonoff_a4400479b3",
]

# The doors that show in the notifications while they are open
DOORS = [
    ("binary_sensor.living_room_front_door_entry_door", "Front door"),
    ("binary_sensor.living_room_side_door_entry_door", "Side door"),
    ("binary_sensor.kitchen_back_door_entry_door", "Back door"),
]

# The speakers of the music pop-up, the favorites and the navigation bar.
# The Echos are the Alexa Media Player entities: the Alexa Devices ones have no play, pause or skip.
SPEAKERS = [
    ("media_player.livingroom_ashers_echo_spot_2", "Living room"),
    ("media_player.kitchen_ashers_white_echo_pop_2", "Kitchen"),
    ("media_player.ashersbedroomechodot2", "Bedroom"),
    ("media_player.office_echo_dot_2", "Office"),
    ("media_player.office_homepod_mini", "HomePod"),
]

SCENE_ICONS = {
    "Bright": "mdi:brightness-7",
    "Concentrate": "mdi:head-lightbulb-outline",
    "Dimmed": "mdi:brightness-4",
    "Energize": "mdi:lightning-bolt-outline",
    "Nightlight": "mdi:weather-night",
    "Read": "mdi:book-open-variant",
    "Relax": "mdi:sofa-outline",
    "Rest": "mdi:bed-outline",
    "I Love Lydia": "mdi:heart-outline",
}

# Each room has a card and a pop-up. `light` is the room's light group, or its only lamp.
# `lamps` are the lamps of the group, each as a whole: a light strip's segments stay out.
ROOMS = [
    {
        "key": "living_room",
        "name": "Living room",
        "short": "Living",
        "icon": "mdi:sofa",
        "light": "light.living_room_lights",
        "lamps": [
            ("light.livingroom_corner_lamp", "Corner lamp"),
            ("light.living_room_living_room_tall_lamp", "Tall lamp"),
            ("light.livingroom_small_green_lamp", "Green lamp"),
            ("light.living_room_front_door_lamp", "Front door lamp"),
        ],
        "scenes": [
            ("scene.livingroom_scene_bright", "Bright"),
            ("scene.livingroom_scene_relax", "Relax"),
            ("scene.livingroom_scene_read", "Read"),
            ("scene.livingroom_scene_dimmed", "Dimmed"),
            ("scene.livingroom_scene_nightlight", "Nightlight"),
            ("scene.livingroom_scene_concentrate", "Concentrate"),
            ("scene.livingroom_scene_energize", "Energize"),
            ("scene.livingroom_scene_rest", "Rest"),
        ],
        "temperature": "sensor.living_room_temp_3_snzb_02p_sonoff_a440047919_temperature",
        "humidity": "sensor.living_room_temp_3_snzb_02p_sonoff_a440047919_humidity",
        "speaker": "media_player.livingroom_ashers_echo_spot_2",
        "tv": TV,
    },
    {
        "key": "kitchen",
        "name": "Kitchen",
        "short": "Kitchen",
        "icon": "mdi:silverware-fork-knife",
        "light": "light.kitchen_sink_light",
        "light_name": "Sink light",
        "lamps": [],
        "scenes": [],
        "temperature": "sensor.temperature_1_snzb_02p_sonoff_a440047912_temperature",
        "humidity": "sensor.temperature_1_snzb_02p_sonoff_a440047912_humidity",
        "speaker": "media_player.kitchen_ashers_white_echo_pop_2",
    },
    {
        "key": "bedroom",
        "name": "Bedroom",
        "short": "Bed",
        "icon": "mdi:bed",
        # A light group to create, as the README in this folder says
        "light": "light.bedroom_lights",
        "lamps": [
            ("light.bedroom_dresser_lamp", "Dresser lamp"),
            ("light.bedroom_bedroom_strip_lights", "Strip lights"),
            ("light.bedlightstrip", "Bed light strip"),
        ],
        "scenes": [("scene.i_love_lydia", "I Love Lydia")],
        "temperature": "sensor.temp_2_snzb_02p_sonoff_a440047917_temperature",
        "humidity": "sensor.temp_2_snzb_02p_sonoff_a440047917_humidity",
        "speaker": "media_player.ashersbedroomechodot2",
    },
    {
        "key": "office",
        "name": "Office",
        "short": "Office",
        "icon": "mdi:desk",
        "light": "light.office_lights",
        "lamps": [
            ("light.office_desk_lamp", "Desk lamp"),
            ("light.office_left_lamp", "Office lamp"),
            ("light.office_ashers_right_corner_lamp", "Corner lamp"),
            ("light.gaming_light_bars", "Light bars"),
            ("light.monitor_camera_lights", "Monitor lights"),
        ],
        "scenes": [
            ("scene.office_scene_bright", "Bright"),
            ("scene.office_scene_relax", "Relax"),
            ("scene.office_scene_read", "Read"),
            ("scene.office_scene_dimmed", "Dimmed"),
            ("scene.office_scene_energize", "Energize"),
        ],
        "temperature": "sensor.office_echo_dot_temperature",
        "speaker": "media_player.office_echo_dot_2",
    },
    {
        "key": "basement",
        "name": "Basement",
        "short": "Basement",
        "icon": "mdi:stairs-down",
        # A light group to create, as the README in this folder says
        "light": "light.basement_lights",
        "lamps": [
            ("light.basement_basement_light_stairs", "Stairs"),
            ("light.basement_basement_light_right_side", "Right side"),
        ],
        "scenes": [],
        # Stays hidden on the phone until a tap on All rooms
        "extra": True,
    },
]

LIVING = ROOMS[0]

# The lights pop-up's power key turns on one of these scenes of the living room, by the hour.
# Each entry has the scene's name, the hour it starts and the hour it ends.
SCENE_HOURS = [("Nightlight", 23, 5), ("Bright", 5, 17), ("Relax", 17, 21), ("Dimmed", 21, 23)]

# The scenes that a hold on the navigation bar's lights button lists
NAVBAR_SCENES = ["Bright", "Relax", "Read", "Dimmed", "Nightlight"]

# Every lamp of the home. The lights button counts these, and Turn off turns these off.
# The tablets' screens are lights in Home Assistant too, so "all lights" would turn them off.
ALL_LAMPS = [lamp for room in ROOMS for lamp, _ in (room["lamps"] or [(room["light"], "")])]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load(name):
    return yaml.safe_load((PARTS / name).read_text(encoding="utf-8"))


def walk(node, change):
    """Returns a copy of node with change() applied to every string, keys included."""
    if isinstance(node, dict):
        return {walk(k, change): walk(v, change) for k, v in node.items()}
    if isinstance(node, list):
        return [walk(v, change) for v in node]
    return change(node) if isinstance(node, str) else node


def swap(node, ids):
    """Replaces entity IDs. An ID only matches as a whole, so light.a leaves light.a_b alone."""
    pattern = re.compile(r"(?<![\w.])(" + "|".join(re.escape(i) for i in sorted(ids, key=len, reverse=True)) + r")(?!\w)")
    return walk(node, lambda text: pattern.sub(lambda m: ids[m.group(1)], text))


def replace(node, old, new):
    """Replaces a piece of text in every string. It has to be there, so a changed part is noticed."""
    found = []

    def change(text):
        if old in text:
            found.append(1)
        return text.replace(old, new)

    result = walk(node, change)
    assert found, f"not found: {old}"
    return result


def js_list(ids):
    return "[" + ", ".join(f"'{i}'" for i in ids) + "]"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def by_name(items, name):
    return next(i for i in items if i.get("name") == name)


def navigate(path):
    return {"action": "navigate", "navigation_path": path}


def scene_action(scene):
    return {"action": "perform-action", "perform_action": "scene.turn_on", "target": {"entity_id": scene}}


def without_blur(css):
    """Leaves out the blur behind a bar or a menu, which an old tablet draws slowly."""
    return "\n".join(line for line in css.split("\n") if "backdrop-filter" not in line)


def light_popup(node, lite):
    """A pop-up without a blurred page behind it on an old tablet."""
    if lite:
        node["performance_mode"] = "performance"
    return node


# ---------------------------------------------------------------------------
# The home view
# ---------------------------------------------------------------------------

def greeting():
    card = swap(load("greeting/card.yaml"), {"weather.home": WEATHER, "calendar.household": CALENDAR})
    card["cards"][1]["entities"] = [
        {"entity": CALENDAR, "before": "24:00:00"},
        VACUUM,
        *[{"entity": door, "name": name} for door, name in DOORS],
    ]
    return card


def weather(kind, lite):
    card = swap(load(f"weather/{kind}.yaml"), {"weather.home": WEATHER})
    if kind == "comparison" and FAHRENHEIT:
        bar = card["button_containers"][2]["buttons"][0]["elements"][0]
        assert bar["bar_min"] == "-10" and bar["bar_max"] == "35"
        bar["bar_min"], bar["bar_max"] = "14", "95"
    if lite:
        # The forecast tiles have a plain fill, without a blur
        card["button_containers"][1]["button_blurred_background"] = False
    return card


def favorites():
    tiles = load("favorites/tiles.yaml")
    old = tiles["sub_button"]["bottom"]
    music = by_name(old, "Music")
    vacuum = swap(by_name(old, "Vacuum"), {"vacuum.robot": VACUUM})
    # The vacuum has no sensor for its progress, so the tile keeps its name
    del vacuum["origami_tiles"]["name"]
    tiles["sub_button"]["bottom"] = [
        *[{**swap(music, {"media_player.bedroom": speaker}), "name": name} for speaker, name in SPEAKERS],
        swap(by_name(old, "Shopping"), {"todo.shopping_list": SHOPPING}),
        swap(by_name(old, "TV"), {"media_player.living_room_tv": TV}),
        vacuum,
    ]
    return [load("favorites/header.yaml"), tiles]


TEMPERATURES_OLD = "['sensor.living_room_temperature', 'sensor.bedroom_temperature', 'sensor.office_temperature']"
HUMIDITIES_OLD = "['sensor.living_room_humidity', 'sensor.bedroom_humidity', 'sensor.office_humidity']"
TEMPERATURES = js_list(r["temperature"] for r in ROOMS if r.get("temperature"))
HUMIDITIES = js_list(r["humidity"] for r in ROOMS if r.get("humidity"))


def rooms_header(table_opens):
    card = replace(load("rooms/header.yaml"), TEMPERATURES_OLD, TEMPERATURES)
    card = replace(card, "['binary_sensor.living_room_window', 'binary_sensor.bedroom_window']", js_list(WINDOWS))
    card = swap(card, {"input_boolean.climate_table": CLIMATE_TABLE})
    if not table_opens:
        # The climate table always shows on this device, so nothing opens it
        values = card["sub_button"]["main"][:2]
        for value in values:
            value["tap_action"] = {"action": "none"}
        card["sub_button"]["main"] = values
    return card


def room_card(room, hidden=False):
    card = swap(load("rooms/room.yaml"), {
        "light.living_room": room["light"],
        "sensor.living_room_temperature": room.get("temperature", ""),
        "sensor.living_room_humidity": room.get("humidity", ""),
    })
    card["name"] = room["name"]
    card["icon"] = room["icon"]
    card["button_action"]["tap_action"]["navigation_path"] = f"#popup_{room['key']}"
    dot, _window, temperature, humidity = card["sub_button"]["bottom"]
    if not room.get("temperature"):
        del card["sub_button"]["bottom"]
    elif room.get("humidity"):
        card["sub_button"]["bottom"] = [dot, temperature, humidity]
    else:
        temperature["origami_base"]["name"] = "${num(state, 0)}°"
        card["sub_button"]["bottom"] = [dot, temperature]
    if hidden:
        card["visibility"] = [{"condition": "state", "entity": "input_boolean.all_rooms", "state": "on"}]
    return card


def climate_table(always, lite):
    card = replace(replace(load("climate-table/card.yaml"), TEMPERATURES_OLD, TEMPERATURES), HUMIDITIES_OLD, HUMIDITIES)
    # The home has no window contact for each room and no thermostats, so those two columns go
    card["origami_table"]["columns"] = [c for c in card["origami_table"]["columns"] if c["name"] not in ("window", "thermostat")]
    rows = []
    for room in ROOMS:
        if not room.get("temperature"):
            continue
        cells = [
            {"entity": room["temperature"], "name": room["short"], "show_name": True, "css_class": "room"},
            {"entity": room["temperature"], "css_class": "temperature"},
        ]
        if room.get("humidity"):
            cells.append({"entity": room["humidity"], "css_class": "humidity"})
        rows.append({"name": room["name"], "group": cells})
    card["sub_button"]["bottom"] = rows
    if not always:
        card["visibility"] = [{"condition": "state", "entity": CLIMATE_TABLE, "state": "on"}]
    if lite:
        del card["origami_base"]
    return card


def calendar():
    return {"type": "calendar", "entities": [CALENDAR], "initial_view": "listWeek", "grid_options": {"columns": "full"}}


def menu(lite, other_view=None):
    card = load("menu/card.yaml")
    buttons = card["buttons"]
    settings = {"name": "Settings", "icon": "mdi:cog-outline", "tap_action": navigate("/config/dashboard")}
    if other_view:
        # A tablet's menu switches between the landscape and the portrait view
        name, icon, path = other_view
        first = [{"name": name, "icon": icon, "tap_action": navigate(path)}, settings]
    else:
        first = [settings, by_name(buttons, "Autom.")]
    card["buttons"] = [*first, by_name(buttons, "Menu"), by_name(buttons, "Edit")]
    if lite:
        card["css"] = without_blur(card["css"])
    return card


def navbar(lite):
    speakers = js_list(s for s, _ in SPEAKERS)
    card = replace(load("navigation-bar/card.yaml"), "['media_player.living_room', 'media_player.bedroom', 'media_player.office']", speakers)
    card = swap(card, {"media_player.living_room_tv": TV, "light.living_room": LIVING["light"]})
    # The lights button counts the home's lamps, without the tablets' screens and the segments of the light strips
    lamps = js_list(ALL_LAMPS)
    card = replace(card, "Object.values(states).some((s) => s.entity_id.startsWith('light.') && s.state === 'on')",
                   f"{lamps}.some((id) => states[id]?.state === 'on')")
    card = replace(card, "Object.values(states).filter((s) => s.entity_id.startsWith('light.') && s.state === 'on' && !s.attributes.entity_id).length",
                   f"{lamps}.filter((id) => states[id]?.state === 'on').length")
    lights = by_name_label(card["routes"], "Lights")
    turn_off, turn_on, evening = lights["popup"][:3]
    turn_off["tap_action"]["target"]["entity_id"] = list(ALL_LAMPS)
    scenes = {name: scene for scene, name in LIVING["scenes"]}
    lights["popup"] = [turn_off, turn_on] + [
        {**swap(evening, {"scene.living_room_evening": scenes[name]}), "label": name, "icon": SCENE_ICONS[name]}
        for name in NAVBAR_SCENES
    ]
    # Nothing is cast to the TV here, so the now playing card has only the speakers
    card["media_player"]["players"] = card["media_player"]["players"][:1]
    if lite:
        card["styles"] = without_blur(card["styles"])
    return card


def by_name_label(items, label):
    return next(i for i in items if i.get("label") == label)


# ---------------------------------------------------------------------------
# The pop-ups
# ---------------------------------------------------------------------------

def lamp_rows(template, lamps):
    return [{**template, "entity": lamp, "name": name} for lamp, name in lamps]


def scenes_list(text, scenes):
    """Replaces the first list of scenes in a template."""
    result, count = re.subn(r"\['scene\.[^\]]*\]", js_list(s for s, _ in scenes), text, count=1)
    assert count, "no list of scenes"
    return result


def room_popup(room, lite):
    popup = swap(load("room/living-room.yaml"), {
        "light.living_room": room["light"],
        "media_player.living_room": room.get("speaker", ""),
        "media_player.living_room_tv": room.get("tv", ""),
        "sensor.living_room_temperature": room.get("temperature", ""),
        "sensor.living_room_humidity": room.get("humidity", ""),
    })
    popup["hash"] = f"#popup_{room['key']}"
    popup["name"] = room["name"]
    media, lights, climate, off = popup["cards"][0]["cards"]
    cards = []

    # Media: the TV has its own sound here, so its card and the speaker's card both show
    players = []
    if room.get("tv"):
        tv = media["cards"][0]["card"]
        tv["origami_media"] = {"layout": "tv"}
        # A Roku TV reports no volume level, so the card has no slider. The TV pop-up has the volume keys.
        del tv["sub_button"]["bottom"]
        tv["rows"] = 1.375
        players.append(tv)
    if room.get("speaker"):
        speaker = media["cards"][1]["card"]
        # The speakers have no Bluetooth source to switch to
        speaker["sub_button"]["main"] = speaker["sub_button"]["main"][:2]
        players.append(speaker)
    if players:
        cards.append({"type": "vertical-stack", "cards": players})

    # Lights
    header, everything = lights["cards"]
    mini = popup["origami_popup"]["mini_popups"]
    palette, power = everything["sub_button"]["main"]
    slider, arrow = everything["sub_button"]["bottom"][0]["group"]
    if room["lamps"]:
        rows = mini["lamps"][0]["sub_button"]["bottom"]
        mini["lamps"][0]["sub_button"]["bottom"] = lamp_rows(rows[0], room["lamps"])
        if room is not LIVING:
            # Only the living room has the lights pop-up. Every other room opens its light group's dialog.
            value = header["sub_button"]["main"][0]
            del value["icon"], value["content_layout"]
            value["show_icon"] = False
            value["tap_action"] = {"action": "more-info"}
    else:
        # One lamp alone: no count in the header and no row for each lamp
        del mini["lamps"], header["sub_button"]
        everything["name"] = room["light_name"]
        everything["icon"] = "mdi:lightbulb"
        everything["sub_button"]["bottom"][0]["group"] = [slider]
    if room["scenes"]:
        box = mini["scenes"]["cards"][0]
        box["origami_button"]["active"] = scenes_list(box["origami_button"]["active"], room["scenes"])
        first = box["sub_button"]["bottom"][0]
        box["sub_button"]["bottom"] = [
            {**first, "name": name, "icon": SCENE_ICONS[name], "tap_action": scene_action(scene)}
            for scene, name in room["scenes"]
        ]
    else:
        del mini["scenes"]
        everything["sub_button"]["main"] = [power]
    if not mini:
        del popup["origami_popup"]
    cards.append(lights)

    # Climate: the home has no fans and no thermostats, so only the header with the temperature stays
    if room.get("temperature"):
        value = climate["cards"][0]
        if not room.get("humidity"):
            del value["sub_button"]["main"][0]["origami_header"]["name"]
        cards.append(value)

    # Everything off turns off the lamps and the TV. Speakers stay out, because some can't be turned off.
    target = off["sub_button"]["bottom"][0]["tap_action"]["target"]
    target["entity_id"] = [room["light"], *([room["tv"]] if room.get("tv") else [])]
    cards.append(off)

    popup["cards"][0]["cards"] = cards
    return light_popup(popup, lite)


def lights_popup(lite):
    group = LIVING["light"]
    scenes = {name: scene for scene, name in LIVING["scenes"]}
    popup = replace(load("lights/pop-up.yaml"), "states.light.living_room.last_changed", f"states['{group}'].last_changed")
    popup = swap(popup, {"light.living_room": group})
    rows = popup["origami_popup"]["mini_popups"]["lamps"][0]["sub_button"]["bottom"]
    popup["origami_popup"]["mini_popups"]["lamps"][0]["sub_button"]["bottom"] = lamp_rows(rows[0], LIVING["lamps"])
    main, row = popup["cards"][0]["cards"]

    # The first power key turns off every lamp of the home. The others turn on the scene for the time of day.
    off, key = main["sub_button"]["main"][:2]
    off["tap_action"]["target"]["entity_id"] = list(ALL_LAMPS)
    keys = [off]
    for name, start, end in SCENE_HOURS:
        outside = f"h >= {end} && h < {start}" if start > end else f"h < {start} || h >= {end}"
        new = copy.deepcopy(key)
        new["origami_base"]["hidden"] = f"${{states('{group}') === 'on' || (h => {outside})(new Date().getHours())}}"
        new["tap_action"] = scene_action(scenes[name])
        keys.append(new)
    main["sub_button"]["main"] = keys

    # The scenes show their icons. A scene's colors and brightness can be added as `field` and `label`.
    button = row["origami_button"]
    button["active"] = scenes_list(button["active"], LIVING["scenes"])
    day = [(name, end) for name, start, end in SCENE_HOURS if start < end]
    night = next(name for name, start, end in SCENE_HOURS if start > end)
    first = day[0]
    start_of_day = next(start for name, start, end in SCENE_HOURS if name == first[0])
    steps = " : ".join(f"h < {end} ? '{slug(name)}'" for name, end in day[:-1])
    button["start"] = (f"${{(h => h < {start_of_day} || h >= {day[-1][1]} ? '{slug(night)}' : {steps} : "
                       f"'{slug(day[-1][0])}')(new Date().getHours())}}")
    template = row["sub_button"]["bottom"][0]["group"][0]
    del template["origami_button"]
    row["sub_button"]["bottom"][0]["group"] = [
        {**template, "name": name, "icon": SCENE_ICONS[name], "css_class": slug(name), "tap_action": scene_action(scene)}
        for scene, name in LIVING["scenes"]
    ]
    return light_popup(popup, lite)


def music_popup(lite):
    popup = load("music/pop-up.yaml")
    # The speakers can't play in groups through Home Assistant, so the group, its volume and the shortcuts go
    del popup["origami_popup"]["mini_popups"]
    select, chip = popup["sub_button"]["main"][:2]
    popup["sub_button"]["main"] = [select] + [swap(chip, {"media_player.living_room": speaker}) for speaker, _ in SPEAKERS]
    music, volume, _ungroup = popup["cards"][0]["cards"]
    music["sub_button"]["main"] = []
    del music["origami_base"]["words"]
    del volume["sub_button"]
    popup["cards"][0]["cards"] = [music, volume]
    if lite:
        # No blurred cover behind the pop-up, and nothing glides
        del popup["origami_popup"]["art"], popup["origami_base"]
    return light_popup(popup, lite)


def remote_command(command):
    return {"action": "perform-action", "perform_action": "remote.send_command",
            "target": {"entity_id": TV_REMOTE}, "data": {"command": command}}


def tv_popup(lite):
    popup = swap(load("tv/pop-up.yaml"), {"media_player.living_room_tv": TV, "remote.living_room_tv": TV_REMOTE})
    # Nothing is cast to the TV here, so no picture shows behind the pop-up
    del popup["origami_popup"]
    tv, row, apps, remote = popup["cards"][0]["cards"]
    tv["origami_media"] = {"layout": "tv"}
    del tv["origami_base"]
    # A Roku TV reports no volume level, so the remote's volume keys take the place of the slider
    del tv["sub_button"]["bottom"]
    tv["rows"] = 1.375
    row["sub_button"]["bottom"] = [{"name": "Volume", "group": [
        {"name": "Quieter", "icon": "mdi:minus", "tap_action": remote_command("volume_down")},
        {"name": "Mute", "icon": "mdi:volume-mute", "tap_action": remote_command("volume_mute")},
        {"name": "Louder", "icon": "mdi:plus", "tap_action": remote_command("volume_up")},
    ]}]
    app = apps["sub_button"]["bottom"][0]
    apps["sub_button"]["bottom"] = [
        {**app, "name": name, "tap_action": {**app["tap_action"], "data": {"source": name}}} for name in TV_APPS
    ]
    # The key names of the Roku remote
    keys = {"Back": "back", "Home": "home", "Up": "up", "Left": "left", "OK": "select", "Right": "right", "Down": "down"}
    for button in remote["sub_button"]["bottom"]:
        button["tap_action"] = remote_command(keys[button["name"]])
    return light_popup(popup, lite)


def vacuum_popup(lite):
    popup = swap(load("vacuum/pop-up.yaml"), {"vacuum.robot": VACUUM, "sensor.robot_battery": VACUUM_BATTERY})
    # The state, the battery and the keys stay. The vacuum has no fan_speed_list for the suction,
    # and the rooms, the map and the maintenance need sensors and names that it doesn't have.
    del popup["origami_popup"]["mini_popups"]
    main = popup["cards"][0]["cards"][0]
    keys = [k for k in main["sub_button"]["bottom"][0]["group"] if k["name"] != "Bin"]
    del by_name(keys, "Stop")["origami_base"]["hidden"]
    main["sub_button"]["bottom"][0]["group"] = keys
    del main["styles"]
    popup["cards"][0]["cards"] = [main]
    return light_popup(popup, lite)


def server_popup(lite):
    popup = load("server/pop-up.yaml")
    if lite:
        # The load graph is a lot to draw for an old tablet
        popup["cards"][0]["cards"] = [c for c in popup["cards"][0]["cards"] if c["type"] != "custom:plotly-graph"]
    return light_popup(popup, lite)


def favorites_popup(lite):
    popup = swap(load("favorites-list/pop-up.yaml"), {
        "media_player.living_room_tv": TV, "vacuum.robot": VACUUM,
        "calendar.household": CALENDAR, "todo.shopping_list": SHOPPING,
    })
    first, _, devices = popup["cards"][0]["cards"][:3]
    first["sub_button"]["bottom"] = [r for r in first["sub_button"]["bottom"] if r["name"] != "Timer"]
    devices["sub_button"]["bottom"] = [r for r in devices["sub_button"]["bottom"] if r["name"] != "Fan"]
    return light_popup(popup, lite)


def popups(lite):
    return [
        *[room_popup(room, lite) for room in ROOMS],
        lights_popup(lite),
        music_popup(lite),
        tv_popup(lite),
        vacuum_popup(lite),
        favorites_popup(lite),
        server_popup(lite),
    ]


# ---------------------------------------------------------------------------
# The views
# ---------------------------------------------------------------------------

def view(device, title, path, icon, columns, other_view=None):
    lite = device["lite"]
    wide = columns >= device.get("table_always", 99)
    start = [greeting(), weather(device["weather"], lite), *favorites()]
    phone = device.get("phone", False)
    rooms = [rooms_header(table_opens=not wide)]
    table = climate_table(always=wide, lite=lite)
    if not wide:
        rooms.append(table)
    rooms += [room_card(room, hidden=phone and room.get("extra", False)) for room in ROOMS]
    if phone:
        rooms.append(load("rooms/all-rooms.yaml"))
    sections = [start, rooms]
    if wide:
        # The main tablet has room for the climate table and the week's events, always in view
        sections.append([table, calendar()])
    # The pop-ups, the bar and the menu take no space, and they have to be in the same view as their buttons
    sections[-1] += [*popups(lite), navbar(lite), menu(lite, other_view)]
    return {
        "type": "sections",
        "title": title,
        "path": path,
        "icon": icon,
        "max_columns": columns,
        "sections": [{"type": "grid", "cards": cards} for cards in sections],
    }


# `lite` is for old hardware: no blur behind pop-ups, the bar and the menu, the calm weather card,
# no load graph and nothing that glides. `landscape` and `portrait` are the columns of each view.
DEVICES = [
    {
        "file": "iphone-origami-dashboard",
        "title": "iPhone Origami Dashboard",
        "about": "iPhones. One column upright, and two columns when the phone lies on its side.",
        "lite": False,
        "phone": True,
        "weather": "diorama",
        "views": [("Home", "home", "mdi:home", 2)],
    },
    {
        "file": "nexus-tablet-origami-dashboard",
        "title": "Nexus Tablet Origami Dashboard",
        "about": "Nexus 7 (2013): 960 x 600 points in landscape, old hardware, so the light build.",
        "lite": True,
        "weather": "comparison",
        "views": [("Landscape", "landscape", "mdi:tablet", 2), ("Portrait", "portrait", "mdi:tablet-android", 1)],
    },
    {
        "file": "fire-hd8-origami-dashboard",
        "title": "Fire HD8 Origami Dashboard",
        "about": "Fire HD 8 (7th generation): about 960 x 600 points in landscape, old hardware, so the light build.",
        "lite": True,
        "weather": "comparison",
        "views": [("Landscape", "landscape", "mdi:tablet", 2), ("Portrait", "portrait", "mdi:tablet-android", 1)],
    },
    {
        "file": "galaxy-tab-origami-dashboard",
        "title": "Galaxy Tab Origami Dashboard",
        "about": "Galaxy Tab A9+: 1280 x 800 points in landscape. The main wall tablet, with everything in view.",
        "lite": False,
        "weather": "diorama",
        # With three columns, the climate table and the calendar have a column of their own
        "table_always": 3,
        "views": [("Landscape", "landscape", "mdi:tablet", 3), ("Portrait", "portrait", "mdi:tablet-android", 2)],
    },
]


class Dumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def text(dumper, data):
    # A text of several lines, such as a card's styles, stays readable as a block
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, text)


def build(device):
    views = []
    for title, path, icon, columns in device["views"]:
        other = None
        if len(device["views"]) > 1:
            name, to, *_ = next(v for v in device["views"] if v[1] != path)
            other = (name, "mdi:phone-rotate-landscape" if to == "landscape" else "mdi:phone-rotate-portrait",
                     f"/{device['file']}/{to}")
        views.append(view(device, title, path, icon, columns, other))
    head = (
        f"# {device['title']}\n"
        f"# For {device['about']}\n"
        f"# Built by build.py from Origami's parts. Paste it into the dashboard's raw configuration editor,\n"
        f"# as the README in this folder says. The dashboard's URL has to be {device['file']}.\n"
    )
    body = yaml.dump({"views": views}, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=4096)
    (HERE / f"{device['file']}.yaml").write_text(head + body, encoding="utf-8")
    return len(body)


if __name__ == "__main__":
    for device in DEVICES:
        print(f"{device['file']}.yaml  {build(device) // 1024} KB")
