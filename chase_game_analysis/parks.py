import overpy
import json
def get_spb_parks():
    api = overpy.Overpass()

    query = """
    [out:json][timeout:25];
    area["name"="Санкт-Петербург"]->.spb;
    (
        way["leisure"="park"]["name"](area.spb)(if:length()>1000);
        relation["leisure"="park"]["name"](area.spb);
    );
    out body;
    >;
    out skel qt;
    """

    result = api.query(query)
    parks = []

    for way in result.ways:
        name = way.tags.get('name')
        if name:
            center_lat = sum(float(node.lat) for node in way.nodes) / len(way.nodes)
            center_lon = sum(float(node.lon) for node in way.nodes) / len(way.nodes)
            
            if 59.8 <= center_lat <= 60.1 and 30.1 <= center_lon <= 30.7:
                park = {
                    'name': name,
                    'center': [center_lat, center_lon]
                }
                parks.append(park)

    # Save results to JSON file
    with open('spb_parks2.json', 'w', encoding='utf-8') as f:
        json.dump(parks, f, ensure_ascii=False, indent=2)

    return parks

if __name__ == "__main__":
    parks = get_spb_parks()
    print(f"Found {len(parks)} major parks within KAD in Saint Petersburg")
