# BPI Challenge 2017

Source: https://ais.win.tue.nl/bpi/2017/challenge.html

## Event

- 13th International Workshop on Business Process Intelligence (BPI 2017)
- Barcelona, Spain — September 10–15, 2017
- Affiliated with BPM 2017

## Challenge Overview

The Seventh International Business Process Intelligence Challenge invited participants to analyze a real-life event log from a financial institution's loan application process. Participants could employ any analytical techniques to answer process-owner questions or uncover novel insights.

Sponsors: **Minit** (BPI2017@minitlabs.com) and **Celonis** (BPI2017@celonis.com).

## The Dataset

Data comes from the same financial institution as the 2012 BPI challenge, capturing the evolved process five years later.

- 1,202,267 events
- 31,509 loan applications
- 42,995 offers created
- 149 originators (employees/systems)

Key difference from 2012: the updated workflow system now supports multiple offers per application, eliminating the workarounds visible in the older log.

### Event categories

Three event types are recorded:

- **Application** state changes
- **Offer** state changes
- **Workflow** events

## Available Attributes

### Application-level
- Requested loan amount (Euro)
- Application type
- Loan purpose (LoanGoal)
- Application ID

### Offer-level
- Offer ID
- Offered amount
- Initial withdrawal amount
- Payback term count
- Monthly costs
- Customer credit score
- Creating employee
- Selection and acceptance status

### Event-level
- Employee responsible
- Timestamp
- XES lifecycle information
- Internal lifecycle events

## Research Questions

The company sought analysis addressing:

1. **Throughput analysis** — distinguish processing time within company systems from applicant response waiting periods.
2. **Incompleteness impact** — examine how frequent completion requests affect offer acceptance rates.
3. **Multi-offer behavior** — quantify customers requesting multiple offers (single vs. multiple conversations) and differences in conversion rates.
4. **Additional insights** — identify interesting trends and dependencies in the process.

## Submission Categories & Criteria

- **Student** — originality, claim validity, deep analysis of specific aspects (control-flow models, performance models, predictive models, etc.).
- **Academic** — novelty of technique and demonstration of practical applicability of tools/methods on real-world data.
- **Professional** — professionalism and completeness of analysis across broader aspects, with emphasis on real-world business improvement utility.

## Deadlines

- Abstract submission: June 2, 2017
- Report submission: June 9, 2017
- Winner announcement: at BPI 2017 in Barcelona

## Awards

All three category winners received invitations to Barcelona for presentations and the prize ceremony.

### 2017 Winners

- **Student** — Elizaveta Povalyaeva, Ismail Khamitov, Artyom Fomenko (Moscow Higher School of Economics): *Density Analysis of the Interaction With Client*
- **Professional** — Liese Blevi, Julie Robbrecht, Lucie Delporte (KPMG Technology Advisory, Belgium): *Process mining on the loan application process of a Dutch Financial Institute*
- **Academic** — Team from Pontifícia Universidade: *Stairway to Value: Mining the loan application process*

## Submission Requirements

- Maximum 30 pages (including figures)
- LNCS/LNBIP Springer format (LaTeX or Word)
- Optional appendices supporting the main text
- Submission via EasyChair: https://www.easychair.org/conferences/?conf=bpi2017
- Must be designated as a challenge entry

## Data Access

Two XES-formatted event logs are provided:

1. **Application event log** — cases indexed by application ID, with offer references.
2. **Offer event log** — cases indexed by offer ID, with application links.

Both files comply with the IEEE XES standard for compatibility with standard process mining tools.

## Submission Statistics

- 3 academic submissions
- 6 professional submissions
- 14 student submissions
- **Total: 23 submissions**

All winning reports and participant submissions were made publicly available following the workshop.
