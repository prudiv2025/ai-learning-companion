"""
AI Learning Companion — Assessment Service
Handles: Quiz creation, answer submission, scoring, adaptive difficulty progression
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Literal
import httpx, os
from datetime import datetime

app = FastAPI(title="Assessment Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

AI_ENGINE_URL = os.getenv("AI_ENGINE_URL", "http://ai-engine:8002")
MASTERY_THRESHOLD = 80  # 80% to achieve mastery

DifficultyLevel = Literal["easy", "medium", "hard", "application", "real_world"]

DIFFICULTY_PROGRESSION = ["easy", "medium", "hard", "application", "real_world"]
DIFFICULTY_WEIGHTS = {"easy": 0.4, "medium": 0.3, "hard": 0.2, "application": 0.1}

class StartAssessmentRequest(BaseModel):
    student_id: str
    subject_id: str
    chapter_id: str
    assessment_type: Literal["quiz", "chapter_test", "diagnostic", "adaptive"] = "adaptive"
    class_grade: int

class SubmitAnswerRequest(BaseModel):
    assessment_id: str
    question_id: str
    student_answer: str
    time_taken_seconds: int = 0

class AssessmentResult(BaseModel):
    assessment_id: str
    total_questions: int
    correct: int
    wrong: int
    skipped: int
    percentage: float
    mastery_achieved: bool
    weak_concepts: List[str]
    next_difficulty: Optional[DifficultyLevel]
    recommendations: List[str]

# ─── In-memory session store (replace with Redis in production) ────────────────
_sessions: dict = {}

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/assessment/start")
async def start_assessment(req: StartAssessmentRequest):
    """Start a new adaptive assessment session."""
    assessment_id = f"asmnt_{req.student_id}_{int(datetime.utcnow().timestamp())}"

    # Fetch questions from AI engine
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{AI_ENGINE_URL}/ai/questions/generate", json={
            "class_grade": req.class_grade,
            "subject": req.subject_id,
            "chapter": req.chapter_id,
            "topic": "all",
            "difficulty": "easy",
            "count": 5,
            "question_type": "mcq"
        }, timeout=30)
        questions = r.json().get("data", {}).get("questions", [])

    _sessions[assessment_id] = {
        "student_id": req.student_id,
        "subject_id": req.subject_id,
        "chapter_id": req.chapter_id,
        "class_grade": req.class_grade,
        "current_difficulty": "easy",
        "answers": [],
        "questions": questions,
        "started_at": datetime.utcnow().isoformat()
    }

    return {
        "success": True,
        "data": {
            "assessment_id": assessment_id,
            "questions": questions,
            "total_questions": len(questions),
            "time_limit_minutes": 15,
            "difficulty": "easy"
        }
    }

@app.post("/assessment/submit-answer")
async def submit_answer(req: SubmitAnswerRequest):
    """Submit an answer and get instant feedback."""
    session = _sessions.get(req.assessment_id)
    if not session:
        raise HTTPException(404, "Assessment session not found")

    # Find the question
    question = next((q for q in session["questions"] if q.get("id") == req.question_id), None)
    if not question:
        raise HTTPException(404, "Question not found")

    is_correct = str(req.student_answer).strip().upper() == str(question.get("correct_answer", "")).strip().upper()

    session["answers"].append({
        "question_id": req.question_id,
        "student_answer": req.student_answer,
        "correct_answer": question.get("correct_answer"),
        "is_correct": is_correct,
        "concept": question.get("concept", ""),
        "time_taken": req.time_taken_seconds
    })

    return {
        "success": True,
        "data": {
            "is_correct": is_correct,
            "correct_answer": question.get("correct_answer"),
            "explanation": question.get("explanation", ""),
            "concept": question.get("concept", "")
        }
    }

@app.post("/assessment/complete/{assessment_id}", response_model=dict)
async def complete_assessment(assessment_id: str):
    """Complete assessment and get full result with gap analysis."""
    session = _sessions.get(assessment_id)
    if not session:
        raise HTTPException(404, "Assessment session not found")

    answers = session["answers"]
    if not answers:
        raise HTTPException(400, "No answers submitted")

    correct = sum(1 for a in answers if a["is_correct"])
    total = len(answers)
    percentage = (correct / total) * 100
    mastery = percentage >= MASTERY_THRESHOLD

    # Identify weak concepts
    weak_concepts = list(set(
        a["concept"] for a in answers
        if not a["is_correct"] and a.get("concept")
    ))

    # Determine next difficulty level
    current_idx = DIFFICULTY_PROGRESSION.index(session["current_difficulty"])
    if mastery and current_idx < len(DIFFICULTY_PROGRESSION) - 1:
        next_difficulty = DIFFICULTY_PROGRESSION[current_idx + 1]
    elif not mastery:
        next_difficulty = session["current_difficulty"]  # Retry same level
    else:
        next_difficulty = None  # Chapter complete!

    # Generate recommendations
    recommendations = []
    if not mastery:
        recommendations.append(f"Review weak concepts: {', '.join(weak_concepts[:3])}")
        recommendations.append("Watch the 5-minute concept video before retrying")
    if percentage >= 60:
        recommendations.append("Good progress! Keep practicing for mastery")
    if mastery:
        recommendations.append(f"🎉 Mastery achieved! Moving to {next_difficulty or 'next chapter'}")

    result = AssessmentResult(
        assessment_id=assessment_id,
        total_questions=total,
        correct=correct,
        wrong=total - correct,
        skipped=0,
        percentage=round(percentage, 2),
        mastery_achieved=mastery,
        weak_concepts=weak_concepts,
        next_difficulty=next_difficulty,
        recommendations=recommendations
    )

    # Clean up session
    del _sessions[assessment_id]

    return {"success": True, "data": result.dict()}

@app.get("/assessment/history/{student_id}")
async def get_assessment_history(student_id: str, subject_id: Optional[str] = None):
    """Get assessment history for a student."""
    # TODO: Fetch from PostgreSQL
    return {"success": True, "data": {"assessments": [], "total": 0}}

@app.get("/assessment/health")
async def health():
    return {"status": "ok", "service": "assessment"}
