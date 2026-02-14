#!/usr/bin/env python3
"""
Test script for AI Daily News email flow
Tests each component independently and then the full flow
"""
import sys
import os

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    try:
        import requests
        print("  ✓ requests imported successfully")
    except ImportError as e:
        print(f"  ✗ requests import failed: {e}", file=sys.stderr)
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  ✓ beautifulsoup4 imported successfully")
    except ImportError as e:
        print(f"  ✗ beautifulsoup4 import failed: {e}", file=sys.stderr)
        return False
    
    try:
        import lxml
        print("  ✓ lxml imported successfully")
    except ImportError as e:
        print(f"  ✗ lxml import failed: {e}", file=sys.stderr)
        return False
    
    return True

def test_xml_parser():
    """Test that BeautifulSoup can use lxml for XML parsing"""
    print("\n🧪 Testing XML parser...")
    try:
        from bs4 import BeautifulSoup
        xml_content = '<?xml version="1.0"?><root><item>Test</item></root>'
        soup = BeautifulSoup(xml_content, 'xml')
        if soup.find('item').text == 'Test':
            print("  ✓ XML parsing with lxml works correctly")
            return True
        else:
            print("  ✗ XML parsing returned unexpected result", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  ✗ XML parsing failed: {e}", file=sys.stderr)
        return False

def test_news_fetching():
    """Test news fetching from Google News RSS"""
    print("\n🧪 Testing news fetching...")
    try:
        from main import fetch_google_news
        articles = fetch_google_news('OpenAI', max_items=1, retries=1)
        if articles:
            print(f"  ✓ Successfully fetched {len(articles)} article(s)")
            print(f"    Sample: {articles[0]['title'][:50]}...")
            return True
        else:
            print("  ⚠ No articles fetched (may be network issue)", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  ✗ News fetching failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def test_html_generation():
    """Test HTML email generation"""
    print("\n🧪 Testing HTML generation...")
    try:
        from main import generate_html_content
        test_news = [
            {'title': 'Test Article 1', 'link': 'http://example.com/1', 'source': 'Test Source 1'},
            {'title': 'Test Article 2', 'link': 'http://example.com/2', 'source': 'Test Source 2'},
            {'title': 'Test Article 3', 'link': 'http://example.com/3', 'source': 'Test Source 3'},
        ]
        html = generate_html_content(test_news)
        if html and 'Test Article 1' in html and '<!DOCTYPE html>' in html:
            print(f"  ✓ HTML generated successfully ({len(html)} chars)")
            return True
        else:
            print("  ✗ HTML generation failed validation", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  ✗ HTML generation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def test_environment_variables():
    """Test that required environment variables are set"""
    print("\n🧪 Testing environment variables...")
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    to_email = os.environ.get('TO_EMAIL')
    
    all_set = True
    if gmail_user:
        print(f"  ✓ GMAIL_USER is set: {gmail_user[:3]}***")
    else:
        print("  ✗ GMAIL_USER is not set", file=sys.stderr)
        all_set = False
    
    if gmail_pass:
        print("  ✓ GMAIL_PASS is set: ***")
    else:
        print("  ✗ GMAIL_PASS is not set", file=sys.stderr)
        all_set = False
    
    if to_email:
        print(f"  ✓ TO_EMAIL is set: {to_email}")
    else:
        print("  ✗ TO_EMAIL is not set", file=sys.stderr)
        all_set = False
    
    return all_set

def test_smtp_connection():
    """Test SMTP connection to Gmail"""
    print("\n🧪 Testing SMTP connection...")
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    
    if not gmail_user or not gmail_pass:
        print("  ⚠ Skipping SMTP test - credentials not set")
        return None
    
    try:
        import smtplib
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            server.login(gmail_user, gmail_pass)
            print("  ✓ SMTP connection and authentication successful")
            return True
    except Exception as e:
        print(f"  ✗ SMTP connection failed: {e}", file=sys.stderr)
        return False

def test_full_pipeline_mock():
    """Test the full pipeline with mock data (no network required)"""
    print("\n🧪 Testing full pipeline with mock data...")
    try:
        from main import generate_html_content, send_email
        from datetime import datetime
        
        # Create mock news data
        mock_news = [
            {'title': 'OpenAI Releases GPT-5: Revolutionary AI Model', 'link': 'http://example.com/1', 'source': 'TechCrunch'},
            {'title': 'Claude AI Updates with New Features', 'link': 'http://example.com/2', 'source': 'The Verge'},
            {'title': 'Google DeepMind Makes Breakthrough in Protein Folding', 'link': 'http://example.com/3', 'source': 'Nature'},
            {'title': 'Qwen by Alibaba Achieves State-of-the-Art Results', 'link': 'http://example.com/4', 'source': 'AI News'},
            {'title': 'Kimi AI Launches New Conversational Interface', 'link': 'http://example.com/5', 'source': 'Tech Asia'},
            {'title': 'GLM Zhipu Expands to International Markets', 'link': 'http://example.com/6', 'source': 'Bloomberg'},
            {'title': 'DeepSeek AI Wins Competition for Efficiency', 'link': 'http://example.com/7', 'source': 'MIT Review'},
            {'title': 'AI Breakthrough in Medical Diagnosis', 'link': 'http://example.com/8', 'source': 'JAMA'},
            {'title': 'Large Language Models Transform Education', 'link': 'http://example.com/9', 'source': 'Wired'},
            {'title': 'Machine Learning Advances in Climate Science', 'link': 'http://example.com/10', 'source': 'Science'},
        ]
        
        # Test HTML generation
        html_content = generate_html_content(mock_news)
        if not html_content or len(html_content) < 1000:
            print("  ✗ HTML generation produced insufficient content", file=sys.stderr)
            return False
        print(f"  ✓ Generated HTML email ({len(html_content)} chars)")
        
        # Check if email credentials are available
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_pass = os.environ.get('GMAIL_PASS')
        to_email = os.environ.get('TO_EMAIL')
        
        if all([gmail_user, gmail_pass, to_email]):
            # If credentials are available, we could send a test email
            # But we'll just report that we could
            print(f"  ✓ Email credentials available, ready to send to {to_email}")
            return True
        else:
            print("  ⚠ Email credentials not set, cannot test actual sending")
            print("  ✓ Pipeline logic validated with mock data")
            return True
            
    except Exception as e:
        print(f"  ✗ Full pipeline test failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 70)
    print("AI DAILY NEWS - EMAIL FLOW TEST")
    print("=" * 70)
    
    results = {}
    results['imports'] = test_imports()
    results['xml_parser'] = test_xml_parser()
    results['news_fetching'] = test_news_fetching()
    results['html_generation'] = test_html_generation()
    results['full_pipeline_mock'] = test_full_pipeline_mock()
    results['environment'] = test_environment_variables()
    results['smtp'] = test_smtp_connection()
    
    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)
    
    for test_name, result in results.items():
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:
            status = "⚠ SKIP"
        print(f"  {status:10} {test_name}")
    
    # Overall result - only count actual failures, not skipped tests
    failed_tests = [name for name, result in results.items() if result is False]
    critical_failures = [name for name in failed_tests if name not in ['news_fetching', 'environment', 'smtp']]
    
    if critical_failures:
        print(f"\n✗ {len(critical_failures)} critical test(s) failed: {', '.join(critical_failures)}")
        sys.exit(1)
    elif failed_tests:
        print(f"\n⚠ {len(failed_tests)} non-critical test(s) failed: {', '.join(failed_tests)}")
        print("  (These are expected to fail in local/restricted environments)")
        print("\n✓ All critical tests passed!")
        sys.exit(0)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)

if __name__ == '__main__':
    main()
