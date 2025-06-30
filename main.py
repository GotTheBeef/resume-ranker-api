from fastapi import FastAPI
from pydantic import BaseModel
import string

# Initialize FastAPI app
app = FastAPI()

# Test endpoint to confirm the API is running
@app.get("/")
async def root():
    return {"message": "Resume Ranker API is running 🚀"}

# Define a Pydantic model for request validation and documentation generation
class ResumeRequest(BaseModel):
    resume: str  # The resume text
    job: str     # The job description text

# Endpoint to rank the resume against the job description
@app.post("/rank_resume")
async def rank_resume(data: ResumeRequest):
    # Convert input text to lowercase for consistent comparison
    resume = data.resume.lower()
    job = data.job.lower()

    # Set of common stop words to exclude from keyword analysis
    stop_words = {
        "a", "an", "and", "the", "with", "for", "in", "of", "to",
        "on", "at", "by", "from", "is", "are", "was", "were",
        "be", "being", "been", "or"
    }

    # Remove punctuation from both resume and job description
    translator = str.maketrans("", "", string.punctuation)
    job_clean = job.translate(translator)
    resume_clean = resume.translate(translator)

    # Split job description into words, remove trailing 's' for basic plural handling, and filter out stop words
    raw_keywords = job_clean.split()
    keywords = list(set([
        word.rstrip('s') for word in raw_keywords
        if word not in stop_words
    ]))

    # Do the same cleaning for resume text and store words in a set for faster lookup
    resume_words = set([
        word.rstrip('s') for word in resume_clean.split()
    ])

    # Determine which keywords are found and which are missing
    found_keywords = [kw for kw in keywords if kw in resume_words]
    missing_keywords = [kw for kw in keywords if kw not in resume_words]

    # Calculate the matching score as a percentage
    score = round((len(found_keywords) / len(keywords)) * 100, 2) if keywords else 0

    # Generate actionable feedback for the user
    feedback = (
        f"✅ Found {len(found_keywords)} of {len(keywords)} important keywords.\n"
        f"❌ Missing important keywords: {', '.join(missing_keywords[:10])}.\n"
        "Consider adding these skills or experiences if relevant to improve your match."
    )

    # Return a structured JSON response for frontend or API consumers
    return {
        "score": score,
        "feedback": feedback,
        "found_keywords": found_keywords,
        "missing_keywords": missing_keywords,
        "resume_excerpt": resume[:50],  # Preview of resume for context
        "job_excerpt": job[:50]         # Preview of job description for context
    }