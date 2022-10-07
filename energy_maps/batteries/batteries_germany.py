import folium
import pandas as pd


# data source: Marktstammdatenregister
# https://www.marktstammdatenregister.de/MaStR/Einheit/Einheiten/ErweiterteOeffentlicheEinheitenuebersicht
# Lead: "Batterietechnologie entspricht Blei-Batterie" AND "Nettonennleistung der Einheit größer als 950"
# Li-Ion: "Batterietechnologie entspricht Hochtemperaturbatterie" AND "Nettonennleistung der Einheit größer als 950"
# Heat: "Batterietechnologie entspricht Lithium-Batterie" AND "Nettonennleistung der Einheit größer als 950"
# other techs were too small for the filter
# download as .csv ...


techs = [
    {"filename": "./data/storage_heat.csv", "name": "High-temperature", "color": "#a32727"},
    {"filename": "./data/storage_lead.csv", "name": "Lead", "color": "#525354"},
    {"filename": "./data/storage_liion.csv", "name": "Li-Ion", "color": "#8541f2"},
]


def popup_text(mastr_id, storage_unit, technology_name):
    return (
        f"<b>Name:</b> {storage_unit['Anzeige-Name der Einheit']}<br>"
        f"<b>Status:</b> {storage_unit['Betriebs-Status']}<br>"
        f"<b>Rated Power:</b> {round(storage_unit['Nettonennleistung der Einheit']/1000, 1)} MW<br>"
        f"<b>E/P:</b> {round(storage_unit['E_to_P'], 1)}<br>"
        f"<b>Operator:</b> {storage_unit['Name des Anlagenbetreibers (nur Org.)']}<br>"
        f"<b>Technology:</b> {technology_name}<br>"
        f"<b>MaStR key:</b> {mastr_id}"
    )


def prepare_data():
    """
    drops projects from abroad (e.g. LU, AT) and without location
    drops erroneous household projects
    drops decommissioned projects
    renames some German lingo
    """

    data = pd.read_csv(tech["filename"], header=0, sep=";", decimal=",", index_col=0)
    data.dropna(subset=["Bundesland"], inplace=True)
    data.dropna(subset=["Koordinate: Breitengrad (WGS84)"], inplace=True)
    data.dropna(subset=["Koordinate: Breitengrad (WGS84)"], inplace=True)
    data = data[~data["Name des Anlagenbetreibers (nur Org.)"].str.contains("natürliche", na=False)]
    data = data[data["Betriebs-Status"] != "Endgültig stillgelegt"]
    data.replace("In Betrieb", "in operation", inplace=True)
    data.replace("In Planung", "in planning", inplace=True)
    data.replace("Vorläufig stillgelegt", "temperarily mothballed", inplace=True)
    data['E_to_P'] = data["Nutzbare Speicherkapazität in kWh"] / data["Nettonennleistung der Einheit"]
    return data


def plot_battery_locations(map):
    for idx, item in data.iterrows():
        folium.Circle(
            location=[
                item["Koordinate: Breitengrad (WGS84)"],
                item["Koordinate: Längengrad (WGS84)"],
            ],
            radius=item["Nettonennleistung der Einheit"],
            popup=folium.Popup(
                html=popup_text(idx, item, tech["name"]), max_width="500"
            ),
            color=tech["color"],
            fill_color=tech["color"],
            fill=True,
        ).add_to(map)


if __name__ == '__main__':
    battery_map = folium.Map(location=[51.2, 10], zoom_start=6)
    for tech in techs:
        data = prepare_data()
        plot_battery_locations(battery_map)
    battery_map.save("battery_map_germany.html")
