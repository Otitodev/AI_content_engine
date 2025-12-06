# AI Content Engine

A Streamlit-based application for generating SEO-optimized content using AI.

### (Live link)[https://aicontentengine.streamlit.app/]


## Features

*   **AI Content Generation**: Generates articles based on topics and keywords using Mistral AI.
*   **SEO Analysis**: Real-time SEO scoring and improvement suggestions.
*   **Plagiarism Check**: Integrated uniqueness verification.
*   **History**: Save and view previously generated articles.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory and add your Mistral API key:
    ```env
    MISTRAL_API_KEY=your_api_key_here
    ```

3.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## Project Structure

*   `app.py`: Main Streamlit application entry point.
*   `src/`: Contains core logic modules (`content_gen`, `seo`, `plagiarism`, `db`).
*   `data/`: Directory for database storage.
*   `Docs.md`: Detailed project documentation and roadmap.
