#!/usr/bin/env python3
"""
Satellite imagery cost estimator.

Reads an area of interest (GeoJSON, KML or Shapefile), calculates its true
area in km2, applies minimum order rules and prints an estimated price for
each resolution tier, for archive and new tasking.

Prices are XRTech Group's published list prices in USD per km2
(https://xrtechgroup.com/buy-high-resolution-satellite-imagery/).
Always confirm the live price for your area before ordering.

Usage:
    python estimate_cost.py site.geojson
    python estimate_cost.py site.kml --stereo --cloud 10 --angle 15
"""

import argparse
import sys

import geopandas as gpd

# USD per km2: (archive, standard tasking)
TIERS = {
    "Standard 1m-2m": (1, 2),
    "High 51cm-80cm": (5, 8),
    "Very High 31cm-50cm": (13, 20),
    "Super High 25cm-30cm": (20, 30),
}

ARCHIVE_MIN_KM2 = 25
TASKING_MIN_KM2 = 100

# Optional surcharges, USD per km2
CLOUD_SURCHARGE = {10: 8, 5: 15}   # max cloud cover % -> extra
ANGLE_SURCHARGE = {15: 3, 10: 9}   # max off-nadir angle deg -> extra


def aoi_area_km2(path: str) -> float:
    """Return the area of all polygons in the file, in km2."""
    if path.lower().endswith(".kml"):
        gdf = gpd.read_file(path, driver="KML")
    else:
        gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    # Project to an equal-area CRS so the area is correct anywhere on Earth
    gdf = gdf.to_crs("ESRI:54009")  # World Mollweide
    return float(gdf.geometry.area.sum() / 1e6)


def estimate(area_km2: float, stereo: bool, cloud: int, angle: int):
    extra = CLOUD_SURCHARGE.get(cloud, 0) + ANGLE_SURCHARGE.get(angle, 0)
    factor = 2 if stereo else 1
    rows = []
    for tier, (archive, tasking) in TIERS.items():
        a_area = max(area_km2, ARCHIVE_MIN_KM2)
        t_area = max(area_km2, TASKING_MIN_KM2)
        a_cost = a_area * archive * factor
        t_cost = t_area * (tasking * factor + extra)
        rows.append((tier, a_area, a_cost, t_area, t_cost))
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("aoi", help="GeoJSON, KML or Shapefile with your area")
    p.add_argument("--stereo", action="store_true",
                   help="price stereo pairs (2x mono)")
    p.add_argument("--cloud", type=int, choices=[10, 5], default=None,
                   help="max cloud cover %% for tasking (adds a surcharge)")
    p.add_argument("--angle", type=int, choices=[15, 10], default=None,
                   help="max off-nadir angle for tasking (adds a surcharge)")
    args = p.parse_args(argv)

    area = aoi_area_km2(args.aoi)
    print(f"Area of interest: {area:,.2f} km2")
    if area < ARCHIVE_MIN_KM2:
        print(f"Below the {ARCHIVE_MIN_KM2} km2 archive minimum: "
              "price is based on the minimum area.")
    print()
    print(f"{'Tier':<22}{'Archive km2':>12}{'Archive USD':>13}"
          f"{'Tasking km2':>13}{'Tasking USD':>13}")
    for tier, a_area, a_cost, t_area, t_cost in estimate(
            area, args.stereo, args.cloud, args.angle):
        print(f"{tier:<22}{a_area:>12,.1f}{a_cost:>13,.0f}"
              f"{t_area:>13,.1f}{t_cost:>13,.0f}")
    print()
    print("List prices before volume discounts (from 250 km2).")
    print("Confirm your quote at https://buysatelliteimages.com/satellite-imagery-portal")
    return 0


if __name__ == "__main__":
    sys.exit(main())
