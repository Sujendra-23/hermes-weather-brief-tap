#!/usr/bin/env python3
"""weather-brief: keyless current weather + forecast from Open-Meteo (standard library only).

Usage:
  python3 weather.py "Los Angeles" [--days 3] [--celsius] [--json]
  python3 weather.py --lat 34.02 --lon -118.29 --label "USC" [--days 2]
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

WMO = {0: "clear", 1: "mainly clear", 2: "partly cloudy", 3: "overcast", 45: "fog", 48: "rime fog",
       51: "light drizzle", 53: "drizzle", 55: "heavy drizzle", 61: "light rain", 63: "rain", 65: "heavy rain",
       71: "light snow", 73: "snow", 75: "heavy snow", 80: "rain showers", 81: "heavy showers",
       82: "violent showers", 95: "thunderstorm", 96: "thunderstorm with hail", 99: "severe thunderstorm"}


def get(url, params):
    req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}",
                                 headers={"User-Agent": "hermes-weather-brief/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def geocode(name):
    hits = get("https://geocoding-api.open-meteo.com/v1/search",
               {"name": name, "count": 1, "language": "en", "format": "json"}).get("results") or []
    if not hits:
        sys.exit(f"location not found: {name}")
    h = hits[0]
    return h["latitude"], h["longitude"], ", ".join(x for x in (h.get("name"), h.get("admin1"), h.get("country_code")) if x), h.get("timezone", "auto")


def brief(high, low, rain, code, fahrenheit):
    hi = high if fahrenheit else high * 9 / 5 + 32
    lo = low if fahrenheit else low * 9 / 5 + 32
    wear = "heavy coat" if lo < 40 else "warm layer" if lo < 52 else "light jacket" if lo < 62 else "t-shirt weather"
    if hi > 88:
        wear += ", stay hydrated"
    wet = rain >= 50 or code in (61, 63, 65, 80, 81, 82, 95, 96, 99)
    return f"{wear}; {'bring an umbrella' if wet else 'no umbrella needed'}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("location", nargs="?", default="")
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    ap.add_argument("--label", default="")
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--celsius", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.lat is not None and a.lon is not None:
        lat, lon, label, tz = a.lat, a.lon, a.label or f"{a.lat},{a.lon}", "auto"
    elif a.location:
        lat, lon, label, tz = geocode(a.location)
    else:
        ap.error("give a location or --lat/--lon")
    f = not a.celsius
    d = get("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat, "longitude": lon, "timezone": tz, "forecast_days": max(1, min(a.days, 7)),
        "temperature_unit": "fahrenheit" if f else "celsius",
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max"})
    u = "°F" if f else "°C"
    cur, dl = d["current"], d["daily"]
    days = [{"date": dl["time"][i], "summary": WMO.get(dl["weather_code"][i], f"code {dl['weather_code'][i]}"),
             "high": round(dl["temperature_2m_max"][i]), "low": round(dl["temperature_2m_min"][i]),
             "rain_pct": dl["precipitation_probability_max"][i] or 0} for i in range(len(dl["time"]))]
    out = {"location": label, "unit": u, "now": {"temp": round(cur["temperature_2m"]),
                                                  "summary": WMO.get(cur["weather_code"], "n/a")},
           "days": days, "brief": brief(days[0]["high"], days[0]["low"], days[0]["rain_pct"],
                                        dl["weather_code"][0], f), "source": "open-meteo.com"}
    if a.json:
        print(json.dumps(out, indent=1))
        return
    print(f"{label}: now {out['now']['temp']}{u}, {out['now']['summary']}")
    for x in days:
        print(f"  {x['date']}: {x['summary']}, high {x['high']}{u} / low {x['low']}{u}, rain {x['rain_pct']}%")
    print(f"BRIEF: {out['brief']}")


if __name__ == "__main__":
    main()
