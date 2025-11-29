#!/usr/bin/env python3
"""
BlogFlow AI - The Autonomous Content Publishing Team
Main orchestration script for multi-agent blog generation.
"""

import os
import argparse
import sys
from pathlib import Path
from colorama import Fore, Style, init

# Import configuration and agents
import config
from memory import MemoryBank
from agents import ResearcherAgent, WriterAgent, SEOAgent, EditorAgent
from utils import format_output_article, sanitize_filename


# Initialize colorama for colored terminal output
init(autoreset=True)


def print_banner():
    """Print the application banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              {Fore.YELLOW}BlogFlow AI{Fore.CYAN}                               ║
║        {Fore.WHITE}The Autonomous Content Publishing Team{Fore.CYAN}         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def validate_api_key():
    """Validate that the API key is configured."""
    if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "your_api_key_here":
        print(f"{Fore.RED}❌ Error: GOOGLE_API_KEY not configured!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please set your API key in the .env file.{Style.RESET_ALL}")
        print(f"1. Copy .env.example to .env")
        print(f"2. Get your API key from: https://aistudio.google.com/app/apikey")
        print(f"3. Add it to the .env file")
        sys.exit(1)


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    output_path = Path(config.OUTPUT_DIR)
    output_path.mkdir(exist_ok=True)
    return output_path


def run_blog_pipeline(topic: str, style_guide: str = None):
    """
    Execute the complete blog generation pipeline.
    
    Pipeline stages:
    1. Researcher gathers information
    2. Writer creates initial draft
    3. SEO Agent optimizes content
    4. Editor reviews (with loop back to Writer if needed)
    5. Final article saved to file
    """
    print(f"\n{Fore.GREEN}🚀 Starting BlogFlow AI Pipeline{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Topic: {topic}{Style.RESET_ALL}\n")
    
    # Initialize memory bank
    memory = MemoryBank(style_guide or config.DEFAULT_STYLE_GUIDE)
    
    # Initialize agents
    researcher = ResearcherAgent(config.GOOGLE_API_KEY)
    writer = WriterAgent(config.GOOGLE_API_KEY)
    seo_agent = SEOAgent(config.GOOGLE_API_KEY)
    editor = EditorAgent(config.GOOGLE_API_KEY)
    
    try:
        # Stage 1: Research
        print(f"{Fore.CYAN}{'='*60}")
        print(f"STAGE 1: RESEARCH")
        print(f"{'='*60}{Style.RESET_ALL}")
        research_brief = researcher.research(topic, memory)
        
        # Stage 2: Initial Writing
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"STAGE 2: WRITING")
        print(f"{'='*60}{Style.RESET_ALL}")
        initial_draft = writer.write_draft(memory)
        memory.add_draft(initial_draft)
        
        # Stage 3: SEO Optimization
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"STAGE 3: SEO OPTIMIZATION")
        print(f"{'='*60}{Style.RESET_ALL}")
        optimized_draft = seo_agent.optimize(initial_draft, topic, memory)
        memory.add_draft(optimized_draft)
        
        # Stage 4: Editorial Review (with loop)
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"STAGE 4: EDITORIAL REVIEW")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        approved = False
        iteration = 0
        
        while not approved and iteration < config.MAX_EDITOR_ITERATIONS:
            iteration += 1
            current_draft = memory.get_latest_draft()
            
            # Editor reviews
            approved, feedback = editor.review(current_draft, memory)
            
            if not approved:
                # Writer revises based on feedback
                print(f"\n{Fore.YELLOW}↩️  Sending back to Writer for revision...{Style.RESET_ALL}")
                revised_draft = writer.write_draft(memory, editor_feedback=feedback)
                memory.add_draft(revised_draft)
        
        # Final Stage: Save Output
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"STAGE 5: FINAL OUTPUT")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        final_draft = memory.get_latest_draft()
        seo_data = memory.get_seo_data()
        
        # Generate meta tags
        meta_tags = seo_agent.generate_meta_tags(
            final_draft,
            seo_data.get('keywords', []),
            topic
        )
        
        # Format article with metadata
        metadata = {
            'title': meta_tags.get('title', topic),
            'date': '2025-11-29',
            'keywords': seo_data.get('keywords', []),
            'sources': research_brief.get('sources', [])
        }
        
        final_article = format_output_article(final_draft, metadata)
        
        # Save to file
        output_dir = ensure_output_directory()
        filename = sanitize_filename(topic) + ".md"
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_article)
        
        # Print summary
        print(f"\n{Fore.GREEN}✅ Blog article generation complete!{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}📄 Article saved to: {Fore.CYAN}{output_path}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}📊 Statistics:{Style.RESET_ALL}")
        print(f"   • Word Count: {len(final_draft.split())} words")
        print(f"   • Draft Iterations: {len(memory.get_all_drafts())}")
        print(f"   • Editor Reviews: {memory.get_feedback_count()}")
        print(f"   • Quality Score: {memory.get_latest_feedback().get('score', 0):.1f}/10")
        print(f"   • Keywords: {len(seo_data.get('keywords', []))}")
        
        # Print editorial report
        print(f"\n{Fore.YELLOW}{editor.generate_final_report(memory)}{Style.RESET_ALL}")
        
        return output_path
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Pipeline failed: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='BlogFlow AI - Generate high-quality blog articles using AI agents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "Future of AI Agents"
  python main.py --topic "Machine Learning Best Practices" --style custom_style.txt
  python main.py -t "Python vs Rust" -v
        """
    )
    
    parser.add_argument(
        '--topic', '-t',
        required=True,
        help='The topic for the blog article'
    )
    
    parser.add_argument(
        '--style',
        help='Path to custom style guide file (optional)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Validate configuration
    validate_api_key()
    
    # Load custom style guide if provided
    style_guide = None
    if args.style:
        style_path = Path(args.style)
        if style_path.exists():
            with open(style_path, 'r', encoding='utf-8') as f:
                style_guide = f.read()
            print(f"{Fore.GREEN}✓ Loaded custom style guide from {args.style}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Style guide file not found, using default{Style.RESET_ALL}")
    
    # Run the pipeline
    output_path = run_blog_pipeline(args.topic, style_guide)
    
    print(f"\n{Fore.GREEN}🎉 Success! Your article is ready.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Open it with: cat {output_path}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
