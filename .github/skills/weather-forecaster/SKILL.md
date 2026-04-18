---
name: weather-forecaster
description: Retrieves current conditions and multi-day forecasts for any location, formatted for human or downstream agent consumption. Invoke when asked about the weather, current conditions, temperature, forecast, rain chance, or climate for any location.
---

# Weather Forecaster

Retrieves and presents current weather conditions and multi-day forecasts for any location worldwide, formatted clearly for humans or structured for downstream agent consumption in workflows such as event planning, travel logistics, or agricultural decisions.

## When to Use

- User asks "what's the weather in [city]?" or "will it rain tomorrow?"
- A travel itinerary needs weather context for the destination and dates
- An outdoor event needs a weather risk assessment
- A workflow requires current conditions as a data input (e.g., logistics, agriculture, outdoor safety)
- User asks for a weather comparison between multiple cities
- A multi-day trip requires day-by-day forecast for route planning
- User wants weather history for a past date at a specific location

## Process

1. **Resolve the location**:
   - Accept: city name, airport code, ZIP/postal code, coordinates (lat/lon), or landmark
   - Disambiguate common names: "Springfield" → ask which state/country, or infer from context
   - Convert to precise coordinates for API lookup
   - For multiple locations, process each in parallel

2. **Determine the request type**:
   - **Current conditions**: temperature, feels-like, humidity, wind speed/direction, visibility, UV index, precipitation (last hour), weather description
   - **Hourly forecast**: next 24–48 hours, hour by hour
   - **Daily forecast**: next 1–10 days (default 7 days), with high/low, precipitation probability, and summary
   - **Weather alerts**: active warnings, watches, or advisories for the area
   - **Extended outlook**: 14-day trend, useful for planning

3. **Retrieve weather data**:
   - Query a weather API (e.g., OpenWeatherMap, WeatherAPI, Open-Meteo, or NWS for US locations)
   - Capture: timestamp of data retrieval, data source, and forecast model used
   - For historical data: use historical weather dataset endpoints

4. **Format for the audience**:
   - **Human-readable**: use natural language, local units (°F or °C based on location/user preference), and contextual descriptions
   - **Machine/agent consumption**: return structured JSON with standardized units and field names
   - Always include the local time and time zone for the location

5. **Add contextual interpretation**:
   - Translate raw numbers into plain-language guidance: "Feels like 98°F — heat advisory in effect; limit outdoor exposure"
   - Flag extreme weather: temperatures >100°F/38°C, wind >40 mph/64 kph, precipitation >1"/25mm per hour, severe storm alerts
   - For travel or event planning: classify each day as Good / Marginal / Risky for outdoor activities
   - Sunset/sunrise times when relevant for planning

6. **Handle special cases**:
   - No data available: note the gap and suggest the nearest available location
   - Extreme precision requests ("exact rain at 3 PM") → explain forecast uncertainty and provide probability
   - Mountain or coastal locations: note orographic effects, sea breeze, or elevation-based temperature adjustments

## Output Format

### Current Conditions (Human)
```
🌤 Weather in San Francisco, CA
As of June 1, 2025 · 2:30 PM PDT

Temperature: 68°F (20°C) · Feels like: 65°F
Sky: Partly cloudy
Wind: WSW at 12 mph
Humidity: 72%
Visibility: 10 miles
UV Index: 5 (Moderate)
Precipitation last hour: None

No active weather alerts.
```

### 7-Day Forecast
```
📅 7-Day Forecast — San Francisco, CA

Mon Jun 2  | ⛅ Partly Cloudy     | High: 70°F · Low: 55°F | Rain: 10%
Tue Jun 3  | 🌧 Showers           | High: 63°F · Low: 52°F | Rain: 75%
Wed Jun 4  | 🌧 AM Rain, PM Clear | High: 65°F · Low: 53°F | Rain: 40%
Thu Jun 5  | ☀️ Sunny              | High: 72°F · Low: 54°F | Rain: 5%
Fri Jun 6  | ☀️ Sunny              | High: 75°F · Low: 56°F | Rain: 5%
Sat Jun 7  | ⛅ Partly Cloudy     | High: 71°F · Low: 55°F | Rain: 15%
Sun Jun 8  | ☀️ Sunny              | High: 74°F · Low: 57°F | Rain: 5%
```

### Structured JSON (Agent Consumption)
```json
{
  "location": { "name": "San Francisco, CA", "lat": 37.7749, "lon": -122.4194, "timezone": "America/Los_Angeles" },
  "retrieved_at": "2025-06-01T21:30:00Z",
  "current": {
    "temp_f": 68, "temp_c": 20, "feels_like_f": 65,
    "description": "Partly Cloudy", "humidity_pct": 72,
    "wind_mph": 12, "wind_direction": "WSW",
    "uv_index": 5, "visibility_miles": 10,
    "alerts": []
  },
  "daily": [
    { "date": "2025-06-02", "high_f": 70, "low_f": 55, "description": "Partly Cloudy", "precip_probability_pct": 10 },
    { "date": "2025-06-03", "high_f": 63, "low_f": 52, "description": "Showers", "precip_probability_pct": 75 }
  ]
}
```

## Examples

### Example Input
```
What's the weather going to be like in London for the next 5 days? I'm planning an outdoor event on Saturday.
```

### Example Output
```
📅 5-Day Forecast — London, UK (all times BST)

Mon Jun 2  | ⛅ Cloudy            | High: 18°C · Low: 12°C | Rain: 20%
Tue Jun 3  | 🌧 Rain              | High: 14°C · Low: 10°C | Rain: 85%
Wed Jun 4  | 🌦 Scattered Showers | High: 16°C · Low: 11°C | Rain: 55%
Thu Jun 5  | ⛅ Partly Cloudy     | High: 19°C · Low: 12°C | Rain: 25%
Fri Jun 6  | ☀️ Sunny              | High: 22°C · Low: 13°C | Rain: 10%
Sat Jun 7  | ☀️ Mostly Sunny      | High: 23°C · Low: 14°C | Rain: 15%

🎉 Saturday Outlook: Good conditions for an outdoor event — mostly sunny, 23°C, only 15% chance of rain. Wind: light at 8 mph. Recommend having a backup plan for afternoon as light showers remain possible.
```

## Boundaries

- Weather forecasts are probabilistic — always communicate uncertainty, especially beyond 5 days.
- Do NOT present forecast data as guaranteed or make high-stakes recommendations based on weather alone (e.g., flight safety decisions).
- Always state the data source, retrieval timestamp, and that conditions may change.
- For severe weather (hurricanes, tornadoes, blizzards), direct users to official national meteorological services (NWS, Met Office) for authoritative guidance.
- If coordinates or location cannot be resolved, ask for clarification rather than guessing.
- Do NOT cache old weather data and present it as current — always note the retrieval time and advise re-fetching for time-sensitive decisions.
