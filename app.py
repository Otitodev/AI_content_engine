import streamlit as st
from dotenv import load_dotenv
import os
from src import content_gen, seo, plagiarism, db

# Load environment variables
load_dotenv()

# Initialize DB
db.init_db()

def main():
    st.set_page_config(page_title="AI Content Engine", layout="wide")
    
    st.title("AI-Powered Content Generation System")
    st.markdown("Generate SEO-optimized articles with real-time analysis.")

    # Sidebar
    st.sidebar.header("Configuration")
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or api_key == "your_mistral_api_key_here":
        st.sidebar.warning("⚠️ Mistral API Key not found in .env")
        api_key_input = st.sidebar.text_input("Enter Mistral API Key", type="password")
        if api_key_input:
            os.environ["MISTRAL_API_KEY"] = api_key_input
            st.sidebar.success("Key set for this session")
    else:
        st.sidebar.success("✅ API Key loaded")

    # History in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("History")
    if st.sidebar.button("Refresh History"):
        history = db.get_articles()
        for row in history:
            st.sidebar.text(f"{row[1]} ({row[5][:10]})")

    # Main Input
    col1, col2 = st.columns([1, 1])
    with col1:
        topic = st.text_input("Topic", placeholder="e.g., Personal Injury Law")
    with col2:
        keywords_input = st.text_input("Keywords (comma separated)", placeholder="e.g., compensation, accident, lawyer")
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

    if st.button("Generate Content", type="primary"):
        if not topic:
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating content with Mistral AI..."):
                generated_text = content_gen.generate_article(topic, keywords)
                
                if generated_text.startswith("Error"):
                    st.error(generated_text)
                else:
                    st.session_state['generated_content'] = generated_text
                    st.session_state['topic'] = topic
                    st.session_state['keywords'] = keywords
                    st.success("Content Generated!")

    # Display & Edit Section
    if 'generated_content' in st.session_state:
        st.markdown("---")
        st.subheader("Editor & Analysis")
        
        col_editor, col_metrics = st.columns([2, 1])
        
        with col_editor:
            # Editable Text Area
            edited_content = st.text_area(
                "Edit Article", 
                value=st.session_state['generated_content'], 
                height=600
            )
            st.session_state['generated_content'] = edited_content
            
            if st.button("Save Article"):
                # Re-analyze before saving to get final stats
                seo_result = seo.analyze_seo(edited_content, st.session_state['keywords'])
                db.save_article(
                    st.session_state['topic'], 
                    st.session_state['keywords'], 
                    edited_content, 
                    seo_result['score']
                )
                st.success("Article saved to database!")

        with col_metrics:
            # Real-time Analysis
            st.markdown("### 📊 SEO Score")
            seo_result = seo.analyze_seo(edited_content, st.session_state['keywords'])
            st.metric("SEO Score", f"{seo_result['score']}/100")
            
            with st.expander("SEO Suggestions", expanded=True):
                if seo_result['suggestions']:
                    for suggestion in seo_result['suggestions']:
                        st.warning(suggestion)
                else:
                    st.success("Great job! No suggestions.")

            st.markdown("### 🕵️ Plagiarism Check")
            plag_result = plagiarism.check_plagiarism(edited_content)
            st.metric("Uniqueness Score", f"{plag_result['uniqueness_score']}%")
            if plag_result['is_plagiarized']:
                st.error(plag_result['details'])
            else:
                st.success(plag_result['details'])

if __name__ == "__main__":
    main()
