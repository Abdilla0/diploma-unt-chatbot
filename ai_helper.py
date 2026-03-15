import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

load_dotenv()

print("🔮 Using Gemini AI")

# ✅ SECURITY FIX: Load API key from environment variable
GEMINI_API_KEY = 

if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
    print("📝 Please create a .env file with: GEMINI_API_KEY=your_key_here")
    model = None
else:
    print(f"🔑 API Key loaded: {GEMINI_API_KEY[:20]}...")
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # ✅ Working model name
        model = genai.GenerativeModel('models/gemini-flash-latest')
        print("✅ Gemini AI configured successfully")
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        model = None

def clean_response(text: str) -> str:
    """Remove unwanted symbols and formatting from AI response"""
    if not text:
        return text
    
    # ✅ Remove ** markdown bold
    text = text.replace('**', '')
    
    # ✅ Remove single * asterisks
    text = text.replace('*', '')
    
    # ✅ Remove $ symbols
    text = text.replace('$', '')
    
    # ✅ Remove ``` code blocks
    text = re.sub(r'```[\w]*\n?', '', text)
    
    # ✅ Remove _ underscores used for italics
    text = text.replace('_', '')
    
    # ✅ Remove excessive newlines (more than 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # ✅ Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def call_ai(prompt: str) -> str:
    """
    Call Gemini AI
    
    Args:
        prompt: The prompt to send to AI
    
    Returns:
        Cleaned AI response text
    """
    if model is None:
        return "⚠️ AI temporarily unavailable"
    
    try:
        # Generate content (Gemini handles timeout internally)
        response = model.generate_content(prompt)
        # ✅ Clean the response before returning
        cleaned_text = clean_response(response.text)
        return cleaned_text
    except Exception as e:
        print(f"❌ Gemini Error: {str(e)[:150]}...")
        return "⚠️ AI temporarily unavailable. Please try again."

def explain_topic(topic, subject, language="en"):
    """
    AI explains a topic for UNT exam preparation
    
    Args:
        topic: Topic name to explain
        subject: Subject area (math, physics, etc.)
        language: Response language ('en', 'ru', 'kk')
    
    Returns:
        AI-generated explanation in specified language
    """
    
    lang_map = {
        'en': 'English',
        'ru': 'Russian',
        'kk': 'Kazakh'
    }
    
    # ✅ FIXED: Removed "UNT Silkway Bot" reference
    prompt = f"""You are a helpful UNT (Unified National Testing) exam preparation assistant.

Explain the topic: "{topic}" in {subject}

IMPORTANT REQUIREMENTS:
- Use {lang_map.get(language, 'English')} language ONLY
- Use plain text ONLY - NO special formatting
- DO NOT use asterisks (**)
- DO NOT use underscores (_)
- DO NOT use dollar signs ($)
- DO NOT use markdown or code blocks
- Make it simple and clear for high school students
- Include practical examples
- Keep under 300 words
- Be encouraging and supportive

Write your explanation in plain, simple text:"""
    
    return call_ai(prompt)

def answer_question(question, subject, language="en"):
    """
    AI answers student's free-form question
    
    Args:
        question: Student's question
        subject: Subject context
        language: Response language ('en', 'ru', 'kk')
    
    Returns:
        AI-generated answer in specified language
    """
    
    lang_map = {
        'en': 'English',
        'ru': 'Russian',
        'kk': 'Kazakh'
    }
    
    prompt = f"""You are a UNT (Unified National Testing) exam preparation assistant.

Student's question: {question}
Subject: {subject}

IMPORTANT REQUIREMENTS:
- Answer in {lang_map.get(language, 'English')} ONLY
- Use plain text ONLY - NO special formatting
- DO NOT use asterisks (**)
- DO NOT use underscores (_)
- DO NOT use dollar signs ($)
- DO NOT use markdown or code blocks
- Be clear, accurate, and helpful
- Include examples if needed
- Keep under 300 words
- Be encouraging

Write your answer in plain, simple text:"""
    
    return call_ai(prompt)

def explain_answer(question_text, correct_answer, user_answer, language="en"):
    """
    Explain why an answer is correct or incorrect
    
    Args:
        question_text: The question that was asked
        correct_answer: The correct answer
        user_answer: What the student answered
        language: Response language ('en', 'ru', 'kk')
    
    Returns:
        AI-generated explanation addressing the student's answer
    """
    
    lang_map = {
        'en': 'English',
        'ru': 'Russian',
        'kk': 'Kazakh'
    }
    
    is_correct = (str(user_answer).upper().strip() == str(correct_answer).upper().strip())
    
    if is_correct:
        prompt = f"""A student answered correctly on their UNT practice!

Question: {question_text}
Correct answer: {correct_answer}

IMPORTANT REQUIREMENTS:
- Write in {lang_map.get(language, 'English')} ONLY
- Use plain text ONLY - NO formatting
- DO NOT use asterisks, underscores, or dollar signs
- Write 2-3 encouraging sentences praising them
- Keep it simple and encouraging

Your response in plain text:"""
    else:
        prompt = f"""Help a UNT student understand their mistake.

Question: {question_text}
Correct answer: {correct_answer}
Student's answer: {user_answer}

IMPORTANT REQUIREMENTS:
- Write in {lang_map.get(language, 'English')} ONLY
- Use plain text ONLY - NO formatting
- DO NOT use asterisks, underscores, or dollar signs
- Explain why the correct answer is right
- Be kind and encouraging
- Keep under 150 words

Your explanation in plain text:"""
    
    return call_ai(prompt)

# ============================================
# TESTING SECTION
# ============================================

if __name__ == "__main__":
    # ✅ FIXED: Removed "UNT Silkway Bot" reference
    print("\n🧪 Testing Gemini AI for UNT preparation system...\n")
    
    print("1️⃣ Testing explain_topic...")
    result = explain_topic("quadratic equations", "math", "en")
    print(f"✅ Result:\n{result}\n")
    print("=" * 60)
    
    print("\n2️⃣ Testing answer_question...")
    result = answer_question("What is 15% of 200?", "math", "en")
    print(f"✅ Result:\n{result}\n")
    print("=" * 60)
    
    print("\n3️⃣ Testing explain_answer (correct)...")
    result = explain_answer("What is 2 + 2?", "4", "4", "en")
    print(f"✅ Result:\n{result}\n")
    print("=" * 60)
    
    print("\n4️⃣ Testing explain_answer (incorrect)...")
    result = explain_answer("Solve: x² - 5x + 6 = 0", "x = 2, x = 3", "x = 1, x = 6", "en")
    print(f"✅ Result:\n{result}\n")
    
    print("\n✅ All tests complete!")
