import random

def check_plagiarism(text: str) -> dict:
    """
    Checks for plagiarism (Mock implementation).
    
    Args:
        text (str): The article content.
        
    Returns:
        dict: Plagiarism score (uniqueness) and details.
    """
    # Mock logic: Randomly assign a high uniqueness score for PoC
    # In a real app, this would call an API like Copyscape or Turnitin
    
    uniqueness_score = random.randint(85, 100)
    
    return {
        "uniqueness_score": uniqueness_score,
        "is_plagiarized": uniqueness_score < 80,
        "details": "No significant matches found (Mock Check)." if uniqueness_score >= 80 else "Potential matches found in external sources."
    }
