# AI Learning Companion
### AI-Powered Personalized Learning Platform for School Students (Classes 3–12)

> An intelligent, adaptive learning system that functions as a personal AI teacher — evaluating students, identifying gaps, teaching concepts, and ensuring mastery before progressing.

---

## 🏗️ Architecture Overview

```
ai-learning-companion/
├── web/                    # Next.js 14 Web App (Student/Teacher/Parent/Admin portals)
├── mobile/                 # Flutter App (Android + iOS + Desktop)
├── backend/
│   ├── services/
│   │   ├── auth/           # Authentication & RBAC (FastAPI)
│   │   ├── assessment/     # Quiz, Tests, Evaluation (FastAPI)
│   │   ├── ai-engine/      # GPT, OCR, Adaptive Learning (FastAPI)
│   │   ├── content/        # NCERT Syllabus, Videos, Materials (FastAPI)
│   │   ├── analytics/      # Learning Analytics & Reports (FastAPI)
│   │   └── notification/   # Push Notifications (FastAPI)
│   └── shared/             # Shared models, utils, DB
├── database/               # PostgreSQL migrations & seeds
├── infra/
│   ├── docker/             # Docker Compose
│   ├── k8s/                # Kubernetes manifests
│   └── nginx/              # Reverse proxy config
└── .github/                # CI/CD & Copilot instructions
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- Flutter 3.x
- PostgreSQL 15+
- Redis 7+

### Run with Docker
```bash
cd infra/docker
docker-compose up -d
```

### Web App (Development)
```bash
cd web
npm install
npm run dev
# Opens at http://localhost:3000
```

### Backend Services
```bash
cd backend/services/auth
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

cd backend/services/ai-engine
uvicorn main:app --reload --port 8002
```

### Mobile App
```bash
cd mobile
flutter pub get
flutter run
```

---

## 🎯 Core Features

| Feature | Description |
|---------|-------------|
| **Adaptive Testing** | Easy → Medium → Hard → Application progression |
| **Handwriting OCR** | Photo upload → AI evaluation of handwritten answers |
| **AI Tutor Chat** | GPT-powered grade-appropriate explanations |
| **Learning Gap Analysis** | Knowledge/Skill/Memory/Application/Analytical gaps |
| **Personalized Path** | Weekly roadmap based on performance |
| **Gamification** | Points, Badges, Streaks, Leaderboards |
| **Parent Dashboard** | Daily/Weekly/Monthly progress with graphs |
| **Teacher Dashboard** | Class analytics, weak students, topic analysis |
| **AI Report Cards** | PDF export with concept-wise scoring |
| **Knowledge Graph** | Visual mastery map per student |

---

## 🗺️ NCERT Syllabus Coverage

- **Classes**: 3 to 12
- **Subjects**: Mathematics, Science, Social Science, English, Hindi, Physics, Chemistry, Biology, Computer Science
- **Hierarchy**: Class → Subject → Chapter → Topic → Concept → Sub-Concept

---

## 🛡️ Security

- JWT Authentication with refresh tokens
- RBAC (Student / Teacher / Parent / Admin)
- AES-256 data encryption
- COPPA-compliant child data protection
- Rate limiting & DDoS protection

---

## 📊 Scale Target

- **1 Million Students**
- Kubernetes horizontal scaling
- Redis caching layer
- PostgreSQL with read replicas
- CDN for video/content delivery
- Vector DB (Pinecone) for AI similarity search

---

## 👥 Team Structure

| Role | Count |
|------|-------|
| Product Manager | 1 |
| Backend Engineers | 3 |
| Frontend Engineers | 2 |
| Flutter Engineers | 2 |
| AI/ML Engineers | 2 |
| DevOps Engineer | 1 |
| UI/UX Designer | 1 |
| QA Engineer | 1 |

---

## 🗓️ Roadmap

| Phase | Timeline | Scope |
|-------|----------|-------|
| MVP | Month 1–3 | Auth, MCQ tests, Basic AI tutor, 3 subjects |
| Beta | Month 4–6 | OCR, Video engine, Parent dashboard, Gamification |
| v1.0 | Month 7–9 | All subjects, Knowledge graph, Report cards |
| Scale | Month 10–12 | 1M users, K8s, Analytics, Mobile release |
