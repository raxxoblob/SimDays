# Workplace daily context (Section 24K).
# workplace_daily_context() returns a context dict for the current shift day,
# including display text and a performance modifier. Integrate at shift start.

init python:

    WORKPLACE_CONTEXTS = {
        "it": [
            {"id": "it_bugfix",  "days": [0,2,4], "text": "There is a tricky bug in the main branch. The team is in quiet focus mode.", "perf_mod": 0},
            {"id": "it_deploy",  "days": [3,4],   "text": "Deployment day. Everyone is slightly on edge.", "perf_mod": 2},
            {"id": "it_quiet",   "days": [1],     "text": "Quiet Tuesday. Good day for focused work.", "perf_mod": 1},
            {"id": "it_review",  "days": [0,3],   "text": "Code review morning. Your work will be seen.", "perf_mod": 1},
        ],
        "corporate": [
            {"id": "corp_monday","days": [0],     "text": "Monday meeting. Everyone in a suit, nobody fully awake.", "perf_mod": 0},
            {"id": "corp_friday","days": [4],     "text": "End-of-week. Reports due. The floor is tense.", "perf_mod": 1},
            {"id": "corp_client","days": [2,3],   "text": "Client visit today. First impressions matter.", "perf_mod": 2},
            {"id": "corp_quiet", "days": [1],     "text": "Quiet midweek. A good day to catch up.", "perf_mod": 1},
        ],
        "hospital": [
            {"id": "hosp_busy",  "days": [0,3,4], "text": "Heavy caseload today. No downtime.", "perf_mod": 0},
            {"id": "hosp_morn",  "days": [1,2],   "text": "Routine morning rounds. Clear and focused.", "perf_mod": 1},
            {"id": "hosp_night", "days": [5,6],   "text": "Weekend shift. Smaller team, broader responsibility.", "perf_mod": 1},
        ],
        "culinary": [
            {"id": "cul_inspect","days": [1,4],   "text": "Health inspection prep. Every surface must be spotless.", "perf_mod": 2},
            {"id": "cul_busy",   "days": [4,5],   "text": "Friday service. Three sittings. No margin for error.", "perf_mod": 1},
            {"id": "cul_prep",   "days": [0,2],   "text": "Long prep morning. Repetitive work, good for focus.", "perf_mod": 1},
        ],
    }

    def workplace_daily_context(career_id, day_value=None):
        dw   = (day_value if day_value is not None else store.day) % 7
        ctxs = [c for c in WORKPLACE_CONTEXTS.get(career_id, []) if dw in c["days"]]
        if not ctxs: return None
        import random as _r
        return _r.Random(store.day * 11 + dw).choice(ctxs)
