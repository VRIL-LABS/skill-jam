---
name: meeting-scheduler
description: Identifies optimal meeting windows across participants' calendars and time zones, and sends invites with agendas. Invoke when asked to schedule a meeting, find a time that works for everyone, coordinate across time zones, or send a calendar invite with an agenda.
---

# Meeting Scheduler

Identifies optimal meeting times across multiple participants' calendars and time zones, proposes ranked scheduling options, generates structured agendas, and creates calendar invites — eliminating the back-and-forth of manual coordination.

## When to Use

- User needs to schedule a meeting with multiple people across different time zones
- User asks to "find a time that works for everyone" for a group meeting
- A recurring meeting series needs to be established
- User wants to send a calendar invite with a structured agenda
- A meeting needs to be rescheduled around a conflict
- User wants to avoid scheduling fatigue by finding low-interruption time slots
- A sequence of project meetings needs to be planned across a project timeline

## Process

1. **Gather scheduling requirements**:
   - **Participants**: names, email addresses, and their time zones (infer from email domain or ask)
   - **Duration**: how long the meeting needs to be
   - **Urgency**: must happen today, this week, or within a specific window
   - **Constraints**: hard constraints ("not before 9 AM", "never on Fridays", "avoid back-to-back") and soft preferences ("morning preferred")
   - **Meeting type**: one-time, recurring (frequency), or ad hoc
   - **Purpose and agenda**: what is the meeting for? What decisions need to be made?

2. **Resolve time zones**:
   - Map each participant to their IANA time zone (`America/New_York`, `Europe/London`, etc.)
   - Identify the overlap of working hours (9 AM–5 PM) across all participants
   - If no full overlap exists: find the closest overlap and flag which participants are at the edge of their working day
   - Account for Daylight Saving Time transitions if the meeting is in the future

3. **Query availability** (when calendar access is available):
   - Fetch free/busy data for each participant during the candidate window
   - Identify blocks where all participants are simultaneously free for at least the required duration
   - Add a 15-minute buffer on each side of proposed slots to avoid back-to-back meetings
   - Flag participants who appear to have no availability in the window

4. **Rank scheduling options**:
   - Score each open slot:
     - +3: falls within core working hours for all participants
     - +2: earlier in the week (reduces calendar anxiety)
     - +2: not immediately before or after lunch for any participant
     - +1: within the requester's stated time preferences
     - −2: requires any participant to join before 8 AM or after 6 PM local time
   - Present the top 3–5 options with time in each participant's local zone

5. **Generate a structured agenda**:
   - Draft an agenda based on the stated meeting purpose
   - Standard structure: Welcome / Context (5 min) → Main Topics → Decisions Needed → Action Item Assignment → Next Steps (5 min)
   - Assign estimated time to each agenda item based on total meeting duration
   - List any pre-reads or prep work participants should complete beforehand

6. **Create the calendar event**:
   - Title: action-oriented and specific ("Q3 Budget Approval" not "Meeting")
   - Include agenda and pre-read links in the description
   - Add video conferencing link if participants are not co-located
   - Set reminders: 24 hours and 15 minutes prior
   - For recurring meetings: specify recurrence rule (RRULE) and end date

7. **Handle no-availability scenarios**:
   - If no slot works for all participants: identify who blocks the most slots and suggest async alternatives (recorded Loom, shared doc for async input)
   - Surface the "least bad" option with explicit note of whose schedule is impacted

## Output Format

### Scheduling Options
```
📅 Meeting: Q3 Roadmap Review (60 min)
Participants: Alice (EST), Bob (PST), Carol (GMT+1 Berlin)

Available Slots (ranked):

1. ✅ Tuesday, June 10 · 10:00 AM EST | 7:00 AM PST | 4:00 PM Berlin
   All within core hours. Best overall fit.

2. ✅ Wednesday, June 11 · 2:00 PM EST | 11:00 AM PST | 8:00 PM Berlin
   ⚠️ Evening for Carol — she confirmed 8 PM is acceptable.

3. ⚠️ Thursday, June 12 · 9:00 AM EST | 6:00 AM PST | 3:00 PM Berlin
   Very early for Bob — not recommended unless urgent.

Recommendation: Option 1 (Tuesday 10 AM EST). Proceed?
```

### Calendar Invite Preview
```
📌 Calendar Invite

Title: Q3 Roadmap Review
Date: Tuesday, June 10, 2025
Time: 10:00 AM – 11:00 AM EST
  · Alice: 10:00 AM EST
  · Bob: 7:00 AM PST
  · Carol: 4:00 PM CEST (Berlin)

Location: Zoom — https://zoom.us/j/987654321

Attendees: alice@co.com · bob@co.com · carol@co.com

---
AGENDA

Pre-read: Q3 OKR draft (link) — please review before the meeting

1. Review Q3 OKR progress [15 min]
2. Prioritize roadmap items for H2 [25 min]
3. Assign owners for each initiative [10 min]
4. Open discussion / blockers [5 min]
5. Next steps and action item confirmation [5 min]

---
Reminders: 24 hours before · 15 minutes before
```

## Examples

### Example Input
```
Schedule a 45-minute retrospective for a team: Sam (London), Lisa (New York), Kim (Singapore). Sometime next week, preferably Tuesday or Wednesday. Generate an agenda for a sprint retro.
```

### Example Output
```
Time zone overlap analysis:
- London (BST, UTC+1) · New York (EDT, UTC-4) · Singapore (SGT, UTC+8)
- Usable overlap for all three within working hours: None exists simultaneously.
- Best compromise: 9:00 AM London / 4:00 AM New York / 4:00 PM Singapore
  OR: 5:00 PM London / 12:00 PM New York / 12:00 AM Singapore (midnight — not viable for Kim)

Best option: Wednesday June 11 · 9:00 AM London · 4:00 AM New York · 4:00 PM Singapore
⚠️ Lisa in New York joins at 4:00 AM — recommend confirming she's comfortable with this, or consider async retro format.

Agenda (45 min):
1. What went well? [10 min — each person shares 1–2 items]
2. What could be improved? [15 min]
3. Action items to improve next sprint [15 min — assign owner and deadline per item]
4. Team shoutouts [5 min]
```

## Boundaries

- Always display meeting times in each participant's local time zone — never only in a single zone.
- Do NOT send calendar invites without explicit user confirmation of the time, participants, and content.
- When working-hour overlap is impossible, flag it clearly and offer async alternatives rather than silently scheduling a 3 AM call.
- Respect stated constraints (no Fridays, no before 9 AM) — do NOT suggest times that violate them without explicit override from the user.
- For recurring meetings, confirm the end date or recurrence limit before creating the series.
- When calendar access is unavailable, present proposed slots as suggestions rather than confirmed bookings.
