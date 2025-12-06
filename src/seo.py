import re

def analyze_seo(text: str, keywords: list[str]) -> dict:
    """
    Analyzes the text for SEO metrics.
    
    Args:
        text (str): The article content.
        keywords (list[str]): Target keywords.
        
    Returns:
        dict: SEO score and suggestions.
    """
    if not text:
        return {"score": 0, "suggestions": ["No content to analyze."]}

    score = 100
    suggestions = []
    
    # Word count check
    word_count = len(text.split())
    if word_count < 300:
        score -= 20
        suggestions.append(f"Content is too short ({word_count} words). Aim for at least 300 words.")
    
    # Keyword density check
    text_lower = text.lower()
    for keyword in keywords:
        keyword_lower = keyword.lower()
        count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text_lower))
        if count == 0:
            score -= 10
            suggestions.append(f"Keyword '{keyword}' not found in text.")
        elif count > 5: # Arbitrary upper limit for stuffing
            score -= 5
            suggestions.append(f"Keyword '{keyword}' appears too frequently ({count} times). Avoid keyword stuffing.")
            
    # Basic readability (sentence length)
    sentences = re.split(r'[.!?]+', text)
    avg_sentence_length = sum(len(s.split()) for s in sentences if s) / len(sentences) if sentences else 0
    if avg_sentence_length > 20:
        score -= 10
        suggestions.append("Sentences are too long on average. Try to shorten them for better readability.")

    return {
        "score": max(0, score),
        "suggestions": suggestions
    }
