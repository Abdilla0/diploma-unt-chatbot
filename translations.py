# translations.py - Complete translation system with ALL topics added
# ✅ FIXED: Removed "UNT Silkway Bot" - now uses generic terms

TRANSLATIONS = {
    'welcome': {
        'en': """🎓 **Welcome to UNT Preparation Assistant!**

I'm your AI study assistant for UNT exam preparation.

**What I can do:**
📚 Explain any topic
❓ Give practice questions
📊 Track your progress
💡 Answer your questions
🎯 Help you prepare for UNT""",
        'ru': """🎓 **Добро пожаловать в помощник по подготовке к ҰБТ!**

Я ваш AI помощник для подготовки к ҰБТ.

**Что я могу:**
📚 Объяснить любую тему
❓ Дать практические вопросы
📊 Отслеживать ваш прогресс
💡 Ответить на вопросы
🎯 Помочь подготовиться к ҰБТ""",
        'kk': """🎓 **ҰБТ дайындық көмекшісіне қош келдіңіз!**

Мен сіздің ҰБТ-ға дайындалуға арналған AI көмекшісімін.

**Мен не істей аламын:**
📚 Кез келген тақырыпты түсіндіру
❓ Жаттығу сұрақтарын беру
📊 Прогресіңізді қадағалау
💡 Сұрақтарға жауап беру
🎯 ҰБТ-ға дайындалуға көмектесу"""
    },
    
    'choose_subject': {
        'en': "Great! Now choose a subject to practice:",
        'ru': "Отлично! Теперь выберите предмет для практики:",
        'kk': "Керемет! Енді жаттығу үшін пәнді таңдаңыз:"
    },
    
    'subject_chosen': {
        'en': "Perfect! You chose **{subject}**\n\nWhat would you like to do?",
        'ru': "Отлично! Вы выбрали **{subject}**\n\nЧто вы хотите сделать?",
        'kk': "Керемет! Сіз **{subject}** таңдадыңыз\n\nНеістегіңіз келеді?"
    },
    
    # Menu buttons
    'btn_practice': {
        'en': '❓ Practice Questions',
        'ru': '❓ Практические вопросы',
        'kk': '❓ Жаттығу сұрақтары'
    },
    'btn_explain': {
        'en': '📚 Explain Topic',
        'ru': '📚 Объяснить тему',
        'kk': '📚 Тақырыпты түсіндіру'
    },
    'btn_ask': {
        'en': '💬 Ask Question',
        'ru': '💬 Задать вопрос',
        'kk': '💬 Сұрақ қою'
    },
    'btn_progress': {
        'en': '📊 My Progress',
        'ru': '📊 Мой прогресс',
        'kk': '📊 Менің прогресім'
    },
    'btn_change_subject': {
        'en': '🔄 Change Subject',
        'ru': '🔄 Сменить предмет',
        'kk': '🔄 Пәнді өзгерту'
    },
    'btn_next': {
        'en': '➡️ Next Question',
        'ru': '➡️ Следующий вопрос',
        'kk': '➡️ Келесі сұрақ'
    },
    'btn_menu': {
        'en': '🏠 Main Menu',
        'ru': '🏠 Главное меню',
        'kk': '🏠 Басты мәзір'
    },
    'btn_leaderboard': {
        'en': '🏆 Leaderboard',
        'ru': '🏆 Таблица лидеров',
        'kk': '🏆 Көшбасшылар тақтасы'
    },
    'btn_topics': {
        'en': '📚 Choose Topic',
        'ru': '📚 Выбрать тему',
        'kk': '📚 Тақырыпты таңдау'
    },
    
    # Subjects
    'subject_math': {
        'en': '📐 Mathematics',
        'ru': '📐 Математика',
        'kk': '📐 Математика'
    },
    'subject_reading': {
        'en': '📖 Reading Literacy',
        'ru': '📖 Грамотность чтения',
        'kk': '📖 Оқу сауаттылығы'
    },
    'subject_history': {
        'en': '🏛️ History of Kazakhstan',
        'ru': '🏛️ История Казахстана',
        'kk': '🏛️ Қазақстан тарихы'
    },
    'subject_physics': {
        'en': '⚡ Physics',
        'ru': '⚡ Физика',
        'kk': '⚡ Физика'
    },
    'subject_chemistry': {
        'en': '⚗️ Chemistry',
        'ru': '⚗️ Химия',
        'kk': '⚗️ Химия'
    },
    'subject_biology': {
        'en': '🧬 Biology',
        'ru': '🧬 Биология',
        'kk': '🧬 Биология'
    },
    'subject_geography': {
        'en': '🌍 Geography',
        'ru': '🌍 География',
        'kk': '🌍 География'
    },
    
    # ==========================================
    # MATHEMATICS TOPICS
    # ==========================================
    'algebra': {
        'en': '🔤 Algebra',
        'ru': '🔤 Алгебра',
        'kk': '🔤 Алгебра'
    },
    'geometry': {
        'en': '📐 Geometry',
        'ru': '📐 Геометрия',
        'kk': '📐 Геометрия'
    },
    'percentages': {
        'en': '💯 Percentages',
        'ru': '💯 Проценты',
        'kk': '💯 Пайыздар'
    },
    'equations': {
        'en': '⚖️ Equations',
        'ru': '⚖️ Уравнения',
        'kk': '⚖️ Теңдеулер'
    },
    'word_problems': {
        'en': '📝 Word Problems',
        'ru': '📝 Текстовые задачи',
        'kk': '📝 Мәтінді есептер'
    },
    
    # ==========================================
    # PHYSICS TOPICS
    # ==========================================
    'mechanics': {
        'en': '🚗 Mechanics',
        'ru': '🚗 Механика',
        'kk': '🚗 Механика'
    },
    'electricity': {
        'en': '⚡ Electricity',
        'ru': '⚡ Электричество',
        'kk': '⚡ Электр'
    },
    'optics': {
        'en': '💡 Optics',
        'ru': '💡 Оптика',
        'kk': '💡 Оптика'
    },
    'thermodynamics': {
        'en': '🌡️ Thermodynamics',
        'ru': '🌡️ Термодинамика',
        'kk': '🌡️ Термодинамика'
    },
    'waves': {
        'en': '🌊 Waves',
        'ru': '🌊 Волны',
        'kk': '🌊 Толқындар'
    },
    
    # ==========================================
    # CHEMISTRY TOPICS
    # ==========================================
    'atomic_structure': {
        'en': '⚛️ Atomic Structure',
        'ru': '⚛️ Атомная структура',
        'kk': '⚛️ Атом құрылымы'
    },
    'chemical_bonding': {
        'en': '🔗 Chemical Bonding',
        'ru': '🔗 Химические связи',
        'kk': '🔗 Химиялық байланыс'
    },
    'reactions': {
        'en': '⚗️ Reactions',
        'ru': '⚗️ Реакции',
        'kk': '⚗️ Реакциялар'
    },
    'acids_bases': {
        'en': '🧪 Acids & Bases',
        'ru': '🧪 Кислоты и основания',
        'kk': '🧪 Қышқылдар және негіздер'
    },
    'organic_chemistry': {
        'en': '🧬 Organic Chemistry',
        'ru': '🧬 Органическая химия',
        'kk': '🧬 Органикалық химия'
    },
    
    # ==========================================
    # BIOLOGY TOPICS
    # ==========================================
    'cell_biology': {
        'en': '🔬 Cell Biology',
        'ru': '🔬 Биология клетки',
        'kk': '🔬 Жасуша биологиясы'
    },
    'genetics': {
        'en': '🧬 Genetics',
        'ru': '🧬 Генетика',
        'kk': '🧬 Генетика'
    },
    'ecology': {
        'en': '🌿 Ecology',
        'ru': '🌿 Экология',
        'kk': '🌿 Экология'
    },
    'human_biology': {
        'en': '🧑 Human Biology',
        'ru': '🧑 Биология человека',
        'kk': '🧑 Адам биологиясы'
    },
    'evolution': {
        'en': '🦴 Evolution',
        'ru': '🦴 Эволюция',
        'kk': '🦴 Эволюция'
    },
    
    # ==========================================
    # HISTORY TOPICS
    # ==========================================
    'kazakhstan_history': {
        'en': '🇰🇿 Kazakhstan History',
        'ru': '🇰🇿 История Казахстана',
        'kk': '🇰🇿 Қазақстан тарихы'
    },
    'world_history': {
        'en': '🌍 World History',
        'ru': '🌍 Всемирная история',
        'kk': '🌍 Әлем тарихы'
    },
    'ancient_civilizations': {
        'en': '🏛️ Ancient Civilizations',
        'ru': '🏛️ Древние цивилизации',
        'kk': '🏛️ Ежелгі өркениеттер'
    },
    'modern_history': {
        'en': '📰 Modern History',
        'ru': '📰 Новейшая история',
        'kk': '📰 Жаңа заман тарихы'
    },
    'cultural_history': {
        'en': '🎭 Cultural History',
        'ru': '🎭 Культурная история',
        'kk': '🎭 Мәдени тарих'
    },
    
    # ==========================================
    # GEOGRAPHY TOPICS
    # ==========================================
    'physical_geography': {
        'en': '🏔️ Physical Geography',
        'ru': '🏔️ Физическая география',
        'kk': '🏔️ Физикалық география'
    },
    'human_geography': {
        'en': '👥 Human Geography',
        'ru': '👥 География населения',
        'kk': '👥 Халық географиясы'
    },
    'kazakhstan_geography': {
        'en': '🇰🇿 Kazakhstan Geography',
        'ru': '🇰🇿 География Казахстана',
        'kk': '🇰🇿 Қазақстан географиясы'
    },
    'world_geography': {
        'en': '🗺️ World Geography',
        'ru': '🗺️ География мира',
        'kk': '🗺️ Әлем географиясы'
    },
    'environmental_geography': {
        'en': '🌱 Environmental Geography',
        'ru': '🌱 Экологическая география',
        'kk': '🌱 Экологиялық география'
    },
    
    # ==========================================
    # TOPIC SELECTION (NEW)
    # ==========================================
    'all_topics': {
        'en': '📚 All Topics (Mixed)',
        'ru': '📚 Все темы (Смешанные)',
        'kk': '📚 Барлық тақырыптар (Аралас)'
    },
    
    # Prompts
    'ask_topic': {
        'en': "📚 What topic would you like me to explain?\n\nExample: 'quadratic equations' or 'photosynthesis'",
        'ru': "📚 Какую тему вы хотите, чтобы я объяснил?\n\nПример: 'квадратные уравнения' или 'фотосинтез'",
        'kk': "📚 Қандай тақырыпты түсіндіргімді келеді?\n\nМысал: 'квадраттық теңдеулер' немесе 'фотосинтез'"
    },
    'ask_question': {
        'en': "💬 What's your question? Ask me anything about your studies!",
        'ru': "💬 Какой у вас вопрос? Спросите меня что угодно о ваших занятиях!",
        'kk': "💬 Сұрағыңыз қандай? Оқу туралы кез келген нәрсені сұраңыз!"
    },
    'ready_more': {
        'en': "Ready for more?",
        'ru': "Готовы продолжить?",
        'kk': "Жалғастыруға дайынсыз ба?"
    },
    'correct': {
        'en': 'Correct!',
        'ru': 'Правильно!',
        'kk': 'Дұрыс!'
    },
    'incorrect': {
        'en': 'Not quite right.',
        'ru': 'Неправильно.',
        'kk': 'Дұрыс емес.'
    },
    'your_stats': {
        'en': '📊 **Your Stats:** {correct}/{total} ({percentage}%)',
        'ru': '📊 **Ваша статистика:** {correct}/{total} ({percentage}%)',
        'kk': '📊 **Сіздің статистикаңыз:** {correct}/{total} ({percentage}%)'
    },
    'no_questions': {
        'en': "Sorry, no questions available for this subject yet!",
        'ru': "Извините, пока нет вопросов по этому предмету!",
        'kk': "Кешіріңіз, бұл пән бойынша әзірше сұрақтар жоқ!"
    },
    'start_practice_first': {
        'en': "Please start practice first with ❓ Practice Questions",
        'ru': "Пожалуйста, начните практику с ❓ Практические вопросы",
        'kk': "Алдымен ❓ Жаттығу сұрақтары арқылы жаттығуды бастаңыз"
    },
    'no_stats': {
        'en': "📊 You haven't answered any questions yet!\n\nStart practicing with ❓ Practice Questions",
        'ru': "📊 Вы еще не ответили ни на один вопрос!\n\nНачните практику с ❓ Практические вопросы",
        'kk': "📊 Сіз әлі ешбір сұраққа жауап бермедіңіз!\n\n❓ Жаттығу сұрақтары арқылы бастаңыз"
    },
    'progress_title': {
        'en': '📊 **Your UNT Preparation Progress**',
        'ru': '📊 **Ваш прогресс подготовки к ҰБТ**',
        'kk': '📊 **ҰБТ-ға дайындық прогресіңіз**'
    },
    'overall_stats': {
        'en': '**Overall Stats:**',
        'ru': '**Общая статистика:**',
        'kk': '**Жалпы статистика:**'
    },
    'total_questions': {
        'en': '✓ Total questions: {total}',
        'ru': '✓ Всего вопросов: {total}',
        'kk': '✓ Барлығы сұрақтар: {total}'
    },
    'correct_answers': {
        'en': '✓ Correct answers: {correct}',
        'ru': '✓ Правильных ответов: {correct}',
        'kk': '✓ Дұрыс жауаптар: {correct}'
    },
    'accuracy': {
        'en': '✓ Accuracy: {percentage}%',
        'ru': '✓ Точность: {percentage}%',
        'kk': '✓ Дәлдік: {percentage}%'
    },
    'keep_practicing': {
        'en': 'Keep practicing to improve your score! 💪',
        'ru': 'Продолжайте практиковаться, чтобы улучшить результат! 💪',
        'kk': 'Нәтижені жақсарту үшін жаттығуды жалғастырыңыз! 💪'
    },
    'streak_message': {
        'en': '🔥 **{days}-Day Streak!**\n\n{emoji} Keep it up! Your best: {best} days',
        'ru': '🔥 **Серия {days} дней!**\n\n{emoji} Так держать! Ваш рекорд: {best} дней',
        'kk': '🔥 **{days} күндік серия!**\n\n{emoji} Жалғастырыңыз! Рекордыңыз: {best} күн'
    },
    'leaderboard_title': {
        'en': '🏆 **Top 10 Students**\n\n',
        'ru': '🏆 **Топ 10 студентов**\n\n',
        'kk': '🏆 **Үздік 10 студент**\n\n'
    },
    'your_rank': {
        'en': '\n📍 **Your Rank:** #{rank}',
        'ru': '\n📍 **Ваше место:** #{rank}',
        'kk': '\n📍 **Сіздің орныңыз:** #{rank}'
    },
    'no_leaderboard': {
        'en': '🏆 Leaderboard is empty!\n\nBe the first to answer questions!',
        'ru': '🏆 Таблица лидеров пуста!\n\nБудьте первым, кто ответит на вопросы!',
        'kk': '🏆 Көшбасшылар тақтасы бос!\n\nСұрақтарға жауап берген бірінші болыңыз!'
    },
    'choose_topic': {
        'en': '📚 Choose a topic to practice:',
        'ru': '📚 Выберите тему для практики:',
        'kk': '📚 Жаттығу үшін тақырыпты таңдаңыз:'
    },
    'weak_areas': {
        'en': '\n\n💡 **Focus on your weak areas:**',
        'ru': '\n\n💡 **Сосредоточьтесь на слабых местах:**',
        'kk': '\n\n💡 **Әлсіз жақтарға назар аударыңыз:**'
    }
}

def t(key, lang='en', **kwargs):
    """Get translation for key in language"""
    text = TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get('en', key))
    if kwargs:
        text = text.format(**kwargs)
    return text


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def get_subject_topics(subject):
    """
    Get list of topic keys for a given subject.
    Returns empty list if subject has no topics defined.
    
    Usage:
        topics = get_subject_topics('mathematics')
        # Returns: ['algebra', 'geometry', 'percentages', 'equations', 'word_problems']
    """
    topic_map = {
        'mathematics': ['algebra', 'geometry', 'percentages', 'equations', 'word_problems'],
        'math': ['algebra', 'geometry', 'percentages', 'equations', 'word_problems'],  # Alias
        'physics': ['mechanics', 'electricity', 'optics', 'thermodynamics', 'waves'],
        'chemistry': ['atomic_structure', 'chemical_bonding', 'reactions', 'acids_bases', 'organic_chemistry'],
        'biology': ['cell_biology', 'genetics', 'ecology', 'human_biology', 'evolution'],
        'history': ['kazakhstan_history', 'world_history', 'ancient_civilizations', 'modern_history', 'cultural_history'],
        'geography': ['physical_geography', 'human_geography', 'kazakhstan_geography', 'world_geography', 'environmental_geography']
    }
    return topic_map.get(subject, [])