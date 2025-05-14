import string
import random
import secrets
import re
import os
import bcrypt
import africastalking
import streamlit as st 
import google.generativeai as genai


from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

africastalking.initialize(
    username='EMID',
    api_key = os.getenv("AT_API_KEY")
)

sms = africastalking.SMS
airtime = africastalking.Airtime
voice = africastalking.Voice

def send_sms(phone_number, otp_sms):
    # amount = "10"
    # currency_code = "KES"

    recipients = [f"+254{str(phone_number)}"]

    # airtime_rec = "+254" + str(phone_number)

    # print(recipients)
    # print(phone_number)

    # Set your message
    message = f"{otp_sms}";

    # Set your shortCode or senderId
    sender = 20880

    try:
        # responses = airtime.send(phone_number=airtime_rec, amount=amount, currency_code=currency_code)
        response = sms.send(message, recipients, sender)

        # print(response)

        # print(responses)

    except Exception as e:
        print(f'Houston, we have a problem: {e}')

    st.toast(f"OTP Sent Successfully")


def init_message(first_name, phone_number):

    recipients = [f"+254{str(phone_number)}"]

    # print(recipients)
    # print(phone_number)

    # Set your message
    message = f"Hi {first_name}, welcome to ExposHer! We're excited to have you join our sisterhood of innovators, leaders, and changemakers. \n#WomenWhoLead";

    # Set your shortCode or senderId
    sender = 20880

    try:
        response = sms.send(message, recipients, sender)

        # print(response)

    except Exception as e:
        print(f'Houston, we have a problem: {e}')

    st.toast(f"Account Created Successfully")



def make_call(phone_number):    
  
  # Set your Africa's Talking phone number in international format
    callFrom = "+254730731123"
  
  # Set the numbers you want to call to in a comma-separated list
    callTo   = [f"+254{str(phone_number)}"]
    
    try:
  # Make the call
        result = voice.call(callFrom, callTo)
        # print (result)
        return result
    except Exception as e:
        # print ("Encountered an error while making the call:%s" %str(e))
        return f"Encountered an error while making the call:%s" %str(e)



def generate_otp(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))



def check_and_encrypt_password(password: str, confirm_password: str):
    
    if password != confirm_password:
        return st.error("Error: Passwords do not match!")

    if len(password) < 8:
        return st.error(f"Error: Password must be at least 8 characters long!")
    
    if not re.search(r"[A-Z]", password):
        return st.error(f"Error: Password must contain at least one uppercase letter!")
    
    if not re.search(r"\d", password):
        return st.error(f"Error: Password must contain at least one number!")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return st.error(f"Error: Password must contain at least one special character!")

    # Encrypt password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return st.text_input(label='Encrypted password', value=hashed_password.decode(), type='password')



def news_summary(prompt):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = f"""
        
            You are a professional news summarizer. Given a transcript, provide a concise, factual, and clear summary in 3–5 sentences. 
            
            Retain key information, names, dates, and outcomes. Assume the audience has no prior knowledge.

            """

            )


    response = model.generate_content(
        "Summarize the following news transcript: " + prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



def news_category(prompt):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = f"""

                You are a news classification expert. Given a transcript, determine the most appropriate category for the story. 

                Use broad categories like: Politics, Sports, Business, Crime, Environment, Health, Culture, Technology, Education, or Other.


            """

            )


    response = model.generate_content(
        "Classify the following news report into one of the standard news categories: " + prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



def news_NER(prompt):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = f"""
    
                You are an advanced NER (Named Entity Recognition) model. Extract and list all names, places, organizations, events, and dates mentioned in the transcript.

            """

            )


    response = model.generate_content(
        "Extract all named entities from the following news content and organize them under: People, Places, Organizations, Dates, Events: " + prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



def user_q_and_a(prompt, user_question):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = f"""

            You are a smart assistant trained on Kenyan local news. Based on the transcript provided, answer user questions factually and directly. 

            If the answer is not found in the transcript, politely state that.
            

            """

            )


    response = model.generate_content(
        f"Based on this news content: \n{context_data} \nAnswer this question: {user_question}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text




def news_translation(language, prompt):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a translation expert. Translate any word or local dialect spoken in the transcript to {language}, while preserving tone and meaning. 

            Retain proper nouns and don’t translate names.

            """

            )


    response = model.generate_content(
        f"Translate the following news transcript to {language}: {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



def news_sentiment(prompt):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a sentiment analyst for media content. Based on the transcript, determine the emotional tone conveyed (e.g., Positive, Negative, Neutral) 

            and explain briefly why.

            """

            )


    response = model.generate_content(
        f"What is the overall sentiment of the following news report? Provide a label (Positive/Negative/Neutral) and a short explanation: {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def news_impact(prompt):

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You assess real-world impact of news. Based on the transcript, analyze and describe how this story may affect local citizens, government policy, 

            economy, or social life.

            """

            )


    response = model.generate_content(
        f"What is the potential local or national impact of the following news story? {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def news_hashtags(prompt):
    
    

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a social media analyst. Read the transcript and generate 3–5 relevant, short, and trending-style hashtags that could be used for posting this 

            news on platforms like Twitter or TikTok.

            """

            )


    response = model.generate_content(
        f"Generate relevant hashtags for this news story: {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def news_agenda_detection(prompt):
    

    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a media bias detector. Determine if the news report has any implied political, economic, or social agenda. If yes, describe it briefly. 

            If neutral, state so.

            """

            )


    response = model.generate_content(
        f"Does this news transcript contain any bias or hidden agenda? Analyze and explain: {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def news_highlight_key_quotes(prompt):
    
  
    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a transcription analyzer. Extract the 2–3 most important or impactful quotes from the transcript. They should capture the essence or emotion of 

            the story.

            """

            )


    response = model.generate_content(
        f"Extract the most important quotes from the following news content: {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def news_local_language_translation(prompt):
    
  
    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a translator for Swahili-speaking and Sheng-speaking audiences. Translate the transcript from English or code-mixed format into clear, 

            conversational Swahili or Sheng based on user preference.

            """

            )


    response = model.generate_content(
        f"Translate the following news transcript into [Swahili/Sheng]: {prompt}",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def news_ama_chat(prompt):
    
  
    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = f"""
        
            You are a news discussion assistant. Based on the news transcript, allow users to ask questions freely and engage in follow-up chat and also allows users to ask any question about the news, even hypothetical or opinion-based.. 

            Answer contextually and offer insights or background if possible.

            """

            )


    response = model.generate_content(
        f"Based on this news transcript: {prompt} \nHere's the user's question: [User’s AMA-style question]",
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



def detailed_news(prompt):
    
  
    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = f"""
        
            You are an expert African news writer and editor. Your task is to expand brief news summaries into fully detailed, coherent, and engaging articles. 

            Your writing should reflect deep context, journalistic clarity, local relevance, and insightful commentary. Ensure language is formal yet accessible, suitable for a media house audience. Where appropriate, include context about location, persons, and significance. Conclude with locally relevant hashtags, including #nationmedia.

            """

            )


    response = model.generate_content(
        f"""
            Based on the following brief news input, write a full-length, in-depth news article suitable for publication by a professional media outlet in Africa.

            Ensure the article is:
            - Well-structured with an engaging headline, intro paragraph, and clear body flow.
            - Enriched with relevant local or regional context.
            - Accurate and human-readable.
            - Ends with a short block of localized hashtags (3-5) including #nationmedia.

            Here is the input:

            {prompt}

            Write the complete article below:
        """,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text



def social_media_news(prompt):
    
  
    model = genai.GenerativeModel("gemini-2.0-flash", 

        system_instruction = """
        
            You are a professional social media editor for a major African news outlet. Your task is to convert detailed news content into short, catchy, and informative posts for platforms like X (formerly Twitter) and Facebook. 

            Maintain clarity, brevity, and relevance. Use an engaging tone that captures attention. Include 2-3 relevant localized hashtags, ending with #nationmedia.
            
            """

            )


    response = model.generate_content(
        f"""
        Create a short and compelling social media post from the following news content.

        - Keep it under 280 characters for X, slightly longer for Facebook if needed.
        - Make it attention-grabbing and easy to understand.
        - End with 2-3 relevant localized hashtags including #nationmedia.

        News content:
        {prompt}

        Write the social media post:

        """,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1, 
      )
    
    )


    
    return response.text


def welcome_message(first_name, phone_number):

    recipients = [f"+254{str(phone_number)}"]

    print(recipients)
    print(phone_number)

    # Set your message
    message = f"Hi {first_name}, Your registration was successful. We are excited to have you on board. Explore the latest updates and get personalized news insights anytime.";

    # Set your shortCode or senderId
    sender = 20880

    try:
        response = sms.send(message, recipients, sender)

        print(response)

    except Exception as e:
        print(f'Houston, we have a problem: {e}')

    st.toast(f"Account Created Successfully")