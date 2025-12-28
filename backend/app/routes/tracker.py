from fastapi import APIRouter

router = APIRouter(prefix="/tracker", tags=["Tracker"])


@router.get("/dashboard")
def get_progress_dashboard():
    """
    Returns EXACT structure expected by ProgressDashboard.tsx
    """

    return {
        "skillsLearned": 8,
        "daysActive": 15,
        "totalHours": 96,
        "streak": 5,
        "roadmapCompletion": 40,

        "weeklyProgress": [
            {"day": "Mon", "hours": 2},
            {"day": "Tue", "hours": 3},
            {"day": "Wed", "hours": 1},
            {"day": "Thu", "hours": 4},
            {"day": "Fri", "hours": 2},
            {"day": "Sat", "hours": 5},
            {"day": "Sun", "hours": 3}
        ],

        "monthlyProgress": [
            {"week": "Week 1", "completion": 25},
            {"week": "Week 2", "completion": 45},
            {"week": "Week 3", "completion": 60},
            {"week": "Week 4", "completion": 80}
        ],

        "skillsProgress": [
            {"skill": "Python", "progress": 85},
            {"skill": "FastAPI", "progress": 75},
            {"skill": "React", "progress": 60},
            {"skill": "Docker", "progress": 30}
        ]
    }
