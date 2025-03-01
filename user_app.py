import streamlit as st
import requests

# Backend URL
BACKEND_URL = "https://ai-equity-analyst.onrender.com"
REDDIT_BACKEND_URL = "https://reddit-opinion-backend.onrender.com/"

st.set_page_config(page_title="Stock Market Insights", layout="wide")
st.title("📊 Stock Market Insights")

# Fetch Available Companies
st.sidebar.header("Select a Company")

try:
    companies_response = requests.get(f"{BACKEND_URL}/companies")
    companies_response.raise_for_status()
    company_list = companies_response.json().get("companies", [])
except requests.exceptions.RequestException:
    company_list = []
    st.sidebar.error("❌ Failed to load companies. Check backend connection.")

if company_list:
    company_name = st.sidebar.selectbox("Choose a Company", company_list)
    
    st.markdown("### Select an Analysis Option")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📑 Get Research Report"):
            try:
                response = requests.get(f"{BACKEND_URL}/summary/{company_name}")
                response.raise_for_status()
                analysis = response.json().get("final_summary", "")
                if analysis:
                    st.markdown("## 📑 AI-Powered Equity Research Report")
                    st.write(analysis)
                    st.markdown("---")
                else:
                    st.warning("⚠️ No analysis available for this company.")
            except requests.exceptions.RequestException:
                st.error("❌ Failed to fetch analysis.")
        st.caption("Research based on latest results, analyst calls, and investor presentations.")
    
    with col2:
        if st.button("📝 Get Reddit Opinion"):
            try:
                response = requests.get(f"{REDDIT_BACKEND_URL}/analyze_stock/{company_name}")
                response.raise_for_status()
                reddit_summary = response.json().get("reddit_summary", "")
                if reddit_summary:
                    st.markdown("## 📝 Reddit Discussion Summary")
                    st.write(reddit_summary)
                    st.markdown("---")
                else:
                    st.warning("⚠️ No Reddit discussions found for this company.")
            except requests.exceptions.RequestException:
                st.error("❌ Failed to fetch Reddit summary.")
        st.caption("Reddit discussion about the company.")
    
    with col3:
        if st.button("📰 Get Latest News"):
            try:
                response = requests.get(f"{REDDIT_BACKEND_URL}/analyze_stock/{company_name}")
                response.raise_for_status()
                news_summary = response.json().get("news_summary", "")
                if news_summary:
                    st.markdown("## 📰 Latest News Summary")
                    st.write(news_summary)
                    st.markdown("---")
                else:
                    st.warning("⚠️ No relevant news found for this company.")
            except requests.exceptions.RequestException:
                st.error("❌ Failed to fetch news summary.")
        st.caption("Latest news summary about the company.")
else:
    st.sidebar.warning("⚠️ No companies available. Try uploading data.")

# 🔹 Disclaimer Section
st.markdown("---")
st.markdown(
    """
    ### ⚠️ Disclaimer:
    This AI-generated content is for informational purposes only and does not constitute financial advice.
    Please consult a qualified financial advisor before making any investment decisions.
    """
)
