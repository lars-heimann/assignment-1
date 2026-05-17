# BPI Challenge 2017 — Forum Q&A

Curated extract of the substantive, answered questions from the ProM forum
category for BPI 2017: <https://promforum.win.tue.nl/categories/-bpi-challenge-2017>

Threads with no replies, pure tooling problems (CSV/XES import errors, ProM-Lite
crashes), and meta posts (deadline extensions, posting rules) are omitted.
Author names preserved as on the forum. `BPIC2017` is the official challenge
account answering on behalf of the data provider.

---

## 1. The organization and process

**Who is the financial institute?** ([thread 748])

> The organization has chosen not to reveal its name, but I can tell their
> domain is **consumer credit**. Their business is mostly **online based**.
> — BPIC2017

**Can a single customer have multiple applications running?** ([thread 789])

> Customers cannot initiate multiple applications simultaneously via the
> website, but employees can start new applications for one person at the same
> time. — BPIC2017

**Who creates offers?** ([thread 764])

> The customer asks for 1 or more offers and the employee creates them and
> sends them to the customer. — rreyes (confirmed by BPIC2017)

**Who sends/returns offers?** ([thread 753])

- `O_Sent (mail and online)` — an employee of the financial institute sends
  the offer (by mail or digitally online).
- `O_Returned` — the customer returns the offer (signed). The signed return
  also includes supporting documents (ID, payslips, bank statements).

---

## 2. The two event logs

**Is the Offer log a subset of the Application log?** ([thread 757])

> All of the events in this log are also in the BPI Challenge 2017 event log.
> This subset is provided for convenience and the IDs are persistent between
> the two datasets. — JBuijs

So: same events, two case notions (case = application vs. case = offer),
shared IDs.

---

## 3. Application states (`A_*`)

From [thread 755] (BPIC2017's canonical definitions):

| State          | Meaning                                                                  |
| -------------- | ------------------------------------------------------------------------ |
| `A_Submitted`  | Customer has submitted a new application from the website                |
| `A_Concept`    | Initial assessment phase after submission (largely automated first pass) |
| `A_Accepted`   | Application approved; the bank creates offers                            |
| `A_Complete`   | Offers have been sent to the customer; bank waits for signed documents   |
| `A_Validating` | Offer and documents are received and being checked                       |
| `A_Incomplete` | Documents are not correct or some documents are still missing            |
| `A_Pending`    | All documents received and assessment is positive — the loan is final    |
| `A_Denied`     | Loan cannot be offered; application doesn't fit acceptance criteria      |
| `A_Cancelled`  | Customer never sends in documents or doesn't need the loan               |

**`A_Concept` specifically** ([thread 799]):

> The application is in the concept state, that means that the customer just
> submitted it (or the bank started it), and a first assessment has been done
> automatically. — FrancescaLucchini

---

## 4. Offer activities (`O_*`)

**`O_Create Offer` vs `O_Created`** ([thread 772]): essentially the same moment,
two records.

> O_Create Offer is the event which triggers the offer status of O_Created.
> — theMarlzy (consensus answer)

> O_Create Offer is always followed by `action=create`; O_Created follows
> `action=statechange`. — rosangelamariah

Frank confirmed both have identical row counts (193,849) and occur at the same
moment.

**`A_Denied` vs `O_Refused`** ([thread 751]):

> `A_Denied` means the application is declined/denied **by the bank**.
> `O_Refused` means the offer is refused **by the bank**. Offers can be refused
> individually, but when an application is denied, all active offer statuses
> automatically become refused. — BPIC2017

Important nuance: `A_Denied` can occur even **after** the customer returned the
offer (`O_Returned`). The signed return ships supporting documents which the
bank still evaluates — if income/documents are insufficient, the application
is denied at that point.

An offer can be refused individually and within the same application another offer can be made. But in case the total application is denied, it means that the status of all active offers is automatically set to refused aswell.

---

## 5. Workitems (`W_*`)

From [thread 764] (BPIC2017):

**Standard workitems** (the "normal" path):

- `W_Handle leads`
- `W_Complete application`
- `W_Validate application`
- `W_Call incomplete files`
- `W_Call after offers`
- `W_Assess potential fraud`

**Custom / less-frequent workitems:**

- `W_Shortened completion` — applies when the customer has a profile
  classified as **lower credit risk**, so the process is sped up.
- `W_Personal Loan Collection` — debit scheduling activity (debits on the
  7th, 14th, 21st, 28th of the month).

**`W_Handle leads` specifically** ([thread 755]): automatic initial assessment;
escalates to manual processing if needed.

**Workitem lifecycle** ([thread 776]): the W_-events have multiple lifecycle
transitions (`schedule`, `start`, `suspend`, `resume`, `complete`, `ate_abort`,
`withdraw`). Note that **ProM's CSV exporter only round-trips `start` and
`complete`** correctly — see §8.

Rough mapping of lifecycle terms vs. event-class names that show up in tools:

| Generic    | In this log |
| ---------- | ----------- |
| New        | Created     |
| Scheduled  | Obtained    |
| Suspended  | Released    |
| Terminated | Deleted     |

---

## 6. Process endpoints

**Valid terminal states** ([thread 752]):

- `O_Cancelled` — offer was sent to applicant, who didn't reply in time.
- `A_Pending` — offer was accepted by the applicant (loan paid out).
- `O_Refused` — offer refused (by bank or, effectively, applicant via
  non-return).
- `A_Cancelled` and `A_Denied` are **also** valid endpoints of the application.
  — BPIC2017

**Why does `O_Cancelled` sometimes appear *after* `A_Pending`?** ([thread 752])

> There can be multiple offers, but just 1 can be accepted. If offer 1 is
> accepted and the application state becomes `A_Pending`, then offer 2 and 3
> are automatically cancelled in the process. — BPIC2017

So a trailing `O_Cancelled` after `A_Pending` is *not* a process anomaly — it's
the system auto-cancelling the sibling offers.

---

## 7. Offer attributes: `Selected` and `Accepted` ([thread 749])

- **`Accepted`** = "is the offer still acceptable?" The bank reassesses the
  application multiple times. If circumstances change (e.g. payslips show
  insufficient income for the offered amount), the offer is no longer
  acceptable. A manual override is possible when `Accepted=false`.
- **`Selected`** = which offer the customer signed and returned. Of the
  multiple offers an application may have, one becomes "selected".

All four combinations occur in the data (counts from gresch's post):

| Selected | Accepted | Count  |
| -------- | -------- | ------ |
| FALSE    | false    | 6,777  |
| FALSE    | true     | 5,960  |
| TRUE     | false    | 14,297 |
| TRUE     | true     | 15,637 |

---

## 8. Question-3 clarifications (multi-offer / conversion)

From the official challenge questions, Q3 asks about "single vs. multiple
conversation" applicants and conversion rates. Clarifications ([thread 789]):

- **"Conversion"** = the application reaches end-state `A_Pending` (the loan
  is actually paid out). — BPIC2017
- **"Conversation"** = an agent **phone call** following application
  submission.
  - *Single conversation* = all offers communicated in one call.
  - *Multiple conversations* = offers spread across separate calls.

The distinction matters because timing/spacing of offer receipt is what's
being studied behaviorally.

---

## 9. "Incompleteness" in Q2 ([thread 802])

The Q2 phrasing "the influence on the frequency of incompleteness on the final
outcome" refers literally to:

> How many times an application gets the status `A_Incomplete`. — BPIC2017

So the operational metric is the count of `A_Incomplete` events per case.

---

## 10. Practical: ProM-Lite CSV export bug ([thread 766])

Worth knowing if you ever route through ProM's CSV export:

> The exporter exports the last `start`/`complete` event it outputted before
> when encountering non-standard lifecycle transitions like `schedule` or
> `withdraw`. Filter problematic events as a workaround.
> — Eric Verbeek (hverbeek)

Filtering them removes all `W_*` activities. Workarounds reported by
participants: parse the XES directly (Python), or export from Celonis
instead. **Recommendation for this project:** load XES directly via pm4py and
don't round-trip through ProM CSV.

---

## Thread index

[thread 748]: https://promforum.win.tue.nl/discussion/748/extra-information
[thread 749]: https://promforum.win.tue.nl/discussion/749/meaning-of-columns-selected-and-accepted
[thread 751]: https://promforum.win.tue.nl/discussion/751/a-denied-and-o-refused
[thread 752]: https://promforum.win.tue.nl/discussion/752/end-points-a-proposition
[thread 753]: https://promforum.win.tue.nl/discussion/753/offer-activities
[thread 755]: https://promforum.win.tue.nl/discussion/755/brief-event-descriptions
[thread 757]: https://promforum.win.tue.nl/discussion/757/difference-between-two-datasets
[thread 764]: https://promforum.win.tue.nl/discussion/764/activity-explanation
[thread 766]: https://promforum.win.tue.nl/discussion/766/mismatch-between-application-event-log-in-prom-lite-and-its-own-exported-csv
[thread 772]: https://promforum.win.tue.nl/discussion/772/meaning-of-o-create-offer-and-o-created
[thread 776]: https://promforum.win.tue.nl/discussion/776/workitem-explanation
[thread 789]: https://promforum.win.tue.nl/discussion/789/clarifications-about-question-three
[thread 799]: https://promforum.win.tue.nl/discussion/799/concept-of-a-loan-a-concept-activity
[thread 802]: https://promforum.win.tue.nl/discussion/802/meaning-of-incompleteness
