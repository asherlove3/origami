# My dashboards

Four dashboards for this home, built from Origami's parts with the home's own entities.

| Dashboard | File | URL | Views |
| --- | --- | --- | --- |
| iPhone Origami Dashboard | [`iphone-origami-dashboard.yaml`](iphone-origami-dashboard.yaml) | `iphone-origami-dashboard` | One view: one column upright, two columns on its side |
| Nexus Tablet Origami Dashboard | [`nexus-tablet-origami-dashboard.yaml`](nexus-tablet-origami-dashboard.yaml) | `nexus-tablet-origami-dashboard` | Landscape with two columns, Portrait with one |
| Fire HD8 Origami Dashboard | [`fire-hd8-origami-dashboard.yaml`](fire-hd8-origami-dashboard.yaml) | `fire-hd8-origami-dashboard` | Landscape with two columns, Portrait with one |
| Galaxy Tab Origami Dashboard | [`galaxy-tab-origami-dashboard.yaml`](galaxy-tab-origami-dashboard.yaml) | `galaxy-tab-origami-dashboard` | Landscape with three columns, Portrait with two |

The Nexus and the Fire HD8 get a light build for their old hardware: no blur behind pop-ups, the bar and the menu, the calm comparison weather card, no load graph in the server pop-up and nothing that glides. On the Galaxy Tab, the climate table and the week's calendar always show in a column of their own.

## Before the dashboards

Keep a copy of the configuration first, such as a backup under **Settings**, **System**, **Backups**.

1. **Origami's basics.** The theme, the font, Bubble Card 3.4 or later with Bubble Card Tools, and all modules from [`bubble_card/modules`](../bubble_card/modules), as [Get started](../README.md#get-started) describes.
2. **The other cards**, from HACS: [Navbar Card](../dashboard/navigation-bar/README.md#setup), [Origami Weather](../dashboard/weather/README.md#setup), [Origami Notifications](../dashboard/greeting/README.md#setup), [Origami Header](../dashboard/menu/README.md#setup) with its lines in `configuration.yaml`, and [Plotly Graph Card](../dashboard/server/README.md#optional) for the load graph on the iPhone and the Galaxy Tab.
3. **Two light groups.** Under **Settings**, **Devices & services**, **Helpers**, create a **Group**, then **Light group**:
   - **Bedroom Lights**, so its entity ID is `light.bedroom_lights`, with Bedroom Dresser Lamp, Bedroom Strip Lights and Govee Bed Light Strip
   - **Basement Lights**, so its entity ID is `light.basement_lights`, with Basement Light Stairs and Basement Light Right Side
4. **The music pop-up.** Follow [its setup](../dashboard/music/README.md#setup) for the scripts **Playback** and **Set group volume** and the helper **Group volume**. The helper **Selected speaker** is there already. Give it these options, and delete its old ones:
   - `media_player.livingroom_ashers_echo_spot`
   - `media_player.kitchen_ashers_white_echo_pop`
   - `media_player.asherbedroomechodot`
   - `media_player.office_echo_dot`
   - `media_player.office_homepod_mini`
5. **The server pop-up.** Turn on the four [System Monitor](../dashboard/server/README.md#setup) sensors, and check that their entity IDs match the ones in that README.

## Create a dashboard

1. Open **Settings**, **Dashboards** and select **Add dashboard**, then **New dashboard from scratch**.
2. Enter the title from the table. Set the URL to the one in the table, because the menu's Portrait and Landscape buttons use it.
3. Open the dashboard and select the pencil, then **Take control** and **Start with an empty dashboard**.
4. In the three-dot menu, select **Raw configuration editor**. Replace everything with the file's contents and select **Save**.

The menu hides Home Assistant's header. To edit a dashboard later, select **Edit** in the menu, or add `?edit=1` to the address. On a tablet, the first button of the menu switches between the Landscape and the Portrait view.

## To check

These were chosen from the entity list alone, so a few may need a change in [`build.py`](build.py):

- **Duplicates.** Some devices have two entities with the same name. The dashboards use the one without `_2` at its end, such as `media_player.office_echo_dot` and `light.kitchen_sink_light`. If a card stays unavailable, the other one is the right one.
- **Light groups.** The living room and the office use `light.living_room_lights` and `light.office_lights`. If `light.livingroom_group` and `light.office_lightgroup` hold the right lamps instead, change `light` in those two rooms.
- **Windows.** The rooms header counts the four window contacts. They have no area in Home Assistant, so no room card and no row of the climate table shows a window yet.
- **Bedroom sensor.** Bedroom Temp Sensor is in the area Living Room in Home Assistant. The dashboards use it for the bedroom, as its name says.
- **TV.** The pop-up controls the Roku TV. `TV_APPS` has three app names as a start, and the names have to match the TV's `source_list` attribute under **Developer tools**, **States**.
- **Vacuum.** The pop-up has the state and the keys. The battery and the suction levels need the vacuum's battery sensor and its `fan_speed_list` attribute.
- **Fahrenheit.** The comparison weather card's bar goes from 14° to 95°. For Celsius, set `FAHRENHEIT = False`.
- **Left out.** The home has no fan, thermostat or timer in its entity list, so the fan pop-up, the thermostat cards and the timer favorite aren't there. `light.echo_lamp` and `light.h6004_2` have no area and are in no room.

"All lights off" turns off the lamps that `build.py` lists, not every light entity. The tablets' screens are lights in Home Assistant too, and they would go dark with the rest.

## Change something

A small change is quickest in the dashboard's own editor. A change for all four dashboards, such as a new lamp or room, goes into the first half of [`build.py`](build.py). Then build the files again and paste them again:

```bash
python3 my-dashboards/build.py
```

The script reads the parts from [`dashboard`](../dashboard), so the same command also brings in an Origami update. It needs Python with PyYAML.
