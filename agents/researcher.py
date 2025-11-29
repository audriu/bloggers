"""Researcher Agent - Gathers factual information using Google Search."""

import json
from google import genai
from google.genai import types
from typing import Dict, Any, List
from utils import compact_research_context, format_research_brief
import config


class ResearcherAgent:
    """
    Agent responsible for conducting research on a given topic.
    Equipped with Google Search tool to find real-time information.
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = config.GEMINI_MODEL
        
    def research(self, topic: str, memory) -> Dict[str, Any]:
        """
        Conduct research on the given topic.
        Returns a structured research brief.
        """
        print(f"\n🔍 Researcher Agent: Starting research on '{topic}'...")
        
        # Create research prompt
        prompt = f"""You are a Research Agent specialized in gathering factual, up-to-date information.

Topic: {topic}

Your task:
1. Search for the latest information, trends, and data about this topic
2. Find credible sources and expert opinions
3. Identify key statistics, case studies, and examples
4. Look for different perspectives and angles
5. Compile a comprehensive research brief

Output your findings in a structured format with:
- Overview of the topic
- Key findings (5-7 main points)
- Important statistics or data
- Notable sources and citations
- Interesting angles or perspectives to explore

Be thorough but concise. Focus on factual, verifiable information."""

        try:
            # Use Google Search tool for real-time information
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.3,  # Lower temperature for factual accuracy
                    max_output_tokens=2048,
                )
            )
            
            # Extract findings from response
            findings = ""
            sources = []
            
            for part in response.candidates[0].content.parts:
                if part.text:
                    findings += part.text
            
            # Extract grounding metadata (sources) if available
            if hasattr(response.candidates[0], 'grounding_metadata'):
                grounding = response.candidates[0].grounding_metadata
                if hasattr(grounding, 'search_entry_point'):
                    sources.append("Google Search")
                if hasattr(grounding, 'grounding_chunks'):
                    for chunk in grounding.grounding_chunks[:5]:
                        if hasattr(chunk, 'web'):
                            sources.append(chunk.web.uri if hasattr(chunk.web, 'uri') else "Web Source")
            
            # Compact the context to prevent overflow
            compacted_findings = compact_research_context([findings])
            
            # Format into structured brief
            research_brief = format_research_brief(topic, compacted_findings, sources)
            
            # Store in memory
            memory.store_research(research_brief)
            
            print(f"✅ Research complete! Found {len(sources)} sources.")
            print(f"📝 Key findings: {len(research_brief['key_points'])} points identified.")
            
            return research_brief
            
        except Exception as e:
            print(f"❌ Error during research: {str(e)}")
            # Fallback: Generate research without search
            fallback_brief = self._fallback_research(topic)
            memory.store_research(fallback_brief)
            return fallback_brief
    
    def _fallback_research(self, topic: str) -> Dict[str, Any]:
        """
        Fallback research method without tools (uses model knowledge).
        """
        print("⚠️  Using fallback research (model knowledge only)...")
        
        prompt = f"""Based on your training data, provide a research brief on: {topic}

Include:
- Overview and context
- 5-7 key points
- Important considerations
- Potential angles for a blog article

Be factual and note that this is based on training data, not real-time search."""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=1500,
                )
            )
            
            findings = response.text
            
            return format_research_brief(
                topic,
                findings,
                ["Model Training Data (Pre-2023)"]
            )
            
        except Exception as e:
            print(f"❌ Fallback research failed: {str(e)}")
            return {
                "topic": topic,
                "findings": f"Research on {topic} - please provide manual input",
                "key_points": [],
                "sources": [],
                "timestamp": "2025-11-29"
            }
