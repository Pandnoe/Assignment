def convertData():
    from database import showDengueReports
    reports = showDengueReports()
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    if reports is not None:
        for report in reports:
            currentCoord = [float(report["longitude"]), float(report["latitude"])]
            existed = False
            for feature in geojson["features"]:
                if currentCoord == feature["geometry"]["coordinates"]:
                    existed = True
                    feature["properties"]["cases"].append(
                            {
                                "caseID": report["id"],
                                "userID": report["user_id"],
                                "Description": report["description"],
                                "Type" : report["report_type"],
                                "Date" : report["date"]
                    })
                    break
            if not existed:
                feature = {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": currentCoord
                                },
                                "properties": {
                                    "cases" : [
                                    {
                                    "caseID": report["id"],
                                    "userID": report["user_id"],
                                    "Description": report["description"],
                                    "Type" : report["report_type"],
                                    "Date" : report["date"]
                                    }
                                    ]
                                }    
                        }
                geojson["features"].append(feature)
  
    return geojson










        