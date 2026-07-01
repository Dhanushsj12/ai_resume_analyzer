from flask import Flask, render_template, request, jsonify
import os
import fitz
import google.generativeai as genai
from dotenv import load_dotenv

# -----------------------------
# Custom Modules
# -----------------------------
from parser import parse_resume
from ats_engine import calculate_ats
from keyword_match import keyword_match
from ai_review import generate_ai_review

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# -----------------------------
# Gemini API
# -----------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )

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

# -----------------------------
# PDF Text Extraction
# Using PyMuPDF
# -----------------------------
def extract_text_from_pdf(pdf_file):

    pdf = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:

        text += page.get_text()

        text += "\n"

    pdf.close()

    return text

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze")
def analyze_page():

    return render_template("analyze.html")
# -----------------------------
# Upload Route
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload_file():

    if "resume" not in request.files:
        return jsonify({
            "error": "No resume uploaded."
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF resumes are supported."
        }), 400

    try:

        # -------------------------
        # Extract Resume Text
        # -------------------------
        resume_text = extract_text_from_pdf(file)

        # -------------------------
        # Job Description
        # -------------------------
        job_description = request.form.get(
            "job_description",
            ""
        )

        # -------------------------
        # Resume Parsing
        # -------------------------
        parsed_resume = parse_resume(
            resume_text
        )

        # -------------------------
        # ATS Engine
        # -------------------------
        ats_result = calculate_ats(
            parsed_resume,
            resume_text
        )

        # -------------------------
        # Keyword Matching
        # -------------------------
        keyword_result = keyword_match(
            parsed_resume,
            job_description
        )

        # -------------------------
        # Gemini AI Review
        # -------------------------
        ai_review = generate_ai_review(
            model=model,
            parsed_resume=parsed_resume,
            ats_result=ats_result,
            keyword_result=keyword_result,
            resume_text=resume_text,
            job_description=job_description
        )

        # -------------------------
        # Return JSON
        # -------------------------
        return jsonify({

            "parsed_resume": parsed_resume,

            "ats": ats_result,

            "keyword_analysis": keyword_result,

            "ai_review": ai_review

        })

    except Exception as e:

        return jsonify({

            "error": str(e)

        }), 500
    
    # -----------------------------
# Health Check
# -----------------------------
@app.route("/health")
def health():

    return jsonify({

        "status": "online",

        "service": "AI Resume Analyzer",

        "version": "2.0 Hybrid ATS + Gemini AI"

    })


# -----------------------------
# Error Handlers
# -----------------------------
@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "error": "Page not found."

    }), 404


@app.errorhandler(413)
def file_too_large(error):

    return jsonify({

        "error": "File size exceeds 16 MB."

    }), 413


@app.errorhandler(500)
def internal_error(error):

    return jsonify({

        "error": "Internal Server Error."

    }), 500


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )