import streamlit as st
import math

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

if "expr" not in st.session_state:
    st.session_state.expr = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "history" not in st.session_state:
    st.session_state.history = []

def safe_eval(expr):
    expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
    expr = expr.replace("π", "math.pi")
    allowed = set("0123456789.+-*/%() ")
    # math.pi is allowed only when explicitly inserted by the app.
    cleaned = expr.replace("math.pi", "")
    if any(c not in allowed for c in cleaned):
        raise ValueError("Invalid input")
    return eval(expr, {"__builtins__": {}}, {"math": math})

def calculate():
    if not st.session_state.expr:
        return
    try:
        result = safe_eval(st.session_state.expr)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        st.session_state.answer = str(result)
        st.session_state.history.insert(0, f"{st.session_state.expr} = {result}")
        st.session_state.history = st.session_state.history[:12]
    except ZeroDivisionError:
        st.session_state.answer = "Cannot divide by 0"
    except Exception:
        st.session_state.answer = "Error"

def press(key):
    if key == "AC":
        st.session_state.expr = ""
        st.session_state.answer = ""
    elif key == "⌫":
        st.session_state.expr = st.session_state.expr[:-1]
    elif key == "=":
        calculate()
    elif key == "√":
        try:
            value = safe_eval(st.session_state.expr)
            if value < 0:
                raise ValueError
            st.session_state.expr = str(math.sqrt(value))
            st.session_state.answer = ""
        except Exception:
            st.session_state.answer = "Error"
    elif key == "%":
        try:
            value = safe_eval(st.session_state.expr)
            st.session_state.expr = str(value / 100)
            st.session_state.answer = ""
        except Exception:
            st.session_state.answer = "Error"
    else:
        st.session_state.expr += key
        st.session_state.answer = ""

# Keyboard bridge: browser keydown -> hidden Streamlit input.
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.stApp { background: linear-gradient(135deg,#111827,#0f172a); }
.block-container { max-width: 520px; padding-top: 25px; }

.calc-card {
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 30px;
    padding: 22px;
    box-shadow: 0 25px 70px rgba(0,0,0,.45);
}

.calc-title {
    color:#f9fafb;
    text-align:center;
    font-size:28px;
    font-weight:800;
    margin-bottom:15px;
}

.display {
    background:#030712;
    border-radius:22px;
    padding:18px 20px;
    min-height:125px;
    margin-bottom:16px;
    text-align:right;
    border:1px solid #374151;
}

.expr {
    color:#9ca3af;
    font-size:20px;
    min-height:30px;
    overflow-wrap:anywhere;
}

.answer {
    color:#fff;
    font-size:42px;
    font-weight:700;
    min-height:55px;
    overflow-wrap:anywhere;
}

div.stButton > button {
    height:64px;
    border-radius:19px;
    border:1px solid #374151;
    background:#374151;
    color:white;
    font-size:22px;
    font-weight:700;
    transition:.12s;
}

div.stButton > button:hover {
    background:#4b5563;
    border-color:#6b7280;
    color:white;
}

div.stButton > button:active {
    transform:scale(.96);
}

.small-help {
    color:#9ca3af;
    text-align:center;
    font-size:13px;
    margin-top:12px;
}
</style>
""", unsafe_allow_html=True)

# JavaScript sends keyboard input into a browser event.
st.markdown("""
<script>
document.addEventListener("keydown", function(e) {
    const key = e.key;
    let value = null;

    if (/^[0-9]$/.test(key) || ["+","-","*","/","%","(",")","."].includes(key)) {
        value = key;
    } else if (key === "Enter" || key === "=") {
        value = "=";
    } else if (key === "Backspace") {
        value = "⌫";
    } else if (key === "Escape" || key === "Delete") {
        value = "AC";
    }

    if (value !== null) {
        e.preventDefault();

        // Find Streamlit buttons by visible label and click them.
        const buttons = Array.from(document.querySelectorAll("button"));
        const map = {
            "=": "=",
            "⌫": "⌫",
            "AC": "AC",
            "*": "×",
            "/": "÷",
            "-": "−"
        };
        const target = map[value] || value;
        const btn = buttons.find(b => b.innerText.trim() === target);

        if (btn) {
            btn.click();
        }
    }
});
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-card">', unsafe_allow_html=True)
st.markdown('<div class="calc-title">🧮 Calculator</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="display"><div class="expr">{st.session_state.expr or "0"}</div>'
    f'<div class="answer">{st.session_state.answer or "&nbsp;"}</div></div>',
    unsafe_allow_html=True
)

def button(label, value=None):
    if st.button(label, use_container_width=True):
        press(value if value is not None else label)
        st.rerun()

# Top function row
c=st.columns(4)
with c[0]: button("AC")
with c[1]: button("⌫")
with c[2]: button("%")
with c[3]: button("÷")

c=st.columns(4)
for col, label in zip(c, ["7","8","9","×"]):
    with col: button(label)

c=st.columns(4)
for col, label in zip(c, ["4","5","6","−"]):
    with col: button(label)

c=st.columns(4)
for col, label in zip(c, ["1","2","3","+"]):
    with col: button(label)

c=st.columns(4)
for col, label in zip(c, ["0",".","√","="]):
    with col: button(label)

st.markdown('<div class="small-help">Keyboard: 0–9 · + − * / · Enter = calculate · Backspace = delete · Esc/Delete = clear</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🕘 Calculation History"):
    if st.session_state.history:
        for item in st.session_state.history:
            st.write(item)
        if st.button("Clear History"):
            st.session_state.history=[]
            st.rerun()
    else:
        st.caption("No calculations yet.")
