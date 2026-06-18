"""
AI Learning Companion — AI Engine Service
Handles: GPT Tutoring, OCR Evaluation, Gap Analysis, Adaptive Testing,
         Personalized Learning Paths, Recommendations
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Literal
from openai import AsyncOpenAI
import base64, os

app = FastAPI(title="AI Engine Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DifficultyLevel = Literal["easy", "medium", "hard", "application", "real_world"]
GapType = Literal["knowledge", "skill", "memory", "application", "analytical"]

# ─── Models ────────────────────────────────────────────────────────────────────

class TutorRequest(BaseModel):
    question: str
    class_grade: int          # 3–12
    subject: str
    topic: Optional[str] = None
    explanation_level: Literal["simple", "medium", "advanced"] = "medium"

class QuestionGenerateRequest(BaseModel):
    class_grade: int
    subject: str
    chapter: str
    topic: str
    difficulty: DifficultyLevel
    count: int = 5
    question_type: Literal["mcq", "short", "long"] = "mcq"

class AnswerEvaluateRequest(BaseModel):
    question: str
    student_answer: str
    correct_answer: Optional[str] = None
    class_grade: int
    subject: str
    max_marks: int = 10

class GapAnalysisRequest(BaseModel):
    student_id: str
    class_grade: int
    subject: str
    assessment_results: List[dict]   # [{question, student_answer, correct, topic, concept}]

class LearningPathRequest(BaseModel):
    student_id: str
    class_grade: int
    subject: str
    weak_concepts: List[str]
    strong_concepts: List[str]
    available_weeks: int = 4

# ─── AI Tutor ──────────────────────────────────────────────────────────────────

@app.post("/ai/tutor/explain")
async def explain_concept(req: TutorRequest):
    """Generate grade-appropriate explanation for a concept."""
    level_map = {
        "simple": "very simple language with relatable examples for a young student",
        "medium": "clear explanations with examples and analogies",
        "advanced": "detailed technical explanations with depth"
    }
    prompt = f"""You are an expert NCERT teacher for Class {req.class_grade} {req.subject}.
Explain the following in {level_map[req.explanation_level]}:

Topic: {req.topic or req.question}
Question: {req.question}

Instructions:
- Use language appropriate for Class {req.class_grade} students
- Include a simple example from everyday life
- Keep it engaging and encouraging
- End with a quick memory tip
- Format: Use bullet points and simple headings"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800
    )
    return {
        "success": True,
        "data": {
            "explanation": response.choices[0].message.content,
            "topic": req.topic,
            "grade": req.class_grade,
            "subject": req.subject
        }
    }

# ─── Question Generation ────────────────────────────────────────────────────────

@app.post("/ai/questions/generate")
async def generate_questions(req: QuestionGenerateRequest):
    """Generate adaptive questions based on NCERT syllabus."""
    difficulty_desc = {
        "easy": "basic recall and definition questions",
        "medium": "application and understanding questions",
        "hard": "analysis and higher-order thinking questions",
        "application": "real-world application problems",
        "real_world": "scenario-based questions connecting to daily life"
    }
    prompt = f"""Generate {req.count} {req.question_type.upper()} questions for:
Class: {req.class_grade}
Subject: {req.subject}
Chapter: {req.chapter}
Topic: {req.topic}
Difficulty: {difficulty_desc[req.difficulty]}

For MCQ, provide 4 options (A, B, C, D) and mark the correct answer.
Format each question as JSON:
{{
  "id": 1,
  "question": "...",
  "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correct_answer": "A",
  "explanation": "...",
  "concept": "...",
  "difficulty": "{req.difficulty}"
}}
Return a JSON array of questions only."""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    import json
    content = json.loads(response.choices[0].message.content)
    return {"success": True, "data": content}

# ─── Answer Evaluation ─────────────────────────────────────────────────────────

@app.post("/ai/evaluate/text")
async def evaluate_text_answer(req: AnswerEvaluateRequest):
    """Evaluate a student's written answer using AI."""
    prompt = f"""You are evaluating a Class {req.class_grade} {req.subject} answer.

Question: {req.question}
Student Answer: {req.student_answer}
{"Correct Answer: " + req.correct_answer if req.correct_answer else ""}
Max Marks: {req.max_marks}

Evaluate and provide JSON response:
{{
  "marks_obtained": <number>,
  "max_marks": {req.max_marks},
  "percentage": <number>,
  "grammar_score": <0-10>,
  "completeness_score": <0-10>,
  "concept_understanding_score": <0-10>,
  "correct_answer": "...",
  "missing_points": ["...", "..."],
  "areas_of_improvement": ["...", "..."],
  "positive_feedback": "...",
  "overall_feedback": "..."
}}"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=1000
    )
    import json
    return {"success": True, "data": json.loads(response.choices[0].message.content)}

# ─── OCR + Handwriting Evaluation ─────────────────────────────────────────────

@app.post("/ai/evaluate/handwriting")
async def evaluate_handwriting(
    file: UploadFile = File(...),
    question: str = "",
    class_grade: int = 8,
    subject: str = "Science",
    max_marks: int = 10
):
    """Upload handwritten answer image → OCR → AI evaluation."""
    contents = await file.read()
    base64_image = base64.b64encode(contents).decode("utf-8")

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""This is a handwritten answer by a Class {class_grade} {subject} student.
Question: {question}
Max Marks: {max_marks}

Step 1: Extract the handwritten text (OCR).
Step 2: Evaluate the answer.
Return JSON:
{{
  "extracted_text": "...",
  "marks_obtained": <number>,
  "max_marks": {max_marks},
  "grammar_score": <0-10>,
  "completeness_score": <0-10>,
  "concept_understanding_score": <0-10>,
  "correct_answer": "...",
  "missing_points": [],
  "areas_of_improvement": [],
  "positive_feedback": "...",
  "overall_feedback": "..."
}}"""
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{file.content_type};base64,{base64_image}"}
                }
            ]
        }],
        response_format={"type": "json_object"},
        max_tokens=1200
    )
    import json
    return {"success": True, "data": json.loads(response.choices[0].message.content)}

# ─── Learning Gap Analysis ─────────────────────────────────────────────────────

@app.post("/ai/gap-analysis")
async def analyze_gaps(req: GapAnalysisRequest):
    """Identify learning gaps from assessment results."""
    results_summary = "\n".join([
        f"Q: {r['question'][:60]}... | Correct: {r['correct']} | Topic: {r.get('topic','?')} | Concept: {r.get('concept','?')}"
        for r in req.assessment_results[:20]
    ])
    prompt = f"""Analyze learning gaps for a Class {req.class_grade} {req.subject} student.

Assessment Results:
{results_summary}

Identify ALL gap types and return JSON:
{{
  "knowledge_gaps": [{{"concept": "...", "severity": "high/medium/low", "description": "..."}}],
  "skill_gaps": [...],
  "memory_gaps": [...],
  "application_gaps": [...],
  "analytical_gaps": [...],
  "weak_areas": ["concept1", "concept2"],
  "strong_areas": ["concept3", "concept4"],
  "recommended_topics": ["topic1", "topic2"],
  "overall_summary": "...",
  "priority_actions": ["action1", "action2"]
}}"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=1500
    )
    import json
    return {"success": True, "data": json.loads(response.choices[0].message.content)}

# ─── Personalized Learning Path ────────────────────────────────────────────────

@app.post("/ai/learning-path")
async def generate_learning_path(req: LearningPathRequest):
    """Generate a personalized weekly learning roadmap."""
    prompt = f"""Create a {req.available_weeks}-week personalized learning roadmap for:
Class: {req.class_grade}
Subject: {req.subject}
Weak Concepts: {', '.join(req.weak_concepts)}
Strong Concepts: {', '.join(req.strong_concepts)}

Return JSON:
{{
  "roadmap": [
    {{
      "week": 1,
      "focus_topic": "...",
      "concepts_to_cover": ["..."],
      "daily_plan": [
        {{"day": "Monday", "activity": "...", "duration_minutes": 30}}
      ],
      "assessment": "...",
      "mastery_target": 80
    }}
  ],
  "total_weeks": {req.available_weeks},
  "estimated_improvement": "..%"
}}"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=2000
    )
    import json
    return {"success": True, "data": json.loads(response.choices[0].message.content)}

@app.get("/ai/health")
async def health():
    return {"status": "ok", "service": "ai-engine"}
