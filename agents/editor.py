"""Editor Agent - Reviews and provides feedback with quality loop."""

from google import genai
from google.genai import types
from typing import Dict, Any, List, Tuple
import config
from utils import calculate_quality_score


class EditorAgent:
    """
    Agent responsible for reviewing drafts and ensuring quality.
    Implements a feedback loop to iterate with the Writer until quality threshold is met.
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = config.GEMINI_MODEL
        
    def review(self, draft: str, memory) -> Tuple[bool, Dict[str, Any]]:
        """
        Review the draft and determine if it meets quality standards.
        
        Returns:
            (approved: bool, feedback: dict)
        """
        iteration = memory.get_feedback_count() + 1
        print(f"\n📋 Editor Agent: Reviewing draft (Iteration {iteration})...")
        
        # Calculate basic quality score
        basic_score = calculate_quality_score(draft)
        
        # Get detailed AI review
        detailed_feedback = self._detailed_review(draft, memory)
        
        # Combine scores
        ai_score = detailed_feedback.get('score', 5.0)
        final_score = (basic_score + ai_score) / 2
        
        detailed_feedback['score'] = final_score
        detailed_feedback['iteration'] = iteration
        
        # Store feedback
        memory.add_editor_feedback(detailed_feedback)
        
        # Check if approved
        approved = final_score >= config.QUALITY_THRESHOLD
        
        print(f"📊 Quality Score: {final_score:.1f}/10")
        
        if approved:
            print(f"✅ Draft APPROVED! Quality threshold met.")
        else:
            print(f"⚠️  Draft needs revision. {len(detailed_feedback.get('issues', []))} issues found.")
            if iteration >= config.MAX_EDITOR_ITERATIONS:
                print(f"⚠️  Maximum iterations reached. Using current draft.")
                approved = True  # Force approval to prevent infinite loop
        
        return approved, detailed_feedback
    
    def _detailed_review(self, draft: str, memory) -> Dict[str, Any]:
        """Perform detailed AI-powered review."""
        
        research = memory.get_research()
        style_guide = memory.style_guide
        
        prompt = f"""You are an Editor Agent reviewing a blog article for quality.

DRAFT TO REVIEW:
{draft}

RESEARCH BRIEF (for fact-checking):
{research.get('findings', '')[:1000]}

STYLE GUIDE:
{style_guide}

Evaluate the draft on these criteria:
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
- [etc]

SUGGESTIONS:
- [specific suggestion 1]
- [specific suggestion 2]
- [etc]

STRENGTHS:
- [what works well 1]
- [what works well 2]

Be constructive but thorough. If there are no issues, say so."""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=1500,
                )
            )
            
            review_text = response.text
            
            # Parse the review
            feedback = self._parse_review(review_text)
            
            return feedback
            
        except Exception as e:
            print(f"❌ Detailed review failed: {str(e)}")
            return {
                "score": 6.0,
                "issues": [f"Review error: {str(e)}"],
                "suggestions": ["Manual review recommended"],
                "strengths": []
            }
    
    def _parse_review(self, review_text: str) -> Dict[str, Any]:
        """Parse the structured review response."""
        
        feedback = {
            "score": 5.0,
            "issues": [],
            "suggestions": [],
            "strengths": []
        }
        
        lines = review_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('SCORE:'):
                try:
                    score_text = line.replace('SCORE:', '').strip()
                    # Extract first number found
                    import re
                    match = re.search(r'\d+\.?\d*', score_text)
                    if match:
                        feedback['score'] = float(match.group())
                except:
                    pass
            elif line == 'ISSUES:':
                current_section = 'issues'
            elif line == 'SUGGESTIONS:':
                current_section = 'suggestions'
            elif line == 'STRENGTHS:':
                current_section = 'strengths'
            elif line.startswith('- ') and current_section:
                item = line[2:].strip()
                if item:
                    feedback[current_section].append(item)
        
        return feedback
    
    def generate_final_report(self, memory) -> str:
        """Generate a summary report of the editing process."""
        
        iterations = memory.get_feedback_count()
        final_feedback = memory.get_latest_feedback()
        
        report = f"""
=== EDITORIAL REVIEW REPORT ===

Total Iterations: {iterations}
Final Quality Score: {final_feedback.get('score', 0):.1f}/10
Status: {'APPROVED' if final_feedback.get('score', 0) >= config.QUALITY_THRESHOLD else 'NEEDS WORK'}

Strengths:
{chr(10).join(f"  ✓ {s}" for s in final_feedback.get('strengths', ['N/A']))}

Final State:
  • Word Count: ~{len(memory.get_latest_draft().split())} words
  • Structure: {'✓' if '##' in memory.get_latest_draft() else '✗'}
  • SEO Optimized: {'✓' if memory.get_seo_data() else '✗'}

==================================
"""
        return report
