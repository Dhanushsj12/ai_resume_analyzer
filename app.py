from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

# Flask App
app = Flask(__name__)

# Upload folder
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

generation_config = {
"temperature": 0.3,
"top_p": 0.9,
"max_output_tokens": 2048,
}

model = genai.GenerativeModel(
"models/gemini-2.5-flash",
generation_config=generation_config
)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def analyze_resume(resume_text, jd_text=""):

    prompt = f"""


You are an Expert ATS Resume Reviewer,
Recruiter, Prompt Engineer and Career Coach.

Analyze the resume against the provided Job Description.

Provide:

1. ATS Score (0-100)

2. Resume Match Score (%)

3. Matching Skills

4. Missing Skills

5. Strengths

6. Weaknesses

7. Project Review

8. Resume Improvements

9. Interview Readiness Score

10. Learning Roadmap

Resume:
{resume_text}

Job Description:
{jd_text}
"""

    response = model.generate_content(prompt)
    return response.text




@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze")
def analyze_page():
    return render_template("analyze.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    if "resume" not in request.files:
        return jsonify({"error": "No resume uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Please upload a PDF file"}), 400

    try:
        resume_text = extract_text_from_pdf(file)

        jd_text = request.form.get(
            "job_description",
            ""
        )

        analysis = analyze_resume(
            resume_text,
            jd_text
        )

        return jsonify({
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)