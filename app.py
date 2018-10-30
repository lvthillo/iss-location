from requests.exceptions import HTTPError

import requests
import folium
import webbrowser
import os

API_KEY = '<YOUR-API-KEY>'


def get_iss_position():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']
    return latitude, longitude


def convert_coordinates_to_place(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?key=%slatlng=%s,%s&sensor=false" % (API_KEY, lat, lng)

    try:
        r = requests.get(url)
        r.raise_for_status()
    except HTTPError:
        print('Could not get data from %s\nMaybe check your API_KEY' % r.url)
    j = r.json()
    try:
        address = j['results'][0]['formatted_address']
        return "<b>Location</b>: %s<br><b>Latency</b>: %s<br><b>Longitude</b>: %s" % (address, lat, lng)
    except IndexError:
        return "<b>Location</b>: Unknown<br><b>Latency</b>: %s<br><b>Longitude</b>: %s" % (lat, lng)


def draw_map(lat, lng):
    map = folium.Map(location=[float(lat), float(lng)], tiles='Stamen Terrain', zoom_start=4)
    text = folium.Html(convert_coordinates_to_place(lat, lng), script=True)
    popup = folium.Popup(text, max_width=2650)
    folium.Marker(location=[float(lat), float(lng)], popup=popup,).add_to(map)
    map.save('map.html')


def open_map():
    lat, lng = get_iss_position()
    draw_map(lat, lng)
    path = os.path.abspath('map.html')
    url = 'file://' + path
    webbrowser.open(url)


if __name__ == "__main__":
    open_map()
