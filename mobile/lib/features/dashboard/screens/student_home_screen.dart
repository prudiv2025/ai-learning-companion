import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class StudentHomeScreen extends StatelessWidget {
  const StudentHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Welcome back! 👋', style: Theme.of(context).textTheme.titleMedium),
            Text('Class 8 • 🔥 7-day streak',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.grey)),
          ],
        ),
        actions: [
          IconButton(icon: const Icon(Icons.notifications_outlined), onPressed: () {}),
          const CircleAvatar(radius: 18, backgroundColor: Color(0xFF6366F1),
            child: Text('S', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold))),
          const SizedBox(width: 8),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Today's goal card
            _buildGoalCard(context),
            const SizedBox(height: 20),

            // Stats row
            _buildStatsRow(),
            const SizedBox(height: 20),

            // Continue learning
            Text('Continue Learning', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildSubjectCards(),
            const SizedBox(height: 20),

            // Weekly progress chart
            Text('Weekly Progress', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildWeeklyChart(),
            const SizedBox(height: 20),

            // Quick actions
            Text('Quick Actions', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildQuickActions(context),
          ],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.book_outlined), selectedIcon: Icon(Icons.book), label: 'Subjects'),
          NavigationDestination(icon: Icon(Icons.smart_toy_outlined), selectedIcon: Icon(Icons.smart_toy), label: 'AI Tutor'),
          NavigationDestination(icon: Icon(Icons.bar_chart_outlined), selectedIcon: Icon(Icons.bar_chart), label: 'Progress'),
          NavigationDestination(icon: Icon(Icons.emoji_events_outlined), selectedIcon: Icon(Icons.emoji_events), label: 'Awards'),
        ],
      ),
    );
  }

  Widget _buildGoalCard(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFF6366F1), Color(0xFF8B5CF6)]),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Today's Goal", style: TextStyle(color: Colors.white70, fontSize: 13)),
          const SizedBox(height: 4),
          const Text("Complete Chapter 3: Force & Pressure", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: LinearProgressIndicator(value: 0.6, minHeight: 8, backgroundColor: Colors.white30,
              valueColor: const AlwaysStoppedAnimation<Color>(Colors.white)),
          ),
          const SizedBox(height: 8),
          const Text("60% Complete • 2 topics left", style: TextStyle(color: Colors.white70, fontSize: 12)),
        ],
      ),
    );
  }

  Widget _buildStatsRow() {
    final stats = [
      {'label': 'Tests Done', 'value': '24', 'icon': '📝'},
      {'label': 'Mastered', 'value': '47', 'icon': '✅'},
      {'label': 'Accuracy', 'value': '82%', 'icon': '🎯'},
      {'label': 'Points', 'value': '1250', 'icon': '⭐'},
    ];
    return Row(
      children: stats.map((s) => Expanded(
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: 4),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2))]),
          child: Column(children: [
            Text(s['icon']!, style: const TextStyle(fontSize: 22)),
            const SizedBox(height: 4),
            Text(s['value']!, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            Text(s['label']!, style: const TextStyle(fontSize: 10, color: Colors.grey), textAlign: TextAlign.center),
          ]),
        ),
      )).toList(),
    );
  }

  Widget _buildSubjectCards() {
    final subjects = [
      {'name': 'Mathematics', 'icon': '🧮', 'progress': 0.72, 'color': const Color(0xFF6366F1)},
      {'name': 'Science', 'icon': '🔬', 'progress': 0.85, 'color': const Color(0xFF10B981)},
      {'name': 'English', 'icon': '📖', 'progress': 0.90, 'color': const Color(0xFFF59E0B)},
    ];
    return SizedBox(
      height: 130,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: subjects.length,
        itemBuilder: (context, i) {
          final s = subjects[i];
          return Container(
            width: 160,
            margin: const EdgeInsets.only(right: 12),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)]),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(s['icon'] as String, style: const TextStyle(fontSize: 28)),
              const SizedBox(height: 8),
              Text(s['name'] as String, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
              const SizedBox(height: 8),
              LinearProgressIndicator(
                value: s['progress'] as double,
                backgroundColor: Colors.grey.shade200,
                valueColor: AlwaysStoppedAnimation<Color>(s['color'] as Color),
              ),
              const SizedBox(height: 4),
              Text('${((s['progress'] as double) * 100).toInt()}%',
                style: TextStyle(fontSize: 11, color: s['color'] as Color, fontWeight: FontWeight.w600)),
            ]),
          );
        },
      ),
    );
  }

  Widget _buildWeeklyChart() {
    return Container(
      height: 180,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)]),
      child: BarChart(BarChartData(
        barGroups: [
          BarChartGroupData(x: 0, barRods: [BarChartRodData(toY: 65, color: const Color(0xFF6366F1), width: 20, borderRadius: BorderRadius.circular(4))]),
          BarChartGroupData(x: 1, barRods: [BarChartRodData(toY: 72, color: const Color(0xFF6366F1), width: 20, borderRadius: BorderRadius.circular(4))]),
          BarChartGroupData(x: 2, barRods: [BarChartRodData(toY: 68, color: const Color(0xFF6366F1), width: 20, borderRadius: BorderRadius.circular(4))]),
          BarChartGroupData(x: 3, barRods: [BarChartRodData(toY: 80, color: const Color(0xFF6366F1), width: 20, borderRadius: BorderRadius.circular(4))]),
          BarChartGroupData(x: 4, barRods: [BarChartRodData(toY: 85, color: const Color(0xFF8B5CF6), width: 20, borderRadius: BorderRadius.circular(4))]),
          BarChartGroupData(x: 5, barRods: [BarChartRodData(toY: 88, color: const Color(0xFF8B5CF6), width: 20, borderRadius: BorderRadius.circular(4))]),
          BarChartGroupData(x: 6, barRods: [BarChartRodData(toY: 82, color: const Color(0xFF6366F1), width: 20, borderRadius: BorderRadius.circular(4))]),
        ],
        titlesData: FlTitlesData(
          bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true,
            getTitlesWidget: (v, _) => Text(['M','T','W','T','F','S','S'][v.toInt()], style: const TextStyle(fontSize: 11)))),
          leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
          rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
        ),
        gridData: FlGridData(show: false),
        borderData: FlBorderData(show: false),
      )),
    );
  }

  Widget _buildQuickActions(BuildContext context) {
    final actions = [
      {'icon': '📷', 'label': 'Upload Answer', 'color': const Color(0xFF8B5CF6)},
      {'icon': '💬', 'label': 'Ask AI Tutor', 'color': const Color(0xFF6366F1)},
      {'icon': '📄', 'label': 'Report Card', 'color': const Color(0xFF10B981)},
    ];
    return Row(
      children: actions.map((a) => Expanded(
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: 4),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: a['color'] as Color, borderRadius: BorderRadius.circular(16)),
          child: Column(children: [
            Text(a['icon'] as String, style: const TextStyle(fontSize: 28)),
            const SizedBox(height: 8),
            Text(a['label'] as String, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600), textAlign: TextAlign.center),
          ]),
        ),
      )).toList(),
    );
  }
}
