"use client";
import { useState } from "react";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

const subjectData = [
  { subject: "Math", score: 72 },
  { subject: "Science", score: 85 },
  { subject: "English", score: 90 },
  { subject: "Hindi", score: 65 },
  { subject: "Social", score: 78 },
];

const weeklyProgress = [
  { day: "Mon", accuracy: 65 }, { day: "Tue", accuracy: 72 },
  { day: "Wed", accuracy: 68 }, { day: "Thu", accuracy: 80 },
  { day: "Fri", accuracy: 85 }, { day: "Sat", accuracy: 88 },
];

const badges = [
  { icon: "🧮", name: "Math Master", earned: true },
  { icon: "🔬", name: "Science Explorer", earned: true },
  { icon: "📖", name: "Reading Champion", earned: false },
  { icon: "🤖", name: "AI Genius", earned: false },
];

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-indigo-700 text-white p-6">
        <div className="flex items-center gap-2 mb-8">
          <span className="text-2xl">🎓</span>
          <span className="font-bold">AI Learning</span>
        </div>
        <nav className="space-y-2">
          {[
            { icon: "🏠", label: "Dashboard", tab: "overview" },
            { icon: "📚", label: "My Subjects", tab: "subjects" },
            { icon: "✏️", label: "Take Test", tab: "test" },
            { icon: "🤖", label: "AI Tutor", tab: "tutor" },
            { icon: "🗺️", label: "Knowledge Map", tab: "knowledge" },
            { icon: "🏆", label: "Achievements", tab: "achievements" },
            { icon: "📊", label: "My Progress", tab: "progress" },
          ].map((item) => (
            <button key={item.tab}
              onClick={() => setActiveTab(item.tab)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                activeTab === item.tab ? "bg-white/20 font-semibold" : "hover:bg-white/10"
              }`}>
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Welcome back, Student! 👋</h1>
            <p className="text-gray-600">Class 8 · 🔥 7-day streak · 1,250 points</p>
          </div>
          <button className="px-6 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700">
            Start Today's Lesson →
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          {[
            { label: "Tests Completed", value: "24", icon: "📝", color: "bg-blue-50 text-blue-700" },
            { label: "Concepts Mastered", value: "47", icon: "✅", color: "bg-green-50 text-green-700" },
            { label: "Weekly Accuracy", value: "82%", icon: "🎯", color: "bg-purple-50 text-purple-700" },
            { label: "Study Streak", value: "7 days", icon: "🔥", color: "bg-orange-50 text-orange-700" },
          ].map((stat, i) => (
            <div key={i} className={`rounded-2xl p-5 ${stat.color}`}>
              <div className="text-3xl mb-2">{stat.icon}</div>
              <div className="text-2xl font-bold">{stat.value}</div>
              <div className="text-sm font-medium">{stat.label}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-6 mb-8">
          {/* Weekly Progress Chart */}
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4">📈 Weekly Accuracy</h3>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={weeklyProgress}>
                <XAxis dataKey="day" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="accuracy" stroke="#6366f1" strokeWidth={2} dot={{ fill: "#6366f1" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Subject Radar */}
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4">🕸️ Subject Performance</h3>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={subjectData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <Radar dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Badges */}
        <div className="bg-white rounded-2xl p-6 shadow-sm mb-6">
          <h3 className="font-semibold text-gray-900 mb-4">🏆 Your Badges</h3>
          <div className="grid grid-cols-4 gap-4">
            {badges.map((b, i) => (
              <div key={i} className={`text-center p-4 rounded-xl ${b.earned ? "bg-yellow-50" : "bg-gray-50 opacity-50"}`}>
                <div className="text-4xl mb-2">{b.icon}</div>
                <div className="text-xs font-medium text-gray-700">{b.name}</div>
                {b.earned && <div className="text-xs text-yellow-600 mt-1">✓ Earned</div>}
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { icon: "📷", label: "Upload Handwritten Answer", desc: "Get AI feedback", color: "bg-purple-600" },
            { icon: "💬", label: "Ask AI Tutor", desc: "Chat with your AI teacher", color: "bg-indigo-600" },
            { icon: "📄", label: "Download Report Card", desc: "PDF export available", color: "bg-green-600" },
          ].map((action, i) => (
            <button key={i} className={`${action.color} text-white rounded-2xl p-5 text-left hover:opacity-90 transition-opacity`}>
              <div className="text-3xl mb-2">{action.icon}</div>
              <div className="font-semibold">{action.label}</div>
              <div className="text-sm opacity-80">{action.desc}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
