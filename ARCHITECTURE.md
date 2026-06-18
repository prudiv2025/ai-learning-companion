# System Architecture — AI Learning Companion

## 1. High-Level Architecture

```mermaid
graph TB
    subgraph Clients
        A[📱 Flutter Mobile\nAndroid / iOS]
        B[🌐 Next.js Web\nStudent/Teacher/Parent/Admin]
    end

    subgraph API Gateway
        C[Nginx\nRate Limiting + Routing]
    end

    subgraph Microservices
        D[Auth Service\n:8001 JWT/RBAC]
        E[AI Engine\n:8002 GPT/OCR]
        F[Assessment Service\n:8003 Adaptive Tests]
        G[Analytics Service\n:8004 Reports/Dashboards]
        H[Content Service\n:8005 Videos/NCERT]
        I[Notification Service\n:8006 Push/Email]
    end

    subgraph Data Layer
        J[(PostgreSQL 15\nPrimary DB)]
        K[(Redis 7\nCache/Sessions)]
        L[(Pinecone\nVector DB)]
        M[S3/MinIO\nFile Storage]
    end

    subgraph AI Services
        N[OpenAI GPT-4o\nTutor/Evaluation]
        O[GPT-4V\nHandwriting OCR]
        P[YouTube API\nVideo Content]
    end

    A --> C
    B --> C
    C --> D & E & F & G & H & I
    D & E & F & G & H --> J
    D & F --> K
    E --> L
    E --> N & O
    H --> P
    F --> E
    G --> M
```

## 2. Core Learning Loop

```mermaid
sequenceDiagram
    participant S as Student
    participant AS as Assessment Service
    participant AI as AI Engine
    participant CS as Content Service

    S->>AS: Start Assessment
    AS->>AI: Generate Questions (Easy)
    AI-->>AS: Questions
    AS-->>S: Show Quiz

    S->>AS: Submit Answers
    AS->>AS: Calculate Score

    alt Score >= 80% (Mastery)
        AS->>AI: Generate Next Level Questions
        AS-->>S: Progress to Next Difficulty
    else Score < 80%
        AS->>AI: Identify Weak Concepts
        AI->>CS: Fetch Video for Weak Concept
        CS-->>S: Recommend Video
        S->>S: Watch Video
        S->>AS: Retake Assessment
    end
```

## 3. Adaptive Testing Engine

```mermaid
graph LR
    A[Start: Easy\n40% weightage] -->|Score >= 80%| B[Medium\n30% weightage]
    B -->|Score >= 80%| C[Hard\n20% weightage]
    C -->|Score >= 80%| D[Application\n10% weightage]
    D -->|Score >= 80%| E[Real World\nBonus Level]
    E -->|Complete| F[🎉 Chapter Mastered!]

    A -->|Score < 80%| G[Watch Video\nRevise Concept]
    B -->|Score < 80%| G
    C -->|Score < 80%| G
    G --> A
```

## 4. AI Pipeline

```mermaid
graph TD
    A[Student Input] --> B{Input Type}
    B -->|Text Answer| C[GPT-4o Evaluation]
    B -->|Handwritten Image| D[GPT-4V OCR + Evaluation]
    B -->|Chat Question| E[GPT-4o Tutor\nGrade-Contextual]
    B -->|Assessment Results| F[Gap Analysis Engine]

    C --> G[Score + Feedback]
    D --> G
    E --> H[Grade-Appropriate Explanation]
    F --> I[Learning Gap Report]
    I --> J[Personalized Learning Path]
    J --> K[Video Recommendations]
    K --> L[Next Assessment]
```

## 5. Database ER Diagram

```mermaid
erDiagram
    USERS ||--o{ STUDENTS : "has"
    USERS ||--o{ TEACHERS : "has"
    SCHOOLS ||--o{ STUDENTS : "enrolls"
    SCHOOLS ||--o{ TEACHERS : "employs"
    STUDENTS ||--o{ ASSESSMENTS : "takes"
    STUDENTS ||--o{ STUDENT_CONCEPT_MASTERY : "has"
    STUDENTS ||--o{ LEARNING_PATHS : "follows"
    STUDENTS ||--o{ LEARNING_GAPS : "has"
    SUBJECTS ||--o{ CHAPTERS : "contains"
    CHAPTERS ||--o{ TOPICS : "contains"
    TOPICS ||--o{ CONCEPTS : "contains"
    CONCEPTS ||--o{ QUESTIONS : "has"
    CONCEPTS ||--o{ VIDEOS : "has"
    ASSESSMENTS ||--o{ ASSESSMENT_ANSWERS : "contains"
    QUESTIONS ||--o{ ASSESSMENT_ANSWERS : "answered in"
```

## 6. Deployment Architecture (Kubernetes)

```mermaid
graph TB
    subgraph Cloud Provider
        subgraph K8s Cluster
            subgraph Ingress
                A[Nginx Ingress\nController]
            end
            subgraph Services
                B[auth-service\n3 replicas]
                C[ai-engine\n2 replicas]
                D[assessment\n3 replicas]
                E[analytics\n2 replicas]
                F[content\n2 replicas]
            end
            subgraph Stateful
                G[PostgreSQL\nPrimary + 2 Replicas]
                H[Redis Cluster\n3 nodes]
            end
        end
        I[CDN\nVideo/Assets]
        J[S3\nFile Storage]
        K[Pinecone\nVector DB]
    end
    L[OpenAI API] -.->|External| C
```

## 7. Security Architecture

```mermaid
graph TD
    A[Client Request] --> B[TLS/HTTPS Termination]
    B --> C[Rate Limiting\n30 req/min per IP]
    C --> D[JWT Verification]
    D --> E{Role Check\nRBAC}
    E -->|Student| F[Student Routes Only]
    E -->|Teacher| G[Teacher + Student Routes]
    E -->|Parent| H[Parent + Child Routes]
    E -->|Admin| I[All Routes]
    F & G & H & I --> J[Service Handler]
    J --> K[DB Query\nRow-level Security]
```

## 8. Development Roadmap

| Phase | Duration | Features |
|-------|----------|----------|
| **MVP** | Month 1–3 | Auth, MCQ tests, GPT tutor, 3 subjects (Math/Science/English), basic dashboard |
| **Beta** | Month 4–6 | OCR handwriting, video engine, parent dashboard, gamification, gap analysis |
| **v1.0** | Month 7–9 | All 9 subjects, knowledge graph, PDF report cards, mobile app launch |
| **Scale** | Month 10–12 | 1M users, K8s, full analytics, SR-IOV, leaderboards, AI video generation |

## 9. Cost Estimation (Monthly at 10K Students)

| Item | Cost |
|------|------|
| Cloud Compute (K8s) | ₹15,000 |
| PostgreSQL RDS | ₹8,000 |
| Redis Cache | ₹3,000 |
| OpenAI API (GPT-4o) | ₹12,000 |
| CDN + S3 Storage | ₹4,000 |
| Firebase Notifications | ₹1,000 |
| **Total** | **~₹43,000/month** |
