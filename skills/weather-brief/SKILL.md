---
name: weather-brief
description: Keyless weather now + multi-day forecast with a one-line "what to wear / bring" brief (Open-Meteo, no API key, stdlib-only script).
version: 1.0.0
author: Sujendra-23
license: MIT
metadata:
  hermes:
    tags: [weather, forecast, briefing, keyless]
    related_skills: [daily-briefing]
---

# Weather brief

Current conditions and a 1–7 day forecast for any city, plus a practical one-line brief ("light jacket,
no umbrella"). Uses the free Open-Meteo API — no account, no key, nothing to leak.

## When to Use
"What's the weather in Seattle?", "do I need an umbrella tomorrow?", "weekend forecast", or the weather line
of a morning briefing.

## Procedure
1. If a `weather_forecast` tool is available (the A3 assistant plugin provides one), call it and skip to step 3.
2. Otherwise run the bundled script from this skill's directory (Python 3.9+, standard library only):
   ```bash
   python3 scripts/weather.py "Los Angeles" --days 3            # Fahrenheit (default)
   python3 scripts/weather.py "Berlin" --days 2 --celsius
   python3 scripts/weather.py --lat 34.02 --lon -118.29 --label "USC" --json
   ```
   It prints a human-readable forecast (or JSON with `--json`) and ends with a `BRIEF:` line.
3. Reply with: current temp + condition, then one line per day (high/low, rain chance), then the brief.
   Mention the location you resolved, so the user can correct a wrong city match.

## Pitfalls
- Ambiguous city names resolve to the most populous match — include state/country when it matters.
- Network failure: report it; do not guess the weather.
- Rain chance is the daily maximum precipitation probability, not the chance it rains all day.

## Verification
`python3 scripts/weather.py "London" --days 1` prints `London, England, GB` and a `BRIEF:` line.
