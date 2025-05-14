import streamlit as st 

reg_page = st.Page("./pgs/registration.py", title="register", icon=":material/thumb_up:")
signin_page = st.Page("./pgs/signin.py", title="sign in", icon=":material/thumb_down:")
home_page = st.Page("./pgs/main.py", title="home page", icon=":material/house:")
hub_page = st.Page("./pgs/news_hub.py", title="hub", icon=":material/query_stats:")
video_page = st.Page("./pgs/video.py", title="news room", icon=":material/video_camera_front:")
content_page = st.Page("./pgs/content_generation.py", title="content generation", icon=":material/auto_stories:")
chatbot_page = st.Page("./pgs/chatbot.py", title="chatbot", icon=":material/chat:")

# team_comparison_page = st.Page("./pgs/team_comparison.py", title="team comparison", icon=":material/group_work:")
# team_profile_page = st.Page("./pgs/team_profile.py", title="team profile", icon=":material/groups:")
# match_prediction_page = st.Page("./pgs/match_prediction.py", title="match prediction", icon=":material/online_prediction:")
# test_page = st.Page("./pgs/test.py", title="test page", icon=":material/online_prediction:")



pg = st.navigation([reg_page, signin_page, home_page, hub_page, video_page, content_page, chatbot_page])



st.set_page_config(
    page_title="EcoMedia",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.echominds.africa',
        'Report a bug': "https://www.echominds.africa",
        'About': "# Driving Impact Through Communication \nTry *EcoMedia* and experience reality!"
    }
)


pg.run()



