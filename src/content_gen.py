import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_article(topic: str, keywords: list[str]) -> str:
    """
    Generates an SEO-optimized article using Mistral AI.
    
    Args:
        topic (str): The main topic of the article.
        keywords (list[str]): A list of keywords to include.
        
    Returns:
        str: The generated article content or an error message.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key == "your_mistral_api_key_here":
        return "Error: MISTRAL_API_KEY not found or invalid in environment variables."

    try:
        # Initialize Mistral AI Chat Model
        llm = ChatMistralAI(
            api_key=api_key,
            model="mistral-large-latest",
            temperature=0.7
        )

        # Define the prompt template
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert legal content writer. Write an SEO-optimized article about the following topic: {topic}.
            
            Include the following keywords naturally within the text: {keywords}.
            
            The article should be professional, informative, and structured with clear headings (Markdown format).
            """
        )

        # Create the chain
        chain = prompt | llm | StrOutputParser()
        
        # Format keywords for the prompt
        keywords_str = ", ".join(keywords) if keywords else "None"
        
        # Invoke the chain
        response = chain.invoke({"topic": topic, "keywords": keywords_str})
        
        return response

    except Exception as e:
        return f"Error generating content: {str(e)}"
