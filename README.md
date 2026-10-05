# 📄 AI Resume Analyzer and Job Recommendation System

An NLP-based web application that analyzes a student's resume and recommends suitable job roles based on their technical skills.

The system extracts skills from PDF/DOCX resumes, compares them with job-role requirements, calculates match scores, identifies skill gaps, and generates a learning roadmap.

---

## 🎯 Project Objective

The main objective of this project is to help students understand how well their resume matches different software/technology job roles.

The system provides:

- Resume skill extraction
- Job-role matching
- Match percentage
- Recommended job roles
- Missing/required skills
- Learning roadmap
- Downloadable PDF analysis report

---

## ✨ Features

### 1. Resume Upload

- Supports PDF resumes
- Supports DOCX resumes

### 2. Resume Text Extraction

The application extracts text from the uploaded resume and processes it for analysis.

### 3. Skill Extraction

The system identifies technical skills such as:

- Python
- C
- SQL
- HTML
- CSS
- JavaScript
- Git
- GitHub
- DBMS
- Data Structures
- Machine Learning
- Deep Learning
- CNN
- APIs
- And other skills included in the skill dictionary

### 4. Job Role Matching

The resume is compared with predefined job roles and their required skills.

The application calculates a match percentage for each role.

### 5. Recommended Job Roles

The system displays the top recommended roles based on the resume match score.

### 6. Skill Gap Analysis

For a selected job role, the system displays:

- Skills already present in the resume
- Skills that need improvement

### 7. Learning Roadmap

For missing skills, the system generates a basic learning roadmap with weekly learning suggestions.

### 8. PDF Report

Users can download a PDF report containing the resume analysis results.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Regular Expressions
- ReportLab
- PyPDF
- python-docx
- HTML/CSS
- Git/GitHub

---

## 🧠 Matching Method

The current system uses **keyword-based skill matching**.

The extracted resume skills are compared with the required skills for each job role.

The match score is calculated based on the proportion of required skills found in the resume.

---

## 📁 Project Structure

```text
AI_Resume_Analyzer/
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── roadmap_generator.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
│
├── sample_resumes/
│
├── reports/
│
└── tests/
    └── test_cases.csv

🚀 How to Run
Install dependencies
pip install -r requirements.txt

Run the application
python -m streamlit run app.py

📊 Workflow
Upload Resume
      ↓
Extract Resume Text
      ↓
Clean and Normalize Text
      ↓
Extract Technical Skills
      ↓
Compare with Job Roles
      ↓
Calculate Match Scores
      ↓
Recommend Job Roles
      ↓
Identify Skill Gaps
      ↓
Generate Learning Roadmap
      ↓
Download PDF Report

📌 Job Roles
The system currently analyzes roles such as:
- Software Developer
- Python Developer
- Web Developer
- Data Scientist
- Data Analyst
- AI Engineer
- ML Engineer
- NLP Engineer
- Computer Vision Engineer
- Backend Developer

⚠️ Limitations
- The current skill extraction system is primarily keyword based.
- Missing keywords do not always mean that a candidate lacks the actual skill.
- Match scores are estimates based on the available job-role requirements.
- The system should not be used as an automatic hiring or rejection system.

🤖 Responsible AI
This project is intended for career guidance and educational purposes.
It focuses on job-related skills and should not evaluate candidates using protected or personal attributes such as:
- Gender
- Age
- Religion
- Nationality
- Marital status
- Photograph
- Disability

👩‍💻 Project
AI Resume Analyzer and Job Recommendation System
Developed as an academic project using Python and Streamlit.
    