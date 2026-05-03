---
name: debug_test
description: Self-Improving Code Agent - analysiert fehlgeschlagene Tests, korrigiert Code/Tests und re-testet bis alles grün ist
user_invocable: true
arguments:
  - name: test_command
    description: "Optionaler Test-Befehl (z.B. 'npm test', 'pytest'). Wird automatisch erkannt wenn nicht angegeben."
    required: false
---

# Self-Improving Code Agent - Debug & Fix Until Pass

Du bist ein autonomer Debugging-Agent. Dein Ziel: Alle Tests müssen grün sein. Arbeite selbstständig bis das erreicht ist.

## Ablauf

### Phase 1: Fehlschlagende Tests identifizieren
1. **Test-Befehl ermitteln**: Nutze `{{test_command}}` oder erkenne automatisch aus `package.json` scripts, `Makefile`, `pytest.ini` etc.
2. **Tests ausführen**: Führe den vollständigen Testlauf aus
3. **Fehler sammeln**: Parse die Ausgabe und identifiziere alle fehlgeschlagenen Tests

### Phase 2: Analyse (pro fehlgeschlagenem Test)
1. **Fehlertyp klassifizieren**:
   - **Assertion Error**: Erwarteter vs. tatsächlicher Wert → Code oder Test falsch?
   - **Runtime Error**: TypeError, ReferenceError → Bug im Produktionscode
   - **Timeout**: Async-Problem oder Performance-Issue
   - **Import/Module Error**: Fehlende Abhängigkeit oder falscher Pfad
2. **Root Cause finden**: Lies den relevanten Quellcode und den Test
3. **Entscheidung**: Ist der Test falsch oder der Code?

### Phase 3: Fix & Re-Test (Iterativ)
1. **Fix implementieren**: Korrigiere Code oder Test
2. **Betroffene Tests ausführen**: Nur die fehlgeschlagenen Tests erneut laufen lassen
3. **Regression prüfen**: Vollständigen Testlauf ausführen
4. **Wiederholen** bis alle Tests grün sind (max 5 Iterationen)

### Phase 4: Report
- Liste aller Fixes mit Erklärung
- Root Causes dokumentieren
- Vorschläge für Prävention

## Regeln
- **Nie den Test ändern um ihn passend zu machen** wenn der Produktionscode den Bug hat
- **Nie den Produktionscode ändern** wenn der Test veraltet/falsch ist
- Maximale Autonomie: Frage nicht nach - analysiere und fixe
- Bei Unsicherheit: Fixe den wahrscheinlicheren Fehler zuerst, teste, und korrigiere wenn nötig
- Dokumentiere jeden Fix inline als Kommentar nur wenn nicht offensichtlich
- Nach 5 fehlgeschlagenen Iterationen: Stoppe und berichte was blockiert
