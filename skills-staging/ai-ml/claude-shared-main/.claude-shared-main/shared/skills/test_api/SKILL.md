---
name: test_api
description: API Contract Tester - überprüft API-Endpunkte auf korrekte Antworten und Dokumentationstreue
user_invocable: true
arguments:
  - name: endpoint
    description: "API-Endpunkt URL oder Route (z.B. '/api/users' oder 'http://localhost:3000/api/users')"
    required: true
---

# API Contract Tester

Du bist ein API-Testing-Spezialist. Überprüfe API-Endpunkte auf Korrektheit, Dokumentationstreue und Robustheit.

## Ablauf

1. **Endpunkt identifizieren**: `{{endpoint}}`
2. **API-Dokumentation suchen**: Prüfe auf OpenAPI/Swagger-Specs, README, oder Route-Handler im Code
3. **Route-Handler analysieren**:
   - Finde den Handler-Code für den Endpunkt
   - Identifiziere erwartete Request-Parameter, Body, Headers
   - Identifiziere Response-Schema und Status-Codes
4. **Testfälle generieren**:
   - **Happy Path**: Korrekter Request → erwartete Response
   - **Validierung**: Fehlende/ungültige Parameter → 400 Bad Request
   - **Auth**: Ohne/mit ungültigem Token → 401/403
   - **Not Found**: Ungültige IDs → 404
   - **Edge Cases**: Leerer Body, zu große Payloads, SQL-Injection-Attempts
5. **Tests implementieren**: Erstelle Testdatei mit dem erkannten Framework
6. **Tests ausführen und verifizieren**

## Test-Template

```typescript
import { describe, it, expect } from 'vitest';
import request from 'supertest';
import app from '../app';

describe('{{endpoint}}', () => {
  describe('GET', () => {
    it('should return 200 with valid data', async () => {
      const res = await request(app).get('{{endpoint}}');
      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('data');
    });

    it('should return 401 without auth token', async () => {
      const res = await request(app).get('{{endpoint}}');
      expect(res.status).toBe(401);
    });
  });

  describe('POST', () => {
    it('should return 400 with invalid body', async () => {
      const res = await request(app)
        .post('{{endpoint}}')
        .send({});
      expect(res.status).toBe(400);
    });
  });
});
```

## Prüfpunkte
- Response-Schema stimmt mit Dokumentation überein
- Korrekte HTTP-Status-Codes für jeden Fall
- Response-Zeiten sind akzeptabel (< 500ms für einfache Requests)
- CORS-Headers korrekt gesetzt
- Rate-Limiting funktioniert wenn konfiguriert
- Pagination funktioniert korrekt
- Fehler-Responses haben konsistentes Format
