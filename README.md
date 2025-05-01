# 🧠 AI Resume Analyzer & Career Recommendation System

A Machine Learning-based web application that analyzes resumes, predicts the most suitable career field based on extracted skills, and recommends relevant online courses to improve employability.

---

## 📌 Problem Statement

Job seekers often struggle to identify which roles best suit their skills and what to improve. Our system solves this by automatically analyzing uploaded resumes, predicting a career path, and recommending skill-specific courses.

---

## 🚀 Features

- 📤 Upload resumes in PDF/DOC/DOCX format  
- 🧠 Extract skills using NLP (pyresparser, spaCy)  
- 🤖 Predict career field using a Naive Bayes classifier  
- 🎓 Recommend skills and curated YouTube courses  
- 📊 Admin dashboard with user data and pie chart analytics  
- 💾 MySQL database integration for storing results  

---

## 💡 Technologies Used

| Component        | Technology                                |
|------------------|--------------------------------------------|
| Frontend         | Streamlit                                 |
| Backend          | Python                                     |
| NLP              | pyresparser, spaCy, nltk, pdfminer, docx2txt |
| Machine Learning | scikit-learn (Naive Bayes, TF-IDF Vectorizer) |
| Database         | MySQL                                      |
| Visualization    | Plotly, Streamlit Tags                     |
| Admin Panel      | Streamlit, MySQL                           |

---

## 📁 Project Structure

```
├── app.py                      # Main Streamlit app
├── model/
│   ├── train_model.py         # ML training script
│   ├── career_model.pkl       # Trained classifier
│   ├── vectorizer.pkl         # TF-IDF vectorizer
│   └── label_encoder.pkl      # Label encoder
├── utils/
│   ├── extract_skills.py      # Resume parsing logic
│   └── Courses.py             # Course mapping logic
├── database/
│   ├── db_config.py           # MySQL connection file
│   └── schema.sql             # DB schema
├── admin/
│   └── dashboard.py           # Admin dashboard
├── data/
│   └── large_resume_data.csv  # Training dataset
├── README.md
├── requirements.txt
```

---

## ⚙️ Installation

1. **Clone the repository**  
```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
```

2. **Install dependencies**  
```bash
pip install -r requirements.txt
```

3. **Set up MySQL database**  
- Create a database (e.g., `resumeDB`)
- Run `schema.sql` to create tables
- Update `db_config.py` with your DB credentials

4. **Run the application**  
```bash
streamlit run app.py
```

---

## 📊 Dataset

- `large_resume_data.csv`  
- Columns:  
  - `skills` – extracted skill keywords  
  - `predicted_role` – target job role for training  

---

## 🔐 Admin Panel

Admin can:
- View analyzed resume data
- See pie charts for predicted roles and experience levels
- Export data if needed

> Admin credentials can be modified in `dashboard.py`.

---

## ✅ Results

- Skill extraction success rate: ~85% for structured resumes  
- Career field prediction accuracy: ~89% (Naive Bayes classifier)  
- Average processing time per resume: <10 seconds  

---

## 👨‍💻 Team Contributions

| Member | Contribution |
|--------|-------------|
| Member 1 | Resume Parsing & NLP |
| Member 2 | ML Model Training & Evaluation |
| Member 3 | Streamlit Frontend Design |
| Member 4 | Backend Integration & MySQL |
| Member 5 | Admin Panel & Visual Analytics |
| Member 6 | Course Recommendation & Testing |

---

## 🔮 Future Improvements

- Use BERT or other advanced NLP models  
- Real-time course integration (e.g., Coursera, Udemy API)  
- Upload multiple resumes at once  
- Add job matching feature using live job APIs  

---

## 📃 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- Apna College (for guidance & inspiration)  
- Pyresparser for resume parsing  
- Streamlit for UI  
- scikit-learn for ML  
```
