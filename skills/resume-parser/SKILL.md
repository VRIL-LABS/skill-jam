---
name: resume-parser
description: Extracts structured candidate data (skills, experience, education) from resumes and CVs in any format. Invoke when asked to parse a resume, extract candidate information, process job applications, build a candidate profile, or screen CVs.
---

# Resume Parser

Extracts structured candidate data from resumes and CVs in any format (PDF, Word, plain text, HTML) — parsing contact information, work experience, education, skills, certifications, and achievements into a clean, normalized data structure ready for applicant tracking systems, screening workflows, or candidate comparison.

## When to Use

- User provides a resume or CV and asks to extract the candidate's data
- A batch of resumes needs to be processed and ingested into an ATS
- Candidate profiles need to be standardized for side-by-side comparison
- A resume needs to be scored against a job description for fit
- User asks to "parse", "process", or "screen" a resume or set of applications
- Candidate data needs to be exported to a CRM or HR system
- User wants to identify gaps or strengths in a candidate's profile

## Process

1. **Ingest the document**:
   - Accept: PDF, DOCX, TXT, HTML, RTF, or plain-text paste
   - Detect language; flag if non-English (still extract but note translation may be needed)
   - Assess if the document is a resume/CV vs. a cover letter or portfolio — process accordingly
   - Handle common resume layouts: chronological, functional, combination/hybrid, academic CV

2. **Extract contact and identity information**:
   - Full name
   - Email address(es)
   - Phone number(s) with country code if present
   - Location: city, state/province, country (do NOT infer full address beyond what's stated)
   - LinkedIn URL, GitHub URL, portfolio URL, or other professional profiles
   - Note: do NOT infer, store, or flag protected characteristics (date of birth, gender, ethnicity, nationality) even if visible on the CV

3. **Parse work experience** (for each position):
   - Job title
   - Company name and industry (infer industry if not stated, with low confidence flag)
   - Start date and end date (or "Present")
   - Duration (computed: years and months)
   - Location (city/country or "Remote")
   - Key responsibilities: bulleted list extracted from the resume text
   - Achievements: quantified accomplishments ("Increased revenue by 40%", "Led team of 12")
   - Seniority level inferred from title: Individual Contributor / Senior IC / Manager / Director / Executive

4. **Parse education**:
   - Degree type (Bachelor's, Master's, PhD, Associate's, Certificate, etc.)
   - Field of study / major
   - Institution name
   - Graduation year (or expected graduation)
   - GPA if listed
   - Honors: cum laude, dean's list, scholarships

5. **Extract skills**:
   - **Technical skills**: programming languages, frameworks, databases, cloud platforms, tools
   - **Domain skills**: finance, healthcare, marketing, operations, etc.
   - **Soft skills**: explicitly stated only (do NOT infer soft skills from job descriptions)
   - **Certifications and licenses**: name, issuing body, date obtained, expiry date if listed
   - Normalize skill names: "JS" → "JavaScript", "Postgres" → "PostgreSQL", "k8s" → "Kubernetes"

6. **Identify additional sections**:
   - Publications / research
   - Awards and recognitions
   - Languages spoken (and proficiency level if stated)
   - Volunteer work and community involvement
   - Projects: name, technologies used, description, link

7. **Compute summary metrics**:
   - Total years of professional experience
   - Most recent role title and company
   - Highest education level
   - Career progression indicator: is each role a step up (title, responsibility), lateral, or step down?
   - Career gap detection: gaps > 6 months in employment history (note, do not interpret)

8. **Optional: Score against a job description** (when both are provided):
   - Match required skills: % of required skills present in resume
   - Match experience level: does candidate's seniority align with the role?
   - Education match: does degree requirement align?
   - Output: match score (0–100) with breakdown by category and key missing qualifications

## Output Format

```json
{
  "candidate": {
    "name": "Jordan Lee",
    "email": "jordan.lee@email.com",
    "phone": "+1-415-555-0192",
    "location": "San Francisco, CA",
    "linkedin": "linkedin.com/in/jordanlee",
    "github": "github.com/jordanlee"
  },
  "summary_metrics": {
    "total_experience_years": 7.5,
    "current_role": "Senior Software Engineer @ Stripe",
    "highest_education": "BS Computer Science, UC Berkeley",
    "career_gaps": [],
    "career_trajectory": "Ascending"
  },
  "experience": [
    {
      "title": "Senior Software Engineer",
      "company": "Stripe",
      "industry": "FinTech",
      "start": "2022-03",
      "end": "Present",
      "duration_months": 39,
      "location": "Remote",
      "seniority": "Senior IC",
      "responsibilities": [
        "Led backend development for Stripe's payment routing service handling $2B+ daily transactions",
        "Mentored 3 junior engineers and conducted technical interviews"
      ],
      "achievements": [
        "Reduced p99 API latency by 40% through query optimization and caching layer redesign",
        "Shipped fraud detection feature reducing chargebacks by 18%"
      ]
    }
  ],
  "education": [
    {
      "degree": "Bachelor of Science",
      "field": "Computer Science",
      "institution": "University of California, Berkeley",
      "graduation_year": 2017,
      "honors": "Cum Laude"
    }
  ],
  "skills": {
    "technical": ["Python", "Go", "PostgreSQL", "Redis", "AWS", "Kubernetes", "gRPC", "Kafka"],
    "domain": ["Payments", "Distributed Systems", "API Design"],
    "certifications": [
      { "name": "AWS Solutions Architect Associate", "issuer": "Amazon Web Services", "date": "2023-05" }
    ]
  },
  "languages": [
    { "language": "English", "proficiency": "Native" },
    { "language": "Mandarin", "proficiency": "Conversational" }
  ]
}
```

## Examples

### Example Input
```
Parse this resume PDF and tell me if this candidate is a good match for a Staff Software Engineer role requiring Go, distributed systems experience, and 8+ years of experience.
```

### Example Output
```
✅ Parsed successfully. Key profile:
- 7.5 years experience (slightly below 8-year requirement)
- Current role: Senior SWE @ Stripe (FinTech, payments systems)
- Go: ✅ listed, with distributed systems experience
- Distributed Systems: ✅ strong evidence (Kafka, gRPC, p99 latency optimization)
- Education: BS CS, UC Berkeley (Cum Laude)

Match Score: 78/100
Strong match on technical skills and domain. Minor gap: 0.5 years below stated experience requirement.
Recommendation: Recommend for phone screen — strong distributed systems background compensates for minor experience gap.
```

## Boundaries

- Do NOT infer, store, or flag protected characteristics (age, gender, race, nationality, disability status) — even if visible on the CV. Process only professional information.
- Always note extraction confidence — flag fields that were ambiguous or uncertain rather than presenting guesses as facts.
- Do NOT make hiring decisions — provide structured data and match scores to inform human decision-makers only.
- Treat all resume data as PII — do not log, cache, or transmit candidate personal information beyond the immediate task.
- When computing a JD match score, be transparent about which criteria were weighted and how the score was derived.
- Flag if a resume appears to have been keyword-stuffed (unusually long skills list with no supporting experience) — note the pattern without making accusations.
