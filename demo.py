#!/usr/bin/env python3
"""
Demo script to test BlogFlow AI with a sample topic.
Run this to verify your installation is working correctly.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from colorama import Fore, Style, init
import config

init(autoreset=True)


def check_dependencies():
    """Check if all required dependencies are installed."""
    print(f"{Fore.CYAN}Checking dependencies...{Style.RESET_ALL}")
    
    missing = []
    
    try:
        import google.genai
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} google-genai")
    except ImportError:
        missing.append("google-genai")
        print(f"{Fore.RED}✗{Style.RESET_ALL} google-genai")
    
    try:
        from dotenv import load_dotenv
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} python-dotenv")
    except ImportError:
        missing.append("python-dotenv")
        print(f"{Fore.RED}✗{Style.RESET_ALL} python-dotenv")
    
    try:
        import colorama
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} colorama")
    except ImportError:
        missing.append("colorama")
        print(f"{Fore.RED}✗{Style.RESET_ALL} colorama")
    
    if missing:
        print(f"\n{Fore.RED}Missing dependencies: {', '.join(missing)}{Style.RESET_ALL}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print(f"{Fore.GREEN}✓ All dependencies installed{Style.RESET_ALL}\n")
    return True


def check_api_key():
    """Check if API key is configured."""
    print(f"{Fore.CYAN}Checking API key...{Style.RESET_ALL}")
    
    if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "your_api_key_here":
        print(f"{Fore.RED}✗ API key not configured{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Setup Instructions:{Style.RESET_ALL}")
        print(f"1. Copy .env.example to .env")
        print(f"2. Get API key from: https://aistudio.google.com/app/apikey")
        print(f"3. Add it to .env file")
        return False
    
    print(f"{Fore.GREEN}✓ API key configured{Style.RESET_ALL}\n")
    return True


def check_output_directory():
    """Check if output directory exists."""
    print(f"{Fore.CYAN}Checking output directory...{Style.RESET_ALL}")
    
    output_path = Path(config.OUTPUT_DIR)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"{Fore.YELLOW}⚠ Created output directory: {output_path}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.GREEN}✓ Output directory exists: {output_path}{Style.RESET_ALL}\n")
    
    return True


def run_demo():
    """Run a demo generation."""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"Running Demo Generation")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Demo Topic: 'The Benefits of Multi-Agent AI Systems'{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This will take about 2-3 minutes...{Style.RESET_ALL}\n")
    
    # Import and run main pipeline
    from main import run_blog_pipeline
    
    try:
        output_path = run_blog_pipeline(
            topic="The Benefits of Multi-Agent AI Systems",
            style_guide=config.DEFAULT_STYLE_GUIDE
        )
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"Demo Complete!")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}Your demo article is ready:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{output_path}{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}View it with:{Style.RESET_ALL}")
        print(f"  cat {output_path}")
        print(f"  code {output_path}")
        
        return True
        
    except Exception as e:
        print(f"\n{Fore.RED}Demo failed: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main demo script."""
    print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              BlogFlow AI - Demo Script                  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    print(f"{Fore.WHITE}This script will:{Style.RESET_ALL}")
    print(f"  1. Check if all dependencies are installed")
    print(f"  2. Verify your API key is configured")
    print(f"  3. Run a demo article generation")
    print()
    
    # Run checks
    checks_passed = True
    
    if not check_dependencies():
        checks_passed = False
    
    if not check_api_key():
        checks_passed = False
    
    if not check_output_directory():
        checks_passed = False
    
    if not checks_passed:
        print(f"{Fore.RED}Pre-flight checks failed. Please fix the issues above.{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✓ All pre-flight checks passed!{Style.RESET_ALL}\n")
    
    # Ask for confirmation
    response = input(f"{Fore.YELLOW}Run demo generation? This will use your API quota. (y/N): {Style.RESET_ALL}")
    
    if response.lower() != 'y':
        print(f"{Fore.YELLOW}Demo cancelled.{Style.RESET_ALL}")
        print(f"\nTo run manually:")
        print(f"  python main.py --topic \"Your Topic Here\"")
        sys.exit(0)
    
    # Run demo
    if run_demo():
        print(f"\n{Fore.GREEN}🎉 Success! BlogFlow AI is working correctly.{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Next steps:{Style.RESET_ALL}")
        print(f"  • Read README.md for full documentation")
        print(f"  • Try: python main.py --topic \"Your Topic\"")
        print(f"  • Customize config.py for your needs")
    else:
        print(f"\n{Fore.RED}Demo failed. Check the error messages above.{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
