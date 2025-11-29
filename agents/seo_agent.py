"""SEO Strategist Agent - Optimizes content for search engines."""

from google import genai
from google.genai import types
from typing import Dict, Any, List
import config


class SEOAgent:
    """
    Agent responsible for SEO optimization.
    Analyzes draft and adds keywords, meta-tags, and structural improvements.
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = config.GEMINI_MODEL
        
    def optimize(self, draft: str, topic: str, memory) -> str:
        """
        Optimize the draft for SEO without compromising readability.
        """
        print(f"\n🎯 SEO Agent: Optimizing content for search engines...")
        
        # First, analyze and identify keywords
        keywords = self._identify_keywords(topic, draft)
        
        # Then optimize the content
        optimized_draft = self._optimize_content(draft, keywords, topic)
        
        # Store SEO data
        seo_data = {
            "keywords": keywords,
            "topic": topic,
            "optimized": True
        }
        memory.store_seo_data(seo_data)
        
        print(f"✅ SEO optimization complete!")
        print(f"🔑 Target keywords: {', '.join(keywords[:5])}")
        
        return optimized_draft
    
    def _identify_keywords(self, topic: str, draft: str) -> List[str]:
        """Identify relevant keywords for the topic."""
        
        prompt = f"""You are an SEO expert. Analyze this topic and draft to identify the most important keywords.

TOPIC: {topic}

DRAFT (first 500 chars):
{draft[:500]}

Identify:
1. Primary keyword (the main focus)
2. 5-8 secondary keywords (related terms)
3. 3-5 long-tail keywords (specific phrases users might search)

Return ONLY a comma-separated list of keywords, starting with the primary keyword.
Example: "AI agents, artificial intelligence, automation, agent systems, multi-agent architecture"
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=200,
                )
            )
            
            keywords_text = response.text.strip()
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            return keywords[:10]  # Limit to top 10
            
        except Exception as e:
            print(f"⚠️  Keyword identification failed: {str(e)}")
            # Fallback: extract from topic
            return [topic.lower(), "blog", "guide", "tutorial"]
    
    def _optimize_content(self, draft: str, keywords: List[str], topic: str) -> str:
        """Optimize content structure and keyword placement."""
        
        prompt = f"""You are an SEO Strategist optimizing a blog article.

DRAFT:
{draft}

TARGET KEYWORDS (in priority order):
{chr(10).join(f"{i+1}. {kw}" for i, kw in enumerate(keywords))}

Your task:
1. Ensure the primary keyword appears in:
   - The first paragraph (H1 or opening)
   - At least one H2 header
   - The conclusion
2. Naturally incorporate secondary keywords throughout
3. Optimize headers for search intent (make them descriptive)
4. Ensure meta-friendly structure (clear hierarchy)
5. Add keyword-rich alt text suggestions for images (as comments)
6. Keep the content natural and readable - NO keyword stuffing
7. Maintain the original tone and quality

CRITICAL: The content must read naturally. Only make changes that improve both SEO AND readability.

Return the optimized draft."""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=3500,
                )
            )
            
            optimized = response.text
            return optimized
            
        except Exception as e:
            print(f"❌ Content optimization failed: {str(e)}")
            return draft  # Return original if optimization fails
    
    def generate_meta_tags(self, draft: str, keywords: List[str], topic: str) -> Dict[str, str]:
        """Generate meta title and description."""
        
        prompt = f"""Generate SEO meta tags for this article.

TOPIC: {topic}
PRIMARY KEYWORD: {keywords[0] if keywords else topic}

ARTICLE (first 300 chars):
{draft[:300]}

Generate:
1. Meta Title (50-60 characters, include primary keyword)
2. Meta Description (150-160 characters, compelling, include primary keyword)

Return in format:
TITLE: [your title]
DESCRIPTION: [your description]"""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=200,
                )
            )
            
            result = response.text
            
            # Parse response
            lines = result.split('\n')
            meta_data = {"title": topic, "description": ""}
            
            for line in lines:
                if line.startswith("TITLE:"):
                    meta_data["title"] = line.replace("TITLE:", "").strip()
                elif line.startswith("DESCRIPTION:"):
                    meta_data["description"] = line.replace("DESCRIPTION:", "").strip()
            
            return meta_data
            
        except Exception as e:
            print(f"⚠️  Meta tag generation failed: {str(e)}")
            return {
                "title": topic,
                "description": f"Learn about {topic} in this comprehensive guide."
            }
