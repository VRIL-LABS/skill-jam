---
name: travel-planner
description: Builds complete travel itineraries from flights, hotels, and activities; accounts for budget, preferences, and transit times. Invoke when asked to plan a trip, build a travel itinerary, find flights and hotels, suggest activities for a destination, or organize a vacation.
---

# Travel Planner

Creates comprehensive, day-by-day travel itineraries tailored to the traveler's budget, interests, travel style, and logistical constraints — covering flights, accommodations, activities, dining, local transit, and practical travel tips.

## When to Use

- User asks to "plan a trip", "create an itinerary", or "organize a vacation"
- A multi-city or multi-country trip needs a structured day-by-day plan
- User wants recommendations for activities, restaurants, or hotels at a destination
- Flight and hotel options need to be surfaced and compared
- A trip needs to be optimized for budget, pace (relaxed vs. packed), or specific interests
- User asks "what should I do in [city]?" or "how should I spend 5 days in [destination]?"
- A business trip needs logistics planned around confirmed meeting times

## Process

1. **Gather trip parameters**:
   - **Destination(s)**: one city, multi-city route, or region
   - **Dates**: departure and return, or duration (e.g., "10 days")
   - **Origin**: departure city and airport
   - **Travelers**: number, ages (especially if children or seniors are traveling)
   - **Budget**: total trip budget or per-day budget, and tier (budget/mid-range/luxury)
   - **Interests**: culture, outdoor adventure, food & drink, nightlife, history, beaches, family activities, etc.
   - **Pace**: relaxed (few activities/day), moderate, or packed
   - **Accommodation type**: hotel, Airbnb, hostel, boutique, resort, etc.
   - **Special requirements**: dietary restrictions, mobility needs, visa requirements, travel insurance

2. **Research the destination**:
   - Identify: best neighborhoods to stay, top attractions, hidden gems, recommended dining by cuisine type, local transportation options, tipping culture, local customs/etiquette
   - Note: visa requirements for the user's passport, local currency and payment norms, safety advisories, weather at travel dates, local public holidays that may affect access to attractions

3. **Plan transportation**:
   - **Flights**: suggest 2–3 flight options (direct vs. connection, airline, typical price range, flight duration), noting the best airports to fly into for each destination
   - **Local transit**: subway, bus, taxi, rideshare, car rental — recommend based on destination and pace
   - **Inter-city travel** (for multi-city trips): train, domestic flight, or drive — compare time vs. cost
   - Estimate transit times between activities to ensure the schedule is realistic

4. **Build the day-by-day itinerary**:
   - Group activities geographically to minimize transit time within each day
   - Sequence: arrival logistics → hotel check-in → first activity appropriate to jet lag / arrival time
   - Balance: mix popular landmarks with off-the-beaten-path experiences
   - Include: morning, afternoon, and evening for each day with approximate times
   - Account for: meal breaks (30–60 min lunch, 90 min dinner), travel between locations, and reasonable walking distances
   - Flag activities that require advance booking (popular restaurants, tours, museums with timed entry)

5. **Recommend accommodations**:
   - Suggest 3 options at different price points, in neighborhoods convenient to the main activities
   - Include: hotel name, approximate nightly rate, key amenities, proximity to main sights, booking platform

6. **Budget summary**:
   - Break down estimated costs: flights, accommodation, food (per day estimate), activities, local transport, misc
   - Flag if the budget is tight for the destination and suggest adjustments

7. **Practical travel tips**:
   - Visa and entry requirements
   - Best apps to download (maps, transit, translation, currency converter)
   - What to pack given weather and activities
   - Safety tips and any current travel advisories

## Output Format

```
## 🌍 5-Day Paris Itinerary
**Dates:** June 10–15, 2025 | **Travelers:** 2 adults | **Budget:** Mid-range (~$250/day)

### ✈️ Flights
Option 1: United — JFK → CDG | Jun 10, 9:00 PM — Jun 11, 10:30 AM (direct) · ~$520/person
Option 2: Air France — JFK → CDG | Jun 10, 7:00 PM — Jun 11, 9:05 AM (direct) · ~$580/person
↩ Return: CDG → JFK, Jun 15 · Book 2–3 months ahead for best pricing.

### 🏨 Accommodation (Paris, Marais District)
1. Hôtel de Jobo ⭐⭐⭐ — ~$180/night | Boutique, great location, free breakfast
2. Hotel Fabric ⭐⭐⭐ — ~$200/night | Hip design hotel, Le Marais neighborhood
3. Airbnb — Marais apartment — ~$140/night | More space, self-catering option

---

### Day 1 — Tuesday, June 10 (Arrival Day)
- Evening: Arrive CDG · Take RER B train to city center (45 min, ~€12) · Check in
- Dinner: Light meal near hotel — try a classic bistro in Le Marais

### Day 2 — Wednesday, June 11
- 9:00 AM: Louvre Museum *(book timed entry in advance — 3 hours)*
- 12:30 PM: Lunch at Café Marly with Louvre courtyard view
- 2:30 PM: Stroll through Tuileries Garden → Place de la Concorde
- 5:00 PM: Champs-Élysées walk → Arc de Triomphe (rooftop, ~€16)
- 7:30 PM: Dinner in Saint-Germain — try L'Avant Comptoir (standing wine bar)

[Days 3–5 follow same format...]

---

### 💰 Estimated Budget Breakdown
| Category      | Estimate     |
|---------------|--------------|
| Flights       | $1,040 (×2)  |
| Hotel (5 nights) | $900      |
| Food (5 days) | $400         |
| Activities    | $200         |
| Local Transit | $80          |
| **Total**     | **~$2,620**  |

### 📱 Recommended Apps: Citymapper (transit), Duolingo (French basics), TheFork (restaurant reservations), Wikiloc (walks)
### 🔑 Tips: Validate Metro tickets before boarding · Tipping not expected but 5–10% appreciated · Book Eiffel Tower tickets 6+ weeks ahead
```

## Examples

### Example Input
```
Plan a 7-day trip to Japan for 2 people in October. We like food, culture, and some nature. Mid-range budget flying from Los Angeles.
```

### Example Output
```
## 🇯🇵 7-Day Japan Itinerary (October)
Route: Tokyo (3 nights) → Kyoto (2 nights) → Osaka (2 nights)

Day 1–3 Tokyo: Shibuya crossing, Senso-ji temple, teamLab digital art, Tsukiji outer market, Harajuku, Shinjuku nightlife
Day 4–5 Kyoto: Arashiyama bamboo grove, Fushimi Inari shrine, Gion geisha district, tea ceremony, Nishiki Market
Day 6–7 Osaka: Dotonbori street food (takoyaki, okonomiyaki), Osaka Castle, Kuromon Market, day trip to Nara (deer park)

Transit: Tokyo↔Kyoto by Shinkansen (2.5 hrs, ~$100 on JR Pass). Get 7-day JR Pass (~$340/person) — covers all intercity trains.

Estimated budget: ~$4,500 for 2 (flights ~$1,400, accommodation $1,200, food $700, activities $500, transport $700).

🔑 October tip: Autumn foliage begins in late October in Kyoto — highly recommended!
```

## Boundaries

- Prices and availability are estimates; always advise users to verify flights, hotels, and activity pricing before booking.
- Do NOT book anything on behalf of the user without explicit confirmation of all details and cost.
- Always note visa requirements for the user's nationality/destination when known; recommend checking official government sources for up-to-date requirements.
- For safety-sensitive destinations, include current travel advisory status and recommend checking official government travel advisories.
- Do NOT plan activities that are illegal, involve protected wildlife harm, or violate local laws and customs.
- Respect the user's pace preferences — don't over-schedule; leave buffer time for rest, spontaneity, and delays.
