import streamlit as st

def render_business_card(business):
    st.markdown(f"""
        <div class="business-card">
            <img src="{business.get('image_url', '')}" alt="Logo" />
            <h4>{business.get('name', 'No Name')}</h4>
            <p>{business.get('description', '')}</p>
        </div>
    """, unsafe_allow_html=True)
