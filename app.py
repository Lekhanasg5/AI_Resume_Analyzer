import streamlit as st
import pandas as pd

from resume_parser import extract_text_from_pdf, extract_text_from_docx
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, calculate_match_scores
from roadmap_generator import generate_roadmap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📄 AI Resume Analyzer and Job Recommendation System")

st.write(
    "Upload your resume to analyze your skills, "
    "match suitable job roles, identify skill gaps, "
    "and generate a learning roadmap."
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

try:
    skill_dictionary = load_skill_dictionary()
    job_roles = load_job_roles()

except Exception as e:
    st.error(f"Error loading project data: {e}")
    st.stop()


# ---------------------------------------------------------
# RESUME UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"],
    help="Upload a PDF or DOCX resume."
)


# ---------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------

if uploaded_file is not None:

    file_name = uploaded_file.name
    file_extension = file_name.split(".")[-1].lower()

    st.success(f"Uploaded: {file_name}")

    # -----------------------------------------------------
    # EXTRACT TEXT
    # -----------------------------------------------------

    try:

        with st.spinner("Extracting resume text..."):

            if file_extension == "pdf":
                raw_text = extract_text_from_pdf(uploaded_file)

            elif file_extension == "docx":
                raw_text = extract_text_from_docx(uploaded_file)

            else:
                st.error("Unsupported file format.")
                st.stop()

    except Exception as e:
        st.error(f"Error reading resume: {e}")
        st.stop()


    # -----------------------------------------------------
    # CHECK TEXT
    # -----------------------------------------------------

    if not raw_text or not str(raw_text).strip():

        st.error(
            "Could not extract text from the resume. "
            "Please upload a clear PDF or DOCX file."
        )

        st.stop()


    # -----------------------------------------------------
    # CLEAN TEXT
    # -----------------------------------------------------

    try:
        cleaned_text = clean_text(raw_text)

    except Exception as e:
        st.error(f"Error cleaning resume text: {e}")
        st.stop()


    # -----------------------------------------------------
    # EXTRACT SKILLS
    # -----------------------------------------------------

    try:

        extracted_skills = extract_skills(
            cleaned_text,
            skill_dictionary
        )

    except Exception as e:
        st.error(f"Error extracting skills: {e}")
        st.stop()


    # -----------------------------------------------------
    # CONVERT EXTRACTED SKILLS TO A SIMPLE LIST
    # -----------------------------------------------------

    resume_skill_names = []


    # Case 1: dictionary returned
    if isinstance(extracted_skills, dict):

        for category, skills in extracted_skills.items():

            if skills is None:
                continue

            if isinstance(skills, (list, tuple, set)):
                resume_skill_names.extend(
                    [str(skill) for skill in skills]
                )

            else:
                resume_skill_names.append(str(skills))


    # Case 2: pandas DataFrame returned
    elif isinstance(extracted_skills, pd.DataFrame):

        if "Skill" in extracted_skills.columns:

            resume_skill_names = (
                extracted_skills["Skill"]
                .dropna()
                .astype(str)
                .tolist()
            )


    # Case 3: pandas Series returned
    elif isinstance(extracted_skills, pd.Series):

        resume_skill_names = (
            extracted_skills
            .dropna()
            .astype(str)
            .tolist()
        )


    # Case 4: list / tuple / set returned
    elif isinstance(extracted_skills, (list, tuple, set)):

        resume_skill_names = [
            str(skill)
            for skill in extracted_skills
        ]


    # Remove duplicates
    resume_skill_names = list(
        dict.fromkeys(resume_skill_names)
    )


    # -----------------------------------------------------
    # DISPLAY SKILLS
    # -----------------------------------------------------

    st.subheader("🛠️ Skills Found in Resume")

    if len(resume_skill_names) > 0:

        st.write(
            ", ".join(resume_skill_names)
        )

    else:

        st.warning(
            "No matching technical skills were found."
        )


    # -----------------------------------------------------
    # JOB ROLE MATCHING
    # -----------------------------------------------------

    st.subheader("🎯 Job Role Matching")

    try:

        results = calculate_match_scores(
            cleaned_text,
            job_roles
        )

    except Exception as e:

        st.error(
            f"Error calculating job match scores: {e}"
        )

        st.stop()


    # -----------------------------------------------------
    # CONVERT RESULTS TO DATAFRAME
    # -----------------------------------------------------

    if isinstance(results, pd.DataFrame):

        results_df = results.copy()

    elif isinstance(results, list):

        results_df = pd.DataFrame(results)

    else:

        st.error(
            "The job matcher returned an unsupported result format."
        )

        st.stop()


    # -----------------------------------------------------
    # IDENTIFY ROLE COLUMN
    # -----------------------------------------------------

    role_column = None

    possible_role_columns = [
        "Job Role",
        "Role",
        "role",
        "job_role"
    ]

    for column in possible_role_columns:

        if column in results_df.columns:
            role_column = column
            break


    if role_column is None:

        st.error(
            "Could not find the job role column in job_roles.csv."
        )

        st.write("Available columns:")
        st.write(list(results_df.columns))

        st.stop()


    # -----------------------------------------------------
    # IDENTIFY SCORE COLUMN
    # -----------------------------------------------------

    score_column = None

    possible_score_columns = [
        "Match_Score",
        "Match Score",
        "match_score",
        "Score",
        "score"
    ]

    for column in possible_score_columns:

        if column in results_df.columns:
            score_column = column
            break


    if score_column is None:

        st.error(
            "Could not find the match score column."
        )

        st.write("Available columns:")
        st.write(list(results_df.columns))

        st.stop()


    # -----------------------------------------------------
    # DISPLAY MATCH RESULTS
    # -----------------------------------------------------

    display_df = results_df[
        [role_column, score_column]
    ].copy()

    display_df.columns = [
        "Job Role",
        "Match Score (%)"
    ]

    # Display match results
    st.markdown("### 📊 Match Results")

    for _, row in display_df.iterrows():

        role = row["Job Role"]
        score = float(row["Match Score (%)"])

        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:space-between;
                padding:12px 18px;
                margin:6px 0;
                border-radius:8px;
                background-color:#1f2937;
            ">
                <span style="font-weight:600;">{role}</span>
                <span style="font-weight:700;">{score:.1f}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # TOP RECOMMENDED ROLES
    # -----------------------------------------------------

    st.subheader("🏆 Recommended Job Roles")

    top_roles = display_df.head(3)

    for _, row in top_roles.iterrows():

        st.write(
            f"**{row['Job Role']}** — "
            f"{row['Match Score (%)']}%"
        )



    # -----------------------------------------------------
    # SELECT TARGET ROLE
    # -----------------------------------------------------

    st.subheader("🔍 Skill Gap Analysis")

    available_roles = (
        display_df["Job Role"]
        .astype(str)
        .tolist()
    )


    if len(available_roles) == 0:

        st.warning(
            "No job roles are available."
        )

        st.stop()


    selected_role = st.selectbox(
        "Select a target job role:",
        available_roles
    )


    # -----------------------------------------------------
    # GET SELECTED ROLE INFORMATION
    # -----------------------------------------------------

    selected_row = results_df[
        results_df[role_column].astype(str)
        == selected_role
    ].iloc[0]


    # -----------------------------------------------------
    # GET REQUIRED SKILLS
    # -----------------------------------------------------

    required_skills = []

    # Find the required-skills column automatically
    required_column = None

    for column in results_df.columns:
        normalized_column = str(column).strip().lower().replace("_", " ")

        if normalized_column == "required skills":
            required_column = column
            break

    if required_column is not None:

        required_value = selected_row[required_column]

        if pd.notna(required_value):

         required_skills = [
             skill.strip().lower()
             for skill in str(required_value).split(",")
             if skill.strip()
         ]
   



    # -----------------------------------------------------
    # MATCHED AND MISSING SKILLS
    # -----------------------------------------------------

    resume_skills_lower = {
        skill.lower().strip()
        for skill in resume_skill_names
    }


    matched_skills = [
        skill.title()
        for skill in required_skills
        if skill in resume_skills_lower
    ]


    missing_skills = [
        skill.title()
        for skill in required_skills
        if skill not in resume_skills_lower
    ]


    # -----------------------------------------------------
    # MATCH SCORE
    # -----------------------------------------------------

    selected_score = selected_row[
        score_column
    ]


    st.metric(
        label=f"Match Score — {selected_role}",
        value=f"{selected_score}%"
    )


    # -----------------------------------------------------
    # TWO COLUMNS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # MATCHED SKILLS
    # -----------------------------------------------------

    with col1:

        st.markdown("### ✅ Skills You Have")

        if len(matched_skills) > 0:

            for skill in matched_skills:
                st.write(f"✅ {skill}")

        else:

            st.info(
                "No required skills matched."
            )


    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------

    with col2:

        st.markdown("### ⚠️ Skills to Improve")

        if len(missing_skills) > 0:

            for skill in missing_skills:
                st.write(f"❌ {skill}")

        else:

            st.success(
                "You already have all the required skills!"
            )


    # -----------------------------------------------------
    # LEARNING ROADMAP
    # -----------------------------------------------------

    st.subheader("🗺️ Learning Roadmap")


    if len(missing_skills) > 0:

        try:

            # Try the roadmap function from your project
            roadmap = generate_roadmap(
                missing_skills
            )

            if roadmap:

                if isinstance(roadmap, list):

                    for item in roadmap:
                        st.write(f"📚 {item}")

                elif isinstance(roadmap, dict):

                    for key, value in roadmap.items():

                        st.markdown(
                            f"**{key}**"
                        )

                        st.write(value)

                else:

                    st.write(roadmap)

            else:

                # Basic fallback roadmap
                for index, skill in enumerate(
                    missing_skills,
                    start=1
                ):

                    st.write(
                        f"**Week {index}:** "
                        f"Learn {skill} fundamentals and practice with a small project."
                    )

        except Exception:

            # Basic fallback roadmap
            for index, skill in enumerate(
                missing_skills,
                start=1
            ):

                st.write(
                    f"**Week {index}:** "
                    f"Learn {skill} fundamentals and practice with a small project."
                )

    else:

        st.success(
            "🎉 No skill gaps found for this role!"
        )


    # -----------------------------------------------------
    # RESPONSIBLE AI NOTE
    # -----------------------------------------------------

    st.divider()

    st.caption(
        "ℹ️ This system provides career guidance based on "
        "resume keywords and job requirements. It should "
        "not be used as an automatic hiring or rejection system."
    )
# -----------------------------------------------------
# DOWNLOAD PDF REPORT
# -----------------------------------------------------

st.subheader("📄 Download Analysis Report")


def create_pdf_report():

    pdf_path = "resume_analysis_report.pdf"

    c = canvas.Canvas(pdf_path, pagesize=A4)

    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Resume Analyzer Report")

    y -= 35

    c.setFont("Helvetica", 11)
    c.drawString(
        50,
        y,
        f"Resume: {file_name}"
    )

    y -= 30

    # Skills
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Skills Found")

    y -= 20

    c.setFont("Helvetica", 10)

    skills_text = ", ".join(resume_skill_names)

    # Wrap long skill list
    words = skills_text.split()
    line = ""

    for word in words:

        test_line = line + word + " "

        if c.stringWidth(test_line, "Helvetica", 10) > 500:

            c.drawString(50, y, line)
            y -= 15
            line = word + " "

        else:
            line = test_line

    if line:
        c.drawString(50, y, line)
        y -= 25


    # Job role scores
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Job Role Match Scores")

    y -= 20

    c.setFont("Helvetica", 10)

    for _, row in display_df.iterrows():

        role = row["Job Role"]
        score = float(row["Match Score (%)"])

        c.drawString(
            60,
            y,
            f"{role}: {score:.1f}%"
        )

        y -= 15

        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)


    # Target role
    y -= 10

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Target Job Role")

    y -= 20

    c.setFont("Helvetica", 10)

    c.drawString(
        60,
        y,
        f"{selected_role}: {float(selected_score):.1f}%"
    )

    y -= 30


    # Skills you have
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Skills You Have")

    y -= 20

    c.setFont("Helvetica", 10)

    if matched_skills:

        for skill in matched_skills:

            c.drawString(
                60,
                y,
                f"✓ {skill}"
            )

            y -= 15

    else:

        c.drawString(
            60,
            y,
            "No matching skills found."
        )

        y -= 15

    y -= 15


    # Missing skills
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Skills to Improve")

    y -= 20

    c.setFont("Helvetica", 10)

    if missing_skills:

        for skill in missing_skills:

            c.drawString(
                60,
                y,
                f"• {skill}"
            )

            y -= 15

    else:

        c.drawString(
            60,
            y,
            "No skill gaps found."
        )

        y -= 15

    y -= 15


    # Roadmap
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Learning Roadmap")

    y -= 20

    c.setFont("Helvetica", 10)

    if missing_skills:

        for index, skill in enumerate(
            missing_skills,
            start=1
        ):

            c.drawString(
                60,
                y,
                f"Week {index}: Learn {skill} fundamentals and practice with a small project."
            )

            y -= 15

            if y < 60:

                c.showPage()

                y = height - 50

                c.setFont(
                    "Helvetica",
                    10
                )

    else:

        c.drawString(
            60,
            y,
            "No additional learning required for this role."
        )


    # Responsible AI note
    y -= 30

    if y < 80:

        c.showPage()
        y = height - 50

    c.setFont("Helvetica-Bold", 10)

    c.drawString(
        50,
        y,
        "Responsible AI Note"
    )

    y -= 15

    c.setFont("Helvetica", 9)

    c.drawString(
        50,
        y,
        "This report provides career guidance based on resume"
    )

    y -= 12

    c.drawString(
        50,
        y,
        "skills and job requirements. It should not be used as"
    )

    y -= 12

    c.drawString(
        50,
        y,
        "an automatic hiring or rejection system."
    )


    c.save()

    return pdf_path


if uploaded_file is not None:

    pdf_file = create_pdf_report()

    with open(pdf_file, "rb") as file:
        pdf_bytes = file.read()

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_bytes,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf"
    )