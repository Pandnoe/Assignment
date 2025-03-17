import streamlit as st
import json
from convert_data import convertData

def render_combined_map():
    # Load dengue cluster data
    with open("DengueClustersGEOJSON.geojson", "r") as f:
        clusters_data = json.load(f)
    clusters_json = json.dumps(clusters_data)
    
    # Load user report data (assuming convertData() returns GeoJSON-like data)
    reports_data = convertData()
    reports_json = json.dumps(reports_data)
    
    # Your Mapbox access token
    mapbox_access_token = "pk.eyJ1IjoicGFuZG5vZSIsImEiOiJjbTdraTc1ODUwMHdmMmtxMzZpMDhpYmJ0In0.7kqBiRPXUNAZLWrR3uoIGg"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8" />
    <title>Combined Map</title>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.css" rel="stylesheet" />
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
    <style>
        body {{ margin: 0; padding: 0; }}
        #container {{
        display: flex;
        flex-direction: column;
        }}
        #map {{
        height: 700px;
        }}
        #info {{
        padding: 10px;
        font-family: sans-serif;
        background-color: #fff;
        border: 1px solid #ccc;
        margin-top: 10px;
        min-height: 50px;
        height: auto;
        overflow-y: auto;
        }}
    </style>
    </head>
    <body>
    <div id="map"></div>
    <div id="info">Click on a feature for details.</div>

    <!-- Modal HTML for Report Table -->
    <div class="modal fade" id="caseDialog" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Dengue Reported Cases</h1>
            <button type="button" id="closeDialog" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="case-details">
            <!-- Table will be injected here -->
            </div>
            <div class="modal-footer">
            <!-- Optional footer content -->
            </div>
        </div>
        </div>
    </div>

    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        mapboxgl.accessToken = '{mapbox_access_token}';
        var map = new mapboxgl.Map({{
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v10',
        center: [103.8198, 1.3521],
        zoom: 12
        }});
        
        map.on('load', function() {{
        // Add dengue clusters (polygons)
        map.addSource('dengueClusters', {{
            'type': 'geojson',
            'data': {clusters_json}
        }});
        map.addLayer({{
            'id': 'clusters',
            'type': 'fill',
            'source': 'dengueClusters',
            'paint': {{
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
        
        // Add dengue reports (points)
        map.addSource('dengueReports', {{
            'type': 'geojson',
            'data': {reports_json}
        }});
        map.addLayer({{
            'id': 'reports',
            'type': 'circle',
            'source': 'dengueReports',
            'paint': {{
            'circle-radius': 8,
            'circle-color': '#AAFF00'
            }}
        }});
        
        // Click handler for clusters
        map.on('click', 'clusters', function(e) {{
            var feature = e.features[0];
            var props = feature.properties;
            document.getElementById('info').innerHTML = 
            "<strong>Cluster:</strong> " + props.LOCALITY +
            "<br><strong>Case Size:</strong> " + props.CASE_SIZE;
        }});
        
        // Click handler for reports to display the table in a modal
        map.on('click', 'reports', function(e) {{
            var cases = JSON.parse(e.features[0]['properties']['cases']);
            // Build table HTML with only the desired columns
            var tableHTML = "<table class='table table-striped table-bordered'>";
            tableHTML += "<thead><tr><th>Type</th><th>User</th><th>Date</th></tr></thead><tbody>";
            cases.forEach(function(item) {{
                tableHTML += "<tr>" +
                                "<td>" + item.Type + "</td>" +
                                "<td>" + item.username + "</td>" +
                                "<td>" + item.Date + "</td>" +
                            "</tr>";
            }});
            tableHTML += "</tbody></table>";
            document.getElementById('info').innerHTML = tableHTML;
        }});

        
        // Change cursor style on hover
        map.on('mouseenter', 'clusters', function() {{
            map.getCanvas().style.cursor = 'pointer';
        }});
        map.on('mouseleave', 'clusters', function() {{
            map.getCanvas().style.cursor = '';
        }});
        map.on('mouseenter', 'reports', function() {{
            map.getCanvas().style.cursor = 'pointer';
        }});
        map.on('mouseleave', 'reports', function() {{
            map.getCanvas().style.cursor = '';
        }});
        }});
    </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=1000)

