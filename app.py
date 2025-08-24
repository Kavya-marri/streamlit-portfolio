# app.py
import streamlit as st
from io import BytesIO
from PIL import Image
import numpy as np

# Optional niceties (pure-Python, small)
try:
    from streamlit_option_menu import option_menu
    HAVE_OPTION_MENU = True
except Exception:
    HAVE_OPTION_MENU = False

# ----------------------- PAGE SETUP -----------------------
st.set_page_config(
    page_title="Kavya Lakshmi Marri • Portfolio",
    page_icon="🎯",
    layout="wide",
)

# ----------------------- THEME / CSS -----------------------
CSS = """
<style>
/* Layout */
.block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1150px;}
/* Top navbar shell */
.navbar {position: sticky; top: 0; z-index: 999; backdrop-filter: blur(8px);
  background: rgba(15, 23, 36, 0.55); border-bottom: 1px solid rgba(255,255,255,0.06);
  padding: 0.6rem 0.2rem 0.6rem 0.2rem; margin-bottom: 0.8rem;}
/* Hero */
.hero {display:flex; gap: 28px; align-items:center; border-radius: 18px;
  background: linear-gradient(135deg, rgba(110,231,183,0.10), rgba(110,231,183,0.02));
  border: 1px solid rgba(110,231,183,0.22); padding: 26px 28px;}
.gradient {
  background: linear-gradient(92deg,#6EE7B7 0%,#A7F3D0 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.kicker {opacity:.8; letter-spacing:.08em; font-size:.85rem;}
.subtle {opacity:.85;}
/* Cards */
.card {border:1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.02);
  border-radius:16px; padding:16px; box-shadow: 0 10px 22px rgba(0,0,0,.15);}
.card:hover {transform: translateY(-2px); transition: all .25s ease;}
.badge {display:inline-block; padding:6px 10px; border-radius:999px;
  border:1px solid rgba(255,255,255,0.12); margin:3px 4px; font-size:.8rem;}
/* Section heading */
.section h2 {font-size:1.35rem; margin-bottom:.25rem}
.section p.lead {opacity:.85; margin-top:0; margin-bottom:1rem}
/* Footer */
.footer {opacity:.75; text-align:center; margin-top: 2rem;}

/* Small polish */
hr {border-color: rgba(255,255,255,0.06);}
a {text-decoration: none;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------- DATA -----------------------
NAME = "Kavya Lakshmi Marri"
TAGLINE = "Aspiring AIML Engineer • Python & Java Developer • Problem Solver"
PHONE = "+91 6300180559"
EMAIL = "marrikavya90@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/kavya-reddy-btech/"
GITHUB = "https://github.com/Kavya-marri"
HACKERRANK = "https://www.hackerrank.com/marrikavya90"

SUMMARY = (
    "Adaptable and quick-learning professional with hands-on experience in software development, "
    "database optimization, and data analytics. Skilled in Python, Java, and SQL; passionate about "
    "building impactful, scalable solutions and collaborating in teams."
)

TECH_SKILLS = [
    "Python", "Java", "SQL", "HTML", "Pandas", "NumPy", "Matplotlib",
    "OpenCV (basics)", "API Integration", "JDBC", "JavaFX", "Git & GitHub", "Streamlit",
]
SOFT_SKILLS = ["Communication", "Decision-making", "Teamwork & Collaboration", "Written Communication", "Research"]

EXPERIENCE = [
    {
        "role": "Intern",
        "org": "Jathin • Hyderabad, India",
        "time": "Dec 2023 – Jun 2024",
        "bullets": [
            "Assisted in development and execution of software solutions.",
            "Improved coding efficiency by ~25% via optimizations and best practices.",
            "Enhanced database performance through advanced SQL queries and indexing.",
            "Contributed to scalable features to improve team productivity."
        ],
    }
]

PROJECTS = [
    {
        "title": "Automated Text Detection System",
        "desc": "GUI-based text detection app built with Python & image processing; boosts document-processing efficiency.",
        "stack": ["Python", "OpenCV", "Tkinter"],
        "repo": "https://github.com/Kavya-marri/Text-detection-GUI-python",
        "interactive_key": "ocr_demo",
        "image": None,
    },
    {
        "title": "Advanced Library Management System",
        "desc": "Full system with Java, JDBC, SQL & JavaFX; improves library ops and record management.",
        "stack": ["Java", "JDBC", "SQL", "JavaFX"],
        "repo": "https://github.com/Kavya-marri/Library-Management-System",
        "interactive_key": None,
        "image": None,
    },
    {
        "title": "Python Mastery Challenge (100 Days of Code)",
        "desc": "Hands-on practice in automation, data analysis, and APIs; broad Python library exposure.",
        "stack": ["Python", "Pandas", "NumPy"],
        "repo": "https://github.com/Kavya-marri/100_days_of_python",
        "interactive_key": None,
        "image": None,
    },
    {
        "title": "AgroConnect (Demo: Crop Recommendation)",
        "desc": "Smart agriculture concept — simple demo predicts a crop from soil & weather inputs.",
        "stack": ["Streamlit", "Rule-based demo"],
        "repo": None,
        "interactive_key": "crop_demo",
        "image": None,
    },
]

EDU = [
    {"degree": "B.Tech in Artificial Intelligence & Machine Learning", "inst": "VVIT (Andhra Pradesh)", "time": "2024 – 2027"},
    {"degree": "Diploma in Artificial Intelligence & Machine Learning (96.4%)", "inst": "Sri Jyothi Polytechnic College", "time": "2021 – 2024"},
]

CERTS = [
    "Python Certification — HackerRank (Basic Level)",
    "Java Certification — OOP, Multithreading, Frameworks",
    "SQL Certification — Data Modeling & Query Optimization",
]

# ----------------------- HELPERS -----------------------
def badges(items):
    st.markdown("".join([f"<span class='badge'>{x}</span>" for x in items]), unsafe_allow_html=True)

def image_edge_detect(pil_img: Image.Image) -> Image.Image:
    img = pil_img.convert("L")
    arr = np.array(img, dtype=np.float32)
    gx = np.zeros_like(arr); gy = np.zeros_like(arr)
    gx[:, 1:-1] = arr[:, 2:] - arr[:, :-2]
    gy[1:-1, :] = arr[2:, :] - arr[:-2, :]
    mag = np.sqrt(gx**2 + gy**2)
    mag = np.uint8(np.clip(mag / mag.max() * 255 if mag.max() > 0 else mag, 0, 255))
    return Image.fromarray(mag)

def crop_rule_based(n, p, k, temp, humidity, ph, rainfall):
    notes = []
    if ph < 5.5: notes.append("Soil pH is low; consider liming.")
    if ph > 8.0: notes.append("Soil pH is high; consider gypsum/organic amendments.")
    if humidity < 35: notes.append("Low humidity may affect germination; ensure irrigation.")
    if rainfall < 50: notes.append("Low rainfall; plan irrigation schedule.")
    if n >= 100 and k >= 100 and 20 <= temp <= 30 and 60 <= humidity <= 85 and 5.8 <= ph <= 7.5:
        crop = "Rice"
    elif n >= 80 and p >= 50 and 18 <= temp <= 28 and 40 <= rainfall <= 200 and 6.0 <= ph <= 7.0:
        crop = "Wheat"
    elif 24 <= temp <= 35 and k >= 80 and 5.5 <= ph <= 7.5 and rainfall >= 50:
        crop = "Maize"
    elif p >= 60 and 20 <= temp <= 30 and 6.0 <= ph <= 7.5:
        crop = "Pulses"
    else:
        crop = "Millets"
    return crop, notes

def resume_download_uploader():
    st.markdown("**Share your resume:** upload a PDF so visitors can download it.")
    up = st.file_uploader("Upload resume (PDF)", type=["pdf"], label_visibility="collapsed")
    if up:
        data = up.read()
        st.download_button("⬇️ Download uploaded PDF", data=data, file_name="Kavya_Resume.pdf")
        st.success("Resume attached for download.")
    else:
        st.info("No resume uploaded yet.")

# ----------------------- TOP NAV -----------------------
with st.container():
    st.markdown("<div class='navbar'></div>", unsafe_allow_html=True)

if HAVE_OPTION_MENU:
    selected = option_menu(
        None,
        ["Home", "About", "Projects", "Skills", "Experience", "Education", "Certifications", "Resume & Contact"],
        icons=["house","person","kanban","cpu","briefcase","mortarboard","patch-check","envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
else:
    # Fallback to sidebar if package isn't installed
    st.sidebar.title("Navigate")
    selected = st.sidebar.radio("Go to", ["Home","About","Projects","Skills","Experience","Education","Certifications","Resume & Contact"], index=0)

# ----------------------- PAGES -----------------------
if selected == "Home":
    st.markdown(
        f"""
        <div class="hero">
          <div style="flex:1">
            <div class="kicker">PORTFOLIO</div>
            <h1 style="margin:.2rem 0 0 0"><span class="gradient">{NAME}</span></h1>
            <h3 class="subtle" style="margin:.2rem 0 1rem 0">{TAGLINE}</h3>
            <p class="subtle">{SUMMARY}</p>
            <div style="margin-top:.6rem;"> 
              <a href="{LINKEDIN}" target="_blank" class="badge">LinkedIn</a>
              <a href="{GITHUB}" target="_blank" class="badge">GitHub</a>
              <a href="{HACKERRANK}" target="_blank" class="badge">HackerRank</a>
              <span class="badge">📞 {PHONE}</span>
              <span class="badge">✉️ {EMAIL}</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    with st.expander("Upload a resume to offer visitors a download (optional)"):
        resume_download_uploader()

elif selected == "About":
    st.markdown("### About Me")
    st.write(SUMMARY)
    st.markdown("---")
    st.write("**Career Goal**: Build reliable systems at the intersection of AI/ML and software engineering, with clean code and real-world impact.")
    st.write("**Strengths**: Fast learner, detail-oriented, calm under deadlines, collaborative.")

elif selected == "Projects":
    st.markdown("### Projects")
    st.caption("Polished cards with inline demos. Click expanders for interactions.")
    # Grid layout: 2 columns
    cols = st.columns(2, gap="large")
    for i, proj in enumerate(PROJECTS):
        with cols[i % 2]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader(proj["title"])
            st.write(proj["desc"])
            badges(proj["stack"])
            if proj.get("repo"):
                st.markdown(f"🔗 **Repository:** [{proj['repo']}]({proj['repo']})")
            # Demo inside expander to keep card compact
            if proj.get("interactive_key") == "ocr_demo":
                with st.expander("Try mini demo: Visual OCR"):
                    img_file = st.file_uploader("Upload an image with text", type=["png", "jpg", "jpeg"], key=f"ocr_{i}")
                    if img_file:
                        img = Image.open(img_file).convert("RGB")
                        edges = image_edge_detect(img)
                        st.image([img, edges], caption=["Original", "Edges (detect-style)"], use_column_width=True)
                    else:
                        st.info("Upload an image to see the detection effect.")
            elif proj.get("interactive_key") == "crop_demo":
                with st.expander("Try mini demo: Crop Recommendation"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        n = st.number_input("Nitrogen (N)", 0, 200, 90)
                        temp = st.number_input("Temperature (°C)", 0, 50, 28)
                    with c2:
                        p = st.number_input("Phosphorus (P)", 0, 200, 60)
                        humidity = st.number_input("Humidity (%)", 0, 100, 70)
                    with c3:
                        k = st.number_input("Potassium (K)", 0, 200, 80)
                        ph = st.number_input("Soil pH", 0.0, 14.0, 6.5, step=0.1)
                    rainfall = st.number_input("Rainfall (mm)", 0, 500, 120)
                    if st.button("Predict Crop", key=f"cropbtn_{i}"):
                        crop, notes = crop_rule_based(n, p, k, temp, humidity, ph, rainfall)
                        st.success(f"Recommended Crop: **{crop}**")
                        for nt in notes:
                            st.write("• " + nt)
            st.markdown("</div>", unsafe_allow_html=True)
            st.write("")

elif selected == "Skills":
    st.markdown("### Skills")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Technical**")
        badges(TECH_SKILLS)
    with c2:
        st.markdown("**Soft**")
        badges(SOFT_SKILLS)
    st.markdown("---")
    st.write("**Tools I often use:** Git, GitHub, VS Code, MySQL, Streamlit, Jupyter")

elif selected == "Experience":
    st.markdown("### Experience")
    for exp in EXPERIENCE:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"{exp['role']} — {exp['org']}")
        st.caption(exp["time"])
        for b in exp["bullets"]:
            st.write("• " + b)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

elif selected == "Education":
    st.markdown("### Education")
    for e in EDU:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(e["degree"])
        st.caption(f"{e['inst']} • {e['time']}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

elif selected == "Certifications":
    st.markdown("### Certifications")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for c in CERTS:
        st.write("• " + c)
    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "Resume & Contact":
    st.markdown("### Resume")
    resume_download_uploader()
    st.markdown("---")
    st.markdown("### Contact")
    c1, c2, c3 = st.columns(3)
    with c1: st.write(f"📞 **{PHONE}**")
    with c2: st.write(f"✉️ **{EMAIL}**")
    with c3: st.write(f"[LinkedIn]({LINKEDIN}) · [GitHub]({GITHUB}) · [HackerRank]({HACKERRANK})")

# ----------------------- FOOTER -----------------------
st.markdown(f"<div class='footer'>© {NAME} — Built with Streamlit</div>", unsafe_allow_html=True)
