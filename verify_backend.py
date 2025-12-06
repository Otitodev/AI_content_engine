import os
import sys
from src import seo, plagiarism, db, content_gen

def test_seo():
    print("Testing SEO...")
    text = "This is a short text. It has some keywords like law and lawyer."
    keywords = ["law", "lawyer", "missing"]
    result = seo.analyze_seo(text, keywords)
    print(f"SEO Score: {result['score']}")
    print(f"Suggestions: {result['suggestions']}")
    assert result['score'] < 100, "Score should be penalized for length"
    assert any("missing" in s for s in result['suggestions']), "Should detect missing keyword"
    print("SEO Test Passed ✅")

def test_plagiarism():
    print("\nTesting Plagiarism...")
    result = plagiarism.check_plagiarism("Some text")
    print(f"Uniqueness: {result['uniqueness_score']}")
    assert 'uniqueness_score' in result
    print("Plagiarism Test Passed ✅")

def test_db():
    print("\nTesting Database...")
    db.init_db()
    db.save_article("Test Topic", ["k1", "k2"], "Test Content", 80)
    articles = db.get_articles()
    assert len(articles) > 0
    print(f"Retrieved {len(articles)} articles.")
    print("DB Test Passed ✅")

def test_content_gen_mock():
    print("\nTesting Content Gen (Mock check)...")
    # We expect an error if no key, or success if key exists.
    # We just want to ensure it doesn't crash.
    response = content_gen.generate_article("Test", ["test"])
    print(f"Response: {response[:50]}...")
    print("Content Gen Test Passed ✅")

if __name__ == "__main__":
    try:
        test_seo()
        test_plagiarism()
        test_db()
        test_content_gen_mock()
        print("\nAll Backend Tests Passed! 🚀")
    except AssertionError as e:
        print(f"\n❌ Test Failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
