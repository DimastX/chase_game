import overpy
import json
import requests
from statistics import mean
from datetime import datetime
from typing import Tuple, Dict

MIN_TIME_MINUTES = 45
MAX_TIME_MINUTES = 90
API_KEY = "95a541dc-65c4-4ab9-8e23-53853faa0336"

class ParkRouter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = f"https://routing.api.2gis.com/public_transport/6.0.0/global?key={api_key}"
    
    def get_routes(self, start: Tuple[float, float], end: Tuple[float, float]) -> Dict:
        data = {
            "locale": "ru",
            "source": {
                "name": "Start Point",
                "point": {
                    "lat": start[0],
                    "lon": start[1]
                }
            },
            "target": {
                "name": "End Point",
                "point": {
                    "lat": end[0],
                    "lon": end[1]
                }
            },
            "transport": ["bus", "tram", "trolleybus"],
            "max_result_count": 5  # Request up to 5 different routes
        }
        
        response = requests.post(self.base_url, json=data)
        routes = parse_2gis_response(response.content)
        print_route_info(routes)
        return routes

def parse_2gis_response(response_data):
    data = json.loads(response_data.decode('utf-8'))
    
        
    # Print full API response
    # print("Full API Response:")
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    
    if not data or len(data) == 0:
        return None
        
    routes = []
    for route in data:
        route_info = {
            'id': route['id'],
            'время_в_пути_мин': round(route['total_duration'] / 60),
            'пересадок': route['transfer_count'],
            'переходов': route['crossing_count'],
            'пешком': route['total_walkway_distance'],
            'транспорт': []
        }
        
        for movement in route['movements']:
            if movement.get('routes'):
                for r in movement['routes']:
                    transport_info = {
                        'тип': r['subtype_name'],
                        'номер': r['names'][0],
                        'время': round(movement['moving_duration'] / 60),
                        'остановки': movement.get('platforms', {}).get('names', [])
                    }
                    route_info['транспорт'].append(transport_info)
            
        routes.append(route_info)
    
    return routes


def get_spb_parks():
    api = overpy.Overpass()

    query = """
    [out:json][timeout:25];
    area["name"="Санкт-Петербург"]->.spb;
    (
        way["leisure"="park"](area.spb);
        relation["leisure"="park"](area.spb);
    );
    out body;
    >;
    out skel qt;
    """

    result = api.query(query)
    parks = []

    for way in result.ways:
        name = way.tags.get('name')
        if name:  # Only process parks with names
            # Calculate center coordinates
            center_lat = mean(float(node.lat) for node in way.nodes)
            center_lon = mean(float(node.lon) for node in way.nodes)
            
            park = {
                'name': name,
                'center': [center_lat, center_lon]
            }
            parks.append(park)

    # Save results to JSON file
    with open('spb_parks.json', 'w', encoding='utf-8') as f:
        json.dump(parks, f, ensure_ascii=False, indent=2)

    return parks
def find_routes_to_park():
    # lat = float(input("Введите широту (например, 59.927067): "))
    # lon = float(input("Введите долготу (например, 30.320826): "))
    lat = 59.957010
    lon = 30.229490
    start_point = (lat, lon)
    
    with open('spb_parks_self.json', 'r', encoding='utf-8') as f:
        parks = json.load(f)
    
    print("\nДоступные парки:")
    for i, park in enumerate(parks, 1):
        print(f"{i}. {park['name']}")
    
    park_number = int(input("\nВведите номер парка: ")) - 1
    selected_park = parks[park_number]
    end_point = tuple(selected_park['center'])
    
    router = ParkRouter(API_KEY)
    print(f"\nСтроим маршруты до парка: {selected_park['name']}")
    routes = router.get_routes(start_point, end_point)
    print_route_info(routes)

def print_route_info(routes):
    print("\nДоступные маршруты:")
    for route in routes:
        print(f"\nМаршрут {route['id']}:")
        print(f"Время в пути: {route['время_в_пути_мин']} минут")
        print(f"Количество пересадок: {route['пересадок']}")
        print(f"Расстояние пешком: {route['пешком']}")
        
        if route['транспорт']:
            print("\nТранспорт:")
            current_stops = None
            alternatives = []
            
            for t in route['транспорт']:
                if current_stops and t['остановки'] == current_stops:
                    alternatives.append(f"{t['тип'].upper()} №{t['номер']}")
                else:
                    if alternatives:
                        print("Альтернативные маршруты:", " или ".join(alternatives))
                        alternatives = []
                    
                    print(f"\n{t['тип'].upper()} №{t['номер']}: {t['время']} минут")
                    print(f"Количество остановок: {len(t['остановки'])}")
                    print(f"Остановки: {', '.join(t['остановки'])}")
                    current_stops = t['остановки']
                    
            if alternatives:
                print("Альтернативные маршруты:", " или ".join(alternatives))



def find_routes_to_parks():
    lat = float(input("Введите широту (например, 59.927067): "))
    lon = float(input("Введите долготу (например, 30.320826): "))
    start_point = (lat, lon)
    
    router = ParkRouter(API_KEY)
    park_routes = []
    
    with open('spb_parks_self.json', 'r', encoding='utf-8') as f:
        parks = json.load(f)
    
    print("\nАнализируем маршруты до парков...")
    
    for park in parks:
        end_point = tuple(park['center'])
        route_info = router.get_routes(start_point, end_point)
        
        travel_time = route_info['время_в_пути_мин']
        if MIN_TIME_MINUTES <= travel_time <= MAX_TIME_MINUTES:
            park_routes.append({
                'название': park['name'],
                'время': travel_time,
                'пересадки': route_info['пересадок'],
                'пешком': route_info['пешком'],
                'транспорт': [f"{route['тип']} {','.join(route['номера'])}" for route in route_info['маршруты']]
            })
    
    # Sort by travel time
    park_routes.sort(key=lambda x: x['время'])
    
    print("\nПодходящие маршруты до парков:")
    print("=" * 80)
    for route in park_routes:
        print(f"\nПарк: {route['название']}")
        print(f"Время в пути: {route['время']} минут")
        print(f"Количество пересадок: {route['пересадки']}")
        print(f"Пешком: {route['пешком']}")
        print(f"Транспорт: {' | '.join(route['транспорт'])}")
        print("-" * 80)
    
    print(f"\nНайдено {len(park_routes)} подходящих маршрутов")


if __name__ == "__main__":
    # parks = get_spb_parks()
    # print(f"Found {len(parks)} named parks in Saint Petersburg")
    
    while True:
        action = input("\nВыберите действие:\n1. Построить маршрут до парка\n2. Выйти\n")
        if action == "1":
            find_routes_to_park()
        elif action == "2":
            break
