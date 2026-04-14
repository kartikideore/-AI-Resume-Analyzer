import streamlit as st
import pdfplumber
from docx import Document
import re
from collections import Counter

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠", layout="wide")

# ========== TEXT EXTRACTION ==========
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    text = ""
    doc = Document(file)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_resume_text(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    return ""

# ========== ADVANCED RESUME ANALYSIS (Specific to each resume) ==========
def analyze_specific_resume(resume_text, job_role):
    resume_lower = resume_text.lower()
    
    # Role-specific keyword databases
    role_keywords = {
        "Software Engineer": ["python", "java", "javascript", "react", "angular", "vue", "node.js", "express", "django", "flask", "spring", "sql", "mongodb", "postgresql", "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "rest api", "graphql", "data structures", "algorithms", "oop", "design patterns", "testing", "jenkins", "ci/cd"],
        
        "Data Analyst": ["python", "r", "sql", "excel", "tableau", "power bi", "looker", "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "statistics", "probability", "hypothesis testing", "regression", "data cleaning", "data visualization", "etl", "jupyter", "spreadsheets", "vba", "dashboard", "kpi", "business intelligence"],
        
        "Web Developer": ["html", "css", "javascript", "typescript", "react", "angular", "vue", "next.js", "node.js", "express", "php", "laravel", "ruby on rails", "mongodb", "mysql", "postgresql", "git", "responsive design", "bootstrap", "tailwind", "api", "rest", "graphql", "wordpress", "hosting", "deployment"],
        
        "Data Scientist": ["python", "r", "sql", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "machine learning", "deep learning", "nlp", "computer vision", "statistics", "linear algebra", "calculus", "data mining", "big data", "spark", "hadoop", "cloud computing"],
        
        "DevOps Engineer": ["linux", "bash", "python", "docker", "kubernetes", "jenkins", "gitlab ci", "github actions", "aws", "azure", "gcp", "terraform", "ansible", "prometheus", "grafana", "elk stack", "nginx", "apache", "monitoring", "logging", "iac"],
        
        "Project Manager": ["agile", "scrum", "kanban", "jira", "confluence", "trello", "ms project", "leadership", "team management", "stakeholder management", "risk management", "budgeting", "scheduling", "waterfall", "pmp", "prince2", "communication", "negotiation", "reporting"]
    }
    
    # Get keywords for selected role
    keywords = role_keywords.get(job_role, role_keywords["Software Engineer"])
    
    # === SPECIFIC ANALYSIS OF THIS RESUME ===
    
    # 1. Find which skills are present (from the keyword list)
    found_skills = []
    missing_skills = []
    
    for skill in keywords:
        if skill in resume_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    # 2. Detect sections (look for common section headers)
    sections_detected = []
    section_patterns = {
        "experience": ["experience", "work experience", "employment", "work history", "professional experience"],
        "education": ["education", "academic background", "degrees", "university", "college", "school"],
        "skills": ["skills", "technical skills", "core competencies", "expertise"],
        "projects": ["projects", "personal projects", "side projects", "portfolio"],
        "certifications": ["certifications", "certificates", "courses"],
        "achievements": ["achievements", "awards", "honors", "recognition"],
        "languages": ["languages", "language proficiency"],
        "volunteering": ["volunteer", "volunteering", "community"]
    }
    
    for section, patterns in section_patterns.items():
        for pattern in patterns:
            if pattern in resume_lower:
                sections_detected.append(section)
                break
    
    sections_detected = list(set(sections_detected))
    
    # 3. Check for action verbs (shows strong writing)
    action_verbs = ["developed", "built", "created", "designed", "implemented", "managed", "led", "improved", "increased", "decreased", "reduced", "achieved", "delivered", "launched", "optimized", "automated", "integrated", "collaborated", "mentored", "trained", "spearheaded", "architected", "refactored", "debugged", "tested", "deployed"]
    
    found_action_verbs = [verb for verb in action_verbs if verb in resume_lower]
    
    # 4. Check for metrics/numbers (shows impact)
    numbers = re.findall(r'\d+%|\d+\s*percent|\d+\s*days|\d+\s*hours|\$\d+|\d+\s*people|\d+\s*team', resume_text)
    
    # 5. Check for soft skills
    soft_skills = ["communication", "teamwork", "problem solving", "leadership", "time management", "critical thinking", "creativity", "adaptability", "collaboration", "organization"]
    found_soft_skills = [skill for skill in soft_skills if skill in resume_lower]
    
    # 6. Check for contact information
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'\+?\d[\d\s\-\(\)]{8,}\d', resume_text))
    has_linkedin = "linkedin.com/in/" in resume_lower or "linkedin.com/pub/" in resume_lower
    
    # 7. Check for formatting issues
    formatting_issues = []
    if len(resume_text.split()) < 200:
        formatting_issues.append("Very short resume - may lack detail")
    if "table" in resume_lower:
        formatting_issues.append("Tables detected - may cause ATS issues")
    if resume_text.count('\t') > 10:
        formatting_issues.append("Multiple tabs - use single column format")
    
    # === SCORING (Based on actual content) ===
    
    # Skills score (40 points)
    skill_score = min(40, int((len(found_skills) / max(len(keywords), 1)) * 40))
    
    # Sections score (20 points)
    expected_sections = ["experience", "education", "skills", "projects"]
    section_score = min(20, int((len([s for s in expected_sections if s in sections_detected]) / 4) * 20))
    
    # Action verbs score (15 points)
    verb_score = min(15, len(found_action_verbs))
    
    # Metrics score (10 points)
    metric_score = min(10, len(numbers))
    
    # Soft skills score (5 points)
    soft_skill_score = min(5, len(found_soft_skills))
    
    # Contact info score (10 points)
    contact_score = 0
    if has_email:
        contact_score += 4
    if has_phone:
        contact_score += 3
    if has_linkedin:
        contact_score += 3
    
    total_score = min(100, skill_score + section_score + verb_score + metric_score + soft_skill_score + contact_score)
    
    # Grade based on actual score
    if total_score >= 85:
        grade = "Outstanding! 🎉 Ready for top companies"
    elif total_score >= 70:
        grade = "Good 👍 A few improvements needed"
    elif total_score >= 55:
        grade = "Decent 📝 Needs some work"
    elif total_score >= 40:
        grade = "Needs Improvement ⚠️ Major updates required"
    else:
        grade = "Poor ❌ Complete overhaul recommended"
    
    # === GENERATE SPECIFIC FEEDBACK ===
    strengths = []
    improvements = []
    
    # Strengths based on actual content
    if skill_score >= 30:
        strengths.append(f"✅ Strong technical skills ({len(found_skills)} relevant skills found)")
    if section_score >= 15:
        strengths.append(f"✅ Good section coverage ({', '.join(sections_detected[:3])})")
    if len(found_action_verbs) >= 5:
        strengths.append(f"✅ Excellent use of action verbs ({len(found_action_verbs)} examples)")
    if len(numbers) >= 3:
        strengths.append(f"✅ Good use of metrics/numbers ({len(numbers)} quantifiable achievements)")
    if has_linkedin:
        strengths.append("✅ LinkedIn profile included")
    if len(found_soft_skills) >= 3:
        strengths.append(f"✅ Shows soft skills: {', '.join(found_soft_skills[:3])}")
    
    # Improvements based on missing content
    if skill_score < 25:
        improvements.append(f"❌ Add more technical skills. Found {len(found_skills)} out of {len(keywords)} expected")
    if "experience" not in sections_detected:
        improvements.append("❌ Missing 'Experience' section - crucial for recruiters")
    if "projects" not in sections_detected:
        improvements.append("❌ Add a 'Projects' section to showcase practical work")
    if len(found_action_verbs) < 3:
        improvements.append("❌ Use stronger action verbs (e.g., 'Developed', 'Led', 'Optimized')")
    if len(numbers) == 0:
        improvements.append("❌ Add quantifiable achievements (e.g., 'Increased sales by 30%')")
    if not has_phone:
        improvements.append("❌ Missing phone number - recruiters need to contact you")
    if not has_linkedin:
        improvements.append("📎 Add LinkedIn profile link for professional presence")
    if len(missing_skills) > 10:
        improvements.append(f"🎯 Missing key skills: {', '.join(missing_skills[:5])}")
    
    # Ensure we have at least 3 suggestions
    if len(improvements) < 3:
        improvements.append("📊 Add metrics to show impact (numbers, percentages, $ amounts)")
        improvements.append("🔧 Tailor resume specifically for this job role")
        improvements.append("📝 Add a professional summary at the top")
    
    return {
        'score': total_score,
        'grade': grade,
        'found_skills': found_skills,
        'missing_skills': missing_skills[:10],
        'sections_detected': sections_detected,
        'found_action_verbs': found_action_verbs,
        'numbers_found': len(numbers),
        'found_soft_skills': found_soft_skills,
        'has_email': has_email,
        'has_phone': has_phone,
        'has_linkedin': has_linkedin,
        'formatting_issues': formatting_issues,
        'strengths': strengths,
        'improvements': improvements,
        'skill_score': skill_score,
        'section_score': section_score,
        'verb_score': verb_score,
        'metric_score': metric_score,
        'soft_skill_score': soft_skill_score,
        'contact_score': contact_score,
        'word_count': len(resume_text.split())
    }

# ========== MAIN APP ==========
st.title("🧠 AI Resume Analyzer")
st.markdown("*Real analysis of YOUR specific resume - not generic templates*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    job_role = st.selectbox(
        "Target Job Role:",
        ["Software Engineer", "Data Analyst", "Web Developer", "Data Scientist", "DevOps Engineer", "Project Manager"]
    )
    st.markdown("---")
    st.markdown("### What gets analyzed:")
    st.markdown("✓ Technical skills (role-specific)")
    strat.markdown("✓ Resume sections")
    st.markdown("✓ Action verbs used")
    st.markdown("✓ Quantifiable achievements")
    st.markdown("✓ Soft skills")
    st.markdown("✓ Contact information")
    st.markdown("✓ ATS compatibility")

# Upload area
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=['pdf', 'docx'],
    help="Each resume gets unique analysis based on its content"
)

if uploaded_file is not None:
    with st.spinner("🔍 Analyzing YOUR specific resume..."):
        resume_text = extract_resume_text(uploaded_file)
        
        if resume_text and len(resume_text) > 100:
            # Analyze this specific resume
            analysis = analyze_specific_resume(resume_text, job_role)
            
            # Show file info
            st.info(f"📄 Analyzing: **{uploaded_file.name}** | Words: {analysis['word_count']} | Sections found: {len(analysis['sections_detected'])}")
            
            # Main score display
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"## 🎯 Overall Score: **{analysis['score']}/100**")
                st.markdown(f"### {analysis['grade']}")
                st.progress(analysis['score'] / 100)
            
            with col2:
                st.metric("Technical Skills", f"{len(analysis['found_skills'])}/{len(analysis['found_skills']) + len(analysis['missing_skills'])}")
            
            with col3:
                st.metric("Sections Found", f"{len(analysis['sections_detected'])}/8")
            
            st.markdown("---")
            
            # Score breakdown
            st.subheader("📊 Score Breakdown (Specific to Your Resume)")
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.metric("Skills", f"{analysis['skill_score']}/40")
            with col2:
                st.metric("Sections", f"{analysis['section_score']}/20")
            with col3:
                st.metric("Action Verbs", f"{analysis['verb_score']}/15")
            with col4:
                st.metric("Metrics", f"{analysis['metric_score']}/10")
            with col5:
                st.metric("Soft Skills", f"{analysis['soft_skill_score']}/5")
            with col6:
                st.metric("Contact", f"{analysis['contact_score']}/10")
            
            st.markdown("---")
            
            # Two columns for strengths and improvements
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✅ What's Working Well")
                if analysis['strengths']:
                    for strength in analysis['strengths']:
                        st.success(strength)
                else:
                    st.info("No major strengths detected yet - focus on improvements below")
            
            with col2:
                st.subheader("❌ Areas to Improve")
                for improvement in analysis['improvements'][:6]:
                    st.error(improvement)
            
            st.markdown("---")
            
            # Detailed analysis sections
            with st.expander("🔍 View Detailed Analysis", expanded=True):
                # Skills section
                st.subheader("🛠️ Technical Skills Analysis")
                if analysis['found_skills']:
                    st.write(f"**Found ({len(analysis['found_skills'])} skills):**")
                    cols = st.columns(4)
                    for i, skill in enumerate(analysis['found_skills'][:20]):
                        cols[i % 4].markdown(f"✓ `{skill}`")
                else:
                    st.warning("No technical skills detected! Add a 'Skills' section.")
                
                if analysis['missing_skills']:
                    st.write(f"**Missing ({len(analysis['missing_skills'])} skills):**")
                    cols = st.columns(4)
                    for i, skill in enumerate(analysis['missing_skills'][:12]):
                        cols[i % 4].markdown(f"✗ `{skill}`")
                
                st.markdown("---")
                
                # Sections found
                st.subheader("📑 Resume Sections Detected")
                if analysis['sections_detected']:
                    for section in analysis['sections_detected']:
                        st.write(f"✓ {section.title()}")
                else:
                    st.warning("No clear sections detected. Use headers like 'Experience', 'Education', 'Skills'")
                
                # Action verbs
                st.subheader("💪 Action Verbs Used")
                if analysis['found_action_verbs']:
                    st.write(f"Found {len(analysis['found_action_verbs'])} strong action verbs:")
                    st.write(", ".join(analysis['found_action_verbs'][:10]))
                else:
                    st.warning("No strong action verbs detected. Start bullet points with verbs like 'Developed', 'Led', 'Created'")
                
                # Metrics
                st.subheader("📊 Quantifiable Achievements")
                if analysis['numbers_found'] > 0:
                    st.success(f"Found {analysis['numbers_found']} numbers/metrics - Great for showing impact!")
                else:
                    st.warning("No numbers or metrics detected. Add percentages, dollar amounts, or time frames to show achievements")
                
                # Soft skills
                st.subheader("🤝 Soft Skills")
                if analysis['found_soft_skills']:
                    st.write(f"Found: {', '.join(analysis['found_soft_skills'])}")
                else:
                    st.info("Add soft skills like 'Communication', 'Leadership', 'Problem Solving'")
                
                # Contact info
                st.subheader("📞 Contact Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("✓ Email" if analysis['has_email'] else "✗ Missing email")
                with col2:
                    st.write("✓ Phone" if analysis['has_phone'] else "✗ Missing phone")
                with col3:
                    st.write("✓ LinkedIn" if analysis['has_linkedin'] else "📎 Add LinkedIn")
                
                # Formatting issues
                if analysis['formatting_issues']:
                    st.subheader("⚠️ Formatting Issues")
                    for issue in analysis['formatting_issues']:
                        st.warning(issue)
            
            # ATS Tips
            st.markdown("---")
            st.subheader("🤖 ATS Optimization Tips")
            tips = [
                "Use standard section headers (Experience, Education, Skills)",
                "Avoid tables, columns, and images",
                "Include keywords from the job description",
                "Save as PDF (not DOCX) for best compatibility",
                "Use a simple, clean format without fancy graphics"
            ]
            for tip in tips:
                st.info(tip)
            
            # Download report option
            report = f"""
            RESUME ANALYSIS REPORT
            =======================
            File: {uploaded_file.name}
            Target Role: {job_role}
            Overall Score: {analysis['score']}/100
            Grade: {analysis['grade']}
            
            SCORE BREAKDOWN:
            - Technical Skills: {analysis['skill_score']}/40
            - Resume Sections: {analysis['section_score']}/20
            - Action Verbs: {analysis['verb_score']}/15
            - Metrics/Impact: {analysis['metric_score']}/10
            - Soft Skills: {analysis['soft_skill_score']}/5
            - Contact Info: {analysis['contact_score']}/10
            
            STRENGTHS:
            {chr(10).join(analysis['strengths'])}
            
            IMPROVEMENTS NEEDED:
            {chr(10).join(analysis['improvements'])}
            
            MISSING SKILLS FOR {job_role.upper()}:
            {', '.join(analysis['missing_skills'][:10])}
            """
            
            st.download_button(
                label="📥 Download Full Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )
            
        else:
            st.error("Could not extract enough text. Make sure your resume is not an image/scanned PDF. Use a text-based PDF or DOCX.")
else:
    # Show demo when no file uploaded
    st.info("👆 **Upload YOUR resume above** to get a personalized analysis")
    
    with st.expander("📖 See how it works (example)"):
        st.markdown("""
        **When you upload a resume, this tool will:**
        
        1. **Extract the actual text** from YOUR specific file
        2. **Count technical skills** that are actually present
        3. **Detect which sections** exist in YOUR resume
        4. **Find action verbs** YOU used
        5. **Identify metrics** in YOUR achievements
        6. **Generate UNIQUE feedback** based only on YOUR content
        
        **Example:**
        - If your resume has "Python, SQL, React" → you'll see those skills
        - If your resume lacks "Projects" section → you'll be told to add it
        - If your resume has numbers like "increased sales 30%" → you'll get credit
        
        **No two analyses are the same** - each result is unique to the uploaded resume!
        """)

st.markdown("---")
st.caption("💡 Real analysis of YOUR specific resume. Works with any PDF/DOCX resume file.")