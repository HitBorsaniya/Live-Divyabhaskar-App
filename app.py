import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Divya Bhaskar — News Intelligence",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Gujarati:wght@400;600;700&display=swap');
#
# html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 1.5rem 2rem; }
#
# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
#     border-right: 1px solid #334155;
# }
# [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
# [data-testid="stSidebar"] .stRadio > div { gap: 10px; }
# [data-testid="stSidebar"] .stRadio label {
#     background: #1e293b !important;
#     border: 1px solid #334155 !important;
#     border-radius: 12px !important;
#     min-height: 52px !important;
#     width: 100% !important;
#     display: flex !important;
#     align-items: center !important;
#     padding: 0 18px !important;
#     margin: 0 !important;
#     font-size: 14px !important;
#     font-weight: 600 !important;
#     transition: all 0.25s ease !important;
#     cursor: pointer !important;
# }
# [data-testid="stSidebar"] .stRadio label:hover {
#     background: #0ea5e9 !important;
#     border-color: #0ea5e9 !important;
#     transform: translateX(4px) !important;
# }
# [data-testid="stSidebar"] .stRadio label:has(input:checked) {
#     background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
#     border-color: #38bdf8 !important;
#     box-shadow: 0 4px 15px rgba(14,165,233,0.3) !important;
# }
# [data-testid="stSidebar"] .stRadio > label { display: none !important; }
#
# .metric-card {
#     background: linear-gradient(135deg, #0f172a, #1e293b);
#     border: 1px solid #334155;
#     border-radius: 16px;
#     padding: 20px 24px;
#     text-align: center;
#     transition: transform 0.2s;
# }
# .metric-card:hover { transform: translateY(-3px); }
# .metric-card .value { font-size: 2rem; font-weight: 700; color: #0ea5e9; line-height: 1.1; }
# .metric-card .label { font-size: 0.75rem; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
#
# .hero-banner {
#     background: linear-gradient(135deg, #0f172a 0%, #0c4a6e 50%, #0f172a 100%);
#     border: 1px solid #0ea5e9;
#     border-radius: 20px;
#     padding: 40px;
#     margin-bottom: 24px;
#     position: relative;
#     overflow: hidden;
# }
# .hero-banner::before {
#     content: '📰';
#     position: absolute; right: 40px; top: 50%;
#     transform: translateY(-50%);
#     font-size: 6rem; opacity: 0.1;
# }
# .hero-title { font-size: 2rem; font-weight: 700; color: #f1f5f9; margin: 0 0 8px 0; }
# .hero-sub   { font-size: 1rem; color: #94a3b8; margin: 0; }
# .hero-badge {
#     display: inline-block; background: #0ea5e9; color: white;
#     padding: 4px 12px; border-radius: 20px;
#     font-size: 0.75rem; font-weight: 600; margin-bottom: 12px;
# }
#
# .result-card {
#     background: linear-gradient(135deg, #0c4a6e, #0f172a);
#     border: 2px solid #0ea5e9; border-radius: 16px;
#     padding: 28px; text-align: center;
# }
# .section-header {
#     font-size: 1.2rem; font-weight: 700; color: #f1f5f9;
#     border-left: 4px solid #0ea5e9;
#     padding-left: 12px; margin: 24px 0 16px 0;
# }
# .divider { border: none; border-top: 1px solid #334155; margin: 20px 0; }
#
# .stTextArea textarea {
#     background: #1e293b !important; border: 1px solid #334155 !important;
#     border-radius: 12px !important; color: #f1f5f9 !important;
#     font-family: 'Noto Sans Gujarati', sans-serif !important; font-size: 1rem !important;
# }
# .stButton button {
#     background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
#     color: white !important; border: none !important;
#     border-radius: 10px !important; font-weight: 600 !important;
#     transition: all 0.2s !important;
# }
# .stButton button:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 4px 12px #0ea5e940 !important;
# }
# </style>
# """, unsafe_allow_html=True)

# ── Category config ──────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Gujarati:wght@400;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit elements */
# MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 1.5rem 2rem; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    cursor: pointer;
    transition: all 0.2s;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #0ea5e9 !important;
    border-color: #0ea5e9;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-card .value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0ea5e9;
    line-height: 1.1;
}
.metric-card .label {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #0c4a6e 50%, #0f172a 100%);
    border: 1px solid #0ea5e9;
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '📰';
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.1;
}
.hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 8px 0;
}
.hero-sub {
    font-size: 1rem;
    color: #94a3b8;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: #0ea5e9;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 12px;
}

/* Predict result card */
.result-card {
    background: linear-gradient(135deg, #0c4a6e, #0f172a);
    border: 2px solid #0ea5e9;
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}
.result-category {
    font-size: 2rem;
    font-weight: 700;
    color: #0ea5e9;
}
.result-confidence {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 6px;
}

/* News card */
.news-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 4px solid #0ea5e9;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.news-card:hover {
    border-left-color: #38bdf8;
    background: #263548;
}
.news-title {
    font-family: 'Noto Sans Gujarati', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1.5;
}
.news-meta {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 6px;
}
.cat-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    background: #0ea5e920;
    color: #38bdf8;
    border: 1px solid #0ea5e940;
}

/* Section header */
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    border-left: 4px solid #0ea5e9;
    padding-left: 12px;
    margin: 24px 0 16px 0;
}

/* Accuracy badge */
.acc-high { color: #22c55e; font-weight: 700; }
.acc-med  { color: #f59e0b; font-weight: 700; }
.acc-low  { color: #ef4444; font-weight: 700; }

/* Input area */
.stTextArea textarea {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
    font-family: 'Noto Sans Gujarati', sans-serif !important;
    font-size: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 2px #0ea5e920 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px #0ea5e940 !important;
}

/* Selectbox */
.stSelectbox select {
    background: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #334155 !important;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #334155;
    margin: 20px 0;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 10px;
}

[data-testid="stSidebar"] .stRadio label {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    min-height: 60px !important;
    width: 100% !important;

    display: flex !important;
    align-items: center !important;

    padding: 0 18px !important;
    margin: 0 !important;

    font-size: 15px !important;
    font-weight: 600 !important;

    transition: all 0.25s ease !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: #0ea5e9 !important;
    border-color: #0ea5e9 !important;
    transform: translateX(4px);
}

/* Selected item */
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border-color: #38bdf8 !important;
    box-shadow: 0 4px 15px rgba(14,165,233,0.3);
}

[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}


</style>
""", unsafe_allow_html=True)

CATEGORY_EMOJI = {
    'sports'        : '🏏',
    'entertainment' : '🎬',
    'business'      : '💼',
    'national'      : '🇮🇳',
    'international' : '🌍',
    'local/gujarat' : '📍',
    'lifestyle'     : '✨',
    'dharm-darshan' : '🕉️',
    'health'        : '🏥',
    'crime'         : '🔍',
    'explainer'     : '📖',
    'utility'       : '🔧',
}
CATEGORY_COLOR = {
    'sports'        : '#f59e0b',
    'entertainment' : '#ec4899',
    'business'      : '#22c55e',
    'national'      : '#f97316',
    'international' : '#8b5cf6',
    'local/gujarat' : '#06b6d4',
    'lifestyle'     : '#a78bfa',
    'dharm-darshan' : '#fbbf24',
    'health'        : '#34d399',
    'crime'         : '#f87171',
    'explainer'     : '#60a5fa',
    'utility'       : '#94a3b8',
}

# ── Model performance data ───────────────────────────────────
PERF_DATA = {
    'Category'  : ['business', 'dharm-darshan', 'entertainment', 'international',
                   'lifestyle', 'local/gujarat', 'national', 'sports'],
    'Precision' : [0.85, 0.97, 0.85, 0.72, 0.83, 0.78, 0.65, 0.92],
    'Recall'    : [0.85, 0.93, 0.84, 0.69, 0.86, 0.87, 0.65, 0.88],
    'F1'        : [0.85, 0.95, 0.85, 0.70, 0.84, 0.82, 0.65, 0.90],
    'Support'   : [1003, 1003, 998, 939, 1002, 992, 937, 971],
}

# ── Load model ───────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = pickle.load(open(r"model.pkl",         "rb"))
    tfidf = pickle.load(open(r"tfidf.pkl",         "rb"))
    le    = pickle.load(open(r"label_encoder.pkl", "rb"))
    return model, tfidf, le

model, tfidf, le = load_model()

# ── Predict ──────────────────────────────────────────────────
def predict(title):
    vec      = tfidf.transform([title])
    pred_id  = model.predict(vec)[0]
    proba    = model.predict_proba(vec)[0]
    category = le.inverse_transform([pred_id])[0]
    all_proba = {
        le.inverse_transform([i])[0]: round(float(p) * 100, 2)
        for i, p in enumerate(proba)
    }
    return category, round(float(proba[pred_id]) * 100, 2), all_proba

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px 0;'>
        <div style='font-size:2.5rem;'>📰</div>
        <div style='font-size:1.1rem; font-weight:700; color:#f1f5f9;'>Divya Bhaskar</div>
        <div style='font-size:0.75rem; color:#64748b;'>News Intelligence Platform</div>
    </div>
    <hr style='border-color:#334155; margin:12px 0;'>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠  Dashboard",
        "🔍  Predict Category",
        # "🤖  Model Insights"
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#334155; margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.75rem; color:#64748b; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:10px;'>
        Project Info
    </div>
    <div style='display:flex; flex-direction:column; gap:8px;'>
        <div style='background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #334155;'>
            <span style='color:#0ea5e9; font-weight:700;'>40,000+</span>
            <span style='color:#64748b; font-size:0.8rem;'> articles scraped</span>
        </div>
        <div style='background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #334155;'>
            <span style='color:#0ea5e9; font-weight:700;'>8</span>
            <span style='color:#64748b; font-size:0.8rem;'> categories</span>
        </div>
        <div style='background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #334155;'>
            <span style='color:#22c55e; font-weight:700;'>82%</span>
            <span style='color:#64748b; font-size:0.8rem;'> model accuracy</span>
        </div>
        <div style='background:#0f172a; border-radius:8px; padding:10px 14px; border:1px solid #334155;'>
            <span style='color:#f59e0b; font-weight:700;'>Gujarati</span>
            <span style='color:#64748b; font-size:0.8rem;'> language NLP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ════════════════════════════════════════════════════════════
if "Dashboard" in page:

    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-badge'>🚀 ML Powered — Gujarati NLP</div>
        <div class='hero-title'>Gujarati News Intelligence</div>
        <p class='hero-sub'>
            Real-time category classification of Divya Bhaskar news<br>
            TF-IDF + Logistic Regression trained on 40,000+ Gujarati headlines
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [
        (c1, "40,000+", "Articles Scraped"),
        (c2, "8",       "Categories"),
        (c3, "82%",     "Model Accuracy"),
        (c4, "Gujarati","Language"),
    ]:
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value'>{val}</div>
                <div class='label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Category distribution — static from training data
    st.markdown("<div class='section-header'>📊 Training Data Distribution</div>", unsafe_allow_html=True)

    train_dist = pd.DataFrame({
        'Category': ['business', 'dharm-darshan', 'entertainment', 'international',
                     'lifestyle', 'local/gujarat', 'national', 'sports'],
        'Count'   : [5000, 5000, 4990, 4695, 5010, 4960, 4685, 4855]
    })

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(
            train_dist, x='Category', y='Count',
            color='Category',
            color_discrete_map=CATEGORY_COLOR,
            text='Count'
        )
        fig.update_traces(textposition='outside', textfont_size=11)
        fig.update_layout(
            plot_bgcolor='#0f172a', paper_bgcolor='#0f172a',
            font_color='#94a3b8', showlegend=False, height=350,
            margin=dict(t=10, b=10),
            xaxis=dict(gridcolor='#1e293b', tickangle=-30),
            yaxis=dict(gridcolor='#1e293b'),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            train_dist, names='Category', values='Count',
            hole=0.55, color='Category',
            color_discrete_map=CATEGORY_COLOR,
        )
        fig2.update_traces(textposition='outside', textinfo='label+percent', textfont_size=9)
        fig2.update_layout(
            plot_bgcolor='#0f172a', paper_bgcolor='#0f172a',
            font_color='#94a3b8', showlegend=False, height=350,
            margin=dict(t=10, b=10),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Quick predict on dashboard
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>⚡ Quick Predict</div>", unsafe_allow_html=True)

    quick_input = st.text_input(
        "Quick Predict Input",
        placeholder="Type any Gujarati headline... e.g. IPL મેચમાં CSK જીત્યું",
        label_visibility="collapsed"
    )
    if quick_input.strip():
        cat, conf, _ = predict(quick_input)
        emoji = CATEGORY_EMOJI.get(cat, '📰')
        color = CATEGORY_COLOR.get(cat, '#0ea5e9')
        st.markdown(f"""
        <div style='background:#1e293b; border:1px solid {color}; border-radius:12px;
                    padding:16px 20px; display:flex; align-items:center; gap:16px; margin-top:8px;'>
            <span style='font-size:2rem;'>{emoji}</span>
            <div>
                <div style='color:{color}; font-size:1.2rem; font-weight:700;'>{cat.title()}</div>
                <div style='color:#64748b; font-size:0.85rem;'>Confidence: {conf}%</div>
            </div>
            <div style='margin-left:auto;'>
                <div style='background:{color}20; border-radius:20px; padding:4px 14px;
                            color:{color}; font-size:0.85rem; font-weight:600;'>{conf}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 2 — PREDICT
# ════════════════════════════════════════════════════════════
elif "Predict" in page:

    st.markdown("<div class='hero-title' style='color:#f1f5f9;'>🔍 Predict News Category</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Enter any Gujarati headline — model classifies it instantly</p>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    user_input = st.text_area(
        "✍️ Gujarati News Title",
        placeholder="દા.ત. IPL મેચમાં CSK જીત્યું...\nદા.ત. શેરબજારમાં ભારે ઘટાડો...",
        height=120
    )

    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    predict_btn = col_btn1.button("🚀 Predict",  use_container_width=True)
    clear_btn   = col_btn2.button("🗑️ Clear",    use_container_width=True)

    if predict_btn and user_input.strip():
        with st.spinner("Analyzing..."):
            time.sleep(0.3)
            category, confidence, all_proba = predict(user_input)

        emoji = CATEGORY_EMOJI.get(category, '📰')
        color = CATEGORY_COLOR.get(category, '#0ea5e9')

        if   confidence >= 80: level, lcolor = "High Confidence",     "#22c55e"
        elif confidence >= 50: level, lcolor = "Moderate Confidence", "#f59e0b"
        else:                  level, lcolor = "Low Confidence",      "#ef4444"

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class='result-card' style='border-color:{color};'>
                <div style='font-size:3.5rem; margin-bottom:8px;'>{emoji}</div>
                <div style='font-size:1.8rem; font-weight:700; color:{color};'>{category.title()}</div>
                <div style='font-size:0.9rem; color:#94a3b8; margin-top:6px;'>Confidence Score</div>
                <div style='font-size:2.5rem; font-weight:800; color:#f1f5f9; margin-top:4px;'>{confidence}%</div>
            </div>
            <div style='background:#1e293b; border-radius:10px; padding:12px 16px;
                        border:1px solid #334155; margin-top:12px; text-align:center;'>
                <span style='color:{lcolor}; font-weight:600;'>● {level}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            proba_df = pd.DataFrame(
                list(all_proba.items()), columns=['Category', 'Confidence']
            ).sort_values('Confidence', ascending=True)
            proba_df['Color'] = proba_df['Category'].map(CATEGORY_COLOR).fillna('#0ea5e9')

            fig = go.Figure(go.Bar(
                x=proba_df['Confidence'],
                y=proba_df['Category'],
                orientation='h',
                marker_color=proba_df['Color'],
                text=[f"{v:.1f}%" for v in proba_df['Confidence']],
                textposition='outside',
                textfont=dict(size=11, color='#94a3b8')
            ))
            fig.update_layout(
                plot_bgcolor='#0f172a', paper_bgcolor='#1e293b',
                font_color='#94a3b8', height=380,
                margin=dict(t=30, b=10, l=10, r=60),
                xaxis=dict(gridcolor='#334155', title='Confidence %'),
                yaxis=dict(gridcolor='#334155'),
                title=dict(text="All Category Probabilities", font=dict(color='#f1f5f9', size=14))
            )
            st.plotly_chart(fig, use_container_width=True)

    elif predict_btn:
        st.warning("⚠️ Please enter a Gujarati headline first!")

    # Quick examples
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>⚡ Try These Examples</div>", unsafe_allow_html=True)

    examples = [
        ("🏏", "IPL મેચમાં CSK જીત્યું"),
        ("💼", "શેરબજારમાં ભારે ઘટાડો"),
        ("🎬", "બોલિવૂડ સ્ટારની નવી ફિલ્મ રિલીઝ"),
        ("🇮🇳", "મોદી સરકારનો મહત્વનો નિર્ણય"),
        ("🌍", "અમેરિકા-ઈરાન વચ્ચે તણાવ વધ્યો"),
        ("🕉️", "ગણેશ ઉત્સવ ધામધૂમથી ઉજવાયો"),
    ]

    cols = st.columns(3)
    for i, (emoji, ex) in enumerate(examples):
        with cols[i % 3]:
            if st.button(f"{emoji} {ex[:28]}", key=f"ex_{i}", use_container_width=True):
                cat, conf, _ = predict(ex)
                color = CATEGORY_COLOR.get(cat, '#0ea5e9')
                st.markdown(f"""
                <div style='background:#1e293b; border:1px solid {color}40;
                            border-radius:10px; padding:12px; margin-top:4px;'>
                    <div style='color:{color}; font-weight:700;'>{cat.title()}</div>
                    <div style='color:#64748b; font-size:0.8rem;'>{conf}% confidence</div>
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PAGE 3 — MODEL INSIGHTS
# ════════════════════════════════════════════════════════════
elif "Model" in page:

    st.markdown("<div class='hero-title' style='color:#f1f5f9;'>🤖 Model Insights</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Performance metrics, training details and category analysis</p>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Top metrics
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in [
        (c1, "TF-IDF",    "Vectorizer"),
        (c2, "Log. Reg.", "Algorithm"),
        (c3, "82%",       "Accuracy"),
        (c4, "40K+",      "Training Data"),
    ]:
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='value'>{val}</div>
                <div class='label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    perf_df = pd.DataFrame(PERF_DATA)

    # Grouped bar — Precision / Recall / F1
    st.markdown("<div class='section-header'>🎯 Precision, Recall & F1 per Category</div>", unsafe_allow_html=True)
    fig_perf = go.Figure()
    for metric, color in [('Precision', '#0ea5e9'), ('Recall', '#22c55e'), ('F1', '#f59e0b')]:
        fig_perf.add_trace(go.Bar(
            name=metric, x=perf_df['Category'], y=perf_df[metric],
            marker_color=color,
            text=[f"{v:.0%}" for v in perf_df[metric]],
            textposition='outside', textfont=dict(size=9)
        ))
    fig_perf.update_layout(
        barmode='group',
        plot_bgcolor='#0f172a', paper_bgcolor='#0f172a',
        font_color='#94a3b8', height=380,
        margin=dict(t=10, b=10),
        xaxis=dict(gridcolor='#1e293b', tickangle=-20),
        yaxis=dict(gridcolor='#1e293b', range=[0, 1.15]),
        legend=dict(bgcolor='#1e293b', bordercolor='#334155')
    )
    st.plotly_chart(fig_perf, use_container_width=True)

    # F1 mini cards
    st.markdown("<div class='section-header'>📈 F1 Score Cards</div>", unsafe_allow_html=True)
    cols = st.columns(len(perf_df))
    for i, (_, row) in enumerate(perf_df.iterrows()):
        f1    = row['F1']
        emoji = CATEGORY_EMOJI.get(row['Category'], '📰')
        color = '#22c55e' if f1 >= 0.85 else '#f59e0b' if f1 >= 0.70 else '#ef4444'
        with cols[i]:
            st.markdown(f"""
            <div class='metric-card' style='padding:14px 8px;'>
                <div style='font-size:1.4rem;'>{emoji}</div>
                <div style='font-size:1.2rem; font-weight:700; color:{color};'>{f1:.0%}</div>
                <div style='font-size:0.62rem; color:#64748b; margin-top:2px;'>{row['Category']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Radar chart
    st.markdown("<div class='section-header'>🕸️ Performance Radar</div>", unsafe_allow_html=True)
    fig_radar = go.Figure()
    categories_r = perf_df['Category'].tolist()
    for metric, color in [('Precision', '#0ea5e9'), ('Recall', '#22c55e'), ('F1', '#f59e0b')]:
        vals = perf_df[metric].tolist()
        fig_radar.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories_r + [categories_r[0]],
            fill='toself', name=metric,
            line_color=color,
            fillcolor=color.replace('#', '#') + '20'
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='#0f172a',
            radialaxis=dict(visible=True, range=[0, 1], gridcolor='#334155', color='#64748b'),
            angularaxis=dict(gridcolor='#334155', color='#94a3b8')
        ),
        paper_bgcolor='#0f172a', font_color='#94a3b8',
        showlegend=True, height=420,
        legend=dict(bgcolor='#1e293b', bordercolor='#334155')
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Model config table
    st.markdown("<div class='section-header'>⚙️ Model Configuration</div>", unsafe_allow_html=True)
    config = {
        "Vectorizer"         : "TF-IDF (char_wb, ngram 2-4)",
        "Max Features"       : "10,000",
        "Algorithm"          : "Logistic Regression",
        "Solver"             : "lbfgs (multinomial)",
        "Class Weight"       : "balanced",
        "Max Iterations"     : "3,000",
        "Train / Test Split" : "80% / 20%",
        "Training Records"   : "~32,000",
        "Test Records"       : "~7,845",
        "Language"           : "Gujarati (ગુજરાતી)",
        "Source"             : "Divya Bhaskar (divyabhaskar.co.in)",
        "Scraping Method"    : "REST API + requests",
    }
    for k, v in config.items():
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; padding:10px 16px;
                    background:#1e293b; border-radius:8px; margin-bottom:6px; border:1px solid #334155;'>
            <span style='color:#94a3b8; font-size:0.85rem;'>{k}</span>
            <span style='color:#0ea5e9; font-weight:600; font-size:0.85rem;'>{v}</span>
        </div>
        """, unsafe_allow_html=True)