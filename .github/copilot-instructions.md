# AI Learning Companion — Copilot Instructions

## Project
Full-stack EdTech platform: Next.js 14 (web) + Flutter (mobile) + FastAPI microservices (backend) + PostgreSQL + Redis + OpenAI GPT.

## Code Style
- Python: PEP8, type hints, async/await throughout
- TypeScript: strict mode, functional components, no `any`
- Flutter: BLoC pattern, null safety
- All API responses follow `{ success, data, error, meta }` structure

## Architecture Rules
- Each microservice is independently deployable
- Services communicate via REST (sync) or Redis pub/sub (async)
- No direct DB access across services — each owns its schema
- All secrets via environment variables, never hardcoded

## AI Integration
- OpenAI GPT-4o for tutoring, evaluation, gap analysis
- Always include grade level context in prompts
- OCR via Tesseract + GPT-4V for handwriting evaluation
- Adaptive difficulty: Easy(40%) → Medium(30%) → Hard(20%) → Application(10%)

## Security
- JWT tokens: access=15min, refresh=7days
- RBAC roles: student, teacher, parent, admin
- COPPA compliance: no PII storage for under-13 without parental consent
- All child data encrypted at rest (AES-256)
