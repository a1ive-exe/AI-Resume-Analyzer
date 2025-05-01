import pickle
import joblib
import numpy as np
import pandas as pd
import re
import os
import io
from pdfminer.high_level import extract_text
import streamlit as st
import pandas as pd
import base64,random
import time,datetime
#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
#import pafy #for uploading youtube videos
#from pytube import YouTube
import yt_dlp
import plotly.express as px #to create visualisations at the admin session
import nltk
nltk.download('stopwords')


# def fetch_yt_video(link):
#     video = pafy.new(link)
#     return video.title

# def fetch_yt_video(link):
#     try:
#         video = YouTube(link)
#         return video.title
#     except Exception as e:
#         return f"Error fetching video: {e}"

# Load ML model and encoders
# with open('career_model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# with open('vectorizer.pkl', 'rb') as vec_file:
#     vectorizer = pickle.load(vec_file)

# with open('label_encoder.pkl', 'rb') as le_file:
#     label_encoder = pickle.load(le_file)



def fetch_yt_video(link):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('title', 'Title not found')
    except Exception as e:
        return f"✅ Error fetching video: {e}"
    
def get_table_download_link(df,filename,text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href



def pdf_reader(file):
    # Extract text using pdfminer
    text = extract_text(file)

    # Clean up text by replacing unwanted line breaks
    text_cleaned = " ".join(text.splitlines())

    # Display cleaned-up text in Streamlit
    # st.write("Extracted Resume Text:")
    # st.text(text_cleaned)  # This will ensure text is displayed correctly

    return text_cleaned

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course





#CONNECT TO DATABASE

connection = pymysql.connect(host='localhost',user='root',password='2003@Adi',db='cv')
cursor = connection.cursor()

# def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
#     DB_table_name = 'user_data'
#     insert_sql = "insert into " + DB_table_name + """
#     values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#     rec_values = (name, email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses)
#     cursor.execute(insert_sql, rec_values)
#     connection.commit()

def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    
    def encode_if_needed(value):
        if isinstance(value, str):
            return value.encode('utf-8').decode('utf-8')
        return value

    rec_values = tuple(encode_if_needed(val) for val in (name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses))
    
    cursor.execute(insert_sql, rec_values)
    connection.commit()



st.set_page_config(
   page_title="AI Resume Analyzer",
   page_icon='./Logo/logo2.png',
)
def run():
    # At the top-level (outside run())
    model = joblib.load('career_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    label_encoder = joblib.load('label_encoder.pkl')


    img = Image.open('./Logo/Lo.png')
    # img = img.resize((250,250))
    st.image(img)
   # st.title("AI Resume Analyser")
    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    link = '[©Developed by Ipsita Mams team]()'
    st.sidebar.markdown(link, unsafe_allow_html=True)


    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
    cursor.execute(db_sql)

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(500) NOT NULL,
                     Email_ID VARCHAR(500) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field BLOB NOT NULL,
                     User_level BLOB NOT NULL,
                     Actual_skills BLOB NOT NULL,
                     Recommended_skills BLOB NOT NULL,
                     Recommended_courses BLOB NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    if choice == 'User':
        st.markdown('''<h3 style='text-align: left; color: #00e013;'> Upload your resume, and get smart recommendations</h3>''',
                    unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Uploading your Resume...'):
                time.sleep(4)
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data and 'skills' in resume_data:
                skills = resume_data['skills']

                # ML Prediction: Join skills into a string and vectorize
                skills_text = " ".join(skills).lower()
                skills_vec = vectorizer.transform([skills_text])

                # Predict using the model
                predicted_role_encoded = model.predict(skills_vec)
                predicted_role = label_encoder.inverse_transform(predicted_role_encoded)[0]

                # Show prediction to user
                st.subheader("**Predicted Career Role Based on Resume**")
                st.success(f"🔮 {predicted_role}")
                        
            def decode_ascii_list(val):
                if isinstance(val, list) and all(isinstance(x, int) for x in val):
                    return ''.join(map(chr, val))
                return val

            # Apply the fix to resume_data fields
            resume_data['name'] = decode_ascii_list(resume_data.get('name'))
            resume_data['email'] = decode_ascii_list(resume_data.get('email'))
            resume_data['skills'] = decode_ascii_list(resume_data.get('skills'))
            
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello "+ resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >=3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)

                # st.subheader("**Skills Recommendation💡**")
                ## Skill shows
                keywords = st_tags(label='### Your Current Skills',
                text='See our skills recommendation below',
                    value=resume_data['skills'],key = '1  ')

                ##  keywords
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                web_keyword = ['html', 'css', 'javascript', 'react', 'node', 'frontend', 'front-end', 'angular', 'vue','react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                # ## Courses recommendation
                # for i in resume_data['skills']:
                #     ## Data science recommendation
                #     if i.lower() in ds_keyword:
                #         print(i.lower())
                #         reco_field = 'Data Science'
                #         #st.success("** Our analysis says you are looking for Data Science Jobs.**")
                #         recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #         text='Recommended skills generated from System',value=recommended_skills,key = '2')
                #         # st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job</h4>''',unsafe_allow_html=True)
                #         # rec_course = course_recommender(ds_course)
                #         break

                #     ## Web development recommendation
                #     elif i.lower() in web_keyword:
                #         print(i.lower())
                #         reco_field = 'Web Development'
                #         #st.success("** Our analysis says you are looking for Web Development Jobs **")
                #         recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                #         # recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #         text='Recommended skills generated from System',value=recommended_skills,key = '3')
                #         # st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                #         # rec_course = course_recommender(web_course)
                #         break

                #     ## Android App Development
                #     elif i.lower() in android_keyword:
                #         print(i.lower())
                #         reco_field = 'Android Development'
                #         #st.success("** Our analysis says you are looking for Android App Development Jobs **")
                #         recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #         text='Recommended skills generated from System',value=recommended_skills,key = '4')
                #         # st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                #         # rec_course = course_recommender(android_course)
                #         break

                #     ## IOS App Development
                #     elif i.lower() in ios_keyword:
                #         print(i.lower())
                #         reco_field = 'IOS Development'
                #         #st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                #         recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #         text='Recommended skills generated from System',value=recommended_skills,key = '5')
                #         # st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                #         # rec_course = course_recommender(ios_course)
                #         break

                #     ## Ui-UX Recommendation
                #     elif i.lower() in uiux_keyword:
                #         print(i.lower())
                #         reco_field = 'UI-UX Development'
                #         #st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                #         recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                #         recommended_keywords = st_tags(label='### Recommended skills for you.',
                #         text='Recommended skills generated from System',value=recommended_skills,key = '6')
                #         # st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                #         # rec_course = course_recommender(uiux_course)
                #         break
                # # Show predicted career field
                # st.success(f"✅ Based on your resume, you're suited for: **{predicted_role}**")

                # # # Recommend courses based on predicted role
                # # if predicted_role == 'Data Science':
                # #     st.subheader("📘 Recommended Courses for Data Science:")
                # #     for course in ds_course:
                # #         st.markdown(f"- [{course['title']}]({course['link']})")

                # # elif predicted_role == 'Web Development':
                # #     st.subheader("🌐 Recommended Courses for Web Development:")
                # #     for course in web_course:
                # #         st.markdown(f"- [{course['title']}]({course['link']})")

                # # elif predicted_role == 'Android Development':
                # #     st.subheader("📱 Recommended Courses for Android Development:")
                # #     for course in android_course:
                # #         st.markdown(f"- [{course['title']}]({course['link']})")

                # # elif predicted_role == 'iOS Development':
                # #     st.subheader("🍏 Recommended Courses for iOS Development:")
                # #     for course in ios_course:
                # #         st.markdown(f"- [{course['title']}]({course['link']})")

                # # elif predicted_role == 'UI/UX':
                # #     st.subheader("🎨 Recommended Courses for UI/UX Design:")
                # #     for course in uiux_course:
                # #         st.markdown(f"- [{course['title']}]({course['link']})")


                # if reco_field == 'Data Scientist':
                #     st.subheader("📘 Recommended Courses for Data Science:")
                #     for course in ds_course:
                #         st.markdown(f"- [{course[0]}]({course[1]})")
                #     recommended_skills = ['Data Visualization', 'Statistical Modeling', 'Pandas', 'NumPy', 'Machine Learning', 'Deep Learning', 'Scikit-learn', 'TensorFlow']

                # elif reco_field == 'Web Developer':
                #     st.subheader("🌐 Recommended Courses for Web Development:")
                #     for course in web_course:
                #         st.markdown(f"- [{course[0]}]({course[1]})")
                #     recommended_skills = ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Express', 'MongoDB', 'REST APIs']

                # elif reco_field == 'Android Developer':
                #     st.subheader("📱 Recommended Courses for Android Development:")
                #     for course in android_course:
                #         st.markdown(f"- [{course[0]}]({course[1]})")
                #     recommended_skills = ['Java', 'Kotlin', 'Flutter', 'Android Studio', 'SQLite', 'Firebase']

                # elif reco_field == 'iOS Developer':
                #     st.subheader("🍏 Recommended Courses for iOS Development:")
                #     for course in ios_course:
                #         st.markdown(f"- [{course[0]}]({course[1]})")
                #     recommended_skills = ['Swift', 'Objective-C', 'Xcode', 'Cocoa Touch', 'Auto Layout', 'Core Data']

                # elif reco_field == 'UI/UX Designer':
                #     st.subheader("🎨 Recommended Courses for UI/UX Design:")
                #     for course in uiux_course:
                #         st.markdown(f"- [{course[0]}]({course[1]})")
                #     recommended_skills = ['Figma', 'Adobe XD', 'Wireframing', 'Prototyping', 'User Research', 'Interaction Design']

                # # else:
                # #     recommended_skills = []
                # #     st.warning("⚠️ No specific skill/course recommendation found for the predicted role.")

                # Skill-based field recommendation
                # reco_field = None
                # recommended_skills = []

                # for i in resume_data['skills']:
                #     skill = i.lower()

                #     if skill in ds_keyword:
                #         reco_field = 'Data Scientist'
                #         recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification',
                #                             'Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability',
                #                             'Scikit-learn','Tensorflow',"Flask",'Streamlit']
                #         break

                #     elif skill in web_keyword:
                #         reco_field = 'Web Developer'
                #         recommended_skills = ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Express', 'MongoDB', 'REST APIs']
                #         break

                #     elif skill in android_keyword:
                #         reco_field = 'Android Developer'
                #         recommended_skills = ['Java','Kotlin','Flutter','Android Studio','SQLite','Firebase']
                #         break

                #     elif skill in ios_keyword:
                #         reco_field = 'iOS Developer'
                #         recommended_skills = ['Swift','Objective-C','Xcode','Cocoa Touch','Auto Layout','Core Data']
                #         break

                #     elif skill in uiux_keyword:
                #         reco_field = 'UI/UX Designer'
                #         recommended_skills = ['Figma','Adobe XD','Wireframing','Prototyping','User Research','Interaction Design']
                #         break

                # # Show predicted role from ML model
                # # st.success(f"✅ Based on your resume, you're suited for: **{predicted_role}**")

                # # Show recommended skills based on rule-based analysis
                # if reco_field:
                #     st.info(f"🔍 Matched skills suggest you may fit the role: **{reco_field}**")
                #     st_tags(label='### Recommended skills for you:',
                #             #text='Skills generated from our system analysis',
                #             value=recommended_skills,
                #             key='recommended_skills')

                #     # Display courses
                #     course_map = {
                #         'Data Scientist': ds_course,
                #         'Web Developer': web_course,
                #         'Android Developer': android_course,
                #         'iOS Developer': ios_course,
                #         'UI/UX Designer': uiux_course
                #     }

                #     if reco_field in course_map:
                #         course_icon = {
                #             'Data Scientist': "📘",
                #             'Web Developer': "🌐",
                #             'Android Developer': "📱",
                #             'iOS Developer': "🍏",
                #             'UI/UX Designer': "🎨"
                #         }

                #         st.subheader(f"{course_icon[reco_field]} Recommended Courses for {reco_field}:")
                #         for course in course_map[reco_field]:
                #             st.markdown(f"- [{course[0]}]({course[1]})")
                # else:
                #     st.warning("⚠️ No specific skill/course recommendation found based on keyword match.")
                # Map predicted roles to skills and course recommendations
                recommended_skills_map = {
                    'Data Scientist': ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification',
                                    'Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability',
                                    'Scikit-learn','Tensorflow',"Flask",'Streamlit'],
                    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Express', 'MongoDB', 'REST APIs'],
                    'Android Developer': ['Java','Kotlin','Flutter','Android Studio','SQLite','Firebase'],
                    'iOS Developer': ['Swift','Objective-C','Xcode','Cocoa Touch','Auto Layout','Core Data'],
                    'UI/UX Designer': ['Figma','Adobe XD','Wireframing','Prototyping','User Research','Interaction Design']
                }

                course_map = {
                    'Data Scientist': ds_course,
                    'Web Developer': web_course,
                    'Android Developer': android_course,
                    'iOS Developer': ios_course,
                    'UI/UX Designer': uiux_course
                }

                course_icon = {
                    'Data Scientist': "📘",
                    'Web Developer': "🌐",
                    'Android Developer': "📱",
                    'iOS Developer': "🍏",
                    'UI/UX Designer': "🎨"
                }
                # Normalize predicted roles that don't exactly match keys in the maps
                role_aliases = {
                    'Frontend Developer': 'Web Developer',
                    'Front-End Developer': 'Web Developer',
                    'Back-End Developer': 'Web Developer',  # Optional
                    'Full Stack Developer': 'Web Developer',  # Optional
                }

                predicted_role = role_aliases.get(predicted_role, predicted_role)

                # Final field to use for recommendations = ML predicted role
                reco_field = predicted_role
                recommended_skills = recommended_skills_map.get(reco_field, [])

                # Show matched field
                if reco_field in recommended_skills_map:
                    st.info(f"🔍 Based on your resume, you're suited for: **{reco_field}**")
                    st_tags(label='### Recommended skills for you:',
                            value=recommended_skills,
                            key='recommended_skills')

                # Show courses
                if reco_field in course_map:
                    st.subheader(f"{course_icon[reco_field]} Recommended Courses for {reco_field}:")
                    for course in course_map[reco_field]:
                        st.markdown(f"- [{course[0]}]({course[1]})")
                else:
                    st.warning("⚠️ No specific skill/course recommendation found for this role.")

                # ML-based career field prediction from skills
                skills = resume_data['skills']
                skills_str = ' '.join(skills)

                # Load model, encoder and vectorizer
                model = joblib.load('career_model.pkl')
                vectorizer = joblib.load('vectorizer.pkl')
                label_encoder = joblib.load('label_encoder.pkl')


                # Transform and predict
                input_vec = vectorizer.transform([skills_str])
                prediction = model.predict(input_vec)
                reco_field = label_encoder.inverse_transform(prediction)[0]

                # st.success(f"**Our ML model predicts you're aiming for `{reco_field}` roles!**")

                # Course recommendations based on predicted role
                # Normalize the predicted role for flexible matching
                normalized_role = reco_field.lower().strip()

                # if 'data' in normalized_role:
                #     recommended = ds_course
                # elif 'web' in normalized_role or 'full' in normalized_role:
                #     recommended = web_course
                # elif 'android' in normalized_role:
                #     recommended = android_course
                # elif 'ios' in normalized_role:
                #     recommended = ios_course
                # elif 'ui' in normalized_role or 'ux' in normalized_role:
                #     recommended = uiux_course
                # else:
                #     recommended = []


                # st.subheader("Top Recommended Courses:")
                # for course in recommended:
                #     st.markdown(f"[{course[0]}]({course[1]})")



                
                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)

                ### Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡**")
                resume_score = 0
                if 'Summary' in resume_text or 'SUMMARY' in resume_text or 'About Me' in resume_text or 'ABOUT ME' in resume_text:
                   resume_score += 10
                   st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary</h4>''', unsafe_allow_html=True)
                else:
                   st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your Summary, it will give your complete overview to the Recruiters.</h4>''', unsafe_allow_html=True)

                if 'Certification' in resume_text or 'CERTIFICATION' in resume_text:
                    resume_score += 10
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Certifications. Highlighting certifications in your resume helps validate your skills and knowledge.</h4>''', unsafe_allow_html=True)

                if 'Hobbies' in resume_text or 'HOBBIES' in resume_text or 'Interests' in resume_text or 'INTERESTS' in resume_text:
                    resume_score += 10
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Hobbies. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''', unsafe_allow_html=True)

                if 'Education' in resume_text or 'EDUCATION' in resume_text:
                    resume_score += 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Education</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Education. It will show your previous background and schooling.</h4>''', unsafe_allow_html=True)

                if 'Projects' in resume_text or 'PROJECTS' in resume_text:
                    resume_score += 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Projects. It will show that you have done work related to the required position or not.</h4>''', unsafe_allow_html=True)

                if 'Achievements' in resume_text or 'ACHIEVEMENTS' in resume_text:
                    resume_score += 10
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements</h4>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements. Including relevant achievements in your resume showcases your capabilities and proven track record.</h4>''', unsafe_allow_html=True)

                if 'skill' in resume_text or 'skills' in resume_text:
                    resume_score += 20
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Skills</h4>''', unsafe_allow_html=True)
                else:
                     st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Skills. It helps recruiters understand your key competencies.</h4>''', unsafe_allow_html=True)

                
                st.subheader("**Resume Score📝**")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
                st.balloons()

                # Decode any list of ASCII codes into strings before storing
                def decode_if_needed(val):
                    if isinstance(val, list) and all(isinstance(x, int) for x in val):
                        return ''.join(map(chr, val))
                    return val

                name = decode_if_needed(resume_data['name'])
                email = decode_if_needed(resume_data['email'])
                skills = decode_if_needed(resume_data['skills'])
                recommended = decode_if_needed(recommended_skills)
                course = decode_if_needed(rec_course)

                print(type(resume_data['name']), resume_data['name'])
                print(type(reco_field), reco_field)
                print(type(cand_level), cand_level)

                #insert_data(name, email, resume_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, rec_course)

                # insert_data(name, email, str(resume_score), timestamp,
                #             str(resume_data['no_of_pages']), reco_field, cand_level, str(skills),
                #             str(recommended), str(course))

                insert_data(
                    resume_data['name'],
                    resume_data['email'],
                    resume_score,
                    timestamp,
                    resume_data['no_of_pages'],
                    reco_field,              # already a string
                    cand_level,              # already a string
                    ', '.join(skills),       # convert list to clean string
                    ', '.join(recommended),  # same here
                    ', '.join(course)        # same here
                )





                # insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                #               str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                #               str(recommended_skills), str(rec_course))


                ## Resume writing video
                st.header("**Bonus Video for Resume Writing Tips💡**")
                resume_vid = random.choice(resume_videos)
                res_vid_title = fetch_yt_video(resume_vid)
                st.subheader("✅ **"+res_vid_title+"**")
                st.video(resume_vid)



                ## Interview Preparation Video
                st.header("**Bonus Video for Interview Tips💡**")
                interview_vid = random.choice(interview_videos)
                int_vid_title = fetch_yt_video(interview_vid)
                st.subheader("✅ **" + int_vid_title + "**")
                st.video(interview_vid)

                connection.commit()
            else:
                st.error('Something went wrong..')
    else:
        ## Admin Side
        st.success('Welcome to Admin Side')
        #st.sidebar.subheader('**ID / Password Required!**')

        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
    
        if st.button('Login'):
            if ad_user == 'IpsitaMamistheBEST' and ad_password == 'password':
                st.success("Welcome Ipsita Mam !")
                
                # Fetch user data from the database
                cursor.execute('''SELECT * FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's Data**")
                
                # Creating a DataFrame from fetched data
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                'Recommended Course'])
                
                # Displaying data in a table
                st.dataframe(df)
                
                # Providing a download link for the data
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                
                # Admin Side Data for Pie Charts
                query = 'SELECT * FROM user_data;'
                plot_data = pd.read_sql(query, connection)

                # 🔧 Decode bytes to string if needed
                plot_data['Predicted_Field'] = plot_data['Predicted_Field'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
                plot_data['User_level'] = plot_data['User_level'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)


                # Pie chart for Predicted Field Recommendations
                st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                # labels = plot_data['Predicted_Field'].unique()
                # values = plot_data['Predicted_Field'].value_counts()
                # fig = px.pie(plot_data, names=labels, values=values, title='Predicted Field according to the Skills')
                # Clean and unify similar fields
                # Define accepted fields
                valid_fields = [
                    'Data Science', 'Web Development', 'Android Development',
                    'IOS Development', 'UI-UX Development'
                ]

                # Clean and standardize
                field_mapping = {
                    'Data Scientist': 'Data Science',
                    'data science': 'Data Science',
                    'Web Developer': 'Web Development',
                    'iOS Developer': 'IOS Development',
                    'UI-UX Developer': 'UI-UX Development'
                }
                plot_data['Predicted_Field'] = plot_data['Predicted_Field'].replace(field_mapping)

                # Convert to string and strip whitespace
                plot_data['Predicted_Field'] = plot_data['Predicted_Field'].astype(str).str.strip()

                # Assign 'Others' to invalid/unexpected fields (like '2')
                plot_data['Predicted_Field'] = plot_data['Predicted_Field'].apply(
                    lambda x: x if x in valid_fields else 'Others'
                )

                # Value counts
                field_counts = plot_data['Predicted_Field'].value_counts().reset_index()
                field_counts.columns = ['Predicted_Field', 'Count']

                # Plot
                fig = px.pie(field_counts, names='Predicted_Field', values='Count',
                            title='Predicted Field according to the Skills')
                st.plotly_chart(fig, key="predicted_field_chart")


                # st.plotly_chart(fig)

                # Pie chart for User's Experienced Level
                st.subheader("**Pie-Chart for User's Experienced Level**")
                # Count and reset index properly
                user_level_counts = plot_data['User_level'].value_counts().reset_index()
                user_level_counts.columns = ['User_level', 'Count']

                # Pie chart
                fig = px.pie(user_level_counts, names='User_level', values='Count',
                            title="Pie-Chart for User's Experienced Level")
                st.plotly_chart(fig)

            
            else:
                    st.error("Wrong ID & Password Provided")
            
run()