from db import get_all_businesses
import streamlit as st

businesses = get_all_businesses()

st.title("🏪 Listed Businesses")

for b in businesses:
    st.subheader(b["business_name"])
    st.write(b["business_description"])
    st.write(f"📞 {b['business_phone']}")
    st.write(f"📍 {b['business_address']}")

    # ✅ Insert WhatsApp button here
    phone_number = b["business_phone"]
    st.markdown(f"""
        <a href="https://wa.me/27{phone_number}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:10px;">
                📲 Chat on WhatsApp
            </button>
        </a>
    """, unsafe_allow_html=True)
