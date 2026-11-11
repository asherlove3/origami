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
3. **Three groups.** Under **Settings**, **Devices & services**, **Helpers**, create a **Group**, then **Light group**:
   - **Bedroom Lights**, so its entity ID is `light.bedroom_lights`, with Bedroom Dresser Lamp, Bedroom Strip Lights and Govee Bed Light Strip
   - **Basement Lights**, so its entity ID is `light.basement_lights`, with Basement Light Stairs and Basement Light Right Side

   Then create one more **Group**, this time a **Binary sensor group**, named **Living Room Windows**, so its entity ID is `binary_sensor.living_room_windows`. Add the Couch, Front Door, Stairs and Typewriter window sensors, and leave **All entities** off, so the group is open while any one window is open. The living room card and the climate table show it.
4. **The music pop-up.** Follow [its setup](../dashboard/music/README.md#setup) for the scripts **Playback** and **Set group volume** and the helper **Group volume**. The helper **Selected speaker** is there already. Give it these options, and delete its old ones:
   - `media_player.livingroom_ashers_echo_spot_2`
   - `media_player.kitchen_ashers_white_echo_pop_2`
   - `media_player.ashersbedroomechodot2`
   - `media_player.office_echo_dot_2`
   - `media_player.office_homepod_mini`
5. **The server pop-up.** Turn on the four [System Monitor](../dashboard/server/README.md#setup) sensors, and check that their entity IDs match the ones in that README.

## Create a dashboard

1. Open **Settings**, **Dashboards** and select **Add dashboard**, then **New dashboard from scratch**.
2. Enter the title from the table. Set the URL to the one in the table, because the menu's Portrait and Landscape buttons use it.
3. Open the dashboard and select the pencil, then **Take control** and **Start with an empty dashboard**.
4. In the three-dot menu, select **Raw configuration editor**. Replace everything with the file's contents and select **Save**.

The menu hides Home Assistant's header. To edit a dashboard later, select **Edit** in the menu, or add `?edit=1` to the address. On a tablet, the first button of the menu switches between the Landscape and the Portrait view.

## Checked in Home Assistant

These were checked in Home Assistant 2026.11.1. Change [`build.py`](build.py) if something in the home changes:

- **Speakers.** Each Echo has two entities: one from Alexa Devices and one from Alexa Media Player. The dashboards use the Alexa Media Player ones, such as `media_player.office_echo_dot_2` and `media_player.ashersbedroomechodot2`, because only they can play, pause and skip. Neither kind of Echo can join a speaker group. The HomePod can.
- **Lamps.** The kitchen sink light and the dresser lamp each have a Matter entity and a Govee entity (`_2`). The dashboards use the Matter ones.
- **Light groups.** `light.living_room_lights` holds all four living room lamps and `light.office_lights` all five office lamps, so the dashboards use them. `light.livingroom_group` and `light.office_lightgroup` hold only two lamps each.
- **Windows.** All four window contacts are in the living room. The rooms header counts them one by one, and the living room card and the climate table show the **Living Room Windows** group while one is open.
- **Bedroom sensor.** Bedroom Temp Sensor is in the area Bedroom.
- **TV.** The app row has Netflix, YouTube, Prime Video, Hulu, Disney+, HBO Max and Fire TV, which is the HDMI ARC input the Fire TV is on. Each matches a name in the Roku's `source_list`, and Disney+ is called Disney Plus there. `TV_APPS` keeps both names.
- **Vacuum.** The pop-up has the state, the battery from `sensor.kitchen_eufy_robovac_battery`, the keys and the eight cleaning modes of `select.kitchen_eufy_robovac_clean_mode`, with shorter names. The vacuum has no `fan_speed_list`, so there's no suction row.
- **Fahrenheit.** The home uses °F, so the comparison weather card's bar goes from 14° to 95°.
- **Basement.** Basement Light Right Side was unavailable during the check, so its tile stays grey until it's back online.
- **Left out.** The home has no fan, thermostat or timer in its entity list, so the fan pop-up, the thermostat cards and the timer favorite aren't there. `light.echo_lamp` and `light.h6004_2` have no area and are in no room.

## To look at later

- **Echos in a speaker group through Music Assistant.** Neither Alexa integration can group the Echos, so the music pop-up can only group the HomePod. Music Assistant has an Alexa provider, and Music Assistant players can join groups. To find out: does the provider see all four Echos, do they play in sync with each other and with the HomePod, and does Music Assistant's sign-in to Amazon hold up. If it works, the music pop-up would use the Music Assistant players instead.

"All lights off" turns off the lamps that `build.py` lists, not every light entity. The tablets' screens are lights in Home Assistant too, and they would go dark with the rest.

## Change something

A small change is quickest in the dashboard's own editor. A change for all four dashboards, such as a new lamp or room, goes into the first half of [`build.py`](build.py). Then build the files again and paste them again:

```bash
python3 my-dashboards/build.py
```

The script reads the parts from [`dashboard`](../dashboard), so the same command also brings in an Origami update. It needs Python with PyYAML.
