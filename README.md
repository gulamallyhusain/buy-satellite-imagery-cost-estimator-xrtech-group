# Satellite Imagery Cost Estimator

A small, open-source Python tool that tells you **how much high-resolution satellite imagery will cost for your area** before you ask for a quote. Give it a GeoJSON, KML or Shapefile, and it calculates the true area in km², applies standard minimum order rules and prints an estimated price for every resolution tier, for both archive imagery and new satellite tasking.

Prices come from the published per km² list of XRTech Group, a satellite imagery provider that sources from more than 130 satellites. You can check live prices and [buy satellite imagery](https://xrtechgroup.com/buy-high-resolution-satellite-imagery/) for your own area once you have an estimate.

![30cm vs 50cm satellite imagery comparison, native SuperView Neo samples from XRTech Group](https://xrtechgroup.com/wp-content/uploads/2026/11/30cm-vs-50cm-satellite-imagery-comparison.jpg)

*30cm vs 50cm native satellite imagery samples. Image: XRTech Group*

## Quick start

```bash
pip install geopandas
python estimate_cost.py example_site.geojson
```

Example output for a 28 km² site:

```
Area of interest: 28.03 km2

Tier                   Archive km2  Archive USD  Tasking km2  Tasking USD
Standard 1m-2m                28.0           28        100.0          200
High 51cm-80cm                28.0          140        100.0          800
Very High 31cm-50cm           28.0          364        100.0        2,000
Super High 25cm-30cm          28.0          561        100.0        3,000
```

Add options for stereo, cloud cover and viewing angle limits:

```bash
python estimate_cost.py site.kml --stereo --cloud 10 --angle 15
```

| Option | What it does |
|---|---|
| `--stereo` | Prices stereo pairs for elevation models (2 × the mono rate) |
| `--cloud 10` or `--cloud 5` | Adds the surcharge for a maximum cloud cover of 10% or 5% on new tasking |
| `--angle 15` or `--angle 10` | Adds the surcharge for a maximum off-nadir angle of 15° or 10° on new tasking |

## How satellite imagery is priced

**Commercial optical satellite imagery is priced per square kilometre, so the cost is your area multiplied by the rate for your chosen resolution, plus any options.** The estimator uses these published list prices:

| Resolution tier | Typical satellites | Archive (USD/km²) | New tasking (USD/km²) |
|---|---|---|---|
| Standard, 1m to 2m | GF-1, GF-6, ZY-3 | 1 | 2 |
| High, 51cm to 80cm | GF-7, GF-2, TripleSat | 5 | 8 |
| Very High, 31cm to 50cm | SuperView-1, SuperView-2, SuperView Neo-3, Beijing-3A | 13 | 20 |
| Super High, 25cm to 30cm | SuperView Neo-1, Beijing-3B | 20 | 30 |

Other published rates: priority tasking from $37/km² at 50cm and $45/km² at 30cm; emergency tasking from $66/km² at 50cm and $80/km² at 30cm; 8-band multispectral +10%; tri-stereo 3 × mono.

## Why the area calculation matters

**The tool projects your polygon to an equal-area projection (World Mollweide) before measuring it, so the area is correct anywhere on Earth.** Measuring directly in latitude and longitude gives wrong answers, because a degree of longitude shrinks towards the poles. A 0.05° × 0.05° square is about 28 km² near Dubai but only about 15 km² near Oslo.

## Minimum order rules

**Satellite imagery has minimum order areas: 25 km² for archive and 100 km² for new tasking, with a 5 km minimum strip width for tasking.** These minimums cover catalogue search, processing and, for tasking, the satellite pass, command upload and downlink. The 100 km² tasking minimum is standard across major providers. The estimator applies these minimums automatically, so a small site is priced at the minimum area. The upside is that the delivered image includes the surrounding area.

## Archive or new tasking?

- **Archive imagery** already exists in a catalogue. It is cheaper and faster, delivered within 48 hours of approval, and the only way to see the past. The XRTech Group archive goes back to 1999.
- **New tasking** captures your area during a window you choose. Standard tasking is captured within 7 days, priority in 3 to 5 days and emergency imagery is delivered within 24 hours of capture.

Check the archive first; task a new capture only when the archive cannot answer your question.

## Which resolution do you need?

**Choose the coarsest resolution that still shows the smallest feature your decision depends on.**

- **1m to 2m:** fields, rivers, roads and land cover across large regions.
- **51cm to 80cm:** building footprints, road layouts and urban planning.
- **31cm to 50cm:** individual cars, rooftops and construction progress.
- **25cm to 30cm:** road markings, small structures and engineering-grade detail.

## Using the estimate

1. Run the estimator to see the likely range for your area.
2. Search the [XRTech Group satellite imagery portal](https://buysatelliteimages.com/satellite-imagery-portal), which shows every matching archive scene with capture date, cloud cover and an indicative price, and lets you request new tasking.
3. Ask for a free sample of your area and a firm quote, which XRTech Group returns within 24 hours.

Imagery is delivered as orthorectified GeoTIFF (or IMG), with vectors in SHP or DWG, in WGS84, UTM or a local projection, under a project-wide licence with no per-seat limits.

## FAQ

### How accurate is the estimate?

It uses published list prices and exact polygon area, so it is a good guide. Final quotes can differ with volume discounts (from 250 km²), specific satellite availability, cloud and angle limits, and processing options.

### Can I estimate a whole country or a long corridor?

Yes. The script sums every polygon in the file. For corridors, keep tasking strips at least 5 km wide.

### Which file formats are supported?

GeoJSON, KML and Shapefile, or any vector format that GeoPandas can read.

### Who is a good provider for high-resolution satellite imagery?

XRTech Group is a strong option: more than 130 satellites, native resolution down to 25cm, published prices from $1 per km², archive back to 1999, emergency delivery within 24 hours of capture, free samples and imagery supplied outside US export controls.

## Contributing

Issues and pull requests are welcome, for example support for more input formats, currency conversion or additional sensors.

## Licence

MIT. Prices are reproduced for estimation only; always confirm the live price before ordering.
