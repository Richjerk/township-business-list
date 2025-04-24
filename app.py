import os
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv

# App modules
from business import add_business_form, view_businesses_form, view_premium_businesses, get_businesses
from chat import load_chatbot, ask_chatbot_form
from ads import show_ads, upload_ad_form
from user import register_buyer
from utils import configure_cloudinary

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Mongo URI
is_streamlit_cloud = os.getenv("STREAMLIT_SERVER_HEADLESS") == "1"
mongo_uri = st.secrets.get("MONGO_URI") if is_streamlit_cloud else os.getenv("MONGO_URI")

# ✅ First Streamlit command
st.set_page_config(
    page_title="Township Business Directory",
    page_icon="📍",
    layout="wide"
)

# ✅ Cloudinary config
configure_cloudinary()

# ✅ Load chatbot
chatbot = load_chatbot()

# 🌗 Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if st.sidebar.checkbox("🌗 Toggle Dark Mode", value=st.session_state.theme == "dark"):
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"

if st.session_state.theme == "dark":
    st.markdown(""" 
        <style>
            body, [data-testid="stAppViewContainer"] {
                background-color: #1e1e1e;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# ✅ Custom CSS
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

# ✅ Sidebar
st.sidebar.title("💼 Township Directory")
st.sidebar.success("✅ Connected to MongoDB" if mongo_uri else "❌ Not Connected to MongoDB")
st.sidebar.markdown("---")
st.sidebar.info(f"Running in {'Streamlit Cloud' if is_streamlit_cloud else 'Local'} Mode")

# 🔁 Auto-refresh ads
st_autorefresh(interval=7000, key="ad_refresh")

# 🔄 Ads display
ads_data = show_ads()
if ads_data:
    st.markdown("### 📢 Featured Advertisement")
    if "ad_index" not in st.session_state:
        st.session_state.ad_index = 0

    current_ad = ads_data[st.session_state.ad_index]
    st.image(current_ad["image_url"], use_column_width=True, caption=current_ad.get("title", "Featured Business"))
    st.session_state.ad_index = (st.session_state.ad_index + 1) % len(ads_data)

st.markdown("---")

# ✅ Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Add Business", 
    "📍 View Businesses", 
    "🙋‍♂️ Register as Buyer",
    "💬 Chatbot", 
    "⭐ Premium Businesses", 
    "📢 Upload Advertisement"
])

with tab1:
    add_business_form()

with tab2:
    st.subheader("📍 Businesses Near You")
    from components.business_card import render_business_card
    businesses = get_businesses()
    for b in businesses:
        render_business_card(b)

with tab3:
    register_buyer()

with tab4:
    ask_chatbot_form()

with tab5:
    view_premium_businesses()

with tab6:
    upload_ad_form()

# ✅ Fallback warning
if not mongo_uri:
    st.warning("⚠️ MongoDB URI is missing! Please check your environment variables or Streamlit secrets.")

# ✅ Optional Debug/Test Section
if st.sidebar.checkbox("🔍 Show Debug Info"):
    st.subheader("🔍 Debug: Mongo URI & Cloudinary Config")
    st.write("Mongo URI:", mongo_uri)
    st.write("Cloudinary cloud name:", st.secrets["cloudinary"]["cloud_name"])
