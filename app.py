# app.py
from flask import Flask, render_template, request, jsonify
from modes import run_hr_mode, run_student_mode, run_gap_mode
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text(file_path):
    ext = file_path.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f, strict=False)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise ValueError(f"PDF read error: {e}")
        return text.strip()
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()

def save_file(uploaded_file, name_prefix, index=""):
    ext = uploaded_file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{name_prefix}{index}.{ext}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(path)
    return path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    mode = request.form.get("mode")

    if mode == "hr":
        jd_file = request.files.get("jd")
        resumes = request.files.getlist("resumes")
        if not jd_file or not resumes:
            return jsonify({"error": "JD aur resumes dono chahiye!"}), 400

        jd_path = save_file(jd_file, "jd")
        jd_text = extract_text(jd_path)

        resume_texts = []
        for i, f in enumerate(resumes):
            rp = save_file(f, "resume_", i)
            resume_texts.append(extract_text(rp))

        result = run_hr_mode(jd_text, resume_texts)
        return jsonify({"mode": "hr", "results": result})

    elif mode == "student":
        resume_file = request.files.get("resume")
        jds = request.files.getlist("jds")
        if not resume_file or not jds:
            return jsonify({"error": "Resume aur JDs dono chahiye!"}), 400

        resume_path = save_file(resume_file, "resume")
        resume_text = extract_text(resume_path)

        jd_texts = []
        for i, f in enumerate(jds):
            jp = save_file(f, "jd_", i)
            jd_texts.append(extract_text(jp))

        result = run_student_mode(resume_text, jd_texts)
        return jsonify({"mode": "student", "results": result})

    elif mode == "gap":
        resume_file = request.files.get("resume")
        jd_file = request.files.get("jd")
        if not resume_file or not jd_file:
            return jsonify({"error": "Resume aur JD dono chahiye!"}), 400

        resume_path = save_file(resume_file, "resume")
        jd_path = save_file(jd_file, "jd")

        resume_text = extract_text(resume_path)
        jd_text = extract_text(jd_path)

        result = run_gap_mode(resume_text, jd_text)
        return jsonify({"mode": "gap", "result": result})

    else:
        return jsonify({"error": "Invalid mode!"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)