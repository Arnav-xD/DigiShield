import streamlit as st
import time
import random
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #1a0a2e 0%, #0a0a0f 50%),
                radial-gradient(ellipse at 80% 100%, #0a1a2e 0%, transparent 50%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Main container ── */
.main .block-container {
    padding: 2rem 3rem 4rem;
    max-width: 1200px;
}

/* ── Header ── */
.shield-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.25rem;
}
.shield-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #00d4ff, #7b5ea7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.shield-sub {
    color: #6b6b8a;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.status-active {
    background: rgba(0, 212, 100, 0.12);
    border: 1px solid rgba(0, 212, 100, 0.4);
    color: #00d464;
}
.status-inactive {
    background: rgba(107, 107, 138, 0.12);
    border: 1px solid rgba(107, 107, 138, 0.3);
    color: #6b6b8a;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}
.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6b6b8a;
    margin-bottom: 0.75rem;
}

/* ── Risk meter ── */
.risk-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.risk-low    { background: linear-gradient(90deg, #00d464, #00b455); }
.risk-medium { background: linear-gradient(90deg, #ffb800, #ff8c00); }
.risk-high   { background: linear-gradient(90deg, #ff4545, #ff0000); }

/* ── Alert box ── */
.alert-box {
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    animation: slideIn 0.3s ease;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.alert-high {
    background: rgba(255, 69, 69, 0.1);
    border: 1px solid rgba(255, 69, 69, 0.35);
}
.alert-medium {
    background: rgba(255, 184, 0, 0.08);
    border: 1px solid rgba(255, 184, 0, 0.3);
}
.alert-low {
    background: rgba(0, 212, 100, 0.08);
    border: 1px solid rgba(0, 212, 100, 0.25);
}
.alert-icon { font-size: 1.1rem; line-height: 1.4; }
.alert-text { font-size: 0.85rem; line-height: 1.5; color: #c8c8d8; }
.alert-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.6;
    display: block;
    margin-bottom: 0.2rem;
}

/* ── Transcript box ── */
.transcript-box {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.25rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
    color: #9898b8;
    min-height: 120px;
    max-height: 220px;
    overflow-y: auto;
}
.transcript-highlight {
    background: rgba(255, 69, 69, 0.2);
    border-radius: 3px;
    padding: 0 2px;
    color: #ff9090;
}
.transcript-speaker {
    color: #00d4ff;
    font-weight: 700;
}

/* ── Safe action buttons ── */
.safe-action {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    font-size: 0.82rem;
    color: #c8c8d8;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.safe-action:hover {
    background: rgba(0, 212, 255, 0.08);
    border-color: rgba(0, 212, 255, 0.3);
    color: #00d4ff;
}

/* ── Metric number ── */
.metric-big {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
}
.metric-label {
    font-size: 0.72rem;
    color: #6b6b8a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'Space Mono', monospace;
    margin-top: 0.25rem;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06); margin: 1.5rem 0; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff22, #7b5ea722);
    border: 1px solid rgba(0, 212, 255, 0.35);
    color: #00d4ff;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    border-radius: 8px;
    padding: 0.5rem 1.25rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: rgba(0, 212, 255, 0.15);
    border-color: rgba(0, 212, 255, 0.6);
    color: #fff;
}
div[data-testid="stTextArea"] textarea {
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #c8c8d8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
}
div[data-testid="stTextInput"] input {
    background: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #c8c8d8 !important;
    font-family: 'Space Mono', monospace !important;
}
.stSlider [data-testid="stSlider"] { accent-color: #00d4ff; }
label, .stSelectbox label, .stTextInput label, .stTextArea label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #6b6b8a !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stCheckbox"] label {
    color: #9898b8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ──────────────────────────────────────────────────────
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0
if "analyzed_count" not in st.session_state:
    st.session_state.analyzed_count = 0
if "consent_given" not in st.session_state:
    st.session_state.consent_given = False


# ── Scam detection logic (rule-based demo) ─────────────────────────────────────
SCAM_PATTERNS = {
    "authority_impersonation": {
        "keywords": ["cbi", "ria", "irs", "police", "arrest warrant", "federal agent",
                     "court order", "officer", "badge number", "interpol", "cybercrime division"],
        "weight": 3,
        "label": "Authority Impersonation",
        "icon": "🎭"
    },
    "digital_arrest": {
        "keywords": ["digital arrest", "you are arrested", "under arrest", "do not move",
                     "stay on the call", "cannot leave", "virtual arrest"],
        "weight": 5,
        "label": "Digital Arrest Tactic",
        "icon": "🔒"
    },
    "urgency_pressure": {
        "keywords": ["immediately", "right now", "last chance", "expire", "urgent",
                     "today only", "no time", "hurry", "deadline", "final warning"],
        "weight": 2,
        "label": "Urgency / Pressure",
        "icon": "⏱️"
    },
    "isolation_tactic": {
        "keywords": ["don't tell anyone", "do not tell", "keep this secret", "confidential matter",
                     "don't call family", "stay silent", "do not hang up"],
        "weight": 4,
        "label": "Isolation Tactic",
        "icon": "🚫"
    },
    "money_demand": {
        "keywords": ["transfer money", "send money", "gift card", "bitcoin", "wire transfer",
                     "pay fine", "clear your name", "bail amount", "penalty fee"],
        "weight": 4,
        "label": "Financial Coercion",
        "icon": "💸"
    },
    "personal_info": {
        "keywords": ["aadhaar", "social security", "bank account", "password", "otp",
                     "pin number", "credit card", "verify your identity", "date of birth"],
        "weight": 3,
        "label": "Personal Info Extraction",
        "icon": "🔑"
    },
}

def analyze_text(text: str):
    text_lower = text.lower()
    findings = []
    total_score = 0

    for pattern_key, pattern in SCAM_PATTERNS.items():
        matched_keywords = [kw for kw in pattern["keywords"] if kw in text_lower]
        if matched_keywords:
            score = pattern["weight"] * len(matched_keywords)
            total_score += score
            findings.append({
                "label": pattern["label"],
                "icon": pattern["icon"],
                "keywords": matched_keywords,
                "score": score,
                "severity": "high" if score >= 5 else "medium" if score >= 2 else "low"
            })

    risk_score = min(100, total_score * 8)
    return findings, risk_score

def get_safe_actions(risk_score, findings):
    actions = []
    labels = [f["label"] for f in findings]

    if risk_score >= 60:
        actions += [
            ("🔴", "Hang up immediately — this is a scam"),
            ("👨‍👩‍👧", "Call a trusted family member or friend"),
            ("🚔", "Report to cybercrime.gov.in or your national fraud hotline"),
        ]
    if "Authority Impersonation" in labels or "Digital Arrest Tactic" in labels:
        actions.append(("ℹ️", "Real agencies never demand immediate payment or threaten arrest over phone"))
    if "Financial Coercion" in labels:
        actions.append(("🏦", "Do NOT transfer money — contact your bank if you already did"))
    if "Isolation Tactic" in labels:
        actions.append(("📢", "Tell someone you trust about this call right now"))
    if risk_score > 0 and risk_score < 40:
        actions.append(("⚠️", "Stay cautious — verify the caller's identity through official channels"))

    return actions


# ── Consent gate ───────────────────────────────────────────────────────────────
if not st.session_state.consent_given:
    st.markdown('<div class="shield-header"><div class="shield-title">🛡️ DigiShield</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="shield-sub">Real-time fraud & coercion detection</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Before we begin")
    st.markdown("""
    <div style="font-size:0.88rem; line-height:1.8; color:#9898b8;">
    DigiShield analyzes your conversations in real time to detect signs of fraud, intimidation, 
    and authority impersonation. Here's what you need to know:
    <br><br>
    🔒 &nbsp;<b style="color:#e8e8f0;">All analysis runs locally</b> — your conversations never leave your device<br>
    🚫 &nbsp;<b style="color:#e8e8f0;">Nothing is recorded or stored</b> — audio and text are discarded after analysis<br>
    👤 &nbsp;<b style="color:#e8e8f0;">You're in control</b> — you can stop monitoring at any time<br>
    🆘 &nbsp;<b style="color:#e8e8f0;">Emergency alerts are optional</b> — you choose if a trusted contact is notified
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1 = st.checkbox("I understand how ScamShield processes my data as described above")
    c2 = st.checkbox("I consent to real-time analysis of conversations on this device")
    c3 = st.checkbox("I am 18 years or older (or have parental consent)")

    if st.button("Activate ScamShield →"):
        if c1 and c2 and c3:
            st.session_state.consent_given = True
            st.rerun()
        else:
            st.error("Please check all boxes to continue.")
    st.stop()


# ── Main App ───────────────────────────────────────────────────────────────────

# Header
st.markdown('<div class="shield-header"><div class="shield-title">🛡️ ScamShield</div></div>', unsafe_allow_html=True)
st.markdown('<div class="shield-sub">Real-time fraud & coercion detection</div>', unsafe_allow_html=True)

# Status pill
if st.session_state.monitoring:
    st.markdown('<div class="status-pill status-active"><div class="status-dot"></div> Monitoring Active</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-pill status-inactive"><div class="status-dot"></div> Standby</div>', unsafe_allow_html=True)

# ── Layout: Left column (input + alerts) | Right column (risk + actions) ──────
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:

    # ── Input panel ──
    st.markdown('<div class="card-label">📝 Paste or type conversation</div>', unsafe_allow_html=True)
    input_text = st.text_area(
        label="input",
        label_visibility="collapsed",
        placeholder='Paste a suspicious message or transcript here...\n\nExample: "This is Officer Singh from CBI. You have an arrest warrant. Do not tell anyone. Transfer ₹50,000 immediately to clear your name."',
        height=160,
        key="main_input"
    )

    btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 3])
    with btn_col1:
        analyze_btn = st.button("⚡ Analyze Now", use_container_width=True)
    with btn_col2:
        demo_btn = st.button("🎭 Load Demo", use_container_width=True)
    with btn_col3:
        clear_btn = st.button("✕ Clear", use_container_width=True)

    # Demo text loader
    DEMO_TEXTS = [
        "This is Officer Rajesh from CBI Cybercrime Division. You are under digital arrest. Do not hang up or tell anyone. You have 30 minutes to transfer ₹75,000 or you will be physically arrested. This is your final warning.",
        "Hello, I'm calling from the IRS. Your social security number has been suspended due to suspicious activity. Press 1 immediately to avoid arrest. This is your last chance before we send officers to your location.",
        "Your Amazon account has been compromised. We need your OTP and credit card details to verify your identity urgently. Do not tell anyone about this call — it's a confidential security investigation.",
    ]

    if demo_btn:
        st.session_state["demo_text"] = random.choice(DEMO_TEXTS)
        st.rerun()

    if "demo_text" in st.session_state and st.session_state.demo_text:
        active_text = st.session_state.demo_text
        st.markdown(f"""
        <div class="transcript-box">
            <span class="transcript-speaker">CALLER:</span><br>
            {active_text}
        </div>
        """, unsafe_allow_html=True)
    else:
        active_text = input_text

    if clear_btn:
        st.session_state.pop("demo_text", None)
        st.session_state.alerts = []
        st.session_state.risk_score = 0
        st.rerun()

    # ── Analysis ──
    if analyze_btn and active_text.strip():
        with st.spinner("Analyzing..."):
            time.sleep(0.6)  # Simulate processing
            findings, risk_score = analyze_text(active_text)
            st.session_state.risk_score = risk_score
            st.session_state.analyzed_count += 1
            st.session_state.alerts = findings

    # ── Alert feed ──
    if st.session_state.alerts:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="card-label">🚨 Detected Patterns</div>', unsafe_allow_html=True)

        for alert in st.session_state.alerts:
            kw_str = ", ".join(f'<span class="transcript-highlight">{k}</span>' for k in alert["keywords"])
            st.markdown(f"""
            <div class="alert-box alert-{alert['severity']}">
                <div class="alert-icon">{alert['icon']}</div>
                <div class="alert-text">
                    <span class="alert-tag">{alert['severity']} risk · {alert['label']}</span>
                    Detected: {kw_str}
                </div>
            </div>
            """, unsafe_allow_html=True)
    elif analyze_btn and active_text.strip():
        st.markdown("""
        <div class="alert-box alert-low">
            <div class="alert-icon">✅</div>
            <div class="alert-text">
                <span class="alert-tag">clear</span>
                No scam patterns detected in this text.
            </div>
        </div>
        """, unsafe_allow_html=True)


with col_right:

    # ── Risk meter ──
    risk = st.session_state.risk_score
    risk_color = "risk-high" if risk >= 60 else "risk-medium" if risk >= 30 else "risk-low"
    risk_label = "HIGH RISK" if risk >= 60 else "MEDIUM RISK" if risk >= 30 else "LOW RISK"
    risk_color_hex = "#ff4545" if risk >= 60 else "#ffb800" if risk >= 30 else "#00d464"

    st.markdown(f"""
    <div class="card">
        <div class="card-label">⚡ Risk Score</div>
        <div class="metric-big" style="color:{risk_color_hex}">{risk}</div>
        <div class="metric-label">{risk_label}</div>
        <div class="risk-bar-bg" style="margin-top:1rem">
            <div class="risk-bar-fill {risk_color}" style="width:{risk}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats ──
    st.markdown(f"""
    <div class="card" style="display:flex; gap:2rem; padding:1rem 1.5rem;">
        <div>
            <div class="metric-big" style="font-size:1.4rem; color:#00d4ff">{len(st.session_state.alerts)}</div>
            <div class="metric-label">Patterns Found</div>
        </div>
        <div>
            <div class="metric-big" style="font-size:1.4rem; color:#7b5ea7">{st.session_state.analyzed_count}</div>
            <div class="metric-label">Analyzed</div>
        </div>
        <div>
            <div class="metric-big" style="font-size:1.4rem; color:#00d464">
                {"ON" if st.session_state.monitoring else "OFF"}
            </div>
            <div class="metric-label">Live Monitor</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Safe actions ──
    if st.session_state.alerts:
        safe_actions = get_safe_actions(risk, st.session_state.alerts)
        if safe_actions:
            st.markdown('<div class="card-label" style="margin-top:0.5rem">🛡️ Suggested Actions</div>', unsafe_allow_html=True)
            for icon, action in safe_actions:
                st.markdown(f"""
                <div class="safe-action">{icon}&nbsp; {action}</div>
                """, unsafe_allow_html=True)

    # ── Emergency contact ──
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="card-label">🆘 Emergency Contact</div>', unsafe_allow_html=True)

    ec_name = st.text_input("Contact name", placeholder="e.g. Priya (Sister)", key="ec_name")
    ec_phone = st.text_input("Phone / Email", placeholder="+91 98765 43210", key="ec_phone")
    ec_enabled = st.checkbox("Auto-alert if risk score exceeds 70", key="ec_enabled")

    if ec_enabled and ec_name and ec_phone:
        if risk >= 70:
            st.markdown(f"""
            <div class="alert-box alert-high" style="margin-top:0.75rem">
                <div class="alert-icon">🆘</div>
                <div class="alert-text">
                    <span class="alert-tag">emergency alert triggered</span>
                    {ec_name} would be notified at {ec_phone}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-box alert-low" style="margin-top:0.75rem">
                <div class="alert-icon">✅</div>
                <div class="alert-text">
                    <span class="alert-tag">standby</span>
                    {ec_name} will be alerted if risk reaches 70+
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Live monitor toggle ──
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button(
        "⏹ Stop Live Monitoring" if st.session_state.monitoring else "▶ Start Live Monitoring",
        use_container_width=True
    ):
        st.session_state.monitoring = not st.session_state.monitoring
        st.rerun()

    if st.session_state.monitoring:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace; font-size:0.68rem; color:#6b6b8a; margin-top:0.5rem; text-align:center;">
            Listening for real-time input...<br>Paste text above to analyze
        </div>
        """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;">
    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a3a5a;">
        🛡️ ScamShield · All processing is local · No data stored
    </div>
    <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#3a3a5a;">
        Report scams: cybercrime.gov.in · 1930 (India Cyber Helpline)
    </div>
</div>
""", unsafe_allow_html=True)