---
name: calendar-manager
description: Creates, reschedules, and summarizes calendar events; finds optimal meeting slots across participants and time zones. Invoke when asked to schedule a meeting, find a free time slot, manage calendar events, check availability, or coordinate across time zones.
---

# Calendar Manager

Manages the full lifecycle of calendar events — creating, updating, canceling, and summarizing events — and intelligently finds optimal meeting windows across multiple participants and time zones.

## When to Use

- User asks to "schedule", "book", or "set up" a meeting
- User needs to find a free slot that works for multiple people
- A recurring event needs to be created or modified
- User asks what's on their calendar for a given day or week
- An event needs to be rescheduled based on a conflict or preference change
- User wants to add context (agenda, location, video link) to an existing event
- User asks to cancel or decline a meeting

## Process

1. **Parse the request**:
   - Extract: participants, preferred time window, duration, time zone, recurrence, location/video link, and agenda
   - Clarify ambiguous references ("tomorrow", "next week", "morning") by anchoring to the current date and the user's local time zone
   - Identify any hard constraints ("not before 10am", "avoid Fridays", "no back-to-back")

2. **Check availability** (when calendar access is available):
   - Query each participant's free/busy data for the proposed window
   - Identify all open slots that satisfy the duration requirement with ≥15 minutes buffer on either side
   - Rank slots by score: working hours preferred, earlier in the week preferred, spreads meetings evenly through the day

3. **Handle time zone coordination**:
   - Convert all times to each participant's local time zone for the confirmation
   - Flag slots that fall outside normal working hours (8am–6pm) for any participant and ask for explicit confirmation
   - Present times in the requester's local zone with secondary display of other participants' zones

4. **Create or update the event**:
   - Title: clear, action-oriented (e.g., "Q3 Planning Kickoff" not "Meeting")
   - Description: include agenda bullet points, pre-read links, and any decisions needed
   - Attach video conferencing link (Zoom, Meet, Teams) if requested or if participants are in different locations
   - Set reminders: 24 hours and 15 minutes before by default

5. **Handle conflicts**:
   - If no slot satisfies all constraints, surface the 3 least-bad options with a tradeoff explanation
   - If a hard conflict exists, propose the soonest available alternative and flag what moves

6. **Confirm and summarize**:
   - Return a human-readable confirmation with all event details
   - List each participant and their local time for the event
   - Include calendar invite preview or ICS attachment when supported

## Output Format

### Meeting Suggestion
```
📅 Proposed Meeting Slots (all times shown in your local time zone — EST):

1. Tuesday, June 10 · 2:00 PM – 3:00 PM EST
   → 11:00 AM PST for Alex · 7:00 PM GMT for the London team

2. Wednesday, June 11 · 10:00 AM – 11:00 AM EST
   → 7:00 AM PST for Alex · 3:00 PM GMT for the London team ⚠️ end of London day

3. Thursday, June 12 · 3:00 PM – 4:00 PM EST
   → 12:00 PM PST for Alex · 8:00 PM GMT for the London team ⚠️ outside London working hours

Recommendation: Option 1 (Tuesday 2 PM EST) works within everyone's core hours.
```

### Event Creation Confirmation
```
✅ Event Created

Title: Q3 Planning Kickoff
Date: Tuesday, June 10, 2025
Time: 2:00 PM – 3:00 PM EST
Location: Zoom — https://zoom.us/j/123456789

Attendees:
- you@company.com (organizer)
- alex@company.com · 11:00 AM PST
- london-team@company.com · 7:00 PM GMT

Agenda:
1. Review Q3 OKRs (10 min)
2. Assign owners to each initiative (20 min)
3. Set milestone dates (20 min)
4. AOB (10 min)

Reminders set: 24 hours before · 15 minutes before
```

## Examples

### Example Input
```
Schedule a 1-hour product review with Alice (NYC), Bob (San Francisco), and Carol (London) sometime next week. Avoid Monday mornings and Fridays.
```

### Example Output
```
Checking availability for Alice (EST), Bob (PST), Carol (GMT) next week (June 9–13), excluding Monday mornings and Friday...

Best options:
1. Tuesday, June 10 · 2:00 PM EST | 11:00 AM PST | 7:00 PM GMT ✅ all within working hours
2. Wednesday, June 11 · 10:00 AM EST | 7:00 AM PST | 3:00 PM GMT ⚠️ early for Bob
3. Thursday, June 12 · 1:00 PM EST | 10:00 AM PST | 6:00 PM GMT ⚠️ end-of-day for Carol

Recommend Option 1. Shall I create the event and send invites?
```

## Boundaries

- Do NOT create or send calendar invites without explicit confirmation of the time, participants, and title.
- Do NOT access calendars without proper API authorization from the user.
- Always clarify ambiguous time expressions (e.g., "morning", "end of day") before scheduling.
- Do NOT schedule meetings outside a participant's normal working hours without explicitly flagging it and receiving confirmation.
- When calendar data is unavailable, return proposed slots as suggestions rather than confirmed bookings.
- Respect recurring event modifications carefully — confirm whether a change applies to a single instance or all future occurrences.
