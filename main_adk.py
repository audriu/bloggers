#!/usr/bin/env python3
"""
BlogFlow AI - ADK-Based Multi-Agent System
Main orchestration using Google ADK framework with built-in UI support.
"""

import os
import argparse
import sys
from pathlib import Path
from colorama import Fore, Style, init
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Print the application banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              {Fore.YELLOW}BlogFlow AI v2.0{Fore.CYAN}                          ║
║        {Fore.WHITE}Powered by Google ADK Framework{Fore.CYAN}               ║
║        {Fore.WHITE}The Autonomous Content Publishing Team{Fore.CYAN}         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def validate_api_key():
    """Validate that the API key is configured."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{Fore.RED}❌ Error: GOOGLE_API_KEY not configured!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set your API key in the .env file.{Style.RESET_ALL}")
        print(f"1. Copy .env.example to .env (or create .env)")
        print(f"2. Get your API key from: https://aistudio.google.com/app/apikey")
        print(f"3. Add it to the .env file: GOOGLE_API_KEY=your_key_here")
        sys.exit(1)
    return api_key


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    output_dir = os.getenv("OUTPUT_DIR", "output")
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    return output_path


def sanitize_filename(topic: str) -> str:
    """Convert topic to a safe filename."""
    # Remove special characters and replace spaces with hyphens
    safe_name = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in topic)
    safe_name = safe_name.strip().replace(' ', '-').lower()
    # Limit length
    return safe_name[:100]


def format_article_output(content: str, topic: str) -> str:
    """Format the final article with metadata."""
    from datetime import datetime
    
    metadata = f"""---
title: "{topic}"
date: {datetime.now().strftime('%Y-%m-%d')}
generated_by: "BlogFlow AI (Google ADK)"
agent_framework: "Google Agent Development Kit"
---

"""
    return metadata + content


def run_adk_pipeline(topic: str, interactive: bool = False):
    """
    Execute blog generation using ADK's agent orchestration.
    
    Args:
        topic: The blog topic to write about
        interactive: If True, use interactive mode with UI
    """
    print(f"\n{Fore.GREEN}🚀 Starting ADK Multi-Agent Pipeline{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Topic: {topic}{Style.RESET_ALL}\n")
    
    try:
        # Import the root agent from agent.py
        from agent import root_agent
        from google.adk.runners import App
        
        # Create app with the agent
        app = App(
            name="blogflow_ai",
            root_agent=root_agent
        )
        
        # Create session service
        session_service = InMemorySessionService()
        
        # Create an ADK runner with the app
        runner = Runner(
            app=app,
            session_service=session_service
        )
        
        # Prepare the user message
        user_prompt = f"""Create a complete, ready-to-publish blog article on the following topic: {topic}

Follow this workflow:
1. Research the topic thoroughly using Google Search
2. Create an engaging, well-structured draft (1200-1800 words)
3. Review the draft for quality (score must be 7.0+)
4. If quality is below threshold, revise based on feedback (max 3 iterations)
5. Optimize the approved draft for SEO
6. Return the final article in markdown format

Requirements:
- Professional yet conversational tone
- Clear structure with headers (##, ###)
- Include specific examples and actionable insights
- Cite sources naturally
- SEO-optimized but naturally readable
- Meta title and description included at the end

Begin the workflow now."""
        
        print(f"{Fore.CYAN}{'='*60}")
        print(f"RUNNING MULTI-AGENT WORKFLOW")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        # Create user message as Content
        user_message = types.Content(
            role='user',
            parts=[types.Part.from_text(text=user_prompt)]
        )
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        user_id = "default_user"
        
        # Run the agent
        print(f"{Fore.CYAN}⚙️  Agents working... (this may take 1-2 minutes){Style.RESET_ALL}\n")
        
        # Collect all events
        final_content = ""
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
            if interactive and hasattr(event, 'content'):
                # In interactive mode, show agent communication
                print(f"{Fore.YELLOW}[Event: {event.__class__.__name__}]{Style.RESET_ALL}")
            
            # Collect content from appropriate event types
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            final_content += part.text
        
        # Save the output
        print(f"\n\n{Fore.CYAN}{'='*60}")
        print(f"SAVING OUTPUT")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        output_dir = ensure_output_directory()
        filename = sanitize_filename(topic) + ".md"
        output_path = output_dir / filename
        
        # Format and save
        formatted_article = format_article_output(final_content, topic)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_article)
        
        # Print success message
        print(f"{Fore.GREEN}✅ Blog article generation complete!{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}📄 Article saved to: {Fore.CYAN}{output_path}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}📊 Statistics:{Style.RESET_ALL}")
        word_count = len(final_content.split())
        print(f"   • Word Count: {word_count} words")
        print(f"   • Output File: {filename}")
        
        return output_path
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Pipeline failed: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def start_adk_ui():
    """Start the ADK web UI for interactive agent development."""
    print(f"\n{Fore.CYAN}🌐 Starting ADK Web UI...{Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}The ADK UI provides:{Style.RESET_ALL}")
    print(f"  • Interactive chat interface")
    print(f"  • Agent execution visualization")
    print(f"  • Function call monitoring")
    print(f"  • Session management")
    print(f"\n{Fore.YELLOW}Access the UI at: {Fore.CYAN}http://localhost:8000{Style.RESET_ALL}\n")
    print(f"{Fore.WHITE}Press Ctrl+C to stop the server{Style.RESET_ALL}\n")
    
    try:
        # Start ADK web server
        os.system("adk web --port 8000")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Shutting down ADK UI...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start UI: {str(e)}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Make sure ADK is properly installed:{Style.RESET_ALL}")
        print(f"  pip install google-adk")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='BlogFlow AI - ADK-powered multi-agent blog generation system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a blog article
  python main.py --topic "Future of AI Agents"
  
  # Generate with interactive mode (see agent communication)
  python main.py --topic "Machine Learning Best Practices" --interactive
  
  # Start the ADK Web UI for development
  python main.py --ui
  
  # Quick generation
  python main.py -t "Python vs Rust" -q
        """
    )
    
    parser.add_argument(
        '--topic', '-t',
        help='The topic for the blog article'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode with visible agent communication'
    )
    
    parser.add_argument(
        '--ui',
        action='store_true',
        help='Start the ADK Web UI for interactive agent development'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output mode'
    )
    
    args = parser.parse_args()
    
    # Print banner (unless quiet mode)
    if not args.quiet:
        print_banner()
    
    # Validate configuration
    validate_api_key()
    
    # Handle UI mode
    if args.ui:
        start_adk_ui()
        return
    
    # Require topic for generation mode
    if not args.topic:
        print(f"{Fore.RED}❌ Error: --topic is required for article generation{Style.RESET_ALL}")
        print(f"\nUse --ui to start the interactive UI, or provide a --topic to generate an article.")
        print(f"Run with --help for more information.")
        sys.exit(1)
    
    # Run the pipeline
    output_path = run_adk_pipeline(args.topic, interactive=args.interactive)
    
    if not args.quiet:
        print(f"\n{Fore.GREEN}🎉 Success! Your article is ready.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}View it with: cat {output_path}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
