import streamlit as st
import google.generativeai as genai
from PIL import Image
import concurrent.futures
import json
import time

# Page Configuration
st.set_page_config(
    page_title="Grade Genie 🧞 - AI Based Automated Exam Evaluation System.",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS3 with more sophisticated animations and styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
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
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
    }

    /* Global styles */
    .stApp {
        background: var(--light-bg);
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Hero Section with 3D elements */
    .hero-section {
        background: var(--gradient-1);
        padding: 6rem 2rem;
        border-radius: 0 0 4rem 4rem;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(67, 97, 238, 0.3);
    }

    .hero-content {
        max-width: 1200px;
        margin: 0 auto;
        text-align: center;
        color: black;
        position: relative;
        z-index: 2;
    }

    # .hero-title {
    #     font-size: 5rem;
    #     font-weight: 700;
    #     margin-bottom: 1.5rem;
    #     animation: fadeInDown 1s ease;
    #     text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    #     background: linear-gradient(to right, #fff, #e0e0e0);
    #     color: white;
    #     -webkit-background-clip: text;
    #     -webkit-text-fill-color: transparent;
    # }

   .hero-title {
   font-size: 5rem;
   font-weight: 700;
   margin-bottom: 1.5rem;
   animation: fadeInDown 1s ease;
   text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
   color: white;
   }

    .hero-subtitle {
        font-size: 1.8rem;
        font-weight: 300;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Enhanced Upload Section */
    .upload-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 2rem;
        padding: 4rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        margin: 3rem 0;
        animation: slideUp 1s ease;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Redesigned Upload Sections */
    .upload-section {
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        padding: 3rem;
        border-radius: 2rem;
        border: 2px dashed var(--primary-color);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1.5rem 0;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .upload-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(60, 207, 78, 0.1));
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .upload-section:hover {
        border-color: var(--secondary-color);
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }

    .upload-section:hover::before {
        opacity: 1;
    }

    /* File Upload Button Styling */
    .stFileUploader {
        width: 100% !important;
        max-width: 100% !important;
    }

    .stFileUploader > div > div {
        padding: 2rem !important;
        border-radius: 1.5rem !important;
        background: white !important;
        border: 2px dashed var(--primary-color) !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader > div > div:hover {
        border-color: var(--secondary-color) !important;
        background: rgba(67, 97, 238, 0.05) !important;
    }

    /* Upload Icon Animation */
    .upload-icon {
        font-size: 3rem;
        color: var(--primary-color);
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-30px);
        }
        60% {
            transform: translateY(-15px);
        }
    }

    /* Glass Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }

    /* Enhanced Buttons */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border-radius: 2rem;
        padding: 1rem 3rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
        font-size: 1.1rem;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: translateX(-100%);
        transition: 0.5s;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 40px rgba(67, 97, 238, 0.4);
    }

    .stButton > button:hover::before {
        transform: translateX(100%);
    }

    /* Additional Animations */
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(67, 97, 238, 0.3);
        }
        50% {
            box-shadow: 0 0 40px rgba(67, 97, 238, 0.5);
        }
    }

    /* Progress Bar Enhancement */
    .stProgress > div > div > div > div {
        background: var(--gradient-1);
        border-radius: 1rem;
        height: 1rem !important;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Loading Animation */
    .loading-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
    }

    .loading-bar {
        width: 4px;
        height: 18px;
        background: var(--primary-color);
        animation: wave 1s ease-in-out infinite;
    }

    @keyframes wave {
        0%, 100% {
            transform: scaleY(1);
        }
        50% {
            transform: scaleY(2);
        }
    }
</style>
""", unsafe_allow_html=True)

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
    # Hero Section with Enhanced Animation   
    st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Grade Genie 🧞</h1>
                <p class="hero-subtitle">Transform Your Grading Process with AI-Powered Intelligence</p>
                <div class="glass-card" style="display: flex; justify-content: space-around; margin-top: 3rem;">
                    <div style="text-align: center; padding: 1rem;">
                        <h3>🚀 Smart Analysis</h3>
                        <p>AI-powered evaluation</p>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <h3>⚡️ Real-Time</h3>
                        <p>Instant feedback</p>
                    </div>
                    <div style="text-align: center; padding: 1rem;">
                        <h3>✨ Accurate</h3>
                        <p>Precise grading</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Enhanced Upload Section
    st.markdown("""
        <div class="upload-container">
            <h2 style="text-align: center; color: var(--dark-bg); margin-bottom: 3rem; font-size: 2.5rem;">
                📤 Upload Your Documents
            </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="upload-section">
                <div class="upload-icon">📝</div>
                <h3 style="margin-bottom: 1rem; color: var(--primary-color);">Answer Scripts</h3>
        """, unsafe_allow_html=True)
        answer_scripts = st.file_uploader(
            "Drop your answer scripts here",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="answer_scripts"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="upload-section">
                <div class="upload-icon">📋</div>
                <h3 style="margin-bottom: 1rem; color: var(--primary-color);">Evaluation Scheme</h3>
        """, unsafe_allow_html=True)
        evaluation_scheme = st.file_uploader(
            "Drop your evaluation scheme here",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            key="eval_scheme"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Add this after the upload sections in main()

    # Enhanced Start Button with Loading Animation
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Start Evaluation", key="start_eval"):
        if not answer_scripts or not evaluation_scheme:
            st.markdown("""
                <div class="glass-card" style="background: rgba(247, 37, 133, 0.1); border-color: var(--accent-color);">
                    <h3 style="color: var(--accent-color); text-align: center;">
                        ⚠️ Please upload both answer scripts and evaluation scheme to proceed
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            return

        with st.spinner(""):
            st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <div class="loading-wave">
                        <div class="loading-bar" style="animation-delay: 0s;"></div>
                        <div class="loading-bar" style="animation-delay: 0.1s;"></div>
                        <div class="loading-bar" style="animation-delay: 0.2s;"></div>
                        <div class="loading-bar" style="animation-delay: 0.3s;"></div>
                        <div class="loading-bar" style="animation-delay: 0.4s;"></div>
                    </div>
                    <p style="margin-top: 1rem; color: var(--primary-color);">Processing your documents...</p>
                </div>
            """, unsafe_allow_html=True)
            
            start_time = time.time()

            # Extract text from evaluation scheme
            try:
                scheme_image = Image.open(evaluation_scheme)
                scheme_text = extract_text_from_image(scheme_image, "Extract the standard answer and evaluation criteria")
                
                # Results Section Header
                st.markdown("""
                    <div class="results-container">
                        <h2 style="text-align: center; color: var(--dark-bg); margin-bottom: 2rem;">
                            🔍 Evaluation Results
                        </h2>
                """, unsafe_allow_html=True)
                
                # Process answer scripts with progress
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_scripts = len(answer_scripts)
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future_to_script = {
                        executor.submit(extract_text_from_image, Image.open(script)): script.name 
                        for script in answer_scripts
                    }
                    
                    completed = 0
                    for future in concurrent.futures.as_completed(future_to_script):
                        script_name = future_to_script[future]
                        completed += 1
                        progress = completed / total_scripts
                        progress_bar.progress(progress)
                        status_text.markdown(f"""
                            <div style="text-align: center; color: var(--primary-color);">
                                Processing script {completed} of {total_scripts}: {script_name}
                            </div>
                        """, unsafe_allow_html=True)
                        
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
                            
                            # Enhanced Result Card
                            with st.expander(f"📄 {script_name}"):
                                st.markdown("""
                                    <div class="glass-card">
                                        <div style="border-bottom: 2px solid rgba(67, 97, 238, 0.1); margin-bottom: 1.5rem;">
                                            <h3 style="color: var(--primary-color); font-size: 1.5rem;">
                                                📝 Student Answer
                                            </h3>
                                        </div>
                                """, unsafe_allow_html=True)
                                st.write(student_text)
                                
                                st.markdown("""
                                    <div style="border-bottom: 2px solid rgba(67, 97, 238, 0.1); margin: 1.5rem 0;">
                                        <h3 style="color: var(--primary-color); font-size: 1.5rem;">
                                            📊 Similarity Score
                                        </h3>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Enhanced Progress Bar
                                progress_color = (
                                    "#4CAF50" if similarity_score >= 80
                                    else "#FFC107" if similarity_score >= 60
                                    else "#F44336"
                                )
                                st.markdown(f"""
                                    <div class="progress-wrapper" style="position: relative; height: 30px; background: rgba(0,0,0,0.1); border-radius: 15px; overflow: hidden;">
                                        <div style="position: absolute; top: 0; left: 0; height: 100%; width: {similarity_score}%; background: {progress_color}; transition: width 1s ease-in-out;"></div>
                                        <div style="position: absolute; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                                            {similarity_score}%
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown("""
                                    <div style="border-bottom: 2px solid rgba(67, 97, 238, 0.1); margin: 1.5rem 0;">
                                        <h3 style="color: var(--primary-color); font-size: 1.5rem;">
                                            📋 Detailed Evaluation
                                        </h3>
                                    </div>
                                """, unsafe_allow_html=True)
                                st.write(detailed_evaluation)
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        except Exception as exc:
                            st.markdown(f"""
                                <div class="glass-card" style="background: rgba(244, 67, 54, 0.1); border-color: #F44336;">
                                    <h3 style="color: #F44336; text-align: center;">
                                        ❌ Error processing {script_name}: {str(exc)}
                                    </h3>
                                </div>
                            """, unsafe_allow_html=True)

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                # Processing Time Display
                end_time = time.time()
                processing_time = end_time - start_time
                
                st.markdown(f"""
                    <div class="glass-card" style="text-align: center; margin: 2rem 0;">
                        <h3 style="color: var(--primary-color);">
                            ⏱️ Total Processing Time: {processing_time:.2f} seconds
                        </h3>
                    </div>
                """, unsafe_allow_html=True)

                # Results Summary with Enhanced Styling
                if results:
                    avg_score = sum(r['similarity_score'] for r in results) / len(results)
                    st.markdown("""
                        <div class="glass-card" style="margin: 2rem 0;">
                            <h3 style="text-align: center; color: var(--dark-bg); margin-bottom: 2rem;">
                                📊 Results Summary
                            </h3>
                            <div style="display: flex; justify-content: space-around; gap: 1rem;">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="glass-card" style="flex: 1; text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: 700; color: var(--primary-color);">
                                {len(results)}
                            </div>
                            <div style="color: var(--dark-bg);">Scripts Evaluated</div>
                        </div>
                        <div class="glass-card" style="flex: 1; text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: 700; color: var(--primary-color);">
                                {avg_score:.1f}%
                            </div>
                            <div style="color: var(--dark-bg);">Average Score</div>
                        </div>
                        <div class="glass-card" style="flex: 1; text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: 700; color: var(--primary-color);">
                                {processing_time:.1f}s
                            </div>
                            <div style="color: var(--dark-bg);">Processing Time</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('</div></div>', unsafe_allow_html=True)

                    # Enhanced Download Button
                    results_json = json.dumps(results, indent=4)
                    st.markdown("""
                        <div style="text-align: center; margin: 2rem 0;">
                    """, unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Download Detailed Results",
                        data=results_json,
                        file_name="evaluation_results.json",
                        mime="application/json",
                        key="download_results"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"""
                    <div class="glass-card" style="background: rgba(244, 67, 54, 0.1); border-color: #F44336;">
                        <h3 style="color: #F44336; text-align: center;">
                            ❌ An error occurred: {str(e)}
                        </h3>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
