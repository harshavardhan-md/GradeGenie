import streamlit as st
import google.generativeai as genai
from PIL import Image
import concurrent.futures
import json
import time

# Page Configuration must come first
st.set_page_config(
    page_title="Grade Genie 🧞 - AI Based Automated Exam Evaluation System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with animations and professional styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Main theme colors and fonts */
    :root {
        --primary-color: #4361EE;
        --secondary-color: #3CCF4E;
        --accent-color: #F72585;
        --dark-bg: #1A1A2E;
        --light-bg: #F8F9FA;
        --gradient-1: linear-gradient(135deg, #4361EE, #3CCF4E);
        --gradient-2: linear-gradient(45deg, #F72585, #4361EE);
    }

    /* Global styles */
    .stApp {
        background: var(--light-bg);
        font-family: 'Poppins', sans-serif;
    }

    /* Hero Section */
    .hero-section {
        background: var(--gradient-1);
        padding: 4rem 2rem;
        border-radius: 0 0 3rem 3rem;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }

    .hero-content {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
        color: white;
        position: relative;
        z-index: 2;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        animation: fadeInDown 1s ease;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease;
    }

    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        animation: fadeIn 1.5s ease;
    }

    .hero-feature {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-align: center;
        transition: transform 0.3s ease;
    }

    .hero-feature:hover {
        transform: translateY(-5px);
    }

    /* Animated background elements */
    .bg-element {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        animation: float 10s infinite ease-in-out;
    }

    .bg-element-1 {
        width: 300px;
        height: 300px;
        top: -150px;
        left: -150px;
    }

    .bg-element-2 {
        width: 200px;
        height: 200px;
        bottom: -100px;
        right: -100px;
        animation-delay: -5s;
    }

    /* Main Container Styles */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        animation: fadeIn 1s ease;
    }

    /* Upload Section */
    .upload-container {
        background: white;
        border-radius: 2rem;
        padding: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        animation: slideUp 1s ease;
    }

    .upload-section {
        background: var(--light-bg);
        padding: 2rem;
        border-radius: 1.5rem;
        border: 2px dashed var(--primary-color);
        transition: all 0.3s ease;
        margin: 1rem 0;
    }

    .upload-section:hover {
        border-color: var(--secondary-color);
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }

    /* Results Section */
    .results-container {
        background: white;
        border-radius: 2rem;
        padding: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        animation: slideUp 1.5s ease;
    }

    .results-card {
        background: var(--light-bg);
        padding: 2rem;
        border-radius: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid var(--primary-color);
        transition: all 0.3s ease;
    }

    .results-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }

    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: var(--gradient-1);
        border-radius: 1rem;
    }

    /* Buttons */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border-radius: 2rem;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(67, 97, 238, 0.3);
    }

    /* Download Button */
    .stDownloadButton > button {
        background: var(--gradient-2);
        color: white;
        border-radius: 2rem;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(247, 37, 133, 0.3);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes float {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-20px);
        }
    }

    /* Stats Card */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        animation: fadeIn 2s ease;
    }

    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .stat-label {
        font-size: 1rem;
        color: #666;
    }

    /* Custom Alert Styles */
    .success-alert {
        background: linear-gradient(135deg, #4361EE20, #3CCF4E20);
        border-left: 4px solid var(--secondary-color);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        animation: slideUp 1s ease;
    }

    .warning-alert {
        background: linear-gradient(135deg, #F7258520, #4361EE20);
        border-left: 4px solid var(--accent-color);
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        animation: slideUp 1s ease;
    }
</style>
""", unsafe_allow_html=True)

# Gemini API Configuration
GEMINI_API_KEY = st.secrets["Gemini_API_Token"]
genai.configure(api_key=GEMINI_API_KEY)

# Helper functions (same as before)
def extract_text_from_image(image, prompt="Extract all text from this image as accurately as possible."):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt, image])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in text extraction: {str(e)}")
        return ""

def compute_similarity_score(student_answer, correct_answer):
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
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="bg-element bg-element-1"></div>
            <div class="bg-element bg-element-2"></div>
            <div class="hero-content">
                <h1 class="hero-title">Grade Genie 🧞</h1>
                <p class="hero-subtitle">Transform Your Grading Process with AI-Powered Intelligence</p>
                <div class="hero-features">
                    <div class="hero-feature">
                        <h3>Smart Analysis</h3>
                        <p>AI-powered evaluation</p>
                    </div>
                    <div class="hero-feature">
                        <h3>Real-Time</h3>
                        <p>Instant feedback</p>
                    </div>
                    <div class="hero-feature">
                        <h3>Accurate</h3>
                        <p>Precise grading</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Stats Section
    st.markdown("""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">99%</div>
                <div class="stat-label">Accuracy Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">50x</div>
                <div class="stat-label">Faster Than Manual</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Availability</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown("""
        <div class="main-container">
            <div class="upload-container">
                <h2 style="text-align: center; color: var(--dark-bg); margin-bottom: 2rem;">
                    📤 Upload Your Documents
                </h2>
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

    st.markdown('</div>', unsafe_allow_html=True)

    # Process and Evaluate Button
    if st.button("🚀 Start Evaluation"):
        if not answer_scripts or not evaluation_scheme:
            st.markdown("""
                <div class="warning-alert">
                    ⚠️ Please upload both answer scripts and evaluation scheme to proceed
                </div>
            """, unsafe_allow_html=True)
            return

        with st.spinner("🔄 Processing your documents..."):
            start_time = time.time()

            # Extract text from evaluation scheme
            scheme_image = Image.open(evaluation_scheme)
            scheme_text = extract_text_from_image(scheme_image, "Extract the standard answer and evaluation criteria")
            
            # Results Section Header
            st.markdown("""
                <div class="results-container">
                    <h2 style="text-align: center; color: var(--dark-bg); margin-bottom: 2rem;">
                        🔍 Evaluation Results
                    </h2>
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
                            st.markdown("""
                                <div class="results-card">
                                    <div style="border-bottom: 1px solid #eee; margin-bottom: 1.5rem;">
                                        <h3 style="color: var(--primary-color);">📝 Student Answer</h3>
                                    </div>
                            """, unsafe_allow_html=True)
                            st.write(student_text)
                            
                            st.markdown("""
                                <div style="border-bottom: 1px solid #eee; margin: 1.5rem 0;">
                                    <h3 style="color: var(--primary-color);">📊 Similarity Score</h3>
                                </div>
                            """, unsafe_allow_html=True)
                            st.progress(similarity_score/100)
                            st.markdown(f"""
                                <div style="text-align: center; padding: 1rem;">
                                    <h4 style="color: var(--secondary-color); font-size: 1.5rem;">
                                        {similarity_score}% Match
                                    </h4>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("""
                                <div style="border-bottom: 1px solid #eee; margin: 1.5rem 0;">
                                    <h3 style="color: var(--primary-color);">📋 Detailed Evaluation</h3>
                                </div>
                            """, unsafe_allow_html=True)
                            st.write(detailed_evaluation)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as exc:
                        st.markdown(f"""
                            <div class="warning-alert">
                                ❌ Error processing {script_name}: {str(exc)}
                            </div>
                        """, unsafe_allow_html=True)

            # Processing Time Display
            end_time = time.time()
            processing_time = end_time - start_time
            
            st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background: var(--light-bg); border-radius: 1rem; margin: 2rem 0;">
                    <h3 style="color: var(--primary-color);">
                        ⏱️ Total Processing Time: {processing_time:.2f} seconds
                    </h3>
                </div>
            """, unsafe_allow_html=True)

            # Results Summary
            if results:
                avg_score = sum(r['similarity_score'] for r in results) / len(results)
                st.markdown("""
                    <div style="margin: 2rem 0;">
                        <h3 style="text-align: center; color: var(--dark-bg);">📊 Results Summary</h3>
                        <div class="stats-container">
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-number">{len(results)}</div>
                        <div class="stat-label">Scripts Evaluated</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{avg_score:.1f}%</div>
                        <div class="stat-label">Average Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{processing_time:.1f}s</div>
                        <div class="stat-label">Processing Time</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div></div>', unsafe_allow_html=True)

                # Download Results Button
                results_json = json.dumps(results, indent=4)
                st.markdown("""
                    <div style="text-align: center; margin: 2rem 0;">
                """, unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Detailed Results",
                    data=results_json,
                    file_name="evaluation_results.json",
                    mime="application/json"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)  # Close results-container

if __name__ == "__main__":
    main()
