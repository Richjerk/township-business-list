import streamlit as st
from streamlit_autorefresh import st_autorefresh
from business import add_business_form, view_businesses_form, view_premium_businesses, get_businesses
from chat import load_chatbot, ask_chatbot_form
from ads import show_ads, upload_ad_form
from user import register_buyer
from utils import configure_cloudinary
from dotenv import load_dotenv
import os

# ✅ Load environment variables for local development
load_dotenv()

# ✅ MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Township Business Directory",
    page_icon="📍",
    layout="wide"
)

# ✅ Cloudinary setup
configure_cloudinary()

# ✅ Load chatbot
chatbot = load_chatbot()

# 🌗 Theme Switcher
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Toggle theme
theme_toggle = st.sidebar.checkbox("🌗 Toggle Dark Mode", value=st.session_state.theme == "dark")
st.session_state.theme = "dark" if theme_toggle else "light"

# Apply theme-based styles
if st.session_state.theme == "dark":
    st.markdown(""" 
        <style>
            body, [data-testid="stAppViewContainer"] {
                background-color: #1e1e1e;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# 🖼 Custom CSS for tabs & cards
st.markdown("""
    <style>
        .stTabs [role="tablist"] {
            border-bottom: 2px solid #ccc;
            margin-bottom: 20px;
        }
        .stTabs [role="tab"] {
            font-size: 18px;
            font-weight: bold;
        }
        .stTabs [aria-selected="true"] {
            color: #0f9d58;
            border-bottom: 3px solid #0f9d58;
        }
        .business-card {
            display: inline-block;
            width: 160px;
            margin: 10px;
            padding: 10px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }
        .business-card img {
            border-radius: 50%;
            height: 100px;
            width: 100px;
            object-fit: cover;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("💼 Township Directory")
st.sidebar.success("Connected to MongoDB")
st.sidebar.markdown("---")

# 🔁 Auto-refresh for ad rotation every 7 seconds
st_autorefresh(interval=7000, key="ad_refresh")

# 🔄 Rotating Ads
ads_data = show_ads()
if ads_data:
    st.markdown("### 📢 Featured Advertisement")
    if "ad_index" not in st.session_state:
        st.session_state.ad_index = 0

    current_ad = ads_data[st.session_state.ad_index]
    st.image(current_ad["image_url"], use_column_width=True, caption=current_ad.get("title", "Featured Business"))

    st.session_state.ad_index = (st.session_state.ad_index + 1) % len(ads_data)

st.markdown("---")

# 🧾 Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Add Business", 
    "📍 View Businesses", 
    "🙋‍♂️ Register as Buyer",
    "💬 Chatbot", 
    "⭐ Premium Businesses", 
    "📢 Upload Advertisement"
])

# Tab content
with tab1:
    add_business_form()

with tab2:
    st.subheader("📍 Businesses Near You")
    businesses = get_businesses()
    for b in businesses:
        with st.container():
            st.markdown(f"""
                <div class="business-card">
                    <img src="{b['logo_url']}" />
                    <div><strong>{b['business_name']}</strong></div>
                </div>
            """, unsafe_allow_html=True)

with tab3:
    register_buyer()

with tab4:
    ask_chatbot_form()

with tab5:
    view_premium_businesses()

with tab6:
    upload_ad_form()

# ✅ Mongo URI fetch — prioritize Streamlit secrets, fallback to env
is_streamlit_cloud = os.getenv("STREAMLIT_SERVER_HEADLESS") == "1"
if is_streamlit_cloud:
    mongo_uri = st.secrets.get("MONGODB_URI")
else:
    mongo_uri = os.getenv("MONGODB_URI")

# Optional: Show message for debug
st.sidebar.info(f"Running in {'Streamlit Cloud' if is_streamlit_cloud else 'Local'} Mode")

# Error handling if URI is still not set
if not mongo_uri:
    st.warning("MongoDB URI is missing!")
