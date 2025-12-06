import os
import sys
from src import seo, plagiarism, db, content_gen

def run_tests():
    try:
        # SEO
        seo.analyze_seo("test", ["test"])
        
        # Plagiarism
        plagiarism.check_plagiarism("test")
        
        # DB
        db.init_db()
        db.save_article("Test", ["k"], "C", 10)
        
        # Content Gen (Mock)
        content_gen.generate_article("T", ["k"])
        
        with open("verification_result.txt", "w") as f:
            f.write("PASS")
            
    except Exception as e:
        with open("verification_result.txt", "w") as f:
            f.write(f"FAIL: {e}")

if __name__ == "__main__":
    run_tests()
