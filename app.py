import streamlit as st
import random

# הגדרות עיצוב וכותרת
st.set_page_config(page_title="מתמטי-קל לעדי", page_icon="📐", layout="centered")

# סגנון מותאם אישית (CSS) ליישור לימין
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, p, div {
        text-align: right;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    .success-msg {
        padding: 10px;
        background-color: #D4EDDA;
        color: #155724;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📐 מתמטי-קל: האימון היומי של עדי")
st.write("היי עדי! ברוכה הבאה לאימון היומי שלך. 20 דקות ביום ואת אלופה!")

# --- ניהול מעקב ימים ---
if 'day_count' not in st.session_state:
    st.session_state.day_count = 1
if 'completed_days' not in st.session_state:
    st.session_state.completed_days = []

# --- מאגר שאלות ---
questions = [
    {"type": "אלגברה", "q": "פתרי את המשוואה: 2x + 5 = 15", "a": "5"},
    {"type": "גיאומטריה", "q": "אם שטח מלבן הוא 24 סמ\"ר וצלע אחת היא 6 ס\"מ, מה אורך הצלע השנייה?", "a": "4"},
    {"type": "שאלות מילוליות", "q": "דני קנה 3 מחברות ב-12 שקלים כל אחת. כמה עודף קיבל מ-50 שקלים?", "a": "14"},
    {"type": "אלגברה", "q": "כנסי איברים דומים: 3a + 2b + 5a", "a": "8a + 2b"},
    {"type": "גיאומטריה", "q": "מה סכום הזוויות במשולש?", "a": "180"},
]

# לוגיקה לבחירת שאלה
day_question = questions[(st.session_state.day_count - 1) % len(questions)]

# --- הצגת ההתקדמות ---
progress = len(st.session_state.completed_days) / 15
st.progress(progress)
st.write(f"התקדמות: השלמת {len(st.session_state.completed_days)} מתוך 15 ימים")

# --- אזור האימון ---
st.header(f"📅 יום {st.session_state.day_count}")

st.info(f"נושא היום: {day_question['type']}")
st.write(f"**השאלה:** {day_question['q']}")

user_answer = st.text_input("התשובה שלך:")

if st.button("בדיקה"):
    # ניקוי רווחים מהתשובה ובדיקה
    clean_answer = user_answer.strip()
    correct_answer = day_question['a']
    
    if clean_answer == correct_answer:
        st.balloons()
        st.markdown('<div class="success-msg">כל הכבוד עדי! תשובה נכונה! ⭐</div>', unsafe_allow_html=True)
        
        if st.session_state.day_count not in st.session_state.completed_days:
             st.session_state.completed_days.append(st.session_state.day_count)
    else:
        st.error
