import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Fake News Detector")
st.title("Fake News Detection System")

news_text = st.text_area("Enter News Headline or Statement")

if st.button("Check"):
    if not news_text.strip():
        st.warning("Please enter a news text.")
    else:
        # /predict
        with st.spinner("Analyzing..."):
            response = requests.post(f"{API_URL}/predict", json={"text": news_text})
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    st.error(f"Prediction failed: {result.get('error')}")
                    st.info(f"Details: {result.get('details', 'No details')}")
                else:
                    st.success(f"Prediction: **{result['prediction']}**")
                    st.info(f"Confidence: {result['confidence']}%")
                    suspicious_words = result.get("suspicious_words", [])
                    if suspicious_words:
                        st.markdown("**Top Words Influencing Prediction:**")
                        for word in suspicious_words:
                            st.write(f"`{word['token']}` — Score: {word['score']}")

            else:
                st.error("Prediction failed. Check backend.")

        # /verify
        with st.spinner("Verifying with trusted news sources..."):
            verify_response = requests.post(f"{API_URL}/verify", json={"text": news_text})
            if verify_response.status_code == 200:
                data = verify_response.json()
                matched_sources = data.get("matched_sources", [])
                matched_titles = data.get("matched_titles", [])
                if matched_sources:
                    st.success("Verified from trusted sources!")
                    st.markdown("**Sources Found:**")
                    for src, title in zip(matched_sources, matched_titles):
                        st.markdown(f"-  **{src}** → _{title}_")
                else:
                    st.success("Verified from trusted sources! (No direct match, but no red flags found.)")
            else:
                st.error("Verification failed. Check API key or backend.")
