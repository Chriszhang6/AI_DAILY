#!/usr/bin/env python3
"""
Send a test email with mock data to verify email delivery works
This script bypasses news fetching and uses predefined test data
"""
import os
import sys
from datetime import datetime

# Check for required lxml dependency
try:
    import lxml
except ImportError:
    print("✗ ERROR: lxml package is required", file=sys.stderr)
    sys.exit(1)

from main import generate_html_content, send_email

def main():
    print("=" * 70)
    print("AI DAILY NEWS - TEST EMAIL SENDER")
    print("=" * 70)
    
    # Check environment variables
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    to_email = os.environ.get('TO_EMAIL')
    
    if not all([gmail_user, gmail_pass, to_email]):
        print("\n✗ ERROR: Missing required environment variables:", file=sys.stderr)
        print(f"  GMAIL_USER: {'✓' if gmail_user else '✗'}", file=sys.stderr)
        print(f"  GMAIL_PASS: {'✓' if gmail_pass else '✗'}", file=sys.stderr)
        print(f"  TO_EMAIL: {'✓' if to_email else '✗'}", file=sys.stderr)
        print("\nPlease set these environment variables:", file=sys.stderr)
        print("  export GMAIL_USER=your_email@gmail.com", file=sys.stderr)
        print("  export GMAIL_PASS=your_app_password", file=sys.stderr)
        print("  export TO_EMAIL=recipient@example.com", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n📧 Preparing test email to: {to_email}")
    
    # Create test news data
    test_news = [
        {
            'title': 'OpenAI Releases GPT-5 with Breakthrough Capabilities',
            'link': 'https://openai.com/blog/gpt-5-release',
            'source': 'OpenAI Blog'
        },
        {
            'title': 'Claude 4 Anthropic Announces Enhanced Constitutional AI',
            'link': 'https://anthropic.com/news/claude-4',
            'source': 'Anthropic News'
        },
        {
            'title': 'Google DeepMind Achieves Quantum Supremacy in AI Training',
            'link': 'https://deepmind.google/research/quantum-ai',
            'source': 'DeepMind Research'
        },
        {
            'title': 'Qwen by Alibaba Surpasses GPT-4 in Multilingual Benchmarks',
            'link': 'https://qwenlm.github.io/blog/qwen-2',
            'source': 'Qwen Blog'
        },
        {
            'title': 'Kimi AI Moonshot Introduces Revolutionary Context Window',
            'link': 'https://kimi.ai/blog/context-window',
            'source': 'Kimi AI'
        },
        {
            'title': 'GLM-4 by Zhipu AI Sets New Standards for Chinese NLP',
            'link': 'https://zhipuai.cn/blog/glm-4',
            'source': 'Zhipu AI'
        },
        {
            'title': 'DeepSeek AI Wins International Code Generation Competition',
            'link': 'https://deepseek.com/news/code-competition',
            'source': 'DeepSeek'
        },
        {
            'title': 'AI Breakthrough: New Model Solves Complex Mathematical Proofs',
            'link': 'https://arxiv.org/abs/2024.12345',
            'source': 'arXiv'
        },
        {
            'title': 'Large Language Models Transform Healthcare Diagnostics',
            'link': 'https://www.nature.com/articles/ai-healthcare-2024',
            'source': 'Nature'
        },
        {
            'title': 'Machine Learning Advances Climate Change Prediction Accuracy',
            'link': 'https://www.science.org/doi/10.1126/science.ai2024',
            'source': 'Science'
        }
    ]
    
    print(f"📝 Generating HTML email with {len(test_news)} test articles...")
    html_content = generate_html_content(test_news)
    print(f"✓ Generated {len(html_content)} chars of HTML content")
    
    subject = f"🧪 AI Daily News Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    print(f"\n📤 Sending test email...")
    print(f"   From: {gmail_user}")
    print(f"   To: {to_email}")
    print(f"   Subject: {subject}")
    
    success = send_email(subject, html_content, to_email, gmail_user, gmail_pass)
    
    if success:
        print("\n" + "=" * 70)
        print("✓ SUCCESS! Test email sent successfully!")
        print("=" * 70)
        print(f"\n📬 Check your inbox at {to_email}")
        print("   If you don't see it, check your spam folder.")
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("✗ FAILURE! Email sending failed")
        print("=" * 70)
        print("\nTroubleshooting tips:")
        print("1. Verify GMAIL_PASS is an App Password (not your account password)")
        print("2. Check if 2FA is enabled on your Google account")
        print("3. Try generating a new App Password at:")
        print("   https://myaccount.google.com/apppasswords")
        print("4. Check the error message above for details")
        sys.exit(1)

if __name__ == '__main__':
    main()
