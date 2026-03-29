"""
Huixin Wu
Module 3: Interactive visual analytics and dashboard
Hands-on Lab: Interactive Visual Analytics with Folium
"""

import folium
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon

## Task 1: Mark all launch sites on a map
# define the world map
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library

#!pip3 install folium==0.5.0
import folium

print('Folium installed and imported!')

world_map = folium.Map()

# display world map

world_map.save("map.html")
print("Map saved as map.html")

# Download and read the `spacex_launch_geo.csv`
import pandas as pd

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"

spacex_df = pd.read_csv(URL)

print(spacex_df.head())

#Now, you can take a look at what are the coordinates for each site.
# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
print(launch_sites_df)

"""
Above coordinates are just plain numbers that can not give you any intuitive insights about where are those launch sites. If you are very good at geography, you can interpret those numbers directly in your mind. If not, that's fine too. Let's visualize those locations by pinning them on a map.
We first need to create a folium Map object, with an initial center location to be NASA Johnson Space Center at Houston, Texas.
"""

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

"""
We could use folium.Circle to add a highlighted circle area with a text label on a specific coordinate. For example,

"""

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

"""
and you should find a small yellow circle near the city of Houston and you can zoom-in to see a larger circle.

Now, let's add a circle for each launch site in data frame launch_sites

TODO: Create and add folium.Circle and folium.Marker for each launch site on the site map

An example of folium.Circle:

folium.Circle(coordinate, radius=1000, color='#000000', fill=True).add_child(folium.Popup(...))

An example of folium.Marker:

folium.map.Marker(coordinate, icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0), html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'label', ))
"""
# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
# Add a circle and marker for each launch site
for index, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    launch_site_name = row['Launch Site']
    
    # Add circle
    folium.Circle(
        coordinate,
        radius=1000,
        color='#d35400',
        fill=True
    ).add_child(folium.Popup(launch_site_name)).add_to(site_map)
    
    # Add marker with label
    folium.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html=f'<div style="font-size: 12; color:#d35400;"><b>{launch_site_name}</b></div>',
        )
    ).add_to(site_map)

# Save final map
site_map.save("spacex_launch_sites_map.html")

print("Map saved as spacex_launch_sites_map.html")

"""
Now, you can explore the map by zoom-in/out the marked areas , and try to answer the following questions:

Are all launch sites in proximity to the Equator line?
Are all launch sites in very close proximity to the coast?
Also please try to explain your findings.

# Task 2: Mark the success/failed launches for each site on the map
We will:

Use the full spacex_df (not grouped)
Color markers:
Green = Success (class = 1)
Red = Failure (class = 0)
Use MarkerCluster so the map stays clean
"""

# Create a new map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Add MarkerCluster
marker_cluster = MarkerCluster()
site_map.add_child(marker_cluster)

# Add launch outcome markers
for index, row in spacex_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    launch_site = row['Launch Site']
    outcome = row['class']
    
    # Choose marker color based on success/failure
    if outcome == 1:
        marker_color = 'green'
    else:
        marker_color = 'red'
    
    # Add marker to cluster
    marker_cluster.add_child(
        folium.Marker(
            location=coordinate,
            popup=f"Site: {launch_site}<br>Outcome: {'Success' if outcome == 1 else 'Failure'}",
            icon=folium.Icon(color=marker_color)
        )
    )

# Save the map
site_map.save("spacex_launch_outcomes_map.html")

print("Map saved as spacex_launch_outcomes_map.html")

"""
Next, let's try to enhance the map by adding the launch outcomes for each site, and see which sites have high success rates. Recall that data frame spacex_df has detailed launch records, and the class column indicates if this launch was successful or not
"""
print(spacex_df.tail(10))

"""
Next, let's create markers for all launch records. If a launch was successful (class=1), then we use a green marker and if a launch was failed, we use a red marker (class=0)

Note that a launch only happens in one of the four launch sites, which means many launch records will have the exact same coordinate. Marker clusters can be a good way to simplify a map containing many markers having the same coordinate.

Let's first create a MarkerCluster object
"""
marker_cluster = MarkerCluster()

"""
TODO: Create a new column in spacex_df dataframe called marker_color to store the marker colors based on the class value
# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
TODO: For each launch result in spacex_df data frame, add a folium.Marker to marker_cluster

"""
# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)
# Create marker_color column based on class
spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# For each launch record
for index, record in spacex_df.iterrows():
    
    coordinate = [record['Lat'], record['Long']]
    
    marker = folium.Marker(
        location=coordinate,
        popup=f"Launch Site: {record['Launch Site']}<br>Outcome: {'Success' if record['class']==1 else 'Failure'}",
        icon=folium.Icon(
            color='white',
            icon_color=record['marker_color']
        )
    )
    
    marker_cluster.add_child(marker)

# Save the final map
site_map.save("spacex_launch_outcomes_clustered.html")

print("Map saved as spacex_launch_outcomes_clustered.html")

"""
From the color-labeled markers in marker clusters, you should be able to easily identify which launch sites have relatively high success rates.

# TASK 3: Calculate the distances between a launch site to its proximities
Next, we need to explore and analyze the proximities of launch sites.

Let's first add a MousePosition on the map to get coordinate for a mouse over a point on the map. As such, while you are exploring the map, you can easily find the coordinates of any points of interests (such as railway)
"""
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)

"""
Now zoom in to a launch site and explore its proximity to see if you can easily find any railway, highway, coastline, etc. Move your mouse to these points and mark down their coordinates (shown on the top-left) in order to the distance to the launch site.
"""
#Step 1 — Select a Launch Site
# Get coordinate of a specific launch site CCAFS LC-40
launch_site_row = launch_sites_df[launch_sites_df['Launch Site'] == 'CCAFS LC-40']

launch_site_lat = launch_site_row.iloc[0]['Lat']
launch_site_lon = launch_site_row.iloc[0]['Long']

launch_coordinate = [launch_site_lat, launch_site_lon]

# Step 2 — Enter Closest Coastline Coordinate
coastline_lat = 28.56419
coastline_lon = -80.56811

coastline_coordinate = [coastline_lat, coastline_lon]

#Step 3 — Calculate Distance
from math import sin, cos, sqrt, atan2, radians
def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

distance_coastline = calculate_distance(
    launch_site_lat, launch_site_lon,
    coastline_lat, coastline_lon
)

print("Distance to coastline:", distance_coastline, "KM")

# Step 4 — Add Coastline Marker with Distance Label
distance_marker = folium.Marker(
    coastline_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>{:10.2f} KM</b></div>'.format(distance_coastline),
    )
)

site_map.add_child(distance_marker)
"""
TODO: Mark down a point on the closest coastline using MousePosition and calculate the distance between the coastline point and the launch site.
"""
# Step 5 — Draw PolyLine Between Points
lines = folium.PolyLine(
    locations=[launch_coordinate, coastline_coordinate],
    weight=2,
    color='blue'
)

site_map.add_child(lines)

"""
TODO: Draw a PolyLine between a launch site to the selected coastline point
"""
#Step 6 — Save Map (IMPORTANT for VS Code)
site_map.save("spacex_distance_analysis.html")
print("Map saved as spacex_distance_analysis.html")

"""
TODO: Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use MousePosition to find the their coordinates on the map first

"""
# Distance to Closest City
#Step 1 — Get Launch Site Coordinate:  Get coordinate of a specific launch site CCAFS LC-40
launch_site_row = launch_sites_df[launch_sites_df['Launch Site'] == 'CCAFS LC-40']

launch_site_lat = launch_site_row.iloc[0]['Lat']
launch_site_lon = launch_site_row.iloc[0]['Long']

launch_coordinate = [launch_site_lat, launch_site_lon]

# store the coordinates of the closest city
city_lat = 28.39222
city_lon = -80.60771

city_coordinate = [city_lat, city_lon]

# step 2: calculate the distance
distance_city = calculate_distance(launch_site_lat, launch_site_lon, city_lat, city_lon)

print("Distance to city:", distance_city, "KM")

# step 3: mark the distance in the map
city_distance_marker = folium.Marker(
    city_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:blue;"><b>{:10.2f} KM</b></div>'.format(distance_city),
    )
)

site_map.add_child(city_distance_marker)

# step 4: draw polyline
city_line = folium.PolyLine(
    locations=[launch_coordinate, city_coordinate],
    weight=2,
    color='green'
)

site_map.add_child(city_line)

# step 5: save the map
site_map.save("spacex_proximity_analysis.html")
print("Map saved as spacex_proximity_analysis.html")


"""
TODO: Similarly, you can draw a line betwee a launch site to its closest city, railway, highway, etc. You need to use MousePosition to find the their coordinates on the map first

"""
# Distance to railway
#Step 1 — Get Launch Site Coordinate:  Get coordinate of a specific launch site CCAFS LC-40
launch_site_row = launch_sites_df[launch_sites_df['Launch Site'] == 'CCAFS LC-40']

launch_site_lat = launch_site_row.iloc[0]['Lat']
launch_site_lon = launch_site_row.iloc[0]['Long']

launch_coordinate = [launch_site_lat, launch_site_lon]
#store the coordinates of the closest railway - Titan III road
railway_lat = 28.56383
railway_lon = -80.58684
railway_coordinate = [railway_lat, railway_lon]

# step 2: calculate the distance
distance_railway = calculate_distance(launch_site_lat, launch_site_lon, railway_lat, railway_lon)

print("Distance to railway:", distance_railway, "KM")

# step 3: mark the distance in the map
railway_distance_marker = folium.Marker(
    railway_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:magenta;"><b>{:10.2f} KM</b></div>'.format(distance_railway),
    )
)

site_map.add_child(railway_distance_marker)

# step 4: draw polyline
city_line = folium.PolyLine(
    locations=[launch_coordinate, railway_coordinate],
    weight=2,
    color='magenta'
)

site_map.add_child(city_line)

# step 5: save the map
site_map.save("spacex_proximity_analysis_railway.html")
print("Map saved as spacex_proximity_analysis_railway.html")

# DISTANCE TO HIGHWAY
#Step 1 — Get Launch Site Coordinate:  Get coordinate of a specific launch site CCAFS LC-40
launch_site_row = launch_sites_df[launch_sites_df['Launch Site'] == 'CCAFS LC-40']

launch_site_lat = launch_site_row.iloc[0]['Lat']
launch_site_lon = launch_site_row.iloc[0]['Long']

launch_coordinate = [launch_site_lat, launch_site_lon]
#store the coordinates of the closest highway - Samuel C. Phillis Parkway
highway_lat = 28.5625
highway_lon = -80.57069
highway_coordinate = [highway_lat, highway_lon]

# step 2: calculate the distance
distance_highway = calculate_distance(launch_site_lat, launch_site_lon, highway_lat, highway_lon)

print("Distance to highway:", distance_highway, "KM")

# step 3: mark the distance in the map
highway_distance_marker = folium.Marker(
    highway_coordinate,
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:orange;"><b>{:10.2f} KM</b></div>'.format(distance_highway),
    )
)

site_map.add_child(highway_distance_marker)

# step 4: draw polyline
city_line = folium.PolyLine(
    locations=[launch_coordinate, highway_coordinate],
    weight=2,
    color='orange'
)

site_map.add_child(city_line)

# step 5: save the map
site_map.save("spacex_proximity_analysis_highway.html")
print("Map saved as spacex_proximity_analysis_highway.html")