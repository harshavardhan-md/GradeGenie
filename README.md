<div align="center">

# 🧞‍♂️ Grade-Genie

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gradegenie.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini-blue)](https://deepmind.google/technologies/gemini/)

> *Your AI-powered companion for automated exam evaluation*

![Grade Genie Banner](https://github.com/harshavardhan-md/assets_for_all_repos/blob/main/GradeGenie/home%20screen%202.png?raw=true)
![Grade Genie Upload Section](https://github.com/harshavardhan-md/assets_for_all_repos/blob/main/GradeGenie/Upload_Sections.png?raw=true)
![Evaluation Rest](https://github.com/harshavardhan-md/assets_for_all_repos/blob/main/GradeGenie/Evaluation_Result.png?raw=true)
![Detailed Evaluation Result](https://github.com/harshavardhan-md/assets_for_all_repos/blob/main/GradeGenie/Detailed_Evaluation.png?raw=true)
![Metrics](https://github.com/harshavardhan-md/assets_for_all_repos/blob/main/GradeGenie/Metrics.png?raw=true)

[Demo](https://gradegenie.streamlit.app/) • [Documentation](#) • [Report Bug](#) • [Request Feature](#)

</div>

## 🌟 Features

### 🤖 AI-Powered Evaluation
- **Smart Text Extraction**: Automatically extracts text from scanned answer scripts
- **Intelligent Scoring**: Computes similarity scores based on multiple evaluation criteria
- **Detailed Analysis**: Provides comprehensive feedback on each answer

### ⚡ Real-Time Processing
- **Concurrent Processing**: Evaluates multiple answer scripts simultaneously
- **Progress Tracking**: Live progress indicators and processing time statistics
- **Instant Results**: View evaluation results as they are completed

### 📊 Comprehensive Reports
- **Similarity Scores**: Visual representation of answer matching
- **Detailed Feedback**: Specific areas of improvement and mistakes
- **Downloadable Results**: Export evaluations in JSON format

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Gemini API key ([Get it here](https://deepmind.google/technologies/gemini/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/grade-genie.git
cd grade-genie
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
   - Create `.streamlit/secrets.toml` file
   - Add your API key:
     ```toml
     Gemini_API_Token = "your-api-key-here"
     ```

4. Run the application:
```bash
streamlit run app.py
```

## 💡 Usage

1. **Upload Documents**
   - Add student answer scripts (PDF/JPG/JPEG/PNG)
   - Upload evaluation scheme document

2. **Start Evaluation**
   - Click "Evaluate Answer Scripts"
   - Watch real-time processing
   - View results as they appear

3. **Review Results**
   - Examine similarity scores
   - Read detailed evaluations
   - Download comprehensive reports

## 🛠️ Technical Architecture

```mermaid
graph LR
    A[Upload Documents] --> B[Text Extraction]
    B --> C[Similarity Analysis]
    C --> D[Detailed Evaluation]
    D --> E[Results Generation]
    E --> F[Download Report]
```

## 📦 Project Structure

```
grade-genie/
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── .streamlit/        # Streamlit configuration
│   └── secrets.toml   # API keys and secrets
└── README.md          # Project documentation
```

## 🔑 Environment Variables

Required environment variables in `.streamlit/secrets.toml`:

```toml
Gemini_API_Token = "your-api-key-here"
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) for powerful AI capabilities
- [Pillow](https://python-pillow.org/) for image processing

---

<div align="center">

Made with ✌🏻 by [Harshavardhan M](https://www.linkedin.com/in/harshavardhan-md)

[⬆ Back to Top](#-grade-genie)

</div>
