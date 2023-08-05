import re
import copy
import time
import requests
import urllib.parse
import json as jsonlib
import numpy as np
import datetime


def tmap_get_coordinate(address, myAppKey):
    tmap_geocode_url = 'https://api2.sktelecom.com/tmap/geo/fullAddrGeo'
    params = {
        'addressFlag': 'F00',
        'coordType': 'WGS84GEO',
        'version': 1,
        'format': 'json',
        'appKey': myAppKey,  # 'l7xx027e9031ab64451d8cf04d76c2dcb8fc',
        'fullAddr': urllib.parse.quote(address),
    }
    resp = requests.get(tmap_geocode_url, params=params)
    status_code = resp.status_code

    if status_code != 200:
        return status_code, (-1., -1., -1., -1.)

    jsondata = jsonlib.loads(resp.text)
    coordinate = jsondata['coordinateInfo']['coordinate'][0]

    if coordinate['matchFlag']:
        lat = float(coordinate['lat'])
        lon = float(coordinate['lon'])
        lat2 = float(coordinate['latEntr'])
        lon2 = float(coordinate['lonEntr'])
    else:
        lat = float(coordinate['newLat'])
        lon = float(coordinate['newLon'])
        lat2 = float(coordinate['newLatEntr'])
        lon2 = float(coordinate['newLonEntr'])

    return status_code, (lat, lon, lat2, lon2)


def get_valid_tmap_data(df, myAppKey):
    address = np.array([re.sub(r'\([^)]*\)', '', a) for a in np.array(df['Address'])])
    name = np.array(df['Name'], dtype=str)

    coords = []
    valid_names, valid_ids, valid_addresses, valid_priority = [], [], [], []
    status_msg = ''

    for i, a in enumerate(address):
        status_code, tmap_coord = tmap_get_coordinate(a, myAppKey)

        if status_code == 200:
            coords.append(tmap_coord)
            valid_names.append(name[i])
            valid_ids.append(i)
            valid_addresses.append(a)
        elif status_code == 500:
            status_msg = str(status_code) + ' (TMAP Internal Server Error)'
        elif status_code == 400:
            status_msg += ' Invalid address ' + name[i]
        else:
            status_msg += ' Invalid address ' + name[i]

    return coords, valid_names, valid_ids, valid_addresses, status_msg


def get_tmap_dist_mat(coords, myAppKey, query_limit=30):
    query_num = len(coords) // query_limit
    if len(coords) % query_limit > 0: query_num += 1

    dist_mat = np.zeros((len(coords), len(coords)))
    duration_mat = np.zeros((len(coords), len(coords)))

    loc = []
    for lat, lon, lat2, lon2 in coords:
        loc.append({"lon": str(lon2), "lat": str(lat2)})

    url = "https://apis.openapi.sk.com/tmap/matrix?version=1"

    query_seq = 0
    for k in range(query_num):
        for l in range(query_num):
            origins = loc[k * query_limit: min((k + 1) * query_limit, len(coords))]
            destinations = loc[l * query_limit: min((l + 1) * query_limit, len(coords))]

            payload = {
                "origins": origins,
                "destinations": destinations,
                "metric": "Static"
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "appKey": myAppKey
            }

            # the results including distances are varing depending on the query time
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                return response.status_code, response.reason, None, None, None, None
            tmap_mat_rst = response.json()

            for r in tmap_mat_rst['matrixRoutes']:
                i, j = r['originIndex'], r['destinationIndex']
                i, j = (k * query_limit) + i, (l * query_limit) + j
                dist_mat[i, j] = r['distance']
                duration_mat[i, j] = r['duration']

            query_seq += 1
            time.sleep(1)  # because of the query limits per sec

    # to handle different start / end points
    adj_dist_mat, adj_duration_mat = copy.deepcopy(dist_mat), copy.deepcopy(duration_mat)

    adj_dist_mat[:, 0] = adj_dist_mat[:, -1]
    adj_dist_mat[0, 0] = 0
    adj_dist_mat = adj_dist_mat[:-1, :-1]

    adj_duration_mat[:, 0] = adj_duration_mat[:, -1]
    adj_duration_mat[0, 0] = 0
    adj_duration_mat = adj_duration_mat[:-1, :-1]

    return response.status_code, None, dist_mat, duration_mat, adj_dist_mat, adj_duration_mat


def postprocess(coords, route, start_time, via_time, myAppKey):
    via_points = []

    for idx, nid in enumerate(route[1:-1]):
        info = {
            "viaPointId": "via{}".format(idx),
            "viaPointName": "node{}".format(nid),
            "viaX": str(coords[nid][3]),
            "viaY": str(coords[nid][2]),
            "viaTime": str(via_time)
        }
        via_points.append(info)

    url = 'https://apis.openapi.sk.com/tmap/routes/routeSequential30?version=1&format=json'

    now = datetime.datetime.now()

    payload = {
        "reqCoordType": "WGS84GEO",
        "resCoordType": "WGS84GEO",
        "startName": "depot",
        "startX": str(coords[0][3]),
        "startY": str(coords[0][2]),
        "endName": "depot",
        "endX": str(coords[1][3]),
        "endY": str(coords[1][2]),
        "startTime": now.strftime('%Y%m%d') + start_time,
        "endPoiId": "",
        "searchOption": "0",
        "carType": "3",
        "viaPoints": via_points
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "appKey": myAppKey
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        tmap_route_rst = response.json()

        tmap_dist = tmap_route_rst['properties']['totalDistance']
        tmap_time = tmap_route_rst['properties']['totalTime']
        tmap_fare = tmap_route_rst['properties']['totalFare']

        return 200, None, tmap_dist, tmap_time, tmap_fare

    else:
        return response.status_code, response.reason, None, None, None

