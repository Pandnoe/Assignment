import json



def displayMap():
    import streamlit as st
    from convert_data import convertData
    geoJson_str = json.dumps(convertData())
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
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
            <style>
            body {{
                margin: 0;
                padding: 0;
            }}

            #map {{
                position: absolute;
                top: 0;
                bottom: 0;
                width: 100%;
            }}
  
            </style>
    </head>
    <body>
    <div id="map"></div>
    <div class="modal fade" id="caseDialog" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Dengue Reported Cases</h1>
                <button type="button" id="closeDialog" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="case-details">
                
            </div>
            <div class="modal-footer">
            </div>
            </div>
        </div>
    </div>

    <script>
        mapboxgl.accessToken = '{mapbox_access_token}';
        var map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/light-v10',
            center: [103.8198, 1.3521],
            zoom: 12
        }});
        map.on('load', function() {{
            map.addSource('geojsonData', {{
                'type': 'geojson',
                'data': {geoJson_str}
            }});
            map.addLayer({{
                'id': 'geojsonLayer',
                'type': 'symbol',
                'source': 'geojsonData',
                'layout': {{
                    'icon-image': 'marker-15',  // Default Mapbox marker
                    'icon-size': 10.0,
                }},
                'filter': ['==', '$type', 'Point']  // Only show point features
            }});
 
            map.on('click', 'geojsonLayer', function(e) {{
                var modal = document.getElementById('caseDialog');
                var bootstrapModal = new bootstrap.Modal(modal); 
                bootstrapModal.show(); 

                var cases = JSON.parse(e.features[0]['properties']['cases'])
                var caseDetailsContainer = document.getElementById("case-details");
                caseDetailsContainer.innerHTML = '';  
                cases.forEach(function(e) {{
                    caseDetailsContainer.innerHTML += `
                <div class="card mb-4">
                 <div class="card-body">
                            <div class="row mb-3">
                                <div class="col-12">
                                    <h3 class="text-body-secondary">${{e.Type}}</h3>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-6">
                                    <h5 class="card-title">${{e.caseID}}</h5>
                                </div>
                                <div class="col-6 text-end">
                                    <h5 class="text-body-secondary">By: ${{e.userID}}</h5>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-12">
                                    <h5 class="card-title">${{e.Date}}</h5>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-12">
                                    <p class="card-text">${{e.Description}}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                        `;
                }})

                var closeButton = document.getElementById('closeDialog');
                closeButton.addEventListener('click', function(e) {{
                    bootstrapModal.hide();
                }})

            }});
        }});
        
       
    </script>
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    
    </body>
    </html>
    """
    st.components.v1.html(html, height=650)