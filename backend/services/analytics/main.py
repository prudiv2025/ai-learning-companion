"""
AI Learning Companion — Analytics Service
Handles: Student progress, learning analytics, report cards, parent/teacher dashboards
"""
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io, os
from datetime import datetime, timedelta

app = FastAPI(title="Analytics Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/analytics/student/{student_id}/overview")
async def student_overview(student_id: str):
    """Get complete student analytics overview."""
    # TODO: Fetch from PostgreSQL
    return {
        "success": True,
        "data": {
            "student_id": student_id,
            "overall_score": 78.5,
            "total_tests": 24,
            "concepts_mastered": 47,
            "concepts_total": 120,
            "mastery_percentage": 39.2,
            "study_streak": 7,
            "total_points": 1250,
            "weekly_accuracy": [65, 72, 68, 80, 85, 88, 82],
            "subject_scores": {
                "Mathematics": 72, "Science": 85, "English": 90,
                "Hindi": 65, "Social Science": 78
            },
            "learning_speed": "medium",
            "badges_earned": ["Math Master", "Science Explorer"],
            "rank_in_class": 5,
            "rank_in_school": 23
        }
    }

@app.get("/analytics/student/{student_id}/knowledge-graph")
async def knowledge_graph(student_id: str, subject_id: str):
    """Get student knowledge graph for a subject."""
    return {
        "success": True,
        "data": {
            "nodes": [
                {"id": "c1", "label": "Force", "status": "mastered", "score": 92},
                {"id": "c2", "label": "Pressure", "status": "learning", "score": 65},
                {"id": "c3", "label": "Atmospheric Pressure", "status": "weak", "score": 40},
                {"id": "c4", "label": "Newton's Laws", "status": "mastered", "score": 88},
                {"id": "c5", "label": "Friction", "status": "not_started", "score": 0},
            ],
            "edges": [
                {"from": "c1", "to": "c2", "label": "prerequisite"},
                {"from": "c2", "to": "c3", "label": "prerequisite"},
                {"from": "c1", "to": "c4", "label": "related"},
                {"from": "c4", "to": "c5", "label": "prerequisite"},
            ]
        }
    }

@app.get("/analytics/parent/{parent_id}/dashboard")
async def parent_dashboard(parent_id: str):
    """Parent dashboard with child's progress."""
    return {
        "success": True,
        "data": {
            "child_name": "Student Name",
            "class_grade": 8,
            "daily_progress": {"today_minutes": 45, "target_minutes": 60, "completion": 75},
            "weekly_summary": {
                "tests_taken": 5, "avg_score": 78, "concepts_learned": 8,
                "time_spent_hours": 3.5
            },
            "monthly_trend": [72, 75, 78, 80, 82, 78],
            "weak_subjects": ["Hindi", "Social Science"],
            "strong_subjects": ["Science", "English"],
            "upcoming_tests": ["Math Chapter 4 Test - Tomorrow", "Science Quiz - Friday"],
            "ai_recommendations": [
                "Your child needs extra practice in Hindi grammar",
                "Excellent progress in Science this week!"
            ]
        }
    }

@app.get("/analytics/teacher/{teacher_id}/class-dashboard")
async def teacher_dashboard(teacher_id: str, class_grade: int, subject_id: str):
    """Teacher dashboard with class analytics."""
    return {
        "success": True,
        "data": {
            "class_grade": class_grade,
            "total_students": 35,
            "avg_class_score": 74.2,
            "topic_performance": [
                {"topic": "Force", "avg_score": 82, "weak_students": 5},
                {"topic": "Pressure", "avg_score": 65, "weak_students": 14},
                {"topic": "Newton's Laws", "avg_score": 78, "weak_students": 8},
            ],
            "top_performers": [
                {"name": "Student A", "score": 95, "rank": 1},
                {"name": "Student B", "score": 92, "rank": 2},
            ],
            "weak_students": [
                {"name": "Student X", "score": 45, "gaps": ["Pressure", "Atmospheric Pressure"]},
                {"name": "Student Y", "score": 52, "gaps": ["Newton's 3rd Law"]},
            ],
            "class_attendance": 88,
            "assessment_completion": 82
        }
    }

@app.get("/analytics/student/{student_id}/report-card")
async def generate_report_card(student_id: str, format: str = "json"):
    """Generate AI report card — JSON or PDF."""
    report_data = {
        "student_name": "Prudhvi Teja",
        "class_grade": 8,
        "school": "Demo School",
        "period": "June 2026",
        "overall_score": 78.5,
        "grade": "B+",
        "subject_scores": {
            "Mathematics": {"score": 72, "grade": "B", "rank": 8},
            "Science": {"score": 85, "grade": "A", "rank": 3},
            "English": {"score": 90, "grade": "A+", "rank": 2},
            "Hindi": {"score": 65, "grade": "C+", "rank": 18},
            "Social Science": {"score": 78, "grade": "B+", "rank": 9},
        },
        "strengths": ["Science", "English", "Mathematics Problem Solving"],
        "improvement_areas": ["Hindi Grammar", "Social Science Map Work"],
        "ai_recommendations": [
            "Focus on Hindi grammar rules — 3 weak areas identified",
            "Excellent performance in Science — consider advanced topics",
            "Mathematics: Algebra needs more practice"
        ],
        "concepts_mastered": 47,
        "concepts_total": 120,
        "attendance": "92%",
        "teacher_comment": "Good progress overall. Needs to focus on Hindi."
    }

    if format == "pdf":
        return await _generate_pdf_report(report_data)

    return {"success": True, "data": report_data}

async def _generate_pdf_report(data: dict) -> Response:
    """Generate PDF report card using ReportLab."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4

    # Header
    c.setFillColor(colors.HexColor("#6366F1"))
    c.rect(0, H - 100, W, 100, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(W/2, H - 45, "AI Learning Companion")
    c.setFont("Helvetica", 13)
    c.drawCentredString(W/2, H - 70, f"Report Card — {data['period']}")

    # Student Info
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, H - 130, f"Student: {data['student_name']}")
    c.setFont("Helvetica", 12)
    c.drawString(50, H - 150, f"Class: {data['class_grade']}  |  School: {data['school']}")
    c.drawString(50, H - 168, f"Overall Score: {data['overall_score']}%  |  Grade: {data['grade']}")

    # Subject table
    y = H - 220
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Subject-wise Performance")
    y -= 25
    c.setFont("Helvetica-Bold", 11)
    for col, x in [("Subject", 50), ("Score", 250), ("Grade", 320), ("Class Rank", 400)]:
        c.drawString(x, y, col)
    y -= 5
    c.line(50, y, W - 50, y)
    y -= 18

    c.setFont("Helvetica", 11)
    for subject, info in data["subject_scores"].items():
        c.drawString(50, y, subject)
        c.drawString(250, y, f"{info['score']}%")
        c.drawString(320, y, info['grade'])
        c.drawString(400, y, f"#{info['rank']}")
        y -= 20

    # Recommendations
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "AI Recommendations")
    y -= 20
    c.setFont("Helvetica", 10)
    for rec in data["ai_recommendations"]:
        c.drawString(60, y, f"• {rec}")
        y -= 16

    c.save()
    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_card_{data['student_name'].replace(' ','_')}.pdf"}
    )

@app.get("/analytics/health")
async def health():
    return {"status": "ok", "service": "analytics"}
