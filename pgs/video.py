import streamlit as st
import africastalking
import os
import sys
import requests
import pyttsx3
import google.generativeai as genai


from streamlit_tags import st_tags
import streamlit_scrollable_textbox as stx



sys.path.insert(1, './modules')
print(sys.path.insert(1, '../modules/'))

from youtube_transcription import get_transcript, extract_youtube_code
from upload_file_rag import text_to_speech
from func import news_summary, news_category, news_NER, user_q_and_a, news_translation, news_sentiment, news_impact, news_hashtags, news_agenda_detection, news_highlight_key_quotes, news_local_language_translation, news_ama_chat

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime


st.image("https://nairobileo.co.ke/storage/uploads/2021/04/IMG-20210424130544.jpg", width=800)


col1, col2 = st.columns([7, 1])

with col1:
    try:
        url = st.text_input(':material/youtube_activity: YouTube URL...')
        
        if url:
            video_id = extract_youtube_code(url)

        else: 
            st.error('Invalid YouTube URL', icon="⚠️")

    except Exception as e:
        st.error(f'Invalid link {e}', icon="⚠️")



with col2:
    st.write('')
    st.write('')
    submit = st.button('Search', type="primary", icon=":material/search:")


if submit == True:
    context_data, summary = get_transcript(url)

    get_news_summary = news_summary(context_data)
    get_news_category = news_category(context_data)
    get_news_NER = news_NER(context_data)
    # get_user_answers = user_q_and_a(context_data)
    
    get_news_sentiment = news_sentiment(context_data)
    get_news_impact = news_impact(context_data)
    get_news_hashtags = news_hashtags(context_data)
    get_news_agenda =news_agenda_detection(context_data)
    get_news_highlight = news_highlight_key_quotes(context_data)
    get_news_local_lang = news_local_language_translation(context_data)
    # get_news_ama = news_ama_chat(context_data)

    swahili = st.toggle("Swahili")

    col1_1, col1_2 = st.columns(2, border=True)


    with col1_1:

        # st.markdown('### Summary')

        # st.write(summary)

        languages_options = ["Afrikaans", "Sheng", "Kikuyu", 'Luo', 'Kamba', 'Kalenjine', "Amharic", "Zulu", "Yoruba", "Hausa", "Shona", "Fula", "Xhosa", "Oromo", "Igbo", "Khoisan", "French", "Spanish", "Finish", "Portoguese", "Swahili", "Mandarin", "German", "Arabic", "Turkish", "Russian", "Italian", "Hindi", "Korean", "Japanese"]



        st.markdown('#### **In Brief**')
        st.write(get_news_summary)
        st.write(f'**Category**: {get_news_category}')

        with st.expander('🌐 **Translate:**'):
            translate_to = st.pills('', options=languages_options)
            get_news_translation = news_translation(translate_to, context_data)

            if translate_to:
                key = f"translation_{translate_to}"
                if key not in st.session_state:
                    st.session_state[key] = news_translation(translate_to, context_data)

                st.write(f'**{translate_to} Translation:**')
                st.write(st.session_state[key])


        with st.expander(f'🗞️ **Name Entity Recognition**:'):
            st.write(f'{get_news_NER}')

        with st.expander(f'📤 **Sentiment**: '):   
            st.write(f'{get_news_sentiment}')

        with st.expander(f'🎯 **Impact**: '):   
            st.write(f'{get_news_impact}')

        with st.expander(f'🏹 **Agenda**:'):   
            st.write(f'{get_news_agenda}')

        with st.expander(f'🧾 **Highlight Quotes**:'):   
            st.write(f'{get_news_highlight}')

        with st.expander(f'💭 **Q&A**'):
            st.write('This is the Q&A Section')
        # st.write(f'**Category**: {get_news_category}')


    with col1_2:
        if "youtube.com" in url or "youtu.be" in url:
            st.video(url)

            stx.scrollableTextbox(context_data, height = 300)

            
            audio_filename = text_to_speech(context_data)
    
            audio_file = open(audio_filename, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
            
            



# def download_audio_from_youtube(youtube_url, output_path="audio.mp3"):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'outtmpl': output_path,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#         }],
#         'quiet': True
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([youtube_url])
#     return output_path

# def transcribe_with_whisper(youtube_url):
#     audio_file = download_audio_from_youtube(youtube_url)
#     model = whisper.load_model("base")  # or "small", "medium", "large" for better accuracy
#     result = model.transcribe(audio_file, language="sw")  # Or just let it auto-detect
#     return result['text']


# st.write(transcribe_with_whisper(url))

# keywords = st_tags(
#     label='# Enter Keywords:',
#     text='Press enter to add more',
#     value=['Zero', 'One', 'Two'],
#     suggestions=['five', 'six', 'seven', 
#                  'eight', 'nine', 'three', 
#                  'eleven', 'ten', 'four'],
#     maxtags = 4,
#     key='1')
