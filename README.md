# Hermes skill tap — `weather-brief`

A public [Hermes Agent skill tap](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
containing one original skill, **weather-brief**: keyless current weather + forecast + a one-line
"what to wear / bring" brief, using the free Open-Meteo API and a standard-library-only Python script.

Created for CSCI 599 Assignment 3 (advanced-integration option: custom skill published to a public GitHub
repository used as a Hermes skill tap).

## Install on any Hermes

```bash
hermes skills tap add Sujendra-23/hermes-weather-brief-tap
hermes skills search weather-brief
hermes skills install Sujendra-23/hermes-weather-brief-tap/skills/weather-brief   # install-time security scan runs
```

Then ask: *"What's the weather in Seattle for the next 3 days? Do I need an umbrella?"*

## Layout

```
skills/
└── weather-brief/
    ├── SKILL.md            # instructions + frontmatter
    └── scripts/weather.py  # stdlib-only Open-Meteo client (no key, no deps)
```

No credentials, personal data or machine-specific paths. License: MIT.
