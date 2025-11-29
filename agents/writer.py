"""Writer Agent - Creates engaging content from research briefs."""

from google import genai
from google.genai import types
from typing import Dict, Any
import config


class WriterAgent:
    """
    Agent responsible for drafting blog content.
    Focuses on narrative flow and engagement without worrying about SEO.
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = config.GEMINI_MODEL
        
    def write_draft(self, memory, editor_feedback: Dict[str, Any] = None) -> str:
        """
        Write or revise a blog post based on research and optional editor feedback.
        """
        research = memory.get_research()
        style_guide = memory.style_guide
        
        if editor_feedback:
            print(f"\n✍️  Writer Agent: Revising draft based on editor feedback...")
            return self._revise_draft(memory, editor_feedback, style_guide)
        else:
            print(f"\n✍️  Writer Agent: Creating initial draft on '{research.get('topic', 'Unknown')}'...")
            return self._create_initial_draft(research, style_guide)
    
    def _create_initial_draft(self, research: Dict[str, Any], style_guide: str) -> str:
        """Create the first draft from research."""
        
        topic = research.get('topic', 'Unknown Topic')
        findings = research.get('findings', '')
        key_points = research.get('key_points', [])
        sources = research.get('sources', [])
        
        prompt = f"""You are a Writer Agent creating a high-quality blog article.

TOPIC: {topic}

RESEARCH BRIEF:
{findings}

KEY POINTS TO COVER:
{chr(10).join(f"- {point}" for point in key_points)}

SOURCES:
{chr(10).join(f"- {source}" for source in sources)}

STYLE GUIDE:
{style_guide}

Your task:
1. Write a compelling, engaging blog article on this topic
2. Start with a strong hook that captures attention
3. Organize content with clear headers (use ## for H2, ### for H3)
4. Use natural, conversational tone while maintaining professionalism
5. Include specific examples and actionable insights
6. Cite sources naturally within the text
7. End with a thought-provoking conclusion
8. DO NOT artificially stuff keywords - write naturally

Target: 1200-1800 words

Focus purely on creating excellent, readable content. SEO optimization will be handled later."""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,  # Higher temperature for creativity
                    max_output_tokens=3000,
                )
            )
            
            draft = response.text
            print(f"✅ Initial draft complete! (~{len(draft.split())} words)")
            return draft
            
        except Exception as e:
            print(f"❌ Error creating draft: {str(e)}")
            return f"# {topic}\n\n[Draft generation failed: {str(e)}]"
    
    def _revise_draft(self, memory, feedback: Dict[str, Any], style_guide: str) -> str:
        """Revise the draft based on editor feedback."""
        
        current_draft = memory.get_latest_draft()
        research = memory.get_research()
        
        issues = feedback.get('issues', [])
        suggestions = feedback.get('suggestions', [])
        score = feedback.get('score', 0)
        
        prompt = f"""You are a Writer Agent revising your blog article based on editor feedback.

ORIGINAL DRAFT:
{current_draft}

EDITOR FEEDBACK:
Quality Score: {score}/10

Issues Found:
{chr(10).join(f"- {issue}" for issue in issues)}

Suggestions:
{chr(10).join(f"- {suggestion}" for suggestion in suggestions)}

RESEARCH DATA (for reference):
{research.get('findings', '')}

STYLE GUIDE:
{style_guide}

Your task:
1. Address ALL issues mentioned by the editor
2. Implement the suggestions while maintaining your voice
3. Improve clarity, accuracy, and engagement
4. Keep the article structure intact unless changes are needed
5. Ensure all facts are accurate and properly cited
6. Maintain natural, readable prose

Revise the article to achieve a quality score above {config.QUALITY_THRESHOLD}."""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=3000,
                )
            )
            
            revised_draft = response.text
            print(f"✅ Revision complete! (~{len(revised_draft.split())} words)")
            return revised_draft
            
        except Exception as e:
            print(f"❌ Error revising draft: {str(e)}")
            return current_draft  # Return original if revision fails
