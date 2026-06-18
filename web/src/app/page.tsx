"use client";
import Link from "next/link";
import { motion } from "framer-motion";

const features = [
  { icon: "🧠", title: "AI-Powered Tutor", desc: "GPT-4 powered personalized explanations based on your grade level" },
  { icon: "📊", title: "Adaptive Testing", desc: "Questions that adapt to your skill level — Easy to Advanced" },
  { icon: "✍️", title: "Handwriting OCR", desc: "Upload your handwritten answers and get instant AI feedback" },
  { icon: "🗺️", title: "Knowledge Graph", desc: "Visual map of what you've mastered and what needs work" },
  { icon: "🏆", title: "Gamification", desc: "Earn badges, streaks, and climb leaderboards" },
  { icon: "📈", title: "Parent Dashboard", desc: "Real-time progress tracking for parents and teachers" },
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <nav className="flex items-center justify-between px-8 py-4 bg-white shadow-sm">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🎓</span>
          <span className="text-xl font-bold text-indigo-700">AI Learning Companion</span>
        </div>
        <div className="flex gap-4">
          <Link href="/auth/login" className="px-4 py-2 text-indigo-600 hover:bg-indigo-50 rounded-lg font-medium">Login</Link>
          <Link href="/auth/register" className="px-4 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700">Get Started</Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="text-center py-20 px-4">
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold text-gray-900 mb-4"
        >
          Your Personal <span className="text-indigo-600">AI Teacher</span>
        </motion.h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Adaptive learning for Classes 3–12 based on NCERT syllabus. AI identifies your gaps,
          teaches concepts, and ensures mastery before moving forward.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/auth/register?role=student"
            className="px-8 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 text-lg">
            Start Learning Free
          </Link>
          <Link href="/demo"
            className="px-8 py-3 border-2 border-indigo-600 text-indigo-600 rounded-xl font-semibold hover:bg-indigo-50 text-lg">
            Watch Demo
          </Link>
        </div>
        <p className="mt-4 text-sm text-gray-500">Classes 3–12 · Mathematics · Science · All NCERT Subjects</p>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Everything You Need to Excel</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-100"
            >
              <div className="text-4xl mb-3">{f.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{f.title}</h3>
              <p className="text-gray-600 text-sm">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Portals */}
      <section className="bg-indigo-600 text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-8">Portals for Everyone</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { role: "student", icon: "📚", label: "Student Portal" },
              { role: "teacher", icon: "👩‍🏫", label: "Teacher Portal" },
              { role: "parent", icon: "👨‍👩‍👧", label: "Parent Portal" },
              { role: "admin", icon: "⚙️", label: "Admin Portal" },
            ].map((p) => (
              <Link key={p.role} href={`/dashboard/${p.role}`}
                className="bg-white/20 hover:bg-white/30 rounded-xl p-4 transition-colors">
                <div className="text-3xl mb-2">{p.icon}</div>
                <div className="font-medium text-sm">{p.label}</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <footer className="text-center py-8 text-gray-500 text-sm">
        © 2026 AI Learning Companion · Built for Indian School Students · NCERT Aligned
      </footer>
    </main>
  );
}
