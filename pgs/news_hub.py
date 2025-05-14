
from __future__ import annotations

import streamlit as st 
import sys
import tempfile
import os



sys.path.insert(1, './modules')

from upload_file_rag import get_qa_chain, query_system

from dotenv import load_dotenv

load_dotenv()



st.markdown(
    """
    <div class=title>
        <div style=" justify-content: center;">
            <h1 style="text-align: center; padding: 5px; color: #F52887;">News Hub 📰</h1>
            <p style="text-align: center;">Informed. Included. Inspired</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.image('https://media.licdn.com/dms/image/v2/D4D12AQENDMtmA8iywg/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1691841691211?e=2147483647&v=beta&t=AqFVKFoQNBrUGPCffdtccgAnhXiCM4esi6BN-iSrH30', width=900)


uploaded_files = st.file_uploader('Upload News pdf', type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:

        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        # Initialize QA chain from saved file
        qa_chain = get_qa_chain(temp_path)

        col1, col2 = st.columns(2)

        with col1:

            # Initialize session state for chat history
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

            # Display chat history
            for message in st.session_state.messages:

                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


            if prompt := st.chat_input("How may I help?", key='RAG chat'):
                # Append user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate AI response
                chat_output = query_system(prompt, qa_chain)
                
                # Append AI response
                with st.chat_message("assistant"):
                    st.markdown(chat_output)

                st.session_state.messages.append({"role": "assistant", "content": chat_output})


        with col2: 
            with st.expander('More information..'):
                st.write('View more informstion')



