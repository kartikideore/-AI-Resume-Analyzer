#  AI Resume Analyzer

An intelligent resume analysis tool that helps job seekers optimize their resumes for specific job roles using AI-powered analysis.

##  Features

| Feature | Description |
|---------|-------------|
|  File Upload | Upload PDF/DOCX resumes |
|  25+ Job Roles | Software Engineer, Data Scientist, Product Manager, etc. |
|  Real-time Scoring | Get score out of 100 instantly |
|  Skill Gap Analysis | Find missing skills for your target role |
|  Section Detection | Checks for Experience, Education, Skills, Projects |
|  Action Verbs | Detects strong action verbs like "Developed", "Led" |
|  Metrics Check | Finds quantifiable achievements (%, $, numbers) |
|  ATS Compatibility | Checks if resume passes automated systems |
|  Smart Suggestions | Get personalized improvement tips |
|  Download Report | Save analysis as TXT file |

##  Tech Stack

- **Python 3.14** - Backend logic
- **Streamlit** - Web framework (frontend + backend)
- **pdfplumber** - PDF text extraction
- **python-docx** - Word document extraction
- **Regex** - Pattern matching for skills

##  Live Demo

[Click here to try the app](https://your-app-name.streamlit.app)

## Screenshots

### Homepage
![Homepage](https://via.placeholder.com/800x400?text=Upload+Resume+Screen)

### Analysis Results
![Results](https://via.placeholder.com/800x400?text=Score+and+Suggestions)

##  How to Run Locally

### Prerequisites
- Python 3.8 or higher
- Git (optional)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/kartikideore/-AI-Resume-Analyzer.git
   cd -AI-Resume-Analyzer

   pip install -r requirements.txt
   streamlit run resume_app.py

    How to Use
Upload your resume (PDF or DOCX format)

Select your target job role from 25+ options

Click Analyze and get instant results

Review your score and missing skills

Download the report for future reference

<img width="1918" height="1062" alt="Screenshot 2026-04-14 233223" src="https://github.com/user-attachments/assets/afab43a8-c7e5-4274-b470-ad2a5d20c7c9" />
<img width="1912" height="1076" alt="Screenshot 2026-04-14 233140" src="https://github.com/user-attachments/assets/0f8a04cd-a9ca-4e69-8935-f0e70ca4f281" />
 Scoring System
Category	Weight	What it checks
Technical Skills	40%	Keywords matching your job role
Resume Sections	20%	Experience, Education, Skills, Projects
Action Verbs	20%	"Developed", "Built", "Led", etc.
Quantifiable Metrics	20%	Percentages, dollar amounts, numbers
 Supported Job Roles (25+)
 Tech Roles
Software Engineer

Data Analyst

Web Developer

Data Scientist

DevOps Engineer

Frontend Developer

Backend Developer

Full Stack Developer

Cloud Engineer

Machine Learning Engineer

AI Engineer

 Management
Product Manager

Project Manager

Technical Project Manager

 Marketing & Sales
Digital Marketing Manager

Social Media Manager

Sales Executive

 HR & Finance
HR Generalist

Financial Analyst

Business Analyst

 Design
Graphic Designer

UX/UI Designer

Product Designer

Security
Cybersecurity Analyst

Security Engineer

 Sample Resume for Testing
text
John Doe - Software Engineer

Skills: Python, Java, SQL, React, Git, AWS

Experience:
- Developed web applications at Tech Company
- Built REST APIs serving 1000+ users
- Led team of 5 developers

Education: BS Computer Science, GPA 3.8

Projects:
- E-commerce platform with 500+ users
- Weather forecasting app

Achievements: Increased efficiency by 40%, Reduced costs by $25K
 Future Enhancements
Add machine learning for context understanding

OCR support for scanned PDFs

LinkedIn profile integration

Job recommendation engine

Multi-resume comparison

Cloud deployment with user accounts

 Developer
Kartiki Deore
Trinity academy of engineering
IT firstyear
DTI Project - 15 April 2026

 License
This project is for educational purposes as part of DTI submission.

 Acknowledgments
Streamlit for the amazing web framework

pdfplumber for PDF text extraction

All the sample resumes used for testing

