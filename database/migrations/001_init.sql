-- AI Learning Companion — Complete Database Schema
-- PostgreSQL 15+

-- ─── Extensions ──────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─── Users & Auth ────────────────────────────────────────────────────────────
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student','teacher','parent','admin')),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE schools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    school_id UUID REFERENCES schools(id),
    class_grade INTEGER NOT NULL CHECK (class_grade BETWEEN 3 AND 12),
    roll_number VARCHAR(50),
    date_of_birth DATE,
    parent_id UUID REFERENCES users(id),
    learning_speed VARCHAR(20) DEFAULT 'medium' CHECK (learning_speed IN ('slow','medium','fast')),
    points INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    last_active TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    school_id UUID REFERENCES schools(id),
    subjects TEXT[],
    classes INTEGER[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Syllabus Structure ───────────────────────────────────────────────────────
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    class_grade INTEGER NOT NULL CHECK (class_grade BETWEEN 3 AND 12),
    description TEXT,
    icon_url VARCHAR(255),
    UNIQUE(name, class_grade)
);

CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id UUID REFERENCES subjects(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    estimated_hours DECIMAL(4,1)
);

CREATE TABLE topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER DEFAULT 0
);

CREATE TABLE concepts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    prerequisite_concept_id UUID REFERENCES concepts(id),
    difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
    order_index INTEGER DEFAULT 0
);

-- ─── Questions Bank ───────────────────────────────────────────────────────────
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id UUID REFERENCES concepts(id),
    question_text TEXT NOT NULL,
    question_type VARCHAR(20) DEFAULT 'mcq' CHECK (question_type IN ('mcq','short','long','image')),
    difficulty VARCHAR(20) DEFAULT 'medium' CHECK (difficulty IN ('easy','medium','hard','application','real_world')),
    options JSONB,           -- {"A":"...", "B":"...", "C":"...", "D":"..."}
    correct_answer VARCHAR(10),
    explanation TEXT,
    marks INTEGER DEFAULT 1,
    is_ai_generated BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Assessments ─────────────────────────────────────────────────────────────
CREATE TABLE assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    subject_id UUID REFERENCES subjects(id),
    chapter_id UUID REFERENCES chapters(id),
    assessment_type VARCHAR(30) DEFAULT 'quiz' CHECK (assessment_type IN ('quiz','chapter_test','weekly_test','mock_exam','diagnostic')),
    total_questions INTEGER,
    total_marks INTEGER,
    marks_obtained DECIMAL(6,2),
    percentage DECIMAL(5,2),
    mastery_achieved BOOLEAN DEFAULT false,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    time_taken_seconds INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE assessment_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_id UUID REFERENCES assessments(id) ON DELETE CASCADE,
    question_id UUID REFERENCES questions(id),
    student_answer TEXT,
    is_correct BOOLEAN,
    marks_obtained DECIMAL(4,2),
    ai_feedback JSONB,
    handwriting_image_url VARCHAR(500),
    time_taken_seconds INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Learning Paths ───────────────────────────────────────────────────────────
CREATE TABLE learning_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    subject_id UUID REFERENCES subjects(id),
    generated_by VARCHAR(20) DEFAULT 'ai',
    roadmap JSONB NOT NULL,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active','completed','paused')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Student Knowledge Graph ──────────────────────────────────────────────────
CREATE TABLE student_concept_mastery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    concept_id UUID REFERENCES concepts(id),
    mastery_score DECIMAL(5,2) DEFAULT 0,
    attempts INTEGER DEFAULT 0,
    last_attempted TIMESTAMPTZ,
    mastery_status VARCHAR(20) DEFAULT 'not_started' CHECK (mastery_status IN ('not_started','learning','mastered','needs_revision')),
    UNIQUE(student_id, concept_id)
);

-- ─── Videos ───────────────────────────────────────────────────────────────────
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concept_id UUID REFERENCES concepts(id),
    title VARCHAR(255) NOT NULL,
    duration_seconds INTEGER,
    video_type VARCHAR(20) DEFAULT 'youtube' CHECK (video_type IN ('youtube','ai_generated','animated','whiteboard')),
    url VARCHAR(500),
    youtube_id VARCHAR(50),
    length_category VARCHAR(10) CHECK (length_category IN ('2min','5min','10min')),
    thumbnail_url VARCHAR(500),
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE student_video_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    video_id UUID REFERENCES videos(id),
    watched_seconds INTEGER DEFAULT 0,
    total_seconds INTEGER,
    completed BOOLEAN DEFAULT false,
    watched_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(student_id, video_id)
);

-- ─── Gamification ────────────────────────────────────────────────────────────
CREATE TABLE badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url VARCHAR(500),
    criteria JSONB,
    points_reward INTEGER DEFAULT 0
);

CREATE TABLE student_badges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    badge_id UUID REFERENCES badges(id),
    earned_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(student_id, badge_id)
);

CREATE TABLE leaderboard (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    class_grade INTEGER,
    school_id UUID REFERENCES schools(id),
    subject_id UUID REFERENCES subjects(id),
    period VARCHAR(20) DEFAULT 'weekly' CHECK (period IN ('daily','weekly','monthly','all_time')),
    rank INTEGER,
    points INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Gap Analysis ────────────────────────────────────────────────────────────
CREATE TABLE learning_gaps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID REFERENCES students(id),
    concept_id UUID REFERENCES concepts(id),
    gap_type VARCHAR(20) CHECK (gap_type IN ('knowledge','skill','memory','application','analytical')),
    severity VARCHAR(10) CHECK (severity IN ('high','medium','low')),
    identified_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    is_resolved BOOLEAN DEFAULT false
);

-- ─── Notifications ────────────────────────────────────────────────────────────
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255),
    message TEXT,
    type VARCHAR(30),
    is_read BOOLEAN DEFAULT false,
    data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Indexes ─────────────────────────────────────────────────────────────────
CREATE INDEX idx_students_class ON students(class_grade);
CREATE INDEX idx_assessments_student ON assessments(student_id);
CREATE INDEX idx_concept_mastery_student ON student_concept_mastery(student_id);
CREATE INDEX idx_learning_gaps_student ON learning_gaps(student_id);
CREATE INDEX idx_questions_concept ON questions(concept_id, difficulty);
CREATE INDEX idx_videos_concept ON videos(concept_id);
CREATE INDEX idx_leaderboard_period ON leaderboard(period, class_grade);
