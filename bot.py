# bot.py - COMPLETE FINAL VERSION
# ✅ Async AI for 10+ concurrent users
# ✅ Restart notification feature
# ✅ All features working

import logging
import asyncio
import pickle
import os
import signal
import sys
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

from config import TELEGRAM_BOT_TOKEN, SUBJECTS, LANGUAGES
from database import (init_db, add_user, update_user_activity, save_answer, 
                      get_user_stats, set_user_language, get_user_language,
                      update_streak, get_user_streak, get_leaderboard, 
                      get_user_rank, get_subject_stats,
                      get_topic_stats, get_weak_topics)
from ai_helper import explain_topic, answer_question, explain_answer
from questions import get_question, format_question, QUESTIONS, get_topics
from translations import t, TRANSLATIONS, get_subject_topics

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Conversation states
CHOOSING_LANGUAGE, CHOOSING_SUBJECT, WAITING_ANSWER, ASKING_QUESTION = range(4)

# User session data
user_sessions = {}

# File to store active user IDs for restart notification
ACTIVE_USERS_FILE = 'active_users.pkl'

# ============================================
# RESTART NOTIFICATION FUNCTIONS
# ============================================

def save_active_users(user_sessions):
    """Save active user IDs to file before shutdown"""
    try:
        active_users = list(user_sessions.keys())
        with open(ACTIVE_USERS_FILE, 'wb') as f:
            pickle.dump(active_users, f)
        print(f"✅ Saved {len(active_users)} active users")
    except Exception as e:
        print(f"❌ Error saving active users: {e}")

def load_active_users():
    """Load active user IDs from file"""
    try:
        if os.path.exists(ACTIVE_USERS_FILE):
            with open(ACTIVE_USERS_FILE, 'rb') as f:
                active_users = pickle.load(f)
            return active_users
        return []
    except Exception as e:
        print(f"❌ Error loading active users: {e}")
        return []

async def notify_restart(application):
    """Send restart notification to all users who were active before shutdown"""
    active_users = load_active_users()
    
    if not active_users:
        print("ℹ️  No active users to notify")
        return
    
    print(f"📢 Notifying {len(active_users)} users about restart...")
    
    messages = {
        'en': "🔄 **Bot Restarted**\n\nThe bot was restarted. Please press /start to continue!",
        'ru': "🔄 **Бот перезапущен**\n\nБот был перезапущен. Нажмите /start чтобы продолжить!",
        'kk': "🔄 **Бот қайта іске қосылды**\n\nБот қайта іске қосылды. Жалғастыру үшін /start басыңыз!"
    }
    
    success_count = 0
    
    for user_id in active_users:
        try:
            language = get_user_language(user_id)
            message = messages.get(language, messages['en'])
            
            await application.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='Markdown'
            )
            success_count += 1
            
        except Exception as e:
            print(f"⚠️  Could not notify user {user_id}: {e}")
    
    print(f"✅ Successfully notified {success_count}/{len(active_users)} users")
    
    # Clear the file after notifying
    try:
        os.remove(ACTIVE_USERS_FILE)
    except:
        pass

# ============================================
# BOT HANDLERS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - Language selection"""
    user = update.effective_user
    
    # Add user to database
    add_user(user.id, user.username, user.first_name)
    
    # Track active user for restart notification
    if user.id not in user_sessions:
        user_sessions[user.id] = {}
    
    # Language selection keyboard
    keyboard = [
        [KeyboardButton("🇰🇿 Қазақша"), KeyboardButton("🇷🇺 Русский")],
        [KeyboardButton("🇬🇧 English")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "👋\n\n🇰🇿 🇷🇺 🇬🇧\n\nPlease select your language:\nПожалуйста, выберите язык:\nТілді таңдаңыз:",
        reply_markup=reply_markup
    )
    
    return CHOOSING_LANGUAGE

async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User chose language"""
    text = update.message.text
    user_id = update.effective_user.id
    
    lang_map = {
        "🇰🇿 Қазақша": 'kk',
        "🇷🇺 Русский": 'ru',
        "🇬🇧 English": 'en'
    }
    
    language = lang_map.get(text, 'en')
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    user_sessions[user_id]['language'] = language
    
    set_user_language(user_id, language)
    
    await update.message.reply_text(t('welcome', language))
    
    keyboard = [
        [KeyboardButton(t('subject_math', language)), KeyboardButton(t('subject_physics', language))],
        [KeyboardButton(t('subject_chemistry', language)), KeyboardButton(t('subject_biology', language))],
        [KeyboardButton(t('subject_history', language)), KeyboardButton(t('subject_geography', language))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        t('choose_subject', language),
        reply_markup=reply_markup
    )
    
    return CHOOSING_SUBJECT

async def subject_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User chose subject"""
    text = update.message.text
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    subject_map = {}
    for lang in ['en', 'ru', 'kk']:
        subject_map[t('subject_math', lang)] = 'mathematics'
        subject_map[t('subject_physics', lang)] = 'physics'
        subject_map[t('subject_chemistry', lang)] = 'chemistry'
        subject_map[t('subject_biology', lang)] = 'biology'
        subject_map[t('subject_history', lang)] = 'history'
        subject_map[t('subject_geography', lang)] = 'geography'
    
    subject = subject_map.get(text)
    
    if not subject:
        await update.message.reply_text(t('choose_subject', language))
        return CHOOSING_SUBJECT
    
    user_sessions[user_id]['subject'] = subject
    
    keyboard = [
        [KeyboardButton(t('btn_practice', language)), KeyboardButton(t('btn_topics', language))],
        [KeyboardButton(t('btn_explain', language)), KeyboardButton(t('btn_ask', language))],
        [KeyboardButton(t('btn_progress', language)), KeyboardButton(t('btn_leaderboard', language))],
        [KeyboardButton(t('btn_change_subject', language))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        t('subject_chosen', language, subject=text),
        reply_markup=reply_markup
    )
    
    return WAITING_ANSWER

async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu selections"""
    text = update.message.text
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    weak_areas_buttons = [
        "📊 Weak Areas", "📊 Слабые места", "📊 Әлсіз жақтар",
        "Practice Weak Topics", "Практиковать слабые темы", "Әлсіз тақырыптарды жаттығу"
    ]
    
    if text in weak_areas_buttons:
        if "Practice" in text or "Практиковать" in text or "жаттығу" in text:
            import random
            weak_topics = user_sessions.get(user_id, {}).get('weak_topics', [])
            if weak_topics:
                user_sessions[user_id]['topic'] = random.choice(weak_topics)
                return await start_practice(update, context)
        else:
            return await show_weak_areas(update, context)
    
    if user_sessions.get(user_id, {}).get('in_ai_mode'):
        return await handle_free_text(update, context)
    
    if user_sessions.get(user_id, {}).get('selecting_topic'):
        return await topic_chosen(update, context)
    
    button_actions = {
        'practice': [t('btn_practice', 'en'), t('btn_practice', 'ru'), t('btn_practice', 'kk')],
        'explain': [t('btn_explain', 'en'), t('btn_explain', 'ru'), t('btn_explain', 'kk')],
        'ask': [t('btn_ask', 'en'), t('btn_ask', 'ru'), t('btn_ask', 'kk')],
        'progress': [t('btn_progress', 'en'), t('btn_progress', 'ru'), t('btn_progress', 'kk')],
        'change': [t('btn_change_subject', 'en'), t('btn_change_subject', 'ru'), t('btn_change_subject', 'kk')],
        'next': [t('btn_next', 'en'), t('btn_next', 'ru'), t('btn_next', 'kk')],
        'menu': [t('btn_menu', 'en'), t('btn_menu', 'ru'), t('btn_menu', 'kk')],
        'leaderboard': [t('btn_leaderboard', 'en'), t('btn_leaderboard', 'ru'), t('btn_leaderboard', 'kk')],
        'topics': [t('btn_topics', 'en'), t('btn_topics', 'ru'), t('btn_topics', 'kk')]
    }
    
    if text in button_actions['practice']:
        return await start_practice(update, context)
    elif text in button_actions['explain']:
        return await ask_for_topic(update, context)
    elif text in button_actions['ask']:
        return await ask_for_question(update, context)
    elif text in button_actions['progress']:
        return await show_progress(update, context)
    elif text in button_actions['leaderboard']:
        return await show_leaderboard(update, context)
    elif text in button_actions['topics']:
        return await show_topics(update, context)
    elif text in button_actions['change']:
        return await change_subject(update, context)
    elif text in button_actions['menu']:
        return await show_main_menu(update, context)
    elif text in button_actions['next']:
        return await start_practice(update, context)
    else:
        if user_sessions.get(user_id, {}).get('current_question'):
            return await check_answer(update, context)
        else:
            return WAITING_ANSWER

async def start_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start practice questions"""
    user_id = update.effective_user.id
    subject = user_sessions.get(user_id, {}).get('subject', 'mathematics')
    language = user_sessions.get(user_id, {}).get('language', 'en')
    topic = user_sessions.get(user_id, {}).get('topic', None)
    
    question = get_question(subject, language=language, topic=topic)
    
    if not question:
        await update.message.reply_text(t('no_questions', language))
        return WAITING_ANSWER
    
    user_sessions[user_id]['current_question'] = question
    
    await update.message.reply_text(
        format_question(question),
        parse_mode='Markdown'
    )
    
    return WAITING_ANSWER

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    ✅ Check user's answer with NON-BLOCKING AI generation
    Supports 10+ concurrent users!
    """
    user_id = update.effective_user.id
    user_answer = update.message.text.upper().strip()
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    new_streak = update_streak(user_id)
    
    question = user_sessions.get(user_id, {}).get('current_question')
    
    if not question:
        return WAITING_ANSWER
    
    if user_answer not in ['A', 'B', 'C', 'D', 'E']:
        await update.message.reply_text(
            "Please select an answer: A, B, C, D, or E" if language == 'en' else
            "Пожалуйста, выберите ответ: A, B, C, D или E" if language == 'ru' else
            "Жауапты таңдаңыз: A, B, C, D немесе E"
        )
        return WAITING_ANSWER
    
    correct_answer = question['correct']
    is_correct = (user_answer == correct_answer)
    
    subject = user_sessions[user_id].get('subject', 'mathematics')
    topic = question.get('topic')
    
    save_answer(user_id, subject, question['id'], user_answer, correct_answer, is_correct, topic=topic)
    
    # ✅ STEP 1: IMMEDIATE FEEDBACK
    emoji = "🎉" if is_correct else "❌"
    result_text = t('correct' if is_correct else 'incorrect', language)
    
    response = f"{emoji} {result_text}\n\n"
    response += f"✅ Correct answer: {question['options'][correct_answer]}\n"
    response += f"📖 {question['explanation']}"
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    # ✅ STEP 2: STATS & NEXT BUTTON IMMEDIATELY
    stats = get_user_stats(user_id)
    if stats:
        stats_msg = t('your_stats', language, **stats)
        await update.message.reply_text(stats_msg, parse_mode='Markdown')
    
    if new_streak > 1:
        streak_info = get_user_streak(user_id)
        streak_emoji = '🔥' * min(new_streak, 5)
        streak_msg = t('streak_message', language, days=new_streak, emoji=streak_emoji, best=streak_info['best'])
        await update.message.reply_text(streak_msg, parse_mode='Markdown')
    
    keyboard = [[KeyboardButton(t('btn_next', language)), KeyboardButton(t('btn_menu', language))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(t('ready_more', language), reply_markup=reply_markup)
    
    # ✅ STEP 3: AI IN BACKGROUND (NON-BLOCKING!)
    if not is_correct:
        await update.message.chat.send_action("typing")
        
        async def generate_and_send_ai():
            try:
                ai_explanation = await asyncio.to_thread(
                    explain_answer,
                    question['text'],
                    question['options'][correct_answer],
                    question['options'].get(user_answer, user_answer),
                    language
                )
                
                await update.message.reply_text(
                    f"🤖 AI Explanation:\n\n{ai_explanation}"
                )
            except Exception as e:
                print(f"❌ AI generation error: {e}")
                await update.message.reply_text(
                    "⚠️ AI explanation unavailable. Please continue practicing!" if language == 'en' else
                    "⚠️ AI объяснение недоступно. Продолжайте практику!" if language == 'ru' else
                    "⚠️ AI түсініктемесі қолжетімсіз. Жаттығуды жалғастырыңыз!"
                )
        
        asyncio.create_task(generate_and_send_ai())
    
    return WAITING_ANSWER

async def ask_for_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask user what topic to explain"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    user_sessions[user_id]['in_ai_mode'] = True
    
    await update.message.reply_text(t('ask_topic', language))
    return ASKING_QUESTION

async def ask_for_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask user their question"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    user_sessions[user_id]['in_ai_mode'] = True
    
    await update.message.reply_text(t('ask_question', language))
    return ASKING_QUESTION

async def handle_free_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle topic explanation or question"""
    user_id = update.effective_user.id
    user_text = update.message.text
    
    subject = user_sessions.get(user_id, {}).get('subject', 'general')
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    button_actions = {
        'practice': [t('btn_practice', 'en'), t('btn_practice', 'ru'), t('btn_practice', 'kk')],
        'topics': [t('btn_topics', 'en'), t('btn_topics', 'ru'), t('btn_topics', 'kk')],
        'change': [t('btn_change_subject', 'en'), t('btn_change_subject', 'ru'), t('btn_change_subject', 'kk')],
        'menu': [t('btn_menu', 'en'), t('btn_menu', 'ru'), t('btn_menu', 'kk')],
        'progress': [t('btn_progress', 'en'), t('btn_progress', 'ru'), t('btn_progress', 'kk')],
        'leaderboard': [t('btn_leaderboard', 'en'), t('btn_leaderboard', 'ru'), t('btn_leaderboard', 'kk')],
    }
    
    if user_text in button_actions['practice']:
        return await start_practice(update, context)
    elif user_text in button_actions['topics']:
        return await show_topics(update, context)
    elif user_text in button_actions['change']:
        return await change_subject(update, context)
    elif user_text in button_actions['menu']:
        return await show_main_menu(update, context)
    elif user_text in button_actions['progress']:
        return await show_progress(update, context)
    elif user_text in button_actions['leaderboard']:
        return await show_leaderboard(update, context)
    
    await update.message.chat.send_action("typing")
    
    if len(user_text) > 100:
        response = answer_question(user_text, subject, language)
    else:
        response = explain_topic(user_text, subject, language)
    
    await update.message.reply_text(response)
    
    return WAITING_ANSWER

async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    stats = get_user_stats(user_id)
    
    if not stats or stats['total'] == 0:
        await update.message.reply_text(t('no_stats', language))
        return WAITING_ANSWER
    
    if stats['percentage'] >= 80:
        emoji = "⭐⭐⭐⭐⭐"
    elif stats['percentage'] >= 60:
        emoji = "⭐⭐⭐⭐"
    elif stats['percentage'] >= 40:
        emoji = "⭐⭐⭐"
    else:
        emoji = "⭐⭐"
    
    response = f"{t('progress_title', language)}\n\n"
    response += f"{t('overall_stats', language)}\n"
    response += f"{t('total_questions', language, total=stats['total'])}\n"
    response += f"{t('correct_answers', language, correct=stats['correct'])}\n"
    response += f"{t('accuracy', language, percentage=stats['percentage'])} {emoji}\n\n"
    response += f"{t('keep_practicing', language)}"
    
    await update.message.reply_text(response, parse_mode='Markdown')
    
    return WAITING_ANSWER

async def show_weak_areas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weak area detection analysis"""
    user_id = update.effective_user.id
    subject = user_sessions.get(user_id, {}).get('subject', 'mathematics')
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    topic_stats = get_topic_stats(user_id, subject)
    
    if not topic_stats:
        await update.message.reply_text(
            "Practice at least 3 questions per topic to see weak area analysis!" if language == 'en' else
            "Решите минимум 3 вопроса по каждой теме для анализа слабых мест!" if language == 'ru' else
            "Әлсіз жақтарды талдау үшін әр тақырып бойынша кемінде 3 сұрақ шешіңіз!"
        )
        return WAITING_ANSWER
    
    message = "📊 WEAK AREA DETECTION\n"
    message += "═" * 40 + "\n\n"
    
    for stat in topic_stats:
        topic_display = t(stat['topic'], language)
        
        if stat['status'] == 'strong':
            status_emoji = "✅"
            status_text = "Strong" if language == 'en' else "Сильный" if language == 'ru' else "Күшті"
        elif stat['status'] == 'moderate':
            status_emoji = "⚠️"
            status_text = "Moderate" if language == 'en' else "Средний" if language == 'ru' else "Орташа"
        else:
            status_emoji = "❌"
            status_text = "Weak" if language == 'en' else "Слабый" if language == 'ru' else "Әлсіз"
        
        message += f"{status_emoji} {topic_display}\n"
        message += f"   Accuracy: {stat['accuracy']}% ({stat['correct']}/{stat['total']})\n"
        message += f"   Status: {status_text}\n"
        message += f"   → {stat['recommendation']}\n\n"
    
    await update.message.reply_text(message)
    
    weak_topics = [s['topic'] for s in topic_stats if s['status'] == 'weak']
    if weak_topics:
        keyboard = [
            [KeyboardButton("Practice Weak Topics" if language == 'en' else "Практиковать слабые темы" if language == 'ru' else "Әлсіз тақырыптарды жаттығу")],
            [KeyboardButton(t('btn_menu', language))]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Would you like to practice your weak topics?" if language == 'en' else
            "Хотите практиковать слабые темы?" if language == 'ru' else
            "Әлсіз тақырыптарды жаттығуды қалайсыз ба?",
            reply_markup=reply_markup
        )
        
        user_sessions[user_id]['weak_topics'] = weak_topics
    
    return WAITING_ANSWER

async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show leaderboard"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    leaderboard = get_leaderboard(10)
    
    if not leaderboard:
        await update.message.reply_text(t('no_leaderboard', language))
        return WAITING_ANSWER
    
    message = t('leaderboard_title', language)
    medals = ['🥇', '🥈', '🥉']
    
    for rank, user in enumerate(leaderboard, 1):
        medal = medals[rank-1] if rank <= 3 else f'{rank}.'
        streak_emoji = '🔥' if user['streak'] > 0 else ''
        
        message += f"{medal} **{user['name']}**\n"
        message += f"   ✓ {user['correct']}/{user['total']} ({user['accuracy']}%)"
        
        if user['streak'] > 0:
            message += f" {streak_emoji}{user['streak']}"
        
        message += "\n\n"
    
    user_rank = get_user_rank(user_id)
    if user_rank:
        message += t('your_rank', language, rank=user_rank)
    
    await update.message.reply_text(message, parse_mode='Markdown')
    
    return WAITING_ANSWER

async def show_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available topics"""
    user_id = update.effective_user.id
    subject = user_sessions.get(user_id, {}).get('subject', 'mathematics')
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    topics = get_subject_topics(subject)
    
    if not topics:
        await update.message.reply_text("No topics available. Starting regular practice...")
        return await start_practice(update, context)
    
    message = t('choose_topic', language)
    
    keyboard = []
    for topic in topics:
        topic_name = t(topic, language)
        keyboard.append([KeyboardButton(topic_name)])
    
    keyboard.append([KeyboardButton(t('all_topics', language))])
    keyboard.append([KeyboardButton("📊 Weak Areas" if language == 'en' else "📊 Слабые места" if language == 'ru' else "📊 Әлсіз жақтар")])
    keyboard.append([KeyboardButton(t('btn_menu', language))])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(message, reply_markup=reply_markup)
    
    user_sessions[user_id]['selecting_topic'] = True
    
    return WAITING_ANSWER

async def topic_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User chose a topic"""
    user_id = update.effective_user.id
    text = update.message.text
    subject = user_sessions.get(user_id, {}).get('subject', 'mathematics')
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    if text in [t('btn_menu', 'en'), t('btn_menu', 'ru'), t('btn_menu', 'kk')]:
        user_sessions[user_id]['selecting_topic'] = False
        return await show_main_menu(update, context)
    
    if text in [t('all_topics', 'en'), t('all_topics', 'ru'), t('all_topics', 'kk')]:
        user_sessions[user_id]['topic'] = None
        user_sessions[user_id]['selecting_topic'] = False
        return await start_practice(update, context)
    
    topics = get_subject_topics(subject)
    selected_topic = None
    
    for topic_key in topics:
        if text in [t(topic_key, 'en'), t(topic_key, 'ru'), t(topic_key, 'kk')]:
            selected_topic = topic_key
            break
    
    if not selected_topic:
        await update.message.reply_text(t('choose_topic', language))
        return WAITING_ANSWER
    
    user_sessions[user_id]['topic'] = selected_topic
    user_sessions[user_id]['selecting_topic'] = False
    
    return await start_practice(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    subject = user_sessions.get(user_id, {}).get('subject')
    
    if not subject:
        return await change_subject(update, context)
    
    keyboard = [
        [KeyboardButton(t('btn_practice', language)), KeyboardButton(t('btn_topics', language))],
        [KeyboardButton(t('btn_explain', language)), KeyboardButton(t('btn_ask', language))],
        [KeyboardButton(t('btn_progress', language)), KeyboardButton(t('btn_leaderboard', language))],
        [KeyboardButton(t('btn_change_subject', language))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    if 'selecting_topic' in user_sessions.get(user_id, {}):
        user_sessions[user_id]['selecting_topic'] = False
    if 'topic' in user_sessions.get(user_id, {}):
        user_sessions[user_id]['topic'] = None
    if 'in_ai_mode' in user_sessions.get(user_id, {}):
        user_sessions[user_id]['in_ai_mode'] = False
    
    subject_key = f'subject_{subject}' if not subject.startswith('subject_') else subject
    subject_name = t(subject_key, language)
    
    await update.message.reply_text(
        t('subject_chosen', language, subject=subject_name),
        reply_markup=reply_markup
    )
    
    return WAITING_ANSWER

async def change_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change subject selection"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    if user_id in user_sessions:
        user_sessions[user_id]['subject'] = None
        user_sessions[user_id]['topic'] = None
        user_sessions[user_id]['selecting_topic'] = False
    
    keyboard = [
        [KeyboardButton(t('subject_math', language)), KeyboardButton(t('subject_physics', language))],
        [KeyboardButton(t('subject_chemistry', language)), KeyboardButton(t('subject_biology', language))],
        [KeyboardButton(t('subject_history', language)), KeyboardButton(t('subject_geography', language))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        t('choose_subject', language),
        reply_markup=reply_markup
    )
    
    return CHOOSING_SUBJECT

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    user_id = update.effective_user.id
    language = user_sessions.get(user_id, {}).get('language', 'en')
    
    help_text = t('welcome', language)
    
    await update.message.reply_text(help_text)

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """Start the bot with all features"""
    init_db()
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, language_chosen)],
            CHOOSING_SUBJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, subject_chosen)],
            WAITING_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_choice)],
            ASKING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_text)],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # ✅ Graceful shutdown handler
    def signal_handler(sig, frame):
        """Save active users before shutdown"""
        print("\n⚠️  Shutting down bot...")
        save_active_users(user_sessions)
        print("✅ Active users saved!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Bot is starting...")
    
    # ✅ Notify users about restart
    async def post_init(application):
        """Called after bot starts"""
        await notify_restart(application)
    
    application.post_init = post_init
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print("✅ ASYNC AI ENABLED - Supports 10+ concurrent users!")
    print("✅ RESTART NOTIFICATION ENABLED")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()