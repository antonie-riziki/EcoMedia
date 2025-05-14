
from __future__ import annotations

import streamlit as st 
import sys



sys.path.insert(1, './models')
print(sys.path.insert(1, '../models/'))


from dotenv import load_dotenv

load_dotenv()



st.markdown(
    """
    <div class=title>
        <div style=" justify-content: center;">
            <h1 style="text-align: center; padding: 5px; color: #005195;">EcoMedia 📰</h1>
            <p style="text-align: center;">From headline to insight, intelligently</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.image('https://media.licdn.com/dms/image/v2/D4D12AQENDMtmA8iywg/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1691841691211?e=2147483647&v=beta&t=AqFVKFoQNBrUGPCffdtccgAnhXiCM4esi6BN-iSrH30', width=900)






