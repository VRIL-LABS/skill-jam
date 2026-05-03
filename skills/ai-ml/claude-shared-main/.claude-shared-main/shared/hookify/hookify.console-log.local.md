---
name: warn-console-log
enabled: true
event: file
pattern: console\.log\(
action: warn
---

Console.log detected. Consider:
- Is this for debugging or production logging?
- Should this use a proper logging library instead?
