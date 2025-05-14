import streamlit as st
import africastalking
import os
import sys
import requests
import google.generativeai as genai

from st_social_media_links import SocialMediaIcons


from datetime import datetime

sys.path.insert(1, './modules')
print(sys.path.insert(1, '../modules/'))

from func import generate_otp, send_sms, make_call, social_media_news, detailed_news



from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime




st.image("https://www.techslang.com/wp-content/uploads/2020/06/automated-jpurnalism-e1593421848489.jpg", width=900)


with st.form("news_form"):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("📰 Title", placeholder="Enter the main headline")
        subtitle = st.text_input("🗞️ Subtitle", placeholder="Enter a supporting headline")
        subcontext = st.text_area("📌 Subcontext", placeholder="Brief summary or context", height=100)
        author = st.text_input("✍️ Author", placeholder="e.g. Jane Doe")

        col1_1, col1_2 = st.columns(2)

        with col1_1:
            date = st.date_input("🗓️ Date", value=datetime.now())
        
        with col1_2:
            time = st.time_input('Time', value="now")

    with col2:
        context = st.text_area("🧾 Full Context", placeholder="Full news story or report", height=320)
        image = st.file_uploader("🖼️ Upload Image", type=["jpg", "jpeg", "png"])
        

    

    submitted = st.form_submit_button("📤 Submit News", type="primary", use_container_width=True)

    if submitted:
        st.success("✅ News article submitted successfully!")

        st.image(image, width=700)

        news_data_string = f"""
            Title: {title}
            Subtitle: {subtitle}
            Author: {author}
            Date & Time: {date} {time}
            Subcontext: {subcontext}

            Full Context:
            {context}
            """

        col2_1, col2_2 = st.columns(2, border=True)

        with col2_1:
            news_details = detailed_news(news_data_string)
            news_details_markdown = st.write(news_details)
            # st.text_area("Detailed News Article", value=st.write(news_details), height=1000, key="long_news")


        with col2_2:
            post = social_media_news(news_data_string)
            post_markdown = st.write(post)
            # st.text_area("Social Media Post", value=st.write(post), height=500, key="summary_news")

            social_media_links = [
                'https://www.x.com',
                'https://www.facebook.com',
                'https://www.instagram.com',
                'https:/www.whatsapp.com',
                
                ]


            social_icons = SocialMediaIcons(social_media_links)
            social_icons.render()

        

