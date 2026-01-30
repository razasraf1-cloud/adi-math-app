import streamlit as st
import random

# --- הגדרות עיצוב ---
st.set_page_config(page_title="מתמטי-קל לעדי", page_icon="📐", layout="centered")

st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, p, div, span {
        text-align: right;
    }
    .stButton>button {
        background-color: #4CAF50; /* ירוק */
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px;
        width: 100%;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #d1d1d1;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- מאגר שאלות מורחב (כיתה ז') ---
if 'questions_pool' not in st.session_state:
    st.session_state.questions_pool = [
        # אלגברה
        {"topic": "אלגברה", "q": "פתרי את המשוואה: 3x - 4 = 11", "a": "5", "hint": "העבירי את ה-4 לצד השני (בפלוס) ואז חלקי ב-3"},
        {"topic": "אלגברה", "q": "אם x = 4, כמה זה 2x + 10?", "a": "18", "hint": "הציבי 4 במקום ה-x"},
        {"topic": "אלגברה", "q": "פשטי את הביטוי: 5a + 2b - 3a", "a": "2a + 2b", "hint": "חברי רק את האיברים עם a"},
        {"topic": "אלגברה", "q": "פתרי: 2(x + 3) = 20", "a": "7", "hint": "פתחי סוגריים קודם: 2x + 6 = 20"},
        
        # גיאומטריה
        {"topic": "גיאומטריה", "q": "למלבן צלעות באורך 5 ס״מ ו-10 ס״מ. מה היקף המלבן?", "a": "30", "hint": "היקף הוא סכום כל הצלעות: 5+5+10+10"},
        {"topic": "גיאומטריה", "q": "במשולש יש זווית של 90 מעלות וזווית של 30 מעלות. מה גודל הזווית השלישית?", "a": "60", "hint": "סכום זוויות במשולש הוא תמיד 180"},
        {"topic": "גיאומטריה", "q": "ריבוע הוא בעל היקף של 20 ס״מ. מה אורך הצלע שלו?", "a": "5", "hint": "לריבוע 4 צלעות שוות. 20 לחלק ל-4"},
        {"topic": "גיאומטריה", "q": "שטח מלבן הוא 50 סמ״ר. צלע אחת היא 5 ס״מ. מה אורך הצלע השנייה?", "a": "10", "hint": "שטח = צלע כפול צלע"},

        # שאלות מילוליות
        {"topic": "חשיבה כמותית", "q": "מחיר חולצה 50 שקלים. יש הנחה של 10%. מה המחיר החדש?", "a": "45", "hint": "10% מ-50 זה 5 שקלים. תפחיתי את זה מהמחיר"},
        {"topic": "חשיבה כמותית", "q": "רוני רץ 2 ק״מ ביום א' ו-3 ק״מ ביום ב'. כמה רץ סה״כ בשבוע אם המשיך ככה כל יום (7 ימים)?", "a": "17.5", "hint": "שאלה מכשילה? אם זה ממוצע 2.5 ליום... בואי נניח שהכוונה ל-2.5 בממוצע כפול 7"},
        {"topic": "מספרים מכוונים", "q": "כמה זה: 5 - (-3)?", "a": "8", "hint": "מינוס ומינוס הופך לפלוס"},
    ]

# --- ניהול מצב האפליקציה ---
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = random.randint(0, len(st.session_state.questions_pool) - 1)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False

# פונקציה להגרלת שאלה חדשה
def next_question():
    st.session_state.current_q_index = random.randint(0, len(st.session_state.questions_pool) - 1)
    st.session_state.answered = False
    st.session_state.user_input = "" # איפוס שדה הטקסט

# --- ממשק משתמש ---
st.title("📐 מתמטי-קל לעדי: אימון חופשי")
st.write(f"הניקוד שלך: **{st.session_state.score}** ⭐")

# שליפת השאלה הנוכחית
q_data = st.session_state.questions_pool[st.session_state.current_q_index]

st.markdown(f"""
<div class="question-box">
    <h3>נושא: {q_data['topic']}</h3>
    <p class="big-font">{q_data['q']}</p>
</div>
""", unsafe_allow_html=True)

# טופס תשובה
with st.form(key='answer_form'):
    user_ans = st.text_input("התשובה שלך:", key="user_input")
    submit = st.form_submit_button(label="בדיקה")

# לוגיקה של בדיקה
if submit:
    if not user_ans:
        st.warning("נא לכתוב תשובה לפני הבדיקה 🙂")
    else:
        # ניקוי רווחים והשוואה
        if user_ans.strip() == q_data['a']:
            st.balloons()
            st.success("🎉 כל הכבוד! תשובה נכונה!")
            if not st.session_state.answered:
                st.session_state.score += 10
                st.session_state.answered = True
        else:
            st.error("לא בדיוק... נסי שוב!")
            if 'hint' in q_data:
                st.info(f"💡 רמז: {q_data['hint']}")

# כפתור לשאלה הבאה (מחוץ לטופס)
st.markdown("---")
if st.button("השאלה הבאה ➡️"):
    next_question()
    st.rerun()
