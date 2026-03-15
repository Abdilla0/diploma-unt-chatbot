import sqlite3
from datetime import datetime, timedelta

def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    # Users table with streak fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language TEXT DEFAULT 'en',
            subject TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP,
            current_streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            last_practice_date TEXT
        )
    ''')
    
    # Answers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            subject TEXT,
            question_id INTEGER,
            user_answer TEXT,
            correct_answer TEXT,
            is_correct BOOLEAN,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    ''')
    
    # ✅ NEW: Topic performance table for weak area detection
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topic_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            subject TEXT,
            topic TEXT,
            question_id INTEGER,
            is_correct BOOLEAN,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id) REFERENCES users (telegram_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized with streak system and weak area detection!")

def add_user(telegram_id, username, first_name):
    """Add a new user to the database"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (telegram_id, username, first_name)
        VALUES (?, ?, ?)
    ''', (telegram_id, username, first_name))
    
    conn.commit()
    conn.close()

def update_user_activity(telegram_id):
    """Update user's last active timestamp"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET last_active = CURRENT_TIMESTAMP
        WHERE telegram_id = ?
    ''', (telegram_id,))
    
    conn.commit()
    conn.close()

def save_answer(telegram_id, subject, question_id, user_answer, correct_answer, is_correct, topic=None):
    """Save user's answer to database with optional topic tracking"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    # Save to answers table
    cursor.execute('''
        INSERT INTO answers (telegram_id, subject, question_id, user_answer, correct_answer, is_correct)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (telegram_id, subject, question_id, user_answer, correct_answer, is_correct))
    
    # ✅ NEW: Save to topic_performance if topic provided
    if topic:
        cursor.execute('''
            INSERT INTO topic_performance (telegram_id, subject, topic, question_id, is_correct)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, subject, topic, question_id, is_correct))
    
    conn.commit()
    conn.close()

def get_user_stats(telegram_id):
    """Get user's overall statistics"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
        FROM answers
        WHERE telegram_id = ?
    ''', (telegram_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] > 0:
        total = result[0]
        correct = result[1]
        percentage = round((correct / total) * 100, 1)
        
        return {
            'total': total,
            'correct': correct,
            'percentage': percentage
        }
    
    return None

def set_user_language(telegram_id, language):
    """Set user's preferred language"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET language = ? WHERE telegram_id = ?
    ''', (language, telegram_id))
    
    conn.commit()
    conn.close()

def get_user_language(telegram_id):
    """Get user's preferred language"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT language FROM users WHERE telegram_id = ?
    ''', (telegram_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else 'en'

# ============================================
# STREAK SYSTEM
# ============================================

def update_streak(telegram_id):
    """Update user's daily streak"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    today = datetime.now().date()
    
    # Get user's last activity
    cursor.execute('''
        SELECT last_practice_date, current_streak 
        FROM users 
        WHERE telegram_id = ?
    ''', (telegram_id,))
    
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return 0
    
    last_date_str, current_streak = result
    
    # Parse last date
    if last_date_str:
        last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
    else:
        last_date = None
    
    # Calculate new streak
    if last_date is None:
        # First time practicing
        new_streak = 1
    elif last_date == today:
        # Already practiced today
        new_streak = current_streak if current_streak else 1
    elif last_date == today - timedelta(days=1):
        # Practiced yesterday - continue streak
        new_streak = (current_streak if current_streak else 0) + 1
    else:
        # Streak broken - start over
        new_streak = 1
    
    # Update database
    cursor.execute('''
        UPDATE users 
        SET current_streak = ?, 
            last_practice_date = ?,
            best_streak = MAX(best_streak, ?)
        WHERE telegram_id = ?
    ''', (new_streak, today.strftime('%Y-%m-%d'), new_streak, telegram_id))
    
    conn.commit()
    conn.close()
    
    return new_streak

def get_user_streak(telegram_id):
    """Get user's current streak"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT current_streak, best_streak 
        FROM users 
        WHERE telegram_id = ?
    ''', (telegram_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'current': result[0] if result[0] else 0,
            'best': result[1] if result[1] else 0
        }
    return {'current': 0, 'best': 0}

# ============================================
# LEADERBOARD SYSTEM
# ============================================

def get_leaderboard(limit=10):
    """Get top users by score"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            u.first_name,
            COUNT(CASE WHEN a.is_correct = 1 THEN 1 END) as correct,
            COUNT(*) as total,
            ROUND(CAST(COUNT(CASE WHEN a.is_correct = 1 THEN 1 END) AS FLOAT) / COUNT(*) * 100, 1) as accuracy,
            u.current_streak
        FROM users u
        INNER JOIN answers a ON u.telegram_id = a.telegram_id
        GROUP BY u.telegram_id
        HAVING total > 0
        ORDER BY accuracy DESC, correct DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    leaderboard = []
    for row in results:
        leaderboard.append({
            'name': row[0],
            'correct': row[1],
            'total': row[2],
            'accuracy': row[3],
            'streak': row[4] if row[4] else 0
        })
    
    return leaderboard

def get_user_rank(telegram_id):
    """Get user's rank on leaderboard"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    # Get all users ranked
    cursor.execute('''
        SELECT 
            u.telegram_id,
            COUNT(CASE WHEN a.is_correct = 1 THEN 1 END) as correct,
            COUNT(*) as total,
            ROUND(CAST(COUNT(CASE WHEN a.is_correct = 1 THEN 1 END) AS FLOAT) / COUNT(*) * 100, 1) as accuracy
        FROM users u
        INNER JOIN answers a ON u.telegram_id = a.telegram_id
        GROUP BY u.telegram_id
        HAVING total > 0
        ORDER BY accuracy DESC, correct DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    # Find user's rank
    for rank, row in enumerate(results, 1):
        if row[0] == telegram_id:
            return rank
    
    return None

# ============================================
# SUBJECT STATS (for topic practice)
# ============================================

def get_subject_stats(telegram_id):
    """Get stats breakdown by subject"""
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            subject,
            COUNT(CASE WHEN is_correct = 1 THEN 1 END) as correct,
            COUNT(*) as total
        FROM answers
        WHERE telegram_id = ?
        GROUP BY subject
    ''', (telegram_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    stats = {}
    for row in results:
        subject = row[0]
        correct = row[1]
        total = row[2]
        percentage = round((correct / total) * 100, 1) if total > 0 else 0
        
        stats[subject] = {
            'correct': correct,
            'total': total,
            'percentage': percentage
        }
    
    return stats

# ============================================
# ✅ NEW: WEAK AREA DETECTION
# ============================================

def get_topic_stats(telegram_id, subject):
    """
    Get statistics per topic for weak area detection
    
    Returns list of dicts with:
    - topic: topic name
    - accuracy: percentage correct
    - status: 'strong'/'moderate'/'weak'
    - recommendation: what to do
    - total: total questions answered
    - correct: correct answers
    """
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            topic,
            COUNT(*) as total,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
        FROM topic_performance
        WHERE telegram_id = ? AND subject = ?
        GROUP BY topic
        HAVING total >= 3
        ORDER BY (CAST(SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100) ASC
    ''', (telegram_id, subject))
    
    results = cursor.fetchall()
    conn.close()
    
    topic_stats = []
    for topic, total, correct in results:
        accuracy = round((correct / total) * 100, 1) if total > 0 else 0
        
        # Determine status based on accuracy
        if accuracy >= 75:
            status = 'strong'
            recommendation = 'Keep Practicing'
        elif accuracy >= 50:
            status = 'moderate'
            recommendation = 'More Practice'
        else:
            status = 'weak'
            recommendation = 'Review Concepts'
        
        topic_stats.append({
            'topic': topic,
            'accuracy': accuracy,
            'status': status,
            'recommendation': recommendation,
            'total': total,
            'correct': correct
        })
    
    return topic_stats

def get_weak_topics(telegram_id, subject, threshold=70):
    """
    Get list of weak topics (below threshold) for focused practice
    
    Args:
        telegram_id: User's Telegram ID
        subject: Subject to analyze
        threshold: Accuracy threshold (default 70%)
    
    Returns:
        List of topic names that are below threshold
    """
    conn = sqlite3.connect('unt_master.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            topic,
            (CAST(SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100) as accuracy
        FROM topic_performance
        WHERE telegram_id = ? AND subject = ?
        GROUP BY topic
        HAVING COUNT(*) >= 3 AND accuracy < ?
        ORDER BY accuracy ASC
    ''', (telegram_id, subject, threshold))
    
    results = cursor.fetchall()
    conn.close()
    
    return [topic for topic, _ in results]