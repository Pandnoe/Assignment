import streamlit as st
import json

def render_map():
    # Load the GeoJSON file
    with open("DengueClustersGEOJSON.geojson", "r") as f:
        geojson_data = json.load(f)

    # Convert the geojson data to a JSON string
    geojson_str = json.dumps(geojson_data)

    # Your Mapbox access token (replace with your own token)
    mapbox_access_token = "pk.eyJ1IjoicGFuZG5vZSIsImEiOiJjbTdraTc1ODUwMHdmMmtxMzZpMDhpYmJ0In0.7kqBiRPXUNAZLWrR3uoIGg"

    # HTML + JavaScript for a Mapbox GL JS map with data-driven styling
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Mapbox GL JS GeoJSON Example</title>
        <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
        <script src="https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.js"></script>
        <link href="https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.css" rel="stylesheet" />
        <style>
            body {{ margin: 0; padding: 0; }}
            #map {{ position: relative; height: 500px; }}
            #info {{
                padding: 10px;
                font-family: sans-serif;
                background-color: #fff;
                border: 1px solid #ccc;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
    <div id="map"></div>
    <div id="info">Click on an area on the map for details.</div>
    <script>
        mapboxgl.accessToken = '{mapbox_access_token}';
        var map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/light-v10',
            center: [103.8198, 1.3521],
            zoom: 12
        }});

        // Add the GeoJSON data as a source
        map.on('load', function() {{
            map.addSource('dengueClusters', {{
                'type': 'geojson',
                'data': {geojson_str}
            }});

            // Add a layer to display the polygons with data-driven fill color:
            map.addLayer({{
                'id': 'clusters',
                'type': 'fill',
                'source': 'dengueClusters',
                'layout': {{}},
                'paint': {{
                    // Interpolate CASE_SIZE from yellow (low) to red (high)
                    'fill-color': [
                        'interpolate',
                        ['linear'],
                        ['get', 'CASE_SIZE'],
                        0, 'yellow',
                        10, 'orange',
                        20, 'red'
                    ],
                    'fill-opacity': 0.6
                }}
            }});

            // Change the cursor to a pointer when hovering over the clusters
            map.on('mouseenter', 'clusters', function() {{
                map.getCanvas().style.cursor = 'pointer';
            }});

            map.on('mouseleave', 'clusters', function() {{
                map.getCanvas().style.cursor = '';
            }});

            // When a cluster is clicked, show details in the #info div
            map.on('click', 'clusters', function(e) {{
                var feature = e.features[0];
                var props = feature.properties;
                document.getElementById('info').innerHTML = 
                    "<strong>Description:</strong> " + props.LOCALITY + 
                    "<br><strong>Case Size:</strong> " + props.CASE_SIZE;
            }});
        }});
    </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=650)
