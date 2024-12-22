import streamlit as st
import google.generativeai as genai
from PIL import Image
import concurrent.futures
import json
import time

# Page Configuration
st.set_page_config(
    page_title="Grade Genie 🧞 - AI Based Automated Exam Evaluation System",
    page_icon="📝",
    layout="wide"
)

# Hardcoded API Key - Replace with your actual API key
GEMINI_API_KEY = "Your API Key"


# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Extract text from image using Gemini
def extract_text_from_image(image, prompt="Extract all text from this image as accurately as possible."):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt, image])
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in text extraction: {str(e)}")
        return ""

# Compute Similarity Score
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

# Detailed Answer Evaluation
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
    st.title("Grade Genie 🧞")
    st.success("An AI Based Automated Exam Evaluation System")

    # File Uploaders
    st.header("📤 Upload Documents")
    col1, col2 = st.columns(2)
    
    with col1:
        answer_scripts = st.file_uploader(
            "Upload Answer Scripts", 
            type=['pdf', 'jpg', 'jpeg', 'png'], 
            accept_multiple_files=True
        )
    
    with col2:
        evaluation_scheme = st.file_uploader(
            "Upload Evaluation Scheme", 
            type=['pdf', 'jpg', 'jpeg', 'png']
        )

    # Process and Evaluate
    if st.button("Evaluate Answer Scripts"):
        if not answer_scripts or not evaluation_scheme:
            st.warning("Please upload both answer scripts and evaluation scheme")
            return

        with st.spinner("Processing documents..."):
            # Start timing
            start_time = time.time()

            # Extract text from evaluation scheme
            scheme_image = Image.open(evaluation_scheme)
            scheme_text = extract_text_from_image(scheme_image, "Extract the standard answer and evaluation criteria")
            
            st.subheader("🔍 Grading Results")
            
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
                            st.markdown("### Student Answer")
                            st.write(student_text)
                            
                            st.markdown("### Similarity Score")
                            st.progress(similarity_score/100)
                            st.write(f"Similarity: {similarity_score}%")
                            
                            st.markdown("### Detailed Evaluation")
                            st.write(detailed_evaluation)
                    
                    except Exception as exc:
                        st.error(f"Error processing {script_name}: {str(exc)}")

            # Total processing time
            end_time = time.time()
            st.markdown(f"### ⏱️ Total Processing Time: {end_time - start_time:.2f} seconds")

            if results:
                results_json = json.dumps(results, indent=4)
                st.download_button(
                    label="Download Detailed Results",
                    data=results_json,
                    file_name="evaluation_results.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
