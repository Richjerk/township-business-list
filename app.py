import streamlit as st
from business import add_business_form, view_businesses_form, view_premium_businesses
from chat import load_chatbot, ask_chatbot_form
from ads import show_ads, upload_ad_form
from user import register_buyer
from utils import configure_cloudinary

# Configure Cloudinary
configure_cloudinary()

# Load chatbot
chatbot = load_chatbot()

# Streamlit config
st.set_page_config(page_title="Township Business Directory", page_icon="📍", layout="wide")

# Sidebar
st.sidebar.title("💼 Township Directory")
st.sidebar.success("Connected to MongoDB")
st.sidebar.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Add Business", "📍 View Businesses", "🙋‍♂️ Register as Buyer",
    "💬 Chatbot", "⭐ Premium Businesses", "📢 Upload Advertisement"
])

# Main sections
ads_data = show_ads()
with tab1:
    add_business_form()
with tab2:
    view_businesses_form()
with tab3:
    register_buyer()
with tab4:
    ask_chatbot_form()
with tab5:
    view_premium_businesses()
with tab6:
    upload_ad_form()


