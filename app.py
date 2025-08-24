import streamlit as st
from io import BytesIO
from PIL import Image, ImageOps
import numpy as np

# ----------------------- PAGE SETUP -----------------------
st.set_page_config(
    page_title="Kavya Lakshmi Marri • Portfolio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------- THEME TWEAKS -----------------------
CUSTOM_CSS = """
<style>
/* Tighten layout a bit */
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* Card look */
.card {
  border-radius: 16px;
  padding: 1rem 1.2rem;
  border: 1px solid rgba(128,128,128,0.25);
  background: rgba(255,255,255,0.02);
  box-shadow: 0 6px 24px rgba(0,0,0,0.15);
}

/* Pill buttons */
.pill {
  display:inline-block; padding: 6px 12px; margin: 4px 6px; border-radius: 999px;
  border:1px solid rgba(128,128,128,0.25);
  font-size: 0.85rem;
}

/* Section titles */
h2 span, h3 span { border-bottom: 2px solid rgba(128,128,128,0.35); padding-bottom: 4px; }

/* Footer */
.footer {
  opacity: 0.8; font-size: 0.9rem; margin-top: 2rem; text-align:center;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------- DATA (YOUR DETAILS) -----------------------
NAME = "Kavya Lakshmi Marri"
TAGLINE = "Aspiring AIML Engineer • Python & Java Developer • Problem Solver"
PHONE = "+91 6300180559"
EMAIL = "marrikavya90@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/kavya-reddy-btech/"
GITHUB = "https://github.com/Kavya-marri"
HACKERRANK = "https://www.hackerrank.com/marrikavya90"

SUMMARY = (
    "Adaptable and quick-learning professional with hands-on experience in software "
    "development, database optimization, and data analytics. Skilled in Python, Java, and SQL; "
    "passionate about building impactful, scalable solutions and collaborating in teams."
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
            "Improved coding efficiency by ~25% through code optimizations and best practices.",
            "Enhanced database performance via advanced SQL queries and indexing.",
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
        "interactive_key": "ocr_demo",  # in-app demo below
    },
    {
        "title": "Advanced Library Management System",
        "desc": "Full system with Java, JDBC, SQL & JavaFX; improves library ops and record management.",
        "stack": ["Java", "JDBC", "SQL", "JavaFX"],
        "repo": "https://github.com/Kavya-marri/Library-Management-System",
        "interactive_key": None,
    },
    {
        "title": "Python Mastery Challenge (100 Days of Code)",
        "desc": "Hands-on practice in automation, data analysis, and APIs; broad Python library exposure.",
        "stack": ["Python", "Pandas", "NumPy", "Matplotlib"],
        "repo": "https://github.com/Kavya-marri/100_days_of_python",
        "interactive_key": None,
    },
    {
        "title": "AgroConnect (Demo: Crop Recommendation)",
        "desc": "Smart agriculture concept — simple demo predicts a crop from soil & weather inputs.",
        "stack": ["Streamlit", "Rule-based demo"],
        "repo": None,
        "interactive_key": "crop_demo",
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
def badge_row(items):
    out = ""
    for x in items:
        out += f"<span class='pill'>{x}</span>"
    st.markdown(out, unsafe_allow_html=True)

def make_card(title, body_md, right_md=None):
    col1, col2 = st.columns([0.68, 0.32])
    with col1:
        st.markdown(f"### {title}")
        st.markdown(body_md)
    with col2:
        st.markdown(right_md or "")

def image_edge_detect(pil_img: Image.Image) -> Image.Image:
    """
    Lightweight 'visual OCR' demo (no Tesseract). We convert to grayscale and
    show edges so it *looks* like detection.
    """
    img = pil_img.convert("L")
    # Sobel-like effect via PIL (cheap approximation)
    arr = np.array(img, dtype=np.float32)
    # Horizontal & vertical gradients
    gx = np.zeros_like(arr)
    gy = np.zeros_like(arr)
    gx[:, 1:-1] = arr[:, 2:] - arr[:, :-2]
    gy[1:-1, :] = arr[2:, :] - arr[:-2, :]
    mag = np.sqrt(gx**2 + gy**2)
    mag = np.uint8(np.clip(mag / mag.max() * 255 if mag.max() > 0 else mag, 0, 255))
    return Image.fromarray(mag)

def crop_rule_based(n, p, k, temp, humidity, ph, rainfall):
    """
    Super-simple, explainable heuristic to demo the idea.
    """
    # Basic guards
    issues = []
    if ph < 5.5: issues.append("Soil pH is low; consider liming.")
    if ph > 8.0: issues.append("Soil pH is high; consider gypsum or organic amendments.")
    if humidity < 35: issues.append("Low humidity may affect germination; ensure irrigation.")
    if rainfall < 50: issues.append("Low rainfall; plan irrigation schedule.")

    # Naive logic
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
    return crop, issues

def download_button_from_bytes(name: str, data: bytes, label: str):
    st.download_button(label=label, data=data, file_name=name)


# ----------------------- SIDEBAR NAV -----------------------
st.sidebar.title("Navigate")
page = st.sidebar.radio(
    "Go to",
    ["Home", "About", "Projects", "Skills", "Experience", "Education", "Certifications", "Resume & Contact"],
    index=0
)

# Quick links
st.sidebar.markdown("### Quick Links")
st.sidebar.markdown(f"[LinkedIn]({LINKEDIN}) • [GitHub]({GITHUB}) • [HackerRank]({HACKERRANK})")

# ----------------------- PAGES -----------------------
if page == "Home":
    left, right = st.columns([0.62, 0.38], vertical_alignment="center")
    with left:
        st.markdown(f"# {NAME}")
        st.markdown(f"**{TAGLINE}**")
        st.markdown(SUMMARY)
        badge_row(["AIML", "Python", "Java", "SQL", "Data Analytics", "Problem Solving"])
        st.markdown("—")
        st.markdown(f"📞 **{PHONE}** &nbsp;|&nbsp; ✉️ **{EMAIL}**")
        st.markdown(f"[LinkedIn]({LINKEDIN}) &nbsp;|&nbsp; [GitHub]({GITHUB}) &nbsp;|&nbsp; [HackerRank]({HACKERRANK})")
    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Download My Resume")
        uploaded_resume = st.file_uploader("Optional: Re-upload updated resume (PDF)", type=["pdf"], label_visibility="collapsed")
        if uploaded_resume is not None:
            data = uploaded_resume.read()
            download_button_from_bytes("Kavya_Resume.pdf", data, "⬇️ Download uploaded PDF")
            st.success("Resume attached for download.")
        else:
            st.info("Upload your latest resume PDF here (so visitors can download).")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "About":
    st.markdown("## <span>About Me</span>", unsafe_allow_html=True)
    st.markdown(SUMMARY)
    st.markdown("—")
    st.markdown("**Career Goal:** Build intelligent, reliable systems at the intersection of AI/ML and software engineering, with clean code and real-world impact.")
    st.markdown("**Strengths:** Fast learner, detail-oriented, calm under deadlines, collaborative.")

elif page == "Projects":
    st.markdown("## <span>Projects</span>", unsafe_allow_html=True)
    st.write("Explore selected work. Some projects include interactive demos.")

    for proj in PROJECTS:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        cols = st.columns([0.7, 0.3])
        with cols[0]:
            st.markdown(f"### {proj['title']}")
            st.write(proj["desc"])
            badge_row(proj["stack"])
            if proj.get("repo"):
                st.markdown(f"🔗 **Repository:** {proj['repo']}")
        with cols[1]:
            if proj.get("interactive_key") == "ocr_demo":
                st.markdown("**Mini Demo: Visual OCR**")
                img_file = st.file_uploader("Upload an image with text", type=["png", "jpg", "jpeg"], key="ocr_upl")
                if img_file:
                    img = Image.open(img_file).convert("RGB")
                    edges = image_edge_detect(img)
                    st.image([img, edges], caption=["Original", "Edges (detect-style)"], use_column_width=True)
                    st.caption("For deployment simplicity, this demo shows edge-based detection visuals.")
                else:
                    st.info("Upload an image to see the detection effect.")
            elif proj.get("interactive_key") == "crop_demo":
                st.markdown("**Mini Demo: Crop Recommendation**")
                with st.form("crop_form"):
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
                    submitted = st.form_submit_button("Predict Crop")
                if submitted:
                    crop, notes = crop_rule_based(n, p, k, temp, humidity, ph, rainfall)
                    st.success(f"Recommended Crop: **{crop}**")
                    if notes:
                        with st.expander("Notes & Tips"):
                            for nt in notes:
                                st.write("• " + nt)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

elif page == "Skills":
    st.markdown("## <span>Skills</span>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Technical")
        badge_row(TECH_SKILLS)
    with col2:
        st.markdown("### Soft")
        badge_row(SOFT_SKILLS)
    st.markdown("—")
    st.markdown("**Tools I often use:** Git, GitHub, VS Code, MySQL, Streamlit, Jupyter")

elif page == "Experience":
    st.markdown("## <span>Experience</span>", unsafe_allow_html=True)
    for exp in EXPERIENCE:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {exp['role']} — {exp['org']}")
        st.caption(exp["time"])
        for b in exp["bullets"]:
            st.write("• " + b)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

elif page == "Education":
    st.markdown("## <span>Education</span>", unsafe_allow_html=True)
    for e in EDU:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {e['degree']}")
        st.caption(f"{e['inst']} &nbsp;•&nbsp; {e['time']}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")

elif page == "Certifications":
    st.markdown("## <span>Certifications</span>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for c in CERTS:
        st.write("• " + c)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Resume & Contact":
    st.markdown("## <span>Resume & Contact</span>", unsafe_allow_html=True)

    # Resume upload/display
    st.markdown("### Resume")
    up = st.file_uploader("Upload a PDF so visitors can download it:", type=["pdf"], key="resume_page_upl")
    if up:
        data = up.read()
        download_button_from_bytes("Kavya_Resume.pdf", data, "⬇️ Download this resume")
        st.success("Resume ready for visitors to download.")
    else:
        st.info("Upload your latest resume here.")

    # Contacts
    st.markdown("### Contact")
    st.write(f"📞 **{PHONE}**")
    st.write(f"✉️ **{EMAIL}**")
    st.write(f"[LinkedIn]({LINKEDIN}) • [GitHub]({GITHUB}) • [HackerRank]({HACKERRANK})")

    # Quick message form (optional — local only; no email sending)
    with st.expander("Send a quick message (demo)"):
        name = st.text_input("Your Name")
        mail = st.text_input("Your Email")
        msg = st.text_area("Message")
        if st.button("Submit"):
            if name and mail and msg:
                st.success("Thanks! (For production, wire this to a Google Form or SMTP.)")
            else:
                st.error("Please fill all fields.")

# ----------------------- FOOTER -----------------------
st.markdown("<div class='footer'>© " + NAME + " — Built with Streamlit</div>", unsafe_allow_html=True)
