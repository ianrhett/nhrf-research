#!/usr/bin/env python3
import json, csv, sys, urllib.request
from shapely.geometry import shape
from shapely.ops import transform, unary_union
from pyproj import Transformer

FOREST = "https://services.arcgis.com/QVENGdaPbd4LUkLV/arcgis/rest/services/Nashvilles_Highland_Rim_Forest/FeatureServer/1/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
DISTRICTS = "https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/2022_Council_Districts_(Future)_view/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson"
POOL = {1, 3, 10, 22, 23, 34, 35}
POOL_DOLLARS = 800000
ACRE_M2 = 4046.8564224

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req))

tr = Transformer.from_crs("EPSG:4326", "EPSG:5070", always_xy=True).transform
forest = transform(tr, unary_union([shape(x["geometry"]) for x in fetch(FOREST)["features"]])).buffer(0)
total = forest.area / ACRE_M2
rows = []
for x in fetch(DISTRICTS)["features"]:
    p = x["properties"]
    g = transform(tr, shape(x["geometry"])).buffer(0)
    acres = g.intersection(forest).area / ACRE_M2
    if acres >= 40:
        rows.append((int(p["DISTRICT"]), p["Representative"], acres, g.area / ACRE_M2))
rows.sort(key=lambda r: -r[2])
pool_acres = sum(r[2] for r in rows if r[0] in POOL)
out = csv.writer(sys.stdout)
out.writerow(["district", "representative", "forest_acres", "pct_of_forest", "pct_of_district", "share_of_pool_pct", "raw_dollars"])
for d, rep, ac, da in rows:
    share = ac / pool_acres if d in POOL else 0
    out.writerow([d, rep, round(ac), f"{100*ac/total:.1f}", f"{100*ac/da:.0f}", f"{100*share:.1f}" if share else "", round(POOL_DOLLARS * share) if share else ""])
out.writerow(["forest_total_acres", "", round(total), "", "", "", ""])
