# 🧠 AI Resume Analyzer & Career Recommendation System

The **AI Resume Analyzer** is a machine learning-based web application that helps users analyze their resumes and get career path recommendations based on extracted skills. It uses natural language processing (NLP) to parse resumes and predict a suitable career field, followed by YouTube course suggestions to help users upskill.

---

## 📽️ Project Demo Videos

🎬 Watch the full project demonstration (Admin + User Panel):  
[🔗 Click here to view on Google Drive](https://drive.google.com/drive/folders/1OC9LZl9O3Da5bEktC8NSHyu-irlFp3p_?usp=sharing)


## 🚀 Features

- Upload and analyze resumes in PDF/DOC/DOCX format
- Extract skills, education, and experience using NLP
- Predict the most suitable career role using a trained ML model
- Recommend YouTube courses based on the predicted role
- Admin dashboard to view resume analytics and role distribution
- Resume data stored in a SQL database for further analysis

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python UI framework)
- **Backend:** Python, scikit-learn, spaCy, pyresparser, pdfminer.six, docx2txt
- **Database:** MySQL
- **Machine Learning:** Naive Bayes Classifier
- **Others:** Pandas, Regex, Joblib

---

## 📂 Project Structure

```

├── train\_model.py              # Trains and saves the ML model
├── app.py                      # Main Streamlit frontend file
├── Courses.py                  # Maps roles to YouTube course recommendations
├── resume\_parser.py            # Handles resume parsing logic
├── utils/                      # Utility scripts and config files
├── database.sql                # MySQL schema for storing parsed data
├── large\_resume\_data.csv       # Dataset used for ML training
├── models/                     # Contains saved ML model and encoders
└── README.md

````

---

## 🧠 How It Works

1. User uploads a resume file via the Streamlit interface.
2. Resume content is extracted using `pyresparser`, `pdfminer`, or `docx2txt`.
3. Parsed skills are vectorized and passed to the trained ML model.
4. The model predicts a role (e.g., Data Scientist, Web Developer).
5. Recommended YouTube courses for the role are displayed to the user.
6. All data is stored in a MySQL database for admin analytics.

---

## 🧪 Machine Learning Model

- Dataset: `large_resume_data.csv` (skills and target roles)
- Algorithm: Naive Bayes (Multinomial)
- Libraries: scikit-learn, joblib
- Preprocessing: CountVectorizer, LabelEncoder

---

## 🖼️ Sample Screenshots

*To be added after deployment or local run screenshots.*

---

## 📊 Admin Panel Features

- View all uploaded resumes and predicted roles
- Visualize role distribution with pie charts
- Export data if needed for further HR analysis

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
pip install -r requirements.txt
streamlit run app.py
````

> Make sure MySQL is running and properly connected. Update DB credentials in the code if needed.

---

## 📁 Dataset

* The dataset `large_resume_data.csv` contains skill-role pairs.
* You can expand it for better model accuracy.

---

## 🧑‍💻 Author

**Adarsh Kumar Sahu**
Solo Developer | B.Tech CSE | KIIT Bhubaneswar
📧 Email: [22053745@kiit.ac.in](mailto:22053745@kiit.ac.in)
🔗 LinkedIn: [linkedin.com/in/adarsh-kumar-sahu-638831293](https://www.linkedin.com/in/adarsh-kumar-sahu-638831293/)

---


## 🌐 Deployment (Optional)

Currently runs locally via Streamlit. Can be deployed on:

* [Streamlit Cloud](https://streamlit.io/cloud)
* Render.com
* Vercel (for frontend) + Flask backend

---

## 🙌 Acknowledgments

* [pyresparser](https://github.com/OmkarPathak/pyresparser)
* [spaCy](https://spacy.io/)
* [scikit-learn](https://scikit-learn.org/)

```
