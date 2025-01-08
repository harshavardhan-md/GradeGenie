import streamlit as st
import google.generativeai as genai
from PIL import Image
import concurrent.futures
import json
import time

# Custom CSS
st.markdown("""
<style>
    /* Main theme colors and fonts */
    :root {
        --primary-color: #4A90E2;
        --secondary-color: #2ECC71;
        --accent-color: #F1C40F;
        --dark-bg: #2C3E50;
        --light-bg: #ECF0F1;
    }

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Custom container */
    .custom-container {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }

    /* Header styles */
    .main-header {
        background: linear-gradient(120deg, #2980B9, #6DD5FA);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .main-header h1 {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    /* Upload section styles */
    .upload-section {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 2px dashed #4A90E2;
        transition: all 0.3s ease;
    }

    .upload-section:hover {
        border-color: #2ECC71;
        transform: translateY(-2px);
    }

    /* Results section */
    .results-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #4A90E2;
        transition: all 0.3s ease;
    }

    .results-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #2ECC71;
    }

    /* Buttons */
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 2rem;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #2980B9;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Expander customization */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #2ECC71;
        color: white;
        border-radius: 2rem;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background-color: #27AE60;
        transform: translateY(-2px);
    }

    /* Custom alert styles */
    .success-alert {
        padding: 1rem;
        background-color: #D4EDDA;
        color: #155724;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="Grade Genie 🧞 - AI Based Automated Exam Evaluation System",
    page_icon="📝",
    layout="wide"
)

# Accessing API Via Streamlit Secrets
GEMINI_API_KEY = st.secrets["Gemini_API_Token"]

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Helper functions remain the same as in your original code
def extract_text_from_image(image, prompt="Extract all text from this image as accurately as possible."):
    # Your existing implementation
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt, image])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in text extraction: {str(e)}")
        return ""

def compute_similarity_score(student_answer, correct_answer):
    # Your existing implementation
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        similarity_prompt = f"""
        Compare the following two texts and provide a similarity score from 0-100:
        Correct Answer: {correct_answer}
        Student Answer: {student_answer}

        Evaluate based on:
        1. Contextual relevance
        2. Key concepts coverage
        3. Accuracy of information
        4. Structural similarity

        Return ONLY the numerical similarity score.
        """
        
        response = model.generate_content(similarity_prompt)
        score = ''.join(filter(str.isdigit, response.text))
        return int(score) if score else 85
    except Exception as e:
        st.error(f"Similarity score computation error: {str(e)}")
        return 85

def evaluate_answer(student_answer, correct_answer):
    # Your existing implementation
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        evaluation_prompt = f"""
        Perform a detailed evaluation of the student's answer:
        Correct Answer Context: {correct_answer}
        Student's Answer: {student_answer}

        Provide a structured analysis including:
        1. Specific areas of mistakes
        2. Concepts misunderstood
        3. Potential improvements
        4. Recommended learning resources

        Format the response in a clear, constructive manner.
        """
        
        response = model.generate_content(evaluation_prompt)
        return response.text
    except Exception as e:
        st.error(f"Detailed evaluation error: {str(e)}")
        return "Evaluation could not be completed"

def main():
    # Custom Header
    st.markdown("""
        <div class="main-header">
            <h1>Grade Genie 🧞</h1>
            <p class="success-alert">AI-Powered Automated Exam Evaluation System</p>
        </div>
    """, unsafe_allow_html=True)

    # File Upload Section
    st.markdown("""
        <div class="custom-container">
            <h2 style="color: #2C3E50; text-align: center;">📤 Upload Your Documents</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        answer_scripts = st.file_uploader(
            "Upload Answer Scripts 📝", 
            type=['pdf', 'jpg', 'jpeg', 'png'], 
            accept_multiple_files=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        evaluation_scheme = st.file_uploader(
            "Upload Evaluation Scheme 📋", 
            type=['pdf', 'jpg', 'jpeg', 'png']
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Process and Evaluate Button
    if st.button("🚀 Evaluate Answer Scripts"):
        if not answer_scripts or not evaluation_scheme:
            st.warning("⚠️ Please upload both answer scripts and evaluation scheme")
            return

        with st.spinner("🔄 Processing documents..."):
            start_time = time.time()

            # Extract text from evaluation scheme
            scheme_image = Image.open(evaluation_scheme)
            scheme_text = extract_text_from_image(scheme_image, "Extract the standard answer and evaluation criteria")
            
            st.markdown("""
                <div class="custom-container">
                    <h2 style="color: #2C3E50; text-align: center;">🔍 Evaluation Results</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Process answer scripts
            results = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_script = {
                    executor.submit(extract_text_from_image, Image.open(script)): script.name 
                    for script in answer_scripts
                }
                
                for future in concurrent.futures.as_completed(future_to_script):
                    script_name = future_to_script[future]
                    try:
                        student_text = future.result()
                        similarity_score = compute_similarity_score(student_text, scheme_text)
                        detailed_evaluation = evaluate_answer(student_text, scheme_text)
                        
                        result = {
                            'script': script_name,
                            'student_answer': student_text,
                            'similarity_score': similarity_score,
                            'detailed_evaluation': detailed_evaluation
                        }
                        results.append(result)
                        
                        with st.expander(f"📄 {script_name}"):
                            st.markdown('<div class="results-card">', unsafe_allow_html=True)
                            
                            st.markdown("### 📝 Student Answer")
                            st.write(student_text)
                            
                            st.markdown("### 📊 Similarity Score")
                            st.progress(similarity_score/100)
                            st.markdown(f"<h4 style='text-align: center; color: #2ECC71;'>Similarity: {similarity_score}%</h4>", unsafe_allow_html=True)
                            
                            st.markdown("### 📋 Detailed Evaluation")
                            st.write(detailed_evaluation)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as exc:
                        st.error(f"❌ Error processing {script_name}: {str(exc)}")

            # Processing Time Display
            end_time = time.time()
            st.markdown(f"""
                <div class="custom-container" style="text-align: center;">
                    <h3>⏱️ Total Processing Time: {end_time - start_time:.2f} seconds</h3>
                </div>
            """, unsafe_allow_html=True)

            # Download Results Button
            if results:
                results_json = json.dumps(results, indent=4)
                st.download_button(
                    label="📥 Download Detailed Results",
                    data=results_json,
                    file_name="evaluation_results.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
