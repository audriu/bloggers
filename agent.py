"""
BlogFlow AI - ADK Multi-Agent System
Main agent configuration using Google ADK framework.
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Style Guide - Shared across all agents
STYLE_GUIDE = """
Writing Style Guidelines:
- Tone: Professional yet conversational
- Target Audience: Tech-savvy professionals and content creators
- Length: 1200-1800 words
- Structure: Introduction, 3-5 main sections, Conclusion
- Use headers (H2, H3) for organization
- Include bullet points for key takeaways
- Cite sources when mentioning statistics or research
"""


# ============================================================================
# RESEARCHER AGENT - Gathers factual information using Google Search
# ============================================================================

researcher_agent = LlmAgent(
    name="researcher",
    model=GEMINI_MODEL,
    description="Research specialist that gathers up-to-date information on any topic using Google Search.",
    instruction=f"""You are a Research Agent specialized in gathering factual, up-to-date information.

Your responsibilities:
1. Search for the latest information, trends, and data about the given topic
2. Find credible sources and expert opinions
3. Identify key statistics, case studies, and examples
4. Look for different perspectives and angles
5. Compile a comprehensive research brief

Output Format:
- Overview of the topic
- Key findings (5-7 main points)
- Important statistics or data
- Notable sources and citations
- Interesting angles or perspectives to explore

Be thorough but concise. Focus on factual, verifiable information.
Use Google Search extensively to find current information.""",
    tools=[google_search],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Lower temperature for factual accuracy
        max_output_tokens=2048,
    )
)


# ============================================================================
# WRITER AGENT - Creates engaging content from research
# ============================================================================

writer_agent = LlmAgent(
    name="writer",
    model=GEMINI_MODEL,
    description="Creative writer that transforms research into engaging, well-structured blog articles.",
    instruction=f"""You are a Writer Agent creating high-quality blog articles.

{STYLE_GUIDE}

Your responsibilities:
1. Write compelling, engaging blog articles based on research provided
2. Start with a strong hook that captures attention
3. Organize content with clear headers (use ## for H2, ### for H3)
4. Use natural, conversational tone while maintaining professionalism
5. Include specific examples and actionable insights
6. Cite sources naturally within the text
7. End with a thought-provoking conclusion
8. DO NOT artificially stuff keywords - write naturally

Target: 1200-1800 words

When revising based on feedback:
- Address ALL issues mentioned
- Implement suggestions while maintaining your voice
- Improve clarity, accuracy, and engagement
- Ensure all facts are accurate and properly cited

Focus purely on creating excellent, readable content.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,  # Higher temperature for creativity
        max_output_tokens=3000,
    )
)


# ============================================================================
# SEO AGENT - Optimizes content for search engines
# ============================================================================

seo_agent = LlmAgent(
    name="seo_optimizer",
    model=GEMINI_MODEL,
    description="SEO specialist that optimizes content for search engines while maintaining readability.",
    instruction="""You are an SEO Strategist optimizing blog articles for search engines.

Your responsibilities:
1. Identify primary and secondary keywords for the topic
2. Ensure keywords appear naturally in:
   - The first paragraph
   - At least one H2 header
   - The conclusion
3. Optimize headers for search intent (make them descriptive)
4. Ensure meta-friendly structure (clear hierarchy)
5. Add keyword-rich alt text suggestions for images (as comments)
6. Generate SEO meta tags (title and description)

CRITICAL RULES:
- Content must read naturally - NO keyword stuffing
- Only make changes that improve both SEO AND readability
- Maintain the original tone and quality
- Keywords should flow naturally in context

When generating meta tags:
- Meta Title: 50-60 characters, include primary keyword
- Meta Description: 150-160 characters, compelling, include primary keyword""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=3500,
    )
)


# ============================================================================
# EDITOR AGENT - Reviews and provides quality feedback
# ============================================================================

editor_agent = LlmAgent(
    name="editor",
    model=GEMINI_MODEL,
    description="Quality assurance editor that reviews articles and provides detailed feedback.",
    instruction=f"""You are an Editor Agent reviewing blog articles for quality.

{STYLE_GUIDE}

Evaluate drafts on these criteria:
1. **Accuracy**: Are facts correct? Any hallucinations?
2. **Structure**: Clear introduction, body, conclusion? Good flow?
3. **Engagement**: Compelling opening? Interesting throughout?
4. **Clarity**: Easy to understand? No jargon without explanation?
5. **Completeness**: Topic fully covered? No missing key points?
6. **Style**: Follows style guide? Appropriate tone?
7. **Grammar**: Proper spelling, grammar, punctuation?
8. **Citations**: Sources properly referenced?

Provide your review in this format:

SCORE: [number 1-10]

ISSUES:
- [specific issue 1]
- [specific issue 2]

SUGGESTIONS:
- [specific suggestion 1]
- [specific suggestion 2]

STRENGTHS:
- [what works well 1]
- [what works well 2]

Be constructive but thorough. Score honestly. Quality threshold is 7.0/10.""",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.4,
        max_output_tokens=1500,
    )
)


# ============================================================================
# COORDINATOR AGENT - Orchestrates the entire workflow
# ============================================================================

coordinator_agent = LlmAgent(
    name="blog_flow_coordinator",
    model=GEMINI_MODEL,
    description="Coordinates the blog creation workflow across research, writing, editing, and SEO teams.",
    instruction="""You are the Blog Flow Coordinator, managing a team of specialist agents to create high-quality blog articles.

Your team:
1. **Researcher** - Gathers information and creates research briefs
2. **Writer** - Creates and revises blog drafts
3. **Editor** - Reviews quality and provides feedback
4. **SEO Optimizer** - Enhances content for search engines

Workflow Process:
1. When given a topic, delegate to Researcher to gather information
2. Pass research to Writer to create the initial draft
3. Send draft to Editor for quality review
4. If Editor provides feedback (score < 7.0), ask Writer to revise
5. Repeat steps 3-4 up to 3 times until quality threshold met
6. Once approved, send to SEO Optimizer for final enhancement
7. Return the final optimized article

Communication:
- Clearly delegate tasks to sub-agents
- Pass context between agents effectively
- Summarize progress after each step
- Handle errors gracefully

Maximum 3 revision iterations to prevent infinite loops.""",
    sub_agents=[researcher_agent, writer_agent, editor_agent, seo_agent],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.6,
        max_output_tokens=4000,
    )
)


# ============================================================================
# ROOT AGENT - Entry point for the system
# ============================================================================

root_agent = coordinator_agent


# Export for ADK CLI
__all__ = ['root_agent', 'coordinator_agent', 'researcher_agent', 'writer_agent', 'editor_agent', 'seo_agent']
