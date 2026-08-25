import streamlit as st
import pandas as pd
import re
import io
import textwrap

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if not hasattr(st, "html"):
    raise RuntimeError(
        "This app requires Streamlit with st.html support. "
        "Run: pip install --upgrade streamlit"
    )


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResumeAI | Smart Candidate Screening",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_html(html):
    """Render custom HTML directly without Markdown code-block parsing."""
    st.html(textwrap.dedent(html).strip())


# =========================================================
# CUSTOM CSS
# =========================================================

render_html("""
<style>

    /* ---------------- GLOBAL ---------------- */

    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(124, 92, 255, 0.12), transparent 25%),
            radial-gradient(circle at 10% 35%, rgba(0, 196, 180, 0.08), transparent 25%),
            #0B1020;
        color: #E8ECF4;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }


    /* ---------------- SIDEBAR ---------------- */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #11182C 0%,
                #0B1020 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    .sidebar-brand {
        padding: 20px 10px 25px 10px;
        text-align: center;
    }

    .sidebar-logo {
        width: 68px;
        height: 68px;
        margin: 0 auto 14px auto;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 26px;
        font-weight: 800;
        letter-spacing: 1px;

        color: white;

        background:
            linear-gradient(
                135deg,
                #7C5CFF,
                #00C4B4
            );

        box-shadow:
            0 10px 30px rgba(124,92,255,0.35);
    }

    .sidebar-name {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    .sidebar-role {
        font-size: 13px;
        color: #9BA7C0;
        line-height: 1.6;
    }

    .sidebar-section-title {
        color: #9BA7C0;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 25px;
        margin-bottom: 10px;
    }


    /* ---------------- HERO ---------------- */

    .hero-container {
        position: relative;
        overflow: hidden;

        padding: 34px 38px;
        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                rgba(124,92,255,0.16),
                rgba(0,196,180,0.08)
            );

        border:
            1px solid rgba(255,255,255,0.10);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.22);

        margin-bottom: 30px;
    }

    .hero-container:before {
        content: "";
        position: absolute;

        width: 300px;
        height: 300px;

        right: -100px;
        top: -160px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(124,92,255,0.35),
                transparent 65%
            );
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1.2px;
        color: #F7F8FC;
        margin-bottom: 8px;
    }

    .hero-title span {
        background:
            linear-gradient(
                90deg,
                #A995FF,
                #43E8D7
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #AAB4C8;
        font-size: 16px;
        max-width: 720px;
        line-height: 1.7;
    }

    .hero-badges {
        margin-top: 20px;
    }

    .hero-badge {
        display: inline-block;

        padding: 7px 13px;
        margin-right: 8px;
        margin-bottom: 5px;

        border-radius: 30px;

        font-size: 12px;
        font-weight: 600;

        color: #DDE3F0;

        background:
            rgba(255,255,255,0.06);

        border:
            1px solid rgba(255,255,255,0.08);
    }


    /* ---------------- TOP BRAND ---------------- */

    .top-brand {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
    }

    .top-brand-text {
        text-align: right;
        line-height: 1.25;
    }

    .top-brand-name {
        color: #F2F4F8;
        font-size: 13px;
        font-weight: 700;
    }

    .top-brand-role {
        color: #7E8AA5;
        font-size: 11px;
    }

    .top-logo {
        width: 38px;
        height: 38px;

        border-radius: 12px;

        display: flex;
        justify-content: center;
        align-items: center;

        font-weight: 800;
        font-size: 14px;

        color: white;

        background:
            linear-gradient(
                135deg,
                #7C5CFF,
                #00C4B4
            );

        box-shadow:
            0 6px 18px rgba(124,92,255,0.30);
    }


    /* ---------------- SECTION HEADINGS ---------------- */

    .section-label {
        color: #8E9AB5;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .section-title {
        color: #F5F7FB;
        font-size: 25px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .section-description {
        color: #8995AE;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* ---------------- STEP CARDS ---------------- */

    .step-card {
        padding: 16px 18px;
        border-radius: 16px;

        background:
            rgba(255,255,255,0.035);

        border:
            1px solid rgba(255,255,255,0.07);

        min-height: 100px;
    }

    .step-number {
        color: #7C5CFF;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .step-name {
        color: #EEF1F7;
        font-size: 15px;
        font-weight: 700;
        margin-top: 5px;
    }

    .step-info {
        color: #7E8AA5;
        font-size: 12px;
        margin-top: 5px;
        line-height: 1.5;
    }


    /* ---------------- METRIC CARDS ---------------- */

    .metric-card {
        padding: 21px;
        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.065),
                rgba(255,255,255,0.025)
            );

        border:
            1px solid rgba(255,255,255,0.09);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.12);
    }

    .metric-label {
        color: #8995AE;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.4px;
    }

    .metric-value {
        color: #F7F8FC;
        font-size: 31px;
        font-weight: 800;
        margin-top: 7px;
    }

    .metric-caption {
        color: #6F7B94;
        font-size: 11px;
        margin-top: 5px;
    }


    /* ---------------- STATUS PILLS ---------------- */

    .status-shortlisted {
        display: inline-block;
        padding: 5px 10px;

        border-radius: 30px;

        font-size: 11px;
        font-weight: 700;

        color: #68E6AE;

        background:
            rgba(39, 199, 126, 0.10);

        border:
            1px solid rgba(39,199,126,0.20);
    }

    .status-review {
        display: inline-block;
        padding: 5px 10px;

        border-radius: 30px;

        font-size: 11px;
        font-weight: 700;

        color: #FFC96B;

        background:
            rgba(255,185,73,0.10);

        border:
            1px solid rgba(255,185,73,0.20);
    }

    .status-rejected {
        display: inline-block;
        padding: 5px 10px;

        border-radius: 30px;

        font-size: 11px;
        font-weight: 700;

        color: #FF8490;

        background:
            rgba(255,100,115,0.10);

        border:
            1px solid rgba(255,100,115,0.20);
    }


    /* ---------------- CANDIDATE CARD ---------------- */

    .candidate-card {
        padding: 22px;
        border-radius: 18px;

        background:
            rgba(255,255,255,0.035);

        border:
            1px solid rgba(255,255,255,0.08);

        margin-bottom: 12px;
    }

    .candidate-name {
        font-size: 18px;
        font-weight: 750;
        color: #F5F7FB;
    }

    .candidate-meta {
        color: #8490A8;
        font-size: 12px;
        margin-top: 5px;
    }

    .candidate-score {
        font-size: 32px;
        font-weight: 850;

        background:
            linear-gradient(
                90deg,
                #A995FF,
                #43E8D7
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    /* ---------------- FOOTER ---------------- */

    .custom-footer {
        margin-top: 60px;
        padding: 28px 20px;
        text-align: center;

        border-top:
            1px solid rgba(255,255,255,0.08);

        color: #7D899F;
        font-size: 13px;
    }

    .footer-name {
        color: #A995FF;
        font-weight: 700;
    }

    .footer-subtext {
        margin-top: 7px;
        font-size: 11px;
        color: #59657C;
    }


    /* ---------------- STREAMLIT COMPONENTS ---------------- */

    .stButton > button {
        border: none !important;

        border-radius: 12px !important;

        min-height: 50px !important;

        font-weight: 750 !important;

        background:
            linear-gradient(
                90deg,
                #7C5CFF,
                #00BFAE
            ) !important;

        color: white !important;

        box-shadow:
            0 10px 25px rgba(124,92,255,0.25) !important;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 15px 30px rgba(124,92,255,0.35) !important;
    }

    .stDownloadButton > button {
        border-radius: 12px !important;
        min-height: 46px !important;
        font-weight: 700 !important;
    }

    [data-testid="stFileUploader"] {
        padding: 15px;
        border-radius: 16px;

        background:
            rgba(255,255,255,0.025);

        border:
            1px dashed rgba(169,149,255,0.45);
    }

    [data-testid="stTextArea"] textarea {
        border-radius: 15px !important;

        background:
            rgba(255,255,255,0.035) !important;

        border:
            1px solid rgba(255,255,255,0.10) !important;

        color: #E8ECF4 !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border:
            1px solid rgba(255,255,255,0.08);
    }

</style>
""")


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS_DATABASE = [

    "python", "java", "c++", "c",
    "javascript", "typescript", "r",
    "sql", "html", "css",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "computer vision",
    "data science",
    "generative ai",
    "llm",
    "large language models",
    "transformers",

    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "keras",
    "xgboost",

    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "excel",
    "power bi",
    "tableau",

    "streamlit",
    "flask",
    "django",
    "fastapi",
    "react",
    "node.js",

    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",

    "aws",
    "azure",
    "google cloud",
    "gcp",
    "docker",
    "kubernetes",
    "git",
    "github",

    "apache spark",
    "spark",
    "hadoop",
    "airflow",
    "etl",

    "api",
    "rest api",
    "linux",
    "statistics",
    "data visualization"
]


# =========================================================
# CORE FUNCTIONS
# =========================================================

def clean_text(text):

    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for skill in SKILLS_DATABASE:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_name(text, filename=""):

    lines = [
        line.strip()
        for line in str(text).split("\n")
        if line.strip()
    ]

    skip_words = [
        "resume",
        "curriculum vitae",
        "email",
        "phone",
        "skills",
        "education",
        "experience",
        "summary",
        "profile",
        "linkedin",
        "professional"
    ]

    for line in lines[:8]:

        if not any(
            word in line.lower()
            for word in skip_words
        ):

            possible_name = re.sub(
                r"[^a-zA-Z\s]",
                "",
                line
            ).strip()

            words = possible_name.split()

            if 2 <= len(words) <= 4:
                return possible_name.title()

    if filename:

        name = filename.rsplit(".", 1)[0]

        name = re.sub(
            r"candidate[_-]?",
            "",
            name,
            flags=re.I
        )

        name = (
            name
            .replace("_", " ")
            .replace("-", " ")
            .strip()
        )

        if name:
            return name.title()

    return "Unknown"


def extract_experience(text):

    text = clean_text(text)

    patterns = [

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",

        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\+?\s*years?"
    ]

    years_found = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            try:
                years_found.append(
                    float(match)
                )

            except ValueError:
                pass

    return max(years_found) if years_found else 0.0


def extract_education(text):

    text = clean_text(text)

    education_levels = [

        (
            ["phd", "ph.d", "doctorate"],
            "PhD"
        ),

        (
            [
                "master",
                "master's",
                "m.tech",
                "mtech",
                "m.sc",
                "msc",
                "mba"
            ],
            "Master's"
        ),

        (
            [
                "bachelor",
                "bachelor's",
                "b.tech",
                "btech",
                "b.e",
                "b.sc",
                "bsc",
                "bca"
            ],
            "Bachelor's"
        ),

        (
            ["diploma"],
            "Diploma"
        )
    ]

    for keywords, level in education_levels:

        if any(
            keyword in text
            for keyword in keywords
        ):
            return level

    return "Not Found"


def parse_resume(text, filename=""):

    return {

        "name": extract_name(
            text,
            filename
        ),

        "skills": extract_skills(
            text
        ),

        "experience": extract_experience(
            text
        ),

        "education": extract_education(
            text
        ),

        "raw_text": str(text)
    }


# =========================================================
# MATCHING FUNCTIONS
# =========================================================

def calculate_skill_match(
    resume_skills,
    job_skills
):

    if not job_skills:
        return 0.0, [], []

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    job_set = {
        skill.lower()
        for skill in job_skills
    }

    matched_skills = (
        resume_set.intersection(job_set)
    )

    missing_skills = (
        job_set.difference(resume_set)
    )

    score = (
        len(matched_skills)
        / len(job_set)
    ) * 100

    return (
        round(score, 2),
        sorted(matched_skills),
        sorted(missing_skills)
    )


def extract_required_experience(
    job_description
):

    text = clean_text(job_description)

    patterns = [

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",

        r"minimum\s+(\d+(?:\.\d+)?)\+?\s*years?",

        r"at least\s+(\d+(?:\.\d+)?)\+?\s*years?"
    ]

    years_found = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            try:
                years_found.append(
                    float(match)
                )

            except ValueError:
                pass

    return (
        max(years_found)
        if years_found
        else 0.0
    )


def calculate_experience_match(
    candidate_experience,
    required_experience
):

    if required_experience == 0:
        return 100.0

    score = min(
        candidate_experience
        / required_experience,
        1
    ) * 100

    return round(score, 2)


def calculate_education_match(
    candidate_education,
    job_description
):

    text = clean_text(job_description)

    education_rank = {

        "Not Found": 0,
        "Diploma": 1,
        "Bachelor's": 2,
        "Master's": 3,
        "PhD": 4
    }

    required_rank = 0

    if any(
        keyword in text
        for keyword in [
            "phd",
            "ph.d",
            "doctorate"
        ]
    ):

        required_rank = 4

    elif any(
        keyword in text
        for keyword in [
            "master",
            "master's",
            "m.tech",
            "mtech",
            "m.sc",
            "msc",
            "mba"
        ]
    ):

        required_rank = 3

    elif any(
        keyword in text
        for keyword in [
            "bachelor",
            "bachelor's",
            "b.tech",
            "btech",
            "b.e",
            "b.sc",
            "bsc",
            "bca"
        ]
    ):

        required_rank = 2

    if required_rank == 0:
        return 100.0

    candidate_rank = education_rank.get(
        candidate_education,
        0
    )

    if candidate_rank >= required_rank:
        return 100.0

    return 50.0


def calculate_tfidf_similarity(
    resume_text,
    job_description
):

    if (
        not str(resume_text).strip()
        or not str(job_description).strip()
    ):
        return 0.0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(
            [
                str(resume_text),
                str(job_description)
            ]
        )

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return round(
            similarity * 100,
            2
        )

    except ValueError:
        return 0.0


def calculate_match_score(
    resume_data,
    job_description
):

    job_skills = extract_skills(
        job_description
    )

    required_experience = (
        extract_required_experience(
            job_description
        )
    )

    (
        skill_score,
        matched_skills,
        missing_skills
    ) = calculate_skill_match(
        resume_data["skills"],
        job_skills
    )

    experience_score = (
        calculate_experience_match(
            resume_data["experience"],
            required_experience
        )
    )

    education_score = (
        calculate_education_match(
            resume_data["education"],
            job_description
        )
    )

    similarity_score = (
        calculate_tfidf_similarity(
            resume_data["raw_text"],
            job_description
        )
    )

    final_score = (

        skill_score * 0.50

        + experience_score * 0.25

        + education_score * 0.15

        + similarity_score * 0.10
    )

    return {

        "match_score": round(
            final_score,
            2
        ),

        "skill_score": skill_score,

        "experience_score": (
            experience_score
        ),

        "education_score": (
            education_score
        ),

        "similarity_score": (
            similarity_score
        ),

        "matched_skills": (
            matched_skills
        ),

        "missing_skills": (
            missing_skills
        )
    }


# =========================================================
# FILE PROCESSING
# =========================================================

def find_column(
    columns,
    possible_names
):

    normalized_columns = {

        str(col).lower().strip(): col

        for col in columns
    }

    for name in possible_names:

        if name in normalized_columns:
            return normalized_columns[name]

    return None


def process_csv_file(uploaded_file):

    try:

        file_content = uploaded_file.getvalue()

        df = pd.read_csv(
            io.BytesIO(file_content)
        )

        df = df.dropna(how="all")

        candidates = []

        name_col = find_column(
            df.columns,
            [
                "name",
                "candidate name",
                "candidate"
            ]
        )

        skills_col = find_column(
            df.columns,
            [
                "skills",
                "technical skills",
                "skill"
            ]
        )

        experience_col = find_column(
            df.columns,
            [
                "experience",
                "years of experience",
                "experience years",
                "years"
            ]
        )

        education_col = find_column(
            df.columns,
            [
                "education",
                "qualification",
                "degree"
            ]
        )

        for index, row in df.iterrows():

            row_text = " ".join(

                str(value)

                for value in row.values

                if pd.notna(value)
            )

            candidate = parse_resume(
                row_text,
                f"{uploaded_file.name}_row_{index + 1}"
            )

            if (
                name_col
                and pd.notna(row[name_col])
            ):

                candidate["name"] = str(
                    row[name_col]
                ).strip()

            if (
                skills_col
                and pd.notna(row[skills_col])
            ):

                candidate["skills"] = (
                    extract_skills(
                        str(row[skills_col])
                    )
                )

            if (
                experience_col
                and pd.notna(row[experience_col])
            ):

                exp_match = re.search(
                    r"(\d+(?:\.\d+)?)",
                    str(row[experience_col])
                )

                if exp_match:

                    candidate["experience"] = (
                        float(
                            exp_match.group(1)
                        )
                    )

            if (
                education_col
                and pd.notna(row[education_col])
            ):

                candidate["education"] = (
                    extract_education(
                        str(row[education_col])
                    )
                )

            candidates.append(
                candidate
            )

        return candidates

    except Exception as e:

        st.error(
            f"Error processing CSV: {e}"
        )

        return []


def process_txt_file(uploaded_file):

    try:

        text = uploaded_file.getvalue().decode(
            "utf-8",
            errors="ignore"
        )

        candidate = parse_resume(
            text,
            uploaded_file.name
        )

        return [candidate]

    except Exception as e:

        st.error(
            f"Error processing "
            f"{uploaded_file.name}: {e}"
        )

        return []


def process_uploaded_files(
    uploaded_files
):

    all_candidates = []

    for uploaded_file in uploaded_files:

        filename = uploaded_file.name.lower()

        if filename.endswith(".txt"):

            all_candidates.extend(
                process_txt_file(
                    uploaded_file
                )
            )

        elif filename.endswith(".csv"):

            all_candidates.extend(
                process_csv_file(
                    uploaded_file
                )
            )

    return all_candidates


# =========================================================
# SIDEBAR BRANDING
# =========================================================

with st.sidebar:

    render_html("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">SV</div>

        <div class="sidebar-name">
            Shreya Verma
        </div>

        <div class="sidebar-role">
            AI & Machine Learning<br>
            Developer Portfolio
        </div>
    </div>
    """)

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-section-title">'
        'SCREENING CONTROLS'
        '</div>',
        unsafe_allow_html=True
    )

    shortlist_threshold = st.slider(
        "Shortlist threshold",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        help="Candidates scoring above this value will be shortlisted."
    )

    st.markdown(
        '<div class="sidebar-section-title">'
        'SCORING MODEL'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption("SKILL COMPATIBILITY")
    st.progress(50)
    st.caption("50% of final score")

    st.caption("EXPERIENCE")
    st.progress(25)
    st.caption("25% of final score")

    st.caption("EDUCATION")
    st.progress(15)
    st.caption("15% of final score")

    st.caption("NLP TEXT SIMILARITY")
    st.progress(10)
    st.caption("10% of final score")

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-section-title">'
        'SUPPORTED INPUTS'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "📄 **TXT files**\n\n"
        "One candidate per file.\n\n"
        "📊 **CSV files**\n\n"
        "One candidate per row."
    )

    render_html("""
    <div style="
        margin-top:35px;
        padding:15px;
        border-radius:14px;
        background:rgba(124,92,255,0.08);
        border:1px solid rgba(124,92,255,0.15);
        text-align:center;
    ">
        <div style="
            color:#A995FF;
            font-size:11px;
            font-weight:700;
            letter-spacing:1px;
        ">
            BUILT BY
        </div>
        <div style="
            color:#F3F5F9;
            font-size:14px;
            font-weight:700;
            margin-top:5px;
        ">
            Shreya Verma
        </div>
    </div>
    """)


# =========================================================
# TOP RIGHT BRAND
# =========================================================

render_html("""
<div class="top-brand">

    <div class="top-brand-text">

        <div class="top-brand-name">
            Shreya Verma
        </div>

        <div class="top-brand-role">
            AI • ML • Data
        </div>

    </div>

    <div class="top-logo">
        SV
    </div>

</div>
""")


# =========================================================
# HERO
# =========================================================

render_html("""
<div class="hero-container">

    <div class="hero-title">
        Resume<span>AI</span>
    </div>

    <div class="hero-subtitle">
        An intelligent candidate screening system that
        automatically analyzes resumes, evaluates skills and
        experience, measures job compatibility, and ranks
        candidates based on a weighted AI-driven scoring model.
    </div>

    <div class="hero-badges">
        <span class="hero-badge">🤖 AI-Powered Screening</span>
        <span class="hero-badge">📊 Smart Candidate Ranking</span>
        <span class="hero-badge">🎯 Skill Gap Analysis</span>
        <span class="hero-badge">⚡ Automated Shortlisting</span>
    </div>

</div>
""")


# =========================================================
# WORKFLOW
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    render_html("""
    <div class="step-card">

        <div class="step-number">
            STEP 01
        </div>

        <div class="step-name">
            Define the Role
        </div>

        <div class="step-info">
            Add a job description and let the system identify
            required skills, experience and education.
        </div>

    </div>
    """)


with col2:

    render_html("""
    <div class="step-card">

        <div class="step-number">
            STEP 02
        </div>

        <div class="step-name">
            Upload Resumes
        </div>

        <div class="step-info">
            Upload multiple TXT files or CSV datasets
            containing candidate information.
        </div>

    </div>
    """)


with col3:

    render_html("""
    <div class="step-card">

        <div class="step-number">
            STEP 03
        </div>

        <div class="step-name">
            Analyze & Rank
        </div>

        <div class="step-info">
            Generate compatibility scores, detect missing
            skills and automatically shortlist candidates.
        </div>

    </div>
    """)


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.markdown(
    '<div class="section-label">01 / ROLE ANALYSIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Define the Job Description</div>',
    unsafe_allow_html=True
)

render_html(
    '''
    <div class="section-description">
        Paste the complete job description. ResumeAI will automatically
        extract relevant skills, experience and education requirements.
    </div>
    '''
)

job_description = st.text_area(
    "Job Description",
    height=240,
    placeholder="""
Example:

Machine Learning Engineer

We are looking for a Machine Learning Engineer with at least
2 years of experience.

Required Skills:
Python, SQL, Machine Learning, Deep Learning,
Scikit-learn, TensorFlow, Pandas, AWS and Docker.

Education:
Bachelor's or Master's degree in Computer Science,
Artificial Intelligence, Data Science or a related field.
""",
    label_visibility="collapsed"
)


# =========================================================
# JOB REQUIREMENT PREVIEW
# =========================================================

if job_description.strip():

    detected_skills = extract_skills(
        job_description
    )

    required_exp = (
        extract_required_experience(
            job_description
        )
    )

    education_preview = (
        extract_education(
            job_description
        )
    )

    st.markdown("<br>", unsafe_allow_html=True)

    preview_cols = st.columns(3)

    with preview_cols[0]:

        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">
                DETECTED SKILLS
            </div>

            <div class="metric-value">
                {len(detected_skills)}
            </div>

            <div class="metric-caption">
                Skills identified from job description
            </div>
        </div>
        """)


    with preview_cols[1]:

        exp_text = (
            f"{required_exp:g}"
            if required_exp > 0
            else "N/A"
        )

        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">
                REQUIRED EXPERIENCE
            </div>

            <div class="metric-value">
                {exp_text}
            </div>

            <div class="metric-caption">
                Minimum years detected
            </div>
        </div>
        """)


    with preview_cols[2]:

        render_html(f"""
        <div class="metric-card">
            <div class="metric-label">
                EDUCATION LEVEL
            </div>

            <div class="metric-value" style="font-size:24px">
                {education_preview}
            </div>

            <div class="metric-caption">
                Highest qualification detected
            </div>
        </div>
        """)


    if detected_skills:

        with st.expander(
            "🔍 View skills detected from the job description"
        ):

            st.write(
                ", ".join(
                    skill.title()
                    for skill in detected_skills
                )
            )


st.markdown("<br><hr><br>", unsafe_allow_html=True)


# =========================================================
# FILE UPLOAD
# =========================================================

st.markdown(
    '<div class="section-label">02 / CANDIDATE INPUT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Upload Candidate Resumes</div>',
    unsafe_allow_html=True
)

render_html(
    '''
    <div class="section-description">
        Upload multiple TXT resumes or a CSV file containing
        multiple candidates.
    </div>
    '''
)

uploaded_files = st.file_uploader(
    "Upload candidate files",
    type=["txt", "csv"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


if uploaded_files:

    st.success(
        f"✓ {len(uploaded_files)} file(s) ready for analysis"
    )

    with st.expander(
        "📁 View uploaded files",
        expanded=False
    ):

        for file in uploaded_files:

            extension = (
                file.name.split(".")[-1].upper()
            )

            size_kb = (
                len(file.getvalue()) / 1024
            )

            st.write(
                f"**{file.name}** "
                f"— {extension} "
                f"— {size_kb:.1f} KB"
            )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze_button = st.button(
    "🚀 Analyze Candidates & Generate Rankings",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if not job_description.strip():

        st.warning(
            "Please add a job description before running the analysis."
        )

    elif not uploaded_files:

        st.warning(
            "Please upload at least one TXT or CSV file."
        )

    else:

        with st.spinner(
            "ResumeAI is analyzing candidate profiles..."
        ):

            candidates = (
                process_uploaded_files(
                    uploaded_files
                )
            )

            results = []

            progress_bar = st.progress(0)

            for index, candidate in enumerate(
                candidates
            ):

                match_data = (
                    calculate_match_score(
                        candidate,
                        job_description
                    )
                )

                results.append({

                    "Name":
                        candidate["name"],

                    "Experience (Years)":
                        candidate["experience"],

                    "Education":
                        candidate["education"],

                    "Skills":
                        ", ".join(
                            candidate["skills"]
                        ),

                    "Matched Skills":
                        ", ".join(
                            match_data["matched_skills"]
                        ),

                    "Missing Skills":
                        ", ".join(
                            match_data["missing_skills"]
                        ),

                    "Skill Match (%)":
                        match_data["skill_score"],

                    "Experience Match (%)":
                        match_data["experience_score"],

                    "Education Match (%)":
                        match_data["education_score"],

                    "NLP Similarity (%)":
                        match_data["similarity_score"],

                    "Resume Match Score (%)":
                        match_data["match_score"]
                })

                if candidates:

                    progress = int(
                        ((index + 1) / len(candidates))
                        * 100
                    )

                    progress_bar.progress(
                        progress
                    )

            progress_bar.empty()


        # =================================================
        # RESULTS
        # =================================================

        if results:

            results_df = pd.DataFrame(
                results
            )

            results_df = results_df.sort_values(
                by="Resume Match Score (%)",
                ascending=False
            ).reset_index(
                drop=True
            )

            results_df.index += 1

            results_df.insert(
                0,
                "Rank",
                results_df.index
            )


            # =============================================
            # RESULTS HEADER
            # =============================================

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                '<div class="section-label">03 / SCREENING RESULTS</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-title">Candidate Intelligence Dashboard</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '''
                <div class="section-description">
                    Candidates ranked by overall compatibility with
                    the selected job description.
                </div>
                ''',
                unsafe_allow_html=True
            )


            # =============================================
            # METRICS
            # =============================================

            total_candidates = len(
                results_df
            )

            shortlisted_df = results_df[
                results_df[
                    "Resume Match Score (%)"
                ] >= shortlist_threshold
            ].copy()

            shortlisted_count = len(
                shortlisted_df
            )

            top_candidate = (
                results_df.iloc[0]["Name"]
            )

            top_score = (
                results_df.iloc[0][
                    "Resume Match Score (%)"
                ]
            )

            average_score = round(
                results_df[
                    "Resume Match Score (%)"
                ].mean(),
                1
            )

            m1, m2, m3, m4 = st.columns(4)

            with m1:

                render_html(f"""
                <div class="metric-card">
                    <div class="metric-label">
                        TOTAL CANDIDATES
                    </div>

                    <div class="metric-value">
                        {total_candidates}
                    </div>

                    <div class="metric-caption">
                        Profiles successfully analyzed
                    </div>
                </div>
                """)


            with m2:

                render_html(f"""
                <div class="metric-card">
                    <div class="metric-label">
                        SHORTLISTED
                    </div>

                    <div class="metric-value">
                        {shortlisted_count}
                    </div>

                    <div class="metric-caption">
                        Score ≥ {shortlist_threshold}%
                    </div>
                </div>
                """)


            with m3:

                render_html(f"""
                <div class="metric-card">
                    <div class="metric-label">
                        TOP MATCH
                    </div>

                    <div class="metric-value">
                        {top_score}%
                    </div>

                    <div class="metric-caption">
                        {top_candidate}
                    </div>
                </div>
                """)


            with m4:

                render_html(f"""
                <div class="metric-card">
                    <div class="metric-label">
                        AVERAGE SCORE
                    </div>

                    <div class="metric-value">
                        {average_score}%
                    </div>

                    <div class="metric-caption">
                        Overall candidate compatibility
                    </div>
                </div>
                """)


            # =============================================
            # TABS
            # =============================================

            st.markdown("<br>", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs([

                "🏆 Rankings",

                "🔍 Candidate Analysis",

                "📥 Shortlist & Export"
            ])


            # =============================================
            # TAB 1 - RANKINGS
            # =============================================

            with tab1:

                display_df = results_df[
                    [
                        "Rank",
                        "Name",
                        "Experience (Years)",
                        "Education",
                        "Skill Match (%)",
                        "Experience Match (%)",
                        "NLP Similarity (%)",
                        "Resume Match Score (%)"
                    ]
                ]

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    height=500
                )

                st.caption(
                    "Ranking is based on the weighted combination "
                    "of skills (50%), experience (25%), education "
                    "(15%) and TF-IDF similarity (10%)."
                )


            # =============================================
            # TAB 2 - CANDIDATE ANALYSIS
            # =============================================

            with tab2:

                for _, candidate in (
                    results_df.iterrows()
                ):

                    score = candidate[
                        "Resume Match Score (%)"
                    ]

                    if score >= shortlist_threshold:

                        status_html = (
                            '<span class="status-shortlisted">'
                            '● SHORTLISTED'
                            '</span>'
                        )

                    elif score >= (
                        shortlist_threshold - 15
                    ):

                        status_html = (
                            '<span class="status-review">'
                            '● REVIEW'
                            '</span>'
                        )

                    else:

                        status_html = (
                            '<span class="status-rejected">'
                            '● NOT SELECTED'
                            '</span>'
                        )


                    with st.expander(

                        f"#{candidate['Rank']}  |  "
                        f"{candidate['Name']}  |  "
                        f"{score}% Match",

                        expanded=False
                    ):

                        left, right = st.columns(
                            [1.1, 1]
                        )

                        with left:

                            render_html(f"""
                            <div class="candidate-card">

                                <div class="candidate-name">
                                    {candidate['Name']}
                                </div>

                                <div class="candidate-meta">
                                    {candidate['Experience (Years)']} years experience
                                    &nbsp; • &nbsp;
                                    {candidate['Education']}
                                </div>

                                <div style="margin-top:14px">
                                    {status_html}
                                </div>

                            </div>
                            """)

                            st.markdown(
                                "#### 🧠 Skills Profile"
                            )

                            st.success(
                                candidate[
                                    "Matched Skills"
                                ]
                                if candidate[
                                    "Matched Skills"
                                ]
                                else "No matching skills detected."
                            )

                            st.markdown(
                                "#### ⚠️ Skill Gaps"
                            )

                            if candidate[
                                "Missing Skills"
                            ]:

                                st.error(
                                    candidate[
                                        "Missing Skills"
                                    ]
                                )

                            else:

                                st.success(
                                    "Perfect skill coverage! No required skills missing."
                                )


                        with right:

                            st.markdown(
                                f"""
                                <div class="candidate-card">

                                    <div class="metric-label">
                                        OVERALL MATCH SCORE
                                    </div>

                                    <div class="candidate-score">
                                        {score}%
                                    </div>

                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            st.metric(
                                "Skill Compatibility",
                                f"{candidate['Skill Match (%)']}%"
                            )

                            st.metric(
                                "Experience Compatibility",
                                f"{candidate['Experience Match (%)']}%"
                            )

                            st.metric(
                                "Education Compatibility",
                                f"{candidate['Education Match (%)']}%"
                            )

                            st.metric(
                                "NLP Text Similarity",
                                f"{candidate['NLP Similarity (%)']}%"
                            )


            # =============================================
            # TAB 3 - SHORTLIST
            # =============================================

            with tab3:

                st.markdown(
                    f"""
                    ### Candidates scoring {shortlist_threshold}% or above
                    """
                )

                if not shortlisted_df.empty:

                    st.success(
                        f"{len(shortlisted_df)} candidate(s) "
                        f"successfully shortlisted."
                    )

                    shortlist_display = shortlisted_df[
                        [
                            "Rank",
                            "Name",
                            "Experience (Years)",
                            "Education",
                            "Matched Skills",
                            "Missing Skills",
                            "Resume Match Score (%)"
                        ]
                    ]

                    st.dataframe(
                        shortlist_display,
                        use_container_width=True,
                        hide_index=True
                    )

                    csv_data = (
                        shortlisted_df
                        .to_csv(index=False)
                        .encode("utf-8")
                    )

                    st.download_button(
                        label=(
                            "⬇️ Download Shortlisted Candidates"
                        ),
                        data=csv_data,
                        file_name=(
                            "shortlisted_candidates.csv"
                        ),
                        mime="text/csv",
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No candidates currently meet the "
                        "shortlisting threshold. Try lowering "
                        "the threshold from the sidebar."
                    )

        else:

            st.error(
                "No valid candidate information could be extracted."
            )


# =========================================================
# FOOTER
# =========================================================

render_html("""
<div class="custom-footer">

    <div>
        Resume<span style="color:#A995FF;font-weight:800">AI</span>
        &nbsp; • &nbsp;
        Designed & Built by
        <span class="footer-name">Shreya Verma</span>
    </div>

    <div class="footer-subtext">
        Intelligent Resume Screening • Machine Learning • NLP
    </div>

</div>
""")