import copy
import datetime

import numpy as np
import pandas as pd
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from orderherosales.tmap_inerface import get_valid_tmap_data, get_tmap_dist_mat, postprocess


def _solve_tsp(data, timeout=10):
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    if timeout >= 10:
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_parameters.time_limit.seconds = timeout
        search_parameters.log_search = False

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        route = _get_routes_from_solution(data, solution, routing, manager)
        return 200, "Feasible", route
    else:
        return 204, "There is no valid route.", None


def _get_routes_from_solution(data, solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = [[] for _ in range(data['num_vehicles'])]

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            routes[vehicle_id].append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        routes[vehicle_id].append(manager.IndexToNode(index))

    return routes[0]


def find_route(raw_data,
               tmap_app_key,
               start_time: str = '0600',
               via_time: int = 600,
               opt_timeout: int = 10,
               duration_minimize: bool = False):
    group_ids = np.unique(raw_data['Group'])
    processed = copy.deepcopy(raw_data)
    arrivals, routes, fares, distances = [], [], [], []

    for g_id in group_ids:
        df = raw_data[raw_data['Group'] == g_id].sort_values('Type')
        coords, names, ids, addresses, rst_msg = get_valid_tmap_data(df, tmap_app_key)
        rst_code, rst_msg, distance, duration, asym_distance, asym_duration = get_tmap_dist_mat(coords, tmap_app_key)

        if rst_code != 200:
            print(rst_msg)
            return rst_code, rst_msg + ' (TMAP distance matrix error)', processed

        data = {}
        data['distance_matrix'] = asym_duration if duration_minimize else asym_distance
        data['num_vehicles'] = 1
        data['depot'] = 0

        rst_code, rst_msg, route = _solve_tsp(data, opt_timeout)

        if rst_code != 200:
            return rst_code, rst_msg + ' (No valid route)', processed

        rst_code, rst_msg, _, _, tot_fare = postprocess(coords, route, start_time, via_time, tmap_app_key)

        if rst_code != 200:
            return rst_code, rst_msg + ' (Postprocessing error)', processed

        # Calculate arrival time
        prev = datetime.datetime.strptime(datetime.datetime.now().strftime('%y%m%d') + start_time, '%y%m%d%H%M')
        arrival = [prev.strftime('%H:%M')]

        for d in asym_duration[route[:-1], route[1:]]:
            prev += datetime.timedelta(seconds=d)
            arrival.append(prev.strftime('%H:%M'))
            prev += datetime.timedelta(seconds=via_time)

        distances.append(asym_distance[route[:-1], route[1:]].sum() / 1000)

        route[-1] = len(route) - 1
        arrivals.extend(arrival)
        routes.append(route)
        fares.append(int(tot_fare))

    row_id = []
    prev_len = 0
    for r in routes:
        row_id.append(np.array(r) + prev_len)
        prev_len = len(r)

    row_id = np.concatenate(row_id)
    assert len(arrivals) == len(row_id)

    processed['Arrival'] = '0000'

    for r, a in zip(row_id, arrivals):
        processed.loc[r, 'Arrival'] = a

    processed = processed.sort_values(['Group', 'Arrival'])

    rst = {'processed_df': processed,
           'arrival_times': arrivals,
           'distances': distances,
           'fares': fares,
           'routes': routes}

    return rst


def save_results_to_csv(rst, fuel_cost, file_dir=".data/processed.csv"):
    processed = rst['processed_df']
    group_ids = np.unique(processed['Group'])

    processed.to_csv(file_dir, mode='w', index=False, encoding='utf-8-sig')

    df = pd.DataFrame()
    df.to_csv(file_dir, mode='a', index=False, encoding='utf-8-sig')

    df = pd.DataFrame({'Group': [g for g in group_ids],
                       'Last arrival': rst['arrival_times'],
                       'Total distance': rst['distances'],
                       'Total fare': rst['fares']})

    df['Fuel cost'] = df['Total distance'] * fuel_cost
    df['Total cost'] = df['Fuel cost'] + df['Total fare']

    df.to_csv(file_dir, mode='a', index=False, encoding='utf-8-sig')
