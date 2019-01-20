import pandas
import folium

output_file = 'Map1.html'
volcanoes_data = 'Volcanoes.txt'
polygons_data = 'world.json'

def get_marker_color(elevation):
    if   elevation > 3000: return 'red'
    elif elevation > 2000: return 'orange'
    elif elevation > 1000: return 'green'
    else: return 'blue'

def add_markers(fg, file_name, lat_col_name, lon_col_name, popup_info_col_name, elevation_col_name, use_circle_marker=False):
    '''
    Adds markers from information in a csv file
    INPUTS:
        fg - feature group to which markers are being added
        file_name - name of csv file containing data for markers
        lat_col_name - name of column containing latitude data
        lon_col_name - name of column containing longitude data
        popup_info_col_name - name of column containing popup data
        elevation_col_name - name of column containing elevation data
        use_circle_marker - True=CircleMarker, False=Marker
    '''
    try:
        df = pandas.read_csv(file_name)
        lats = list(df[lat_col_name])
        lons = list(df[lon_col_name])
        names = list(df[popup_info_col_name])
        elevs = list(df[elevation_col_name])
    except:
        print(f'Problem reading data from {file_name}.')
        print(f'No markers added.  Please check file and column names.')
        return

    # Loop through lists using same index to add markers to feature group
    for lat, lon, name, elev in zip(lats, lons, names, elevs):
        name = name + ' (' + str(elev) + 'm)'
        if use_circle_marker:
            fg.add_child(folium.CircleMarker(location=[lat, lon], 
                                            popup=name,
                                            radius=10,
                                            fill=True, 
                                            fill_color=get_marker_color(elev), 
                                            color='grey', 
                                            fill_opacity=0.7))
        else:
            fg.add_child(folium.Marker(location=[lat, lon], 
                                       popup=name, 
                                       icon=folium.Icon(color=get_marker_color(elev))))
    return fg

if __name__ == "__main__":
    map = folium.Map(location=[32.772, -117.197],
                     zoom_start=5, 
                     tiles="Mapbox Bright")

    # Mark Volcanoes
    fg = folium.FeatureGroup(name='Volcanoes')
    add_markers(fg=fg, 
                file_name=volcanoes_data, 
                lat_col_name='LAT', 
                lon_col_name='LON', 
                popup_info_col_name='NAME', 
                elevation_col_name='ELEV',
                use_circle_marker=False)
    map.add_child(fg)
    print('.../Volcano marker feature group added.')

    # Add Polygons to color countries by population
    fg = folium.FeatureGroup(name='Polygons')
    fg.add_child(folium.GeoJson(data=open(polygons_data, 'r', 
                                encoding='utf-8-sig').read(),
                                style_function=lambda x: {
                                    'fillColor': 'red' if x['properties']['POP2005'] > 20000000
                                    else 'orange' if x['properties']['POP2005'] > 10000000 
                                    else 'green'}))
    map.add_child(fg)
    print('.../Polygons feature group added.')

    map.add_child(folium.LayerControl())

    map.save(output_file)
    print(f'.../{output_file} created.')

    print('Done.')