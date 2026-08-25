# 🤖 Day 26 -- AI Resume Screening Tool

## 📌 Project Overview

This project was completed as part of my **RFT Python Internship at GOW
AI Academy**.

The **AI Resume Screening Tool** is designed to automate the initial
resume screening process. It reads candidate resumes from **TXT files or
CSV files**, extracts key candidate information, compares candidate
profiles with a job description, calculates a weighted Resume Match
Score, ranks candidates, highlights missing skills, and exports
shortlisted candidates to a CSV file.

The project also includes an interactive and branded **Streamlit
interface** for uploading resumes and analyzing candidates.

------------------------------------------------------------------------

## 🎯 Objectives

The main objectives of this project are:

-   Read multiple candidate resume files in TXT and CSV formats
-   Extract candidate details such as:
    -   Name
    -   Skills
    -   Experience
    -   Education
-   Match candidate resumes against a job description
-   Calculate a Resume Match Score
-   Rank candidates based on their scores
-   Highlight missing or unmatched skills
-   Shortlist candidates using a configurable threshold
-   Export shortlisted candidates to CSV
-   Build an interactive Streamlit interface for resume upload and
    analysis

------------------------------------------------------------------------

## 📂 Project Files

``` text
Day 26/
│
├── AI_Resume_Screening_Tool.ipynb
├── ai_resume_screening_tool.py
├── app.py
├── requirements.txt
│
├── candidate_1.txt
├── candidate_2.txt
├── candidate_3.txt
├── candidate_4.txt
├── candidate_5.txt
│
├── candidates.csv
├── sample_job_description.txt
├── shortlisted_candidates.csv
│
└── README.md
```

------------------------------------------------------------------------

## 🛠️ Technologies Used

### Programming Language

-   Python

### Libraries

-   Pandas
-   Scikit-learn
-   Streamlit

### Development Tools

-   Jupyter Notebook
-   VS Code
-   Git
-   GitHub

------------------------------------------------------------------------

## 📄 Supported Resume Inputs

### 📄 TXT Files

Each TXT file can contain the details of one candidate, including
information such as:

-   Name
-   Skills
-   Experience
-   Education

Multiple TXT resumes can be uploaded and screened together.

### 📊 CSV Files

The tool also supports CSV files containing multiple candidates.

Each row represents a candidate, allowing the system to process and rank
multiple candidate profiles from a single file.

------------------------------------------------------------------------

## 🧠 Resume Screening Process

The screening workflow consists of the following steps:

### 1. Candidate Information Extraction

The application reads the uploaded resume data and extracts relevant
candidate information such as:

-   Candidate name
-   Technical skills
-   Years of experience
-   Education details

------------------------------------------------------------------------

### 2. Job Description Analysis

A job description is provided to define the requirements for the role.

The application uses the job description as the basis for evaluating
candidate compatibility.

------------------------------------------------------------------------

### 3. Skill Matching

Candidate skills are compared with skills and requirements identified
from the job description.

This helps determine:

-   Matching skills
-   Missing skills
-   Overall skill compatibility

------------------------------------------------------------------------

### 4. Experience Matching

Candidate experience is evaluated against the experience requirements of
the job description.

------------------------------------------------------------------------

### 5. Education Matching

The candidate's education details are compared with the educational
requirements of the role.

------------------------------------------------------------------------

### 6. NLP Text Similarity

The application also compares resume content and job-description content
using text similarity techniques to measure overall relevance.

------------------------------------------------------------------------

### 7. Resume Match Score

A weighted score is calculated to evaluate the overall compatibility of
each candidate.

The Streamlit application displays the contribution of:

-   Skill Compatibility --- 50%
-   Experience --- 25%
-   Education --- 15%
-   NLP Text Similarity --- 10%

Candidates are then ranked according to their final Resume Match Score.

------------------------------------------------------------------------

## 📊 Candidate Analysis

For each candidate, the application can display:

-   Overall Match Score
-   Skill Compatibility
-   Experience Compatibility
-   Education Compatibility
-   NLP Text Similarity
-   Matched Skills
-   Missing Skills / Skill Gaps
-   Shortlisting Status

This makes the screening process more transparent and easier to review.

------------------------------------------------------------------------

## ⭐ Bonus Challenge -- Missing Skills Analysis

The project includes skill-gap analysis.

The application identifies skills required by the job description that
are missing from a candidate's profile.

This helps recruiters quickly understand where a candidate may not meet
the role requirements.

------------------------------------------------------------------------

## 🖥️ Bonus Challenge -- Interactive Streamlit Interface

An interactive Streamlit application was created for resume screening
and candidate analysis.

### Dashboard Features

-   Enter or paste a job description
-   Upload multiple TXT resumes
-   Upload CSV files containing multiple candidates
-   Analyze candidate resumes
-   Calculate weighted compatibility scores
-   Rank candidates automatically
-   View individual candidate analysis
-   Identify matched skills
-   Highlight skill gaps
-   Adjust the shortlist threshold
-   Export shortlisted candidates to CSV

The interface also includes custom branding and a modern dashboard-style
layout.

### Run the Dashboard Locally

Open the terminal inside the project folder and run:

``` bash
streamlit run app.py
```

Streamlit will generate a local URL, usually:

``` text
http://localhost:8501
```

Open this URL in your browser to use the AI Resume Screening Tool.

------------------------------------------------------------------------

## 📤 Shortlisted Candidates Export

Candidates meeting the selected shortlist threshold are exported as:

``` text
shortlisted_candidates.csv
```

This file contains the shortlisted candidates and their relevant
screening results.

------------------------------------------------------------------------

## 📚 Key Learnings

Through this project, I practiced and improved my understanding of:

-   Working with TXT files in Python
-   Working with CSV files using Pandas
-   Extracting structured information from text
-   Text preprocessing
-   Skill matching
-   Missing skill analysis
-   Candidate ranking
-   Weighted scoring systems
-   Resume-to-job-description matching
-   NLP-based text similarity
-   Using Scikit-learn
-   Exporting results to CSV
-   Building interactive applications using Streamlit
-   Designing a user-friendly dashboard interface

------------------------------------------------------------------------

## 🚀 How to Run the Project

### Step 1: Clone the Repository

``` bash
git clone https://github.com/Shreya934-bot/rftinternship.git
```

### Step 2: Navigate to the Project Folder

``` bash
cd RFTinternship/Day\ 26
```

### Step 3: Install Required Libraries

``` bash
pip install -r requirements.txt
```

### Step 4: Run the Python Screening Script

``` bash
python ai_resume_screening_tool.py
```

### Step 5: Run the Streamlit Application

``` bash
streamlit run app.py
```

------------------------------------------------------------------------

## 📌 Project Outcome

This project successfully demonstrates an end-to-end **AI Resume
Screening Tool**.

The system automates important parts of the initial resume evaluation
process through:

-   Multi-format resume input
-   Candidate information extraction
-   Job description matching
-   Skill compatibility analysis
-   Experience evaluation
-   Education evaluation
-   NLP text similarity
-   Weighted Resume Match Score calculation
-   Candidate ranking
-   Missing skill identification
-   Automated shortlisting
-   CSV export
-   Interactive Streamlit dashboard development

------------------------------------------------------------------------

## 👩‍💻 About Me

I am **Shreya Verma**, a Computer Science Engineering student
specializing in **Artificial Intelligence & Machine Learning**.

I am passionate about building practical projects in:

-   Machine Learning
-   Data Science
-   Data Analytics
-   Artificial Intelligence
-   Python Development

This project is part of my continuous hands-on learning journey during
the **RFT Python Internship at GOW AI Academy**.

------------------------------------------------------------------------

## 🔗 Connect With Me

-   **GitHub:** https://github.com/Shreya934-bot
-   **LinkedIn:** https://www.linkedin.com/in/shreya-verma-2b73b6290

------------------------------------------------------------------------

⭐ **Day 26 of the RFT Python Internship -- AI Resume Screening Tool**
