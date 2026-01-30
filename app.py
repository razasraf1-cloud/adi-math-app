import streamlit as st
import random
import time

# --- הגדרות עמוד ועיצוב משחקי ---
st.set_page_config(page_title="האתגר של עדי", page_icon="📐", layout="centered")

st.markdown("""
<style>
    .stApp { direction: rtl; text-align: right; }
    h1, h2, h3, p, span, div { text-align: right; }
    
    .question-card {
        background-color: #E3F2FD;
        border: 2px solid #2196F3;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .stat-box {
        background-color: #FFF3E0;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #FF9800;
        margin-bottom: 10px;
    }

    .stButton>button {
        background-color: #FF4081;
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
    st.session_state.daily_progress = 0
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

# --- מחולל שאלות אוטומטי (הלב של המערכת) ---
def generate_math_problem():
    # בוחרים באקראי סוג שאלה: 1=אלגברה, 2=גיאומטריה, 3=כללי
    category = random.choice(['algebra', 'geometry', 'general'])
    
    problem = {}
    
    if category == 'algebra':
        subtype = random.choice(['eq_simple', 'eq_hard', 'substitution'])
        if subtype == 'eq_simple': # משוואה x + a = b
            x = random.randint(2, 20)
            a = random.randint(1, 20)
            b = x + a
            problem = {
                "topic": "אלגברה (משוואות)",
                "q": f"פתרי את המשוואה: x + {a} = {b}",
                "a": str(x),
                "hint": f"תפחיתי {a} מ-{b}"
            }
        elif subtype == 'eq_hard': # משוואה ax + b = c
            x = random.randint(2, 10)
            a = random.randint(2, 5)
            b = random.randint(1, 10)
            c = a * x + b
            problem = {
                "topic": "אלגברה (משוואות)",
                "q": f"פתרי את המשוואה: {a}x + {b} = {c}",
                "a": str(x),
                "hint": f"קודם תחסרי {b} מהתוצאה, ואז תחלקו ב-{a}"
            }
        else: # הצבה: אם x=.. כמה זה..
            x = random.randint(2, 8)
            a = random.randint(2, 6)
            res = a * x
            problem = {
                "topic": "אלגברה (הצבה)",
                "q": f"אם x = {x}, כמה זה {a}x?",
                "a": str(res),
                "hint": f"פשוט תכפילי {x} ב-{a}"
            }

    elif category == 'geometry':
        subtype = random.choice(['rect_area', 'rect_perimeter', 'triangle_angle'])
        if subtype == 'rect_area':
            w = random.randint(3, 10)
            h = random.randint(3, 10)
            problem = {
                "topic": "גיאומטריה (שטח)",
                "q": f"חשבי שטח מלבן שצלעותיו {w} ו-{h}",
                "a": str(w * h),
                "hint": "שטח מלבן זה צלע כפול צלע"
            }
        elif subtype == 'rect_perimeter':
            w = random.randint(3, 10)
            h = random.randint(3, 10)
            perm = 2 * (w + h)
            problem = {
                "topic": "גיאומטריה (היקף)",
                "q": f"חשבי היקף מלבן שצלעותיו {w} ו-{h}",
                "a": str(perm),
                "hint": "חיבור כל הצלעות: פעמיים הרוחב ועוד פעמיים האורך"
            }
        else: # זוויות במשולש
            a1 = random.randint(30, 80)
            a2 = random.randint(30, 80)
            a3 = 180 - (a1 + a2)
            problem = {
                "topic": "גיאומטריה (משולשים)",
                "q": f"במשולש יש זוויות של {a1} ו-{a2} מעלות. מה גודל הזווית השלישית?",
                "a": str(a3),
                "hint": "סכום זוויות במשולש הוא תמיד 180"
            }

    else: # כללי / מילולי / מספרים מכוונים
        subtype = random.choice(['percent', 'negative', 'word_prob'])
        if subtype == 'percent':
            num = random.choice([100, 200, 50, 400])
            perc = random.choice([10, 20, 25, 50])
            ans = int((perc / 100) * num)
            problem = {
                "topic": "אחוזים",
                "q": f"כמה זה {perc}% מתוך {num}?",
                "a": str(ans),
                "hint": f"נסי לחשב כמה זה 10 אחוז ואז להכפיל, או שבר פשוט"
            }
        elif subtype == 'negative':
            a = random.randint(3, 10)
            b = random.randint(12, 20)
            problem = {
                "topic": "מספרים מכוונים",
                "q": f"פתרי: {a} - {b}",
                "a": str(a - b),
                "hint": "המספר השני גדול יותר, אז התוצאה במינוס"
            }
        else:
            price = random.randint(2, 8)
            amount = random.randint(3, 10)
            total = price * amount
            problem = {
                "topic": "בעיה מילולית",
                "q": f"דני קנה {amount} מחברות במחיר {price} שקלים לאחת. כמה שילם?",
                "a": str(total),
                "hint": "תרגיל כפל פשוט"
            }
            
    return problem

# --- פונקציות עזר ---
def get_new_question():
    # כאן הקסם: במקום לשלוף מרשימה, אנחנו מייצרים שאלה חדשה
    st.session_state.current_q = generate_math_problem()
    st.session_state.input_key += 1 

def start_next_day():
    st.session_state.day += 1
    st.session_state.daily_progress = 0
    get_new_question()

# אתחול ראשוני
if st.session_state.current_q is None:
    get_new_question()

# --- מסכי סיום ---
if st.session_state.day > 15:
    st.balloons()
    st.markdown("""
    <div style="text-align: center; padding: 50px; background-color: #D4EDDA; border-radius: 20px;">
        <h1>🏆 אלופה!!! 🏆</h1>
        <h2>סיימת את כל 15 הימים של האתגר!</h2>
    </div>
    """, unsafe_allow_html=True)
    if st.button("התחל מחדש"):
        st.session_state.day = 1
        st.session_state.total_score = 0
        st.rerun()
    st.stop()

if st.session_state.daily_progress >= 15:
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: #FFF3E0; border-radius: 20px;">
        <h1>🌙 סיימת את יום {st.session_state.day}!</h1>
        <h3>כל הכבוד! פתרת 15 תרגילים היום.</h3>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
    st.button("להתחיל את יום המחר? ☀️", on_click=start_next_day)
    st.stop()

# --- המסך הראשי ---
q = st.session_state.current_q

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="stat-box">📅 יום: <b>{st.session_state.day}/15</b></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box">⭐ ניקוד: <b>{st.session_state.total_score}</b></div>', unsafe_allow_html=True)

st.write(f"התקדמות יומית: {st.session_state.daily_progress}/15 שאלות")
st.progress(st.session_state.daily_progress / 15)

st.markdown(f"""
<div class="question-card">
    <div style="color: #666; font-size: 14px;">נושא: {q['topic']}</div>
    <div class="big-question">{q['q']}</div>
</div>
""", unsafe_allow_html=True)

with st.expander("💡 צריכה רמז?"):
    st.info(q['hint'])

with st.form(key='game_form'):
    ans = st.text_input("התשובה שלך:", key=f"user_ans_{st.session_state.input_key}")
    submitted = st.form_submit_button("בדיקה ✅")

    if submitted:
        if ans.strip() == q['a']:
            st.success("נכון מאוד! 🎉")
            st.session_state.daily_progress += 1
            st.session_state.total_score += 10
            time.sleep(1)
            get_new_question()
            st.rerun()
        else:
            st.error("לא בדיוק... נסי שוב 💪")

if st.button("דלגי לשאלה הבאה ⏭️"):
    get_new_question()
    st.rerun()
