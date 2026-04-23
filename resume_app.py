import streamlit as st
import pdfplumber
from docx import Document
import re

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

# ========== RESUME ANALYSIS FUNCTION ==========
def analyze_specific_resume(resume_text, job_role):
    resume_lower = resume_text.lower()
    
    # Complete keyword database for 50+ job roles
    role_keywords = {
        #  SOFTWARE DEVELOPMENT
        "Software Engineer": ["python", "java", "javascript", "react", "sql", "git", "docker", "aws", "data structures", "algorithms", "spring", "node.js", "c++", "microservices", "rest api"],
        "Frontend Developer": ["html", "css", "javascript", "typescript", "react", "vue", "angular", "tailwind", "bootstrap", "git", "responsive design", "next.js", "figma"],
        "Backend Developer": ["python", "java", "node.js", "sql", "mongodb", "api", "rest", "graphql", "spring", "django", "flask", "git", "microservices", "redis"],
        "Full Stack Developer": ["javascript", "react", "node.js", "python", "sql", "mongodb", "html", "css", "git", "api", "express", "typescript", "aws", "docker"],
        "Mobile Developer": ["swift", "kotlin", "java", "react native", "flutter", "ios", "android", "xcode", "android studio", "firebase", "rest api"],
        "Game Developer": ["unity", "unreal engine", "c#", "c++", "3d modeling", "animation", "physics", "game design", "opengl", "directx"],
        "Embedded Engineer": ["c", "c++", "embedded systems", "microcontrollers", "arduino", "raspberry pi", "iot", "firmware", "rtos", "circuit design"],
        "DevOps Engineer": ["linux", "bash", "python", "docker", "kubernetes", "jenkins", "gitlab", "aws", "azure", "terraform", "ansible", "prometheus", "grafana", "ci/cd"],
        "Site Reliability Engineer": ["linux", "python", "go", "kubernetes", "docker", "aws", "monitoring", "prometheus", "grafana", "incident response", "scalability"],
        "Quality Assurance Engineer": ["manual testing", "automation testing", "selenium", "junit", "pytest", "test cases", "bug tracking", "jira", "api testing"],
        
        #  DATA & AI
        "Data Analyst": ["python", "sql", "excel", "tableau", "power bi", "pandas", "numpy", "statistics", "data visualization", "etl", "kpi", "data cleaning"],
        "Data Scientist": ["python", "r", "sql", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "machine learning", "deep learning", "nlp", "statistics", "data mining"],
        "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "scikit-learn", "machine learning", "deep learning", "sql", "pandas", "numpy", "aws", "mlops", "docker"],
        "AI Engineer": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "nlp", "llm", "openai", "langchain", "rag", "vector databases"],
        "Data Engineer": ["python", "sql", "spark", "hadoop", "airflow", "etl", "data warehouse", "aws", "azure", "big data", "kafka", "pipeline"],
        "Business Intelligence Analyst": ["sql", "tableau", "power bi", "excel", "data visualization", "dashboards", "kpi", "business analytics", "reporting"],
        "Database Administrator": ["sql", "oracle", "mysql", "postgresql", "mongodb", "database design", "backup", "recovery", "performance tuning", "security"],
        
        #  CLOUD & SECURITY
        "Cloud Engineer": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "linux", "python", "ci/cd", "serverless", "lambda", "ec2", "s3"],
        "Cloud Architect": ["aws", "azure", "gcp", "cloud architecture", "microservices", "serverless", "security", "cost optimization", "scalability", "high availability"],
        "Security Engineer": ["python", "linux", "network security", "penetration testing", "cloud security", "aws security", "incident response", "cryptography", "authentication"],
        "Cybersecurity Analyst": ["network security", "firewalls", "penetration testing", "risk assessment", "compliance", "siem", "incident response", "python", "linux"],
        "Network Engineer": ["cisco", "routing", "switching", "tcp/ip", "dns", "dhcp", "firewalls", "vpn", "load balancers", "network security"],
        
        #  PRODUCT & PROJECT MANAGEMENT
        "Product Manager": ["agile", "scrum", "jira", "product strategy", "user stories", "roadmap", "stakeholder management", "analytics", "market research", "kpi"],
        "Project Manager": ["agile", "scrum", "jira", "project planning", "risk management", "budgeting", "leadership", "communication", "pmp", "waterfall"],
        "Technical Project Manager": ["agile", "scrum", "jira", "project planning", "risk management", "python", "sql", "git", "stakeholder management", "technical documentation"],
        "Product Owner": ["agile", "scrum", "product backlog", "user stories", "acceptance criteria", "stakeholder management", "jira", "prioritization"],
        "Scrum Master": ["agile", "scrum", "jira", "sprint planning", "daily standup", "retrospective", "team facilitation", "conflict resolution"],
        "Business Analyst": ["requirements gathering", "agile", "scrum", "jira", "sql", "data analysis", "use cases", "stakeholder management", "documentation", "brd"],
        
        # MARKETING & DIGITAL
        "Digital Marketing Manager": ["seo", "sem", "google analytics", "social media", "content marketing", "email marketing", "ppc", "marketing strategy", "facebook ads", "google ads"],
        "Social Media Manager": ["instagram", "facebook", "twitter", "linkedin", "tiktok", "content creation", "social media strategy", "analytics", "canva", "hootsuite"],
        "SEO Specialist": ["seo", "google analytics", "search console", "keyword research", "backlinks", "on page seo", "off page seo", "technical seo", "ahrefs", "semrush"],
        "Content Marketer": ["content strategy", "blogging", "copywriting", "seo", "email marketing", "social media", "storytelling", "content creation", "wordpress"],
        "Email Marketing Specialist": ["email marketing", "mailchimp", "hubspot", "automation", "campaign management", "a/b testing", "analytics", "copywriting"],
        "Growth Hacker": ["growth strategy", "a/b testing", "analytics", "seo", "social media", "email marketing", "conversion optimization", "data driven"],
        
        #  SALES
        "Sales Executive": ["sales", "negotiation", "crm", "lead generation", "business development", "communication", "salesforce", "cold calling", "account management"],
        "Business Development Manager": ["business development", "sales", "negotiation", "partnerships", "lead generation", "market research", "strategic planning", "crm"],
        "Account Manager": ["client relationship", "account management", "customer success", "upselling", "cross selling", "communication", "crm", "salesforce"],
        "Customer Success Manager": ["customer success", "client relationship", "onboarding", "retention", "upselling", "support", "communication", "crm"],

        #  MECHANICAL ENGINEERING ROLES
        "Mechanical engineer": ["cad","solidworks", "solidworks", "autocad", "catia", "creo", "engineering drawing", "gd&t", "manufacturing", "thermodynamics", "fluid mechanics", "heat transfer", "materials science", "fmea", "root cause analysis", "project management", "quality control"],
        "Design Engineer": ["solidworks", "catia", "creo", "autocad", "3d modeling", "parametric design", "assembly design", "drafting", "gd&t", "simulation", "finite element analysis", "design validation", "prototyping", "bom management"],
        "Production Engineer": ["manufacturing", "lean manufacturing", "six sigma", "process improvement", "production planning", "inventory management", "quality control", "sap", "erp", "supply chain", "kaizen", "5s", "root cause analysis"],
        "Quality Engineer": ["quality control", "quality assurance", "six sigma", "statistical process control", "fmea", "root cause analysis", "iso 9001", "calibration", "inspection", "testing", "quality management system", "capability analysis"],
        "Thermal Engineer": ["thermodynamics", "heat transfer", "fluid mechanics", "cfd", "ansys", "heat exchanger", "hvac", "thermal analysis", "cooling systems", "energy efficiency", "simulation"],
        "HVAC Engineer": ["hvac", "load calculation", "duct design", "piping", "chillers", "boilers", "air conditioning", "ventilation", "heating systems", "energy efficiency", "building automation", "revit"],
        "Automotive Engineer": ["automotive design", "vehicle dynamics", "engine systems", "transmission", "chassis", "suspension", "brakes", "steering", "electric vehicles", "battery technology", "cad", "catia"],
        "Robotics Engineer": ["robotics", "automation", "control systems", "sensors", "actuators", "programming", "c++", "python", "ros", "path planning", "computer vision", "machine learning", "mechatronics"],
        "Mechatronics Engineer": ["mechanics", "electronics", "programming", "control systems", "sensors", "actuators", "plc", "microcontrollers", "arduino", "raspberry pi", "automation", "robotics"],
        
        #  Civil Engineering Roles
        "Civil Engineer": ["autocad", "revit", "staad pro", "etabs", "sap2000", "structural analysis", "soil mechanics", "geotechnical", "transportation", "hydrology", "construction management", "project planning", "cost estimation", "quality control"],
        "Structural Engineer": ["structural analysis", "staad pro", "etabs", "sap2000", "safe", "rc design", "steel design", "foundation design", "seismic design", "wind load", "building codes", "is codes", "aci", "eurocodes"],
        "Geotechnical Engineer": ["soil mechanics", "foundation engineering", "site investigation", "soil testing", "geotechnical analysis", "plaxis", "slope stability", "retaining walls", "pile foundation", "liquefaction", "rock mechanics"],
        "Transportation Engineer": ["highway design", "traffic engineering", "transportation planning", "pavement design", "mx road", "autocad civil 3d", "vissim", "synchro", "traffic analysis", "road safety", "intelligent transport systems"],
        "Water Resources Engineer": ["hydrology", "hydraulic modeling", "water supply", "wastewater treatment", "stormwater management", "dam design", "canal design", "hms", "hec-ras", "swmm", "pipe network", "water distribution"],
        "Environmental Engineer": ["environmental impact assessment", "pollution control", "waste management", "water treatment", "air quality", "environmental monitoring", "sustainability", "green building", "leed", "environmental compliance"],
        "Construction Manager": ["construction management", "project planning", "scheduling", "primavera", "ms project", "cost control", "budgeting", "resource allocation", "site management", "safety management", "contract management"],
        "Site Engineer": ["site supervision", "quality control", "billing", "material management", "labor management", "safety compliance", "work execution", "coordination", "site planning", "concrete works", "formwork"],
        "Survey Engineer": ["land surveying", "total station", "gps surveying", "autocad", "gis", "topographic survey", "boundary survey", "contour mapping", "digital terrain model", "quantity survey", "survey data processing"],
        "Urban Planner": ["urban planning", "town planning", "land use planning", "zoning", "transportation planning", "gis", "master plan", "development control", "smart cities", "sustainable development", "urban design"],
        "Project Planner": ["project planning", "primavera p6", "ms project", "scheduling", "resource planning", "cost estimation", "earned value management", "critical path method", "work breakdown structure", "progress monitoring"],
        "Quantity Surveyor": ["quantity takeoff", "cost estimation", "billing", "rate analysis", "tendering", "contract management", "cost control", "valuation", "auto cad", "ms excel", "measurement", "specifications"],
        "BIM Engineer": ["bim", "revit", "navisworks", "autocad", "3d modeling", "clash detection", "coordination", "4d simulation", "5d cost", "bim 360", "point cloud", "scan to bim", "families creation"],
        
        #  HUMAN RESOURCES
        "HR Generalist": ["recruitment", "onboarding", "employee relations", "hr policies", "performance management", "training", "hrms", "labor laws", "benefits administration"],
        "Talent Acquisition Specialist": ["recruitment", "sourcing", "interviewing", "candidate screening", "ats", "linkedin recruiter", "employer branding"],
        "HR Business Partner": ["hr strategy", "employee relations", "performance management", "talent management", "organizational development", "change management"],
        "Learning & Development Specialist": ["training", "learning management system", "instructional design", "curriculum development", "workshop facilitation", "e learning"],
        
        #  FINANCE
        "Financial Analyst": ["excel", "financial modeling", "accounting", "budgeting", "forecasting", "vba", "sql", "tableau", "financial reporting", "variance analysis"],
        "Investment Banker": ["financial modeling", "valuation", "due diligence", "mergers and acquisitions", "capital markets", "excel", "pitch books"],
        "Accountant": ["accounting", "gaap", "financial statements", "tax preparation", "audit", "quickbooks", "sap", "excel", "general ledger"],
        "Auditor": ["auditing", "accounting", "gaap", "risk assessment", "internal controls", "financial statements", "compliance", "data analysis"],
        
        #  DESIGN
        "Graphic Designer": ["photoshop", "illustrator", "indesign", "figma", "sketch", "adobe creative suite", "typography", "color theory", "branding"],
        "UX/UI Designer": ["figma", "adobe xd", "sketch", "prototyping", "user research", "wireframing", "usability testing", "html", "css", "responsive design"],
        "Product Designer": ["figma", "prototyping", "user research", "wireframing", "ui design", "ux design", "design systems", "user testing", "visual design"],
        "Web Designer": ["html", "css", "javascript", "figma", "adobe xd", "responsive design", "wordpress", "ui design", "user experience"],
        "Motion Graphics Designer": ["after effects", "premiere pro", "animation", "motion graphics", "video editing", "cinema 4d", "photoshop", "illustrator"],
        
        # HEALTHCARE
        "Healthcare Administrator": ["healthcare management", "patient care", "medical records", "regulatory compliance", "budgeting", "staff management"],
        "Clinical Data Manager": ["clinical data", "data management", "sql", "excel", "clinical trials", "data validation", "medical terminology"],
        "Medical Writer": ["medical writing", "clinical research", "regulatory documents", "scientific writing", "publications", "research papers"],
        
        #  EDUCATION
        "Instructional Designer": ["instructional design", "curriculum development", "e learning", "lms", "training materials", "needs analysis", "assessment design"],
        "Teacher": ["lesson planning", "classroom management", "curriculum development", "student assessment", "parent communication"],
        "Academic Counselor": ["student advising", "academic planning", "career counseling", "student support", "communication"],

        #  ARCHITECTURE & INTERIOR DESIGN
        "Architect": ["autocad", "revit", "sketchup", "rhino", "3ds max", "lumion", "archicad", "building design", "construction documentation", "building codes", "site analysis", "spatial planning", "conceptual design", "schematic design", "design development", "project coordination", "client presentation", "bim", "rendering"],
        "Interior Designer": ["autocad", "sketchup", "3ds max", "revit", "photoshop", "illustrator", "space planning", "materials selection", "furniture design", "lighting design", "color theory", "rendering", "client consultation", "ff&e", "mood boards", "construction documents"],
        "Landscape Architect": ["autocad", "sketchup", "rhino", "lumion", "gis", "site planning", "planting design", "grading", "drainage", "irrigation", "sustainable design", "urban design", "parks design", "landscape construction", "3d modeling"],
        "Urban Designer": ["urban design", "urban planning", "gis", "autocad", "sketchup", "photoshop", "illustrator", "indesign", "master planning", "zoning", "land use", "transportation planning", "public space design", "placemaking", "community engagement"],
        "BIM Modeler": ["revit", "autocad", "navisworks", "bim 360", "clash detection", "3d modeling", "parametric design", "families creation", "coordination", "lodi", "construction documents", "dynamo"],
        "3D Visualizer": ["3ds max", "vray", "corona renderer", "lumion", "sketchup", "photoshop", "after effects", "rendering", "texturing", "lighting", "animation", "post production", "virtual reality", "walkthrough"],
        "CAD Technician": ["autocad", "drafting", "2d drawings", "3d modeling", "construction documents", "technical drawings", "detail drawings", "sections", "elevations", "floor plans", "site plans", "revisions"],
        "Project Architect": ["architectural design", "project management", "construction administration", "client coordination", "consultant coordination", "building codes", "permits", "construction documents", "specifications", "bidding", "contract administration", "revit", "autocad"],
        "Architectural Designer": ["conceptual design", "schematic design", "design development", "revit", "autocad", "sketchup", "rhino", "3ds max", "photoshop", "indesign", "model making", "rendering", "construction documents"],
        "Set Designer": ["sketchup", "autocad", "3ds max", "photoshop", "illustrator", "theatre design", "film design", "stage design", "scenic design", "model making", "drafting", "rendering", "construction", "props"],
        
        #  OTHER
        "Operations Manager": ["operations management", "process improvement", "team leadership", "budgeting", "supply chain", "logistics", "kpi tracking"],
        "Supply Chain Manager": ["supply chain", "logistics", "inventory management", "procurement", "vendor management", "forecasting"],
        "Legal Associate": ["legal research", "document drafting", "case management", "client communication", "contract review"],
        "Research Analyst": ["research methodology", "data analysis", "statistics", "qualitative research", "quantitative research", "report writing"],
        "Executive Assistant": ["calendar management", "travel coordination", "meeting planning", "communication", "document preparation"]
    }
    
       # CHECK IF ROLE EXISTS IN DATABASE
    if job_role in role_keywords:
        # Role found - use specific keywords
        keywords = role_keywords[job_role]
        role_type = "specific"
    else:
        # CUSTOM ROLE - Extract keywords from the role name itself!
        custom_keywords = []
        
        # Split the custom role name into words
        role_words = job_role.lower().split()
        
        # Common skill keywords to look for in custom roles
        common_skills = {
            "engineer": ["engineering", "design", "analysis", "problem solving", "technical", "project management"],
            "developer": ["programming", "coding", "software development", "debugging", "algorithms", "data structures"],
            "analyst": ["data analysis", "reporting", "statistics", "excel", "sql", "visualization", "insights"],
            "manager": ["leadership", "team management", "planning", "budgeting", "stakeholder management", "strategy"],
            "designer": ["design", "creativity", "figma", "adobe", "prototyping", "user experience", "visual"],
            "marketing": ["seo", "social media", "content", "analytics", "campaigns", "branding"],
            "sales": ["negotiation", "crm", "lead generation", "client relations", "revenue", "closing"],
            "hr": ["recruitment", "onboarding", "employee relations", "training", "performance management"],
            "finance": ["financial analysis", "budgeting", "forecasting", "accounting", "excel", "reporting"],
            "data": ["data analysis", "sql", "python", "visualization", "statistics", "etl"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "devops", "infrastructure"],
            "security": ["network security", "firewalls", "risk assessment", "compliance", "encryption"],
            "robotics": ["robotics", "automation", "control systems", "sensors", "actuators", "c++", "python", "ros"],
            "blockchain": ["blockchain", "smart contracts", "ethereum", "solidity", "cryptography", "web3"],
            "ai": ["machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "python", "algorithms"],
            "ml": ["machine learning", "deep learning", "scikit-learn", "pandas", "numpy", "python", "models"]
        }
        
        # Match role words to common skills
        for word in role_words:
            for skill_category, skills in common_skills.items():
                if skill_category in word or word in skill_category:
                    custom_keywords.extend(skills)
        
        # Add general professional keywords
        custom_keywords.extend(["communication", "teamwork", "problem solving", "leadership", "time management", 
                               "critical thinking", "creativity", "adaptability", "collaboration", "organization"])
        
        # Remove duplicates
        custom_keywords = list(set(custom_keywords))
        
        keywords = custom_keywords
        role_type = "custom"
    
    # Find present and missing skills
    found_skills = [skill for skill in keywords if skill in resume_lower]
    missing_skills = [skill for skill in keywords if skill not in resume_lower]
    
    # Section detection
    sections_detected = []
    section_patterns = {
        "experience": ["experience", "work experience", "employment", "work history"],
        "education": ["education", "academic", "university", "college", "school"],
        "skills": ["skills", "technical skills", "core competencies"],
        "projects": ["projects", "personal projects", "portfolio"],
        "certifications": ["certifications", "certificates", "courses"],
        "achievements": ["achievements", "awards", "honors"]
    }
    
    for section, patterns in section_patterns.items():
        for pattern in patterns:
            if pattern in resume_lower:
                sections_detected.append(section)
                break
    sections_detected = list(set(sections_detected))
    
    # Action verbs detection
    action_verbs = ["developed", "built", "created", "designed", "implemented", "managed", "led", "improved", "increased", "decreased", "achieved", "delivered", "launched", "optimized", "automated"]
    found_action_verbs = [verb for verb in action_verbs if verb in resume_lower]
    
    # Metrics detection
    numbers = re.findall(r'\d+%|\$\d+|\d+\s*percent', resume_text)
    
    # Soft skills detection
    soft_skills = ["communication", "teamwork", "problem solving", "leadership", "time management", "critical thinking", "creativity", "adaptability", "collaboration"]
    found_soft_skills = [skill for skill in soft_skills if skill in resume_lower]
    
    # Contact info detection
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'\+?\d[\d\s\-\(\)]{8,}\d', resume_text))
    has_linkedin = "linkedin.com/in/" in resume_lower
    
    # Scoring
    skill_score = min(40, int((len(found_skills) / max(len(keywords), 1)) * 40))
    expected_sections = ["experience", "education", "skills", "projects"]
    section_score = min(20, int((len([s for s in expected_sections if s in sections_detected]) / 4) * 20))
    verb_score = min(15, len(found_action_verbs))
    metric_score = min(10, len(numbers))
    soft_skill_score = min(5, len(found_soft_skills))
    contact_score = (4 if has_email else 0) + (3 if has_phone else 0) + (3 if has_linkedin else 0)
    
    total_score = min(100, skill_score + section_score + verb_score + metric_score + soft_skill_score + contact_score)
    
    # Grade
    if total_score >= 85:
        grade = "Outstanding!  Ready for top companies"
    elif total_score >= 70:
        grade = "Good  A few improvements needed"
    elif total_score >= 55:
        grade = "Decent Needs some work"
    elif total_score >= 40:
        grade = "Needs Improvement  Major updates required"
    else:
        grade = "Poor  Complete overhaul recommended"
    
    # Generate feedback
    strengths = []
    improvements = []
    
    if skill_score >= 30:
        strengths.append(f" Strong technical skills ({len(found_skills)} relevant skills)")
    if section_score >= 15:
        strengths.append(f" Good section coverage ({', '.join(sections_detected[:3])})")
    if len(found_action_verbs) >= 5:
        strengths.append(f" Excellent action verbs ({len(found_action_verbs)} examples)")
    if len(numbers) >= 3:
        strengths.append(f" Good use of metrics ({len(numbers)} achievements)")
    if has_linkedin:
        strengths.append(" LinkedIn profile included")
    
    if skill_score < 25:
        improvements.append(f" Add more technical skills. Found {len(found_skills)} out of {len(keywords)}")
    if "experience" not in sections_detected:
        improvements.append(" Missing 'Experience' section")
    if "projects" not in sections_detected:
        improvements.append(" Add a 'Projects' section")
    if len(found_action_verbs) < 3:
        improvements.append(" Use stronger action verbs (Developed, Led, Built)")
    if len(numbers) == 0:
        improvements.append(" Add quantifiable achievements (e.g., 'Increased sales by 30%')")
    if not has_phone:
        improvements.append(" Missing phone number")
    if not has_linkedin:
        improvements.append(" Add LinkedIn profile link")
    if missing_skills:
        improvements.append(f" Missing key skills: {', '.join(missing_skills[:5])}")
    elif role_type == "custom" and missing_skills:
        improvements.append(f" For '{job_role}', focus on adding role-specific keywords and achievements")
    elif missing_skills:
        improvements.append(f" Missing key skills: {', '.join(missing_skills[:5])}")
    
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
        'strengths': strengths,
        'improvements': improvements[:8],
        'skill_score': skill_score,
        'section_score': section_score,
        'verb_score': verb_score,
        'metric_score': metric_score,
        'soft_skill_score': soft_skill_score,
        'contact_score': contact_score,
        'word_count': len(resume_text.split()),
        'total_keywords': len(keywords)
    }

# ========== MAIN APP UI ==========
st.title(" AI Resume Analyzer")
st.markdown("*Real analysis of YOUR specific resume - 50+ job roles + Custom Role option!*")

with st.sidebar:
    st.header(" Settings")
    
    # ===== THIS IS THE "OTHER" OPTION =====
    job_role_type = st.radio(
        "Choose job role option:",
        [" Select from list", " Enter custom role"]
    )
    
    if job_role_type == " Select from list":
        job_role = st.selectbox("Select Target Job Role:", [
            "SOFTWARE DEVELOPMENT",
            "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
            "Mobile Developer", "Game Developer", "Embedded Engineer", "DevOps Engineer",
            "Site Reliability Engineer", "Quality Assurance Engineer",
            
            "DATA & AI",
            "Data Analyst", "Data Scientist", "Machine Learning Engineer", "AI Engineer",
            "Data Engineer", "Business Intelligence Analyst", "Database Administrator",
            
            "CLOUD & INFRASTRUCTURE",
            "Cloud Engineer", "Cloud Architect", "Security Engineer", "Cybersecurity Analyst", "Network Engineer",
            
            "PRODUCT & PROJECT MANAGEMENT",
            "Product Manager", "Project Manager", "Technical Project Manager", "Product Owner",
            "Scrum Master", "Business Analyst",
            
            "MARKETING & DIGITAL",
            "Digital Marketing Manager", "Social Media Manager", "SEO Specialist", "Content Marketer",
            "Email Marketing Specialist", "Growth Hacker",
            
            "SALES & BUSINESS DEVELOPMENT",
            "Sales Executive", "Business Development Manager", "Account Manager", "Customer Success Manager",
            
            "HUMAN RESOURCES",
            "HR Generalist", "Talent Acquisition Specialist", "HR Business Partner", "Learning & Development Specialist",
            
            "FINANCE & ACCOUNTING",
            "Financial Analyst", "Investment Banker", "Accountant", "Auditor",
            
            "DESIGN & CREATIVE",
            "Graphic Designer", "UX/UI Designer", "Product Designer", "Web Designer", "Motion Graphics Designer",
            
            "HEALTHCARE",
            "Healthcare Administrator", "Clinical Data Manager", "Medical Writer",
            
             "EDUCATION",
            "Instructional Designer", "Teacher", "Academic Counselor",
            
             "OTHER PROFESSIONAL ROLES",
            "Operations Manager", "Supply Chain Manager", "Legal Associate", "Research Analyst", "Executive Assistant",

             "MECHANICAL ENGINEERING",
            "Mechanical Engineer", "Design Engineer", "Production Engineer", "Quality Engineer",
            "Thermal Engineer", "HVAC Engineer", "Automotive Engineer", "Robotics Engineer",
            "Mechatronics Engineer",

            "CIVIL ENGINEERING",
            "Civil Engineer", "Structural Engineer", "Geotechnical Engineer", "Transportation Engineer",
            "Water Resources Engineer", "Environmental Engineer", "Construction Manager", "Site Engineer",
            "Survey Engineer", "Urban Planner", "Project Planner", "Quantity Surveyor", "BIM Engineer",

            "ARCHITECTURE & DESIGN",
            "Architect", "Interior Designer", "Landscape Architect", "Urban Designer",
            "BIM Modeler", "3D Visualizer", "CAD Technician", "Project Architect",
            "Architectural Designer", "Set Designer",
        ])
    else:
        job_role = st.text_input("Enter your custom job role:", placeholder="e.g., Robotics Engineer, Blockchain Developer, UI Animator, Cloud Native Developer")
        if not job_role.strip():
            job_role = "Custom Role"
        st.info(f" Analyzing for: **{job_role}**")
        st.caption(" For custom roles, we analyze general resume quality and key skills.")
    
    st.markdown("---")
    st.markdown(f"** Supports 50+ job roles + Custom**")
    st.markdown("### What gets analyzed:")
    st.markdown("✓ Technical skills (role-specific)")
    st.markdown("✓ Resume sections")
    st.markdown("✓ Action verbs used")
    st.markdown("✓ Quantifiable achievements")
    st.markdown("✓ Soft skills")
    st.markdown("✓ Contact information")

# Upload area
uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=['pdf', 'docx'],
    help="Each resume gets unique analysis based on its content"
)

if uploaded_file is not None:
    with st.spinner(" Analyzing YOUR specific resume..."):
        resume_text = extract_resume_text(uploaded_file)
        
        if resume_text and len(resume_text) > 100:
            analysis = analyze_specific_resume(resume_text, job_role)
            
            st.info(f" Analyzing: **{uploaded_file.name}** | Words: {analysis['word_count']} | Sections: {len(analysis['sections_detected'])}")
            
            # Score display
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"##  Score: **{analysis['score']}/100**")
                st.markdown(f"### {analysis['grade']}")
                st.progress(analysis['score'] / 100)
            with col2:
                st.metric("Skills Match", f"{len(analysis['found_skills'])}/{analysis['total_keywords']}")
            with col3:
                st.metric("Sections Found", f"{len(analysis['sections_detected'])}/6")
            
            st.markdown("---")
            
            # Score breakdown
            st.subheader(" Score Breakdown")
            cols = st.columns(6)
            cols[0].metric("Skills", f"{analysis['skill_score']}/40")
            cols[1].metric("Sections", f"{analysis['section_score']}/20")
            cols[2].metric("Action Verbs", f"{analysis['verb_score']}/15")
            cols[3].metric("Metrics", f"{analysis['metric_score']}/10")
            cols[4].metric("Soft Skills", f"{analysis['soft_skill_score']}/5")
            cols[5].metric("Contact", f"{analysis['contact_score']}/10")
            
            st.markdown("---")
            
            # Strengths and Improvements
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(" Strengths")
                for s in analysis['strengths']:
                    st.success(s)
                if not analysis['strengths']:
                    st.info("Focus on improvements below")
            
            with col2:
                st.subheader(" Improvements")
                for i in analysis['improvements']:
                    st.error(i)
            
            # Detailed analysis expander
            with st.expander(" View Detailed Analysis"):
                if analysis['found_skills']:
                    st.subheader(" Skills Found")
                    st.write(", ".join(analysis['found_skills'][:15]))
                
                if analysis['missing_skills']:
                    st.subheader(" Missing Skills")
                    st.write(", ".join(analysis['missing_skills'][:10]))
                
                st.subheader(" Sections Found")
                st.write(", ".join(analysis['sections_detected']) if analysis['sections_detected'] else "None detected")
                
                st.subheader(" Action Verbs Found")
                st.write(", ".join(analysis['found_action_verbs'][:10]) if analysis['found_action_verbs'] else "None")
                
                st.subheader(" Contact Info")
                st.write(f"Email: {'✓' if analysis['has_email'] else '✗'}")
                st.write(f"Phone: {'✓' if analysis['has_phone'] else '✗'}")
                st.write(f"LinkedIn: {'✓' if analysis['has_linkedin'] else '✗'}")
            
            # Download report
            report = f"""
            ========================================
            AI RESUME ANALYZER - FULL REPORT
            ========================================
            
            File: {uploaded_file.name}
            Target Role: {job_role}
            Score: {analysis['score']}/100
            Grade: {analysis['grade']}
            
            SCORE BREAKDOWN:
            - Technical Skills: {analysis['skill_score']}/40
            - Resume Sections: {analysis['section_score']}/20
            - Action Verbs: {analysis['verb_score']}/15
            - Metrics: {analysis['metric_score']}/10
            - Soft Skills: {analysis['soft_skill_score']}/5
            - Contact Info: {analysis['contact_score']}/10
            
            STRENGTHS:
            {chr(10).join(analysis['strengths'])}
            
            IMPROVEMENTS NEEDED:
            {chr(10).join(analysis['improvements'])}
            
            MISSING SKILLS:
            {', '.join(analysis['missing_skills'][:10])}
            
            ========================================
            """
            st.download_button(" Download Report", report, "resume_report.txt", "text/plain")
        else:
            st.error("Could not extract text. Make sure your resume is not an image/scanned PDF.")
else:
    st.info(" **Upload your resume to get started!**")
    
    with st.expander(" How it works"):
        st.markdown("""
        **1. Upload your resume** (PDF or DOCX)
        
        **2. Choose job role option:**
        - Select from 50+ pre-defined roles
        - OR enter any custom role (e.g., "Robotics Engineer")
        
        **3. Get instant analysis:**
        - Score out of 100
        - Found vs missing skills
        - Section detection
        - Action verb analysis
        - Personalized suggestions
        
        **4. Download detailed report**
        """)

st.markdown("---")
st.caption(" AI Resume Analyzer | 50+ Job Roles + Custom Role Option | Analyze, Optimize, Succeed")
