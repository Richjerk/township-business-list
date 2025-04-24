import datetime
import streamlit as st
import cloudinary.uploader

def show_ads():
    sort_option = st.selectbox("Sort Ads by", ["Latest", "Most Clicked"])
    ads_data = list(ads.find().sort("created_at" if sort_option == "Latest" else "clicks", -1))

    if ads_data:
        for ad in ads_data:
            st.subheader(ad.get("title", "Untitled"))
            if ad.get("image_url"):
                st.image(ad["image_url"], use_column_width=True)
            if ad.get("advertiser"):
                st.write(f"🧾 Advertiser: {ad['advertiser']}")
            if ad.get("url"):
                if st.button(f"🔗 Visit {ad['title']}", key=f"btn_{ad['_id']}"):
                    ads.update_one({"_id": ad["_id"]}, {"$inc": {"clicks": 1}})
                    st.markdown(f"[Visit Site]({ad['url']})", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.info("No ads available yet.")

def upload_ad_form():
    st.header("📢 Upload Advertisement")
    title = st.text_input("Ad Title")
    advertiser = st.text_input("Advertiser Name")
    url = st.text_input("Ad URL")
    image_file = st.file_uploader("Upload Ad Image", type=["jpg", "jpeg", "png"])

    if st.button("Upload Ad"):
        if title and advertiser and url:
            image_url = None
            if image_file:
                uploaded = cloudinary.uploader.upload(image_file, folder="ads")
                image_url = uploaded.get("secure_url")

            ads.insert_one({
                "title": title,
                "advertiser": advertiser,
                "url": url,
                "image_url": image_url,
                "clicks": 0,
                "created_at": datetime.datetime.utcnow()
            })
            st.success("📢 Advertisement uploaded successfully!")
        else:
            st.warning("Please fill in all the required fields.")
