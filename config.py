"""Configuration settings for BlogFlow AI."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Agent Configuration
MAX_EDITOR_ITERATIONS = 3
QUALITY_THRESHOLD = 7.0  # Minimum quality score (out of 10)
MAX_RESEARCH_RESULTS = 10

# Output Configuration
OUTPUT_DIR = "output"

# Style Guide (Shared Memory)
DEFAULT_STYLE_GUIDE = """
Writing Style Guidelines:
- Tone: Professional yet conversational
- Target Audience: Tech-savvy professionals and content creators
- Length: 1200-1800 words
- Structure: Introduction, 3-5 main sections, Conclusion
- Use headers (H2, H3) for organization
- Include bullet points for key takeaways
- Cite sources when mentioning statistics or research
"""
