import streamlit as st
import random
import time

# --- הגדרות עמוד ועיצוב משחקי ---
st.set_page_config(page_title="האתגר של עדי", page_icon="🎮", layout="centered")

st.markdown("""
<style>
    /* כיוון טקסט לימין */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* עיצוב כותרות וטקסטים */
    h1, h2, h3, p, span, div {
        text-align: right;
    }
    
    /* כרטיסייה לשאלה - צבעונית ויפה */
    .question-card {
        background-color: #E3F2FD; /* כחול בהיר */
        border: 2px solid #2196F3;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .stat-box {
        background-color: #FFF3E0; /* כתום בהיר */
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #FF9800;
        margin-bottom: 10px;
    }

    /* עיצוב כפתורים */
    .stButton>button {
        background-color: #FF4081; /* ורוד עז */
        color: white;
        border-radius: 20px;
        font-weight: bold;
        font-size: 18px;
        border: none;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #F50057;
        transform: scale(1.02);
    }
    
    /* טקסט השאלה */
    .big-question {
        font-size: 24px;
        color: #1565C0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- ניהול מצב המשחק (Session State) ---
if 'day' not in st.session_state:
    st.session_state.day = 1
if 'daily_progress' not in st.session_state:
    st.session_state.daily_progress = 0 # כמה שאלות פתרה היום
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = None

# --- מאגר שאלות מורחב ---
questions_pool = [
    # אלגברה
    {"topic": "אלגברה", "q": "פתרי: 2x = 10", "a": "5", "hint": "כמה פעמים 2 נכנס ב-10?"},
    {"topic": "אלגברה", "q": "פתרי: x + 7 = 20", "a": "13", "hint": "תורידי 7 מ-20"},
    {"topic": "אלגברה", "q": "מה הערך של x אם: 3x - 1 = 8", "a": "3", "hint": "קודם תוסיפי 1 לשני הצדדים, ואז תחלקו ב-3"},
    {"topic": "אלגברה", "q": "כנס איברים: 2a + 4a + 5", "a": "6a + 5", "hint": "מחברים רק את ה-a עם ה-a"},
    {"topic": "אלגברה", "q": "אם a=2, כמה זה 5a?", "a": "10", "hint": "5 כפול 2"},
    
    # גיאומטריה
    {"topic": "גיאומטריה", "q": "כמה מעלות יש בזווית ישרה?", "a": "90", "hint": "כמו פינה של דף"},
    {"topic": "גיאומטריה", "q": "משולש שווה צלעות - מה גודל כל זווית?", "a": "60", "hint": "סכום הזוויות 180, לחלק ל-3 זויות שוות"},
    {"topic": "גיאומטריה", "q": "שטח ריבוע עם צלע 4?", "a": "16", "hint": "צלע כפול צלע (4 כפול 4)"},
    {"topic": "גיאומטריה", "q": "היקף מלבן עם צלעות 2 ו-6?", "a": "16", "hint": "2+2+6+6"},
    
    # חשיבה ומילולי
    {"topic": "מילולי", "q": "ירדן קנתה 5 ארטיקים ב-5 שקלים לאחד. כמה שילמה?", "a": "25", "hint": "פעולת כפל פשוטה"},
    {"topic": "מספרים מכוונים", "q": "כמה זה 3 - 10?", "a": "-7", "hint": "אנחנו יורדים מתחת לאפס"},
    {"topic": "אחוזים", "q": "כמה זה 50% מתוך 100?", "a": "50", "hint": "חצי מ-100"},
]

# פונקציה להגרלת שאלה
def get_new_question():
    st.session_state.current_q = random.choice(questions_pool)
    st.session_state.user_ans_input = "" # איפוס שדה הטקסט

# פונקציה למעבר ליום הבא
def start_next_day():
    st.session_state.day += 1
    st.session_state.daily_progress = 0
    get_new_question()

# אתחול ראשוני
if st.session_state.current_q is None:
    get_new_question()

# --- לוגיקת סיום המשחק ---
if st.session_state.day > 15:
    st.balloons()
    st.markdown("""
    <div style="text-align: center; padding: 50px; background-color: #D4EDDA; border-radius: 20px;">
        <h1>🏆 אלופה!!! 🏆</h1>
        <h2>סיימת את כל 15 הימים של האתגר!</h2>
        <p>את מוכנה למבחן לגמרי!</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("התחל מחדש"):
        st.session_state.day = 1
        st.session_state.total_score = 0
        st.rerun()
    st.stop()

# --- לוגיקת סיום יום ---
if st.session_state.daily_progress >= 15:
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: #FFF3E0; border-radius: 20px;">
        <h1>🌙 סיימת את יום {st.session_state.day}!</h1>
        <h3>כל הכבוד! פתרת 15 תרגילים היום.</h3>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
    
    if st.button("להתחיל את יום המחר? ☀️", on_click=start_next_day):
        pass # הפונקציה כבר רצה ב-on_click
    st.stop()


# --- המסך הראשי של המשחק ---

# כותרת עליונה עם סטטיסטיקה
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="stat-box">📅 יום: <b>{st.session_state.day}/15</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box">⭐ ניקוד: <b>{st.session_state.total_score}</b></div>', unsafe_allow_html=True)

# סרגל התקדמות יומי
st.write(f"התקדמות יומית: {st.session_state.daily_progress}/15 שאלות")
progress_bar = st.progress(st.session_state.daily_progress / 15)

# הצגת השאלה
q = st.session_state.current_q

st.markdown(f"""
<div class="question-card">
    <div style="color: #666; font-size: 14px;">נושא: {q['topic']}</div>
    <div class="big-question">{q['q']}</div>
</div>
""", unsafe_allow_html=True)

# אזור הרמז - תמיד זמין
with st.expander("💡 צריכה רמז? לחצי כאן"):
    st.info(q['hint'])

# טופס תשובה
with st.form(key='game_form'):
    ans = st.text_input("התשובה שלך:", key="user_ans_input")
    submitted = st.form_submit_button("בדיקה ✅")

    if submitted:
        if ans.strip() == q['a']:
            st.success("נכון מאוד! 🎉")
            st.session_state.daily_progress += 1
            st.session_state.total_score += 10
            time.sleep(1) # השהייה קטנה כדי לראות את ההצלחה
            get_new_question()
            st.rerun()
        else:
            st.error("לא בדיוק... נסי שוב 💪")

# כפתור דילוג (אופציונלי, אם נתקעים)
if st.button("דלגי לשאלה הבאה ⏭️"):
    get_new_question()
    st.rerun()
