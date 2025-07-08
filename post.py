import streamlit as st
import requests

st.set_page_config(page_title="LinkedIn Poster", page_icon="💼")
st.title("💼 Post on LinkedIn")

st.markdown("Post directly to your LinkedIn feed using your access token.")

# Input form
with st.form("linkedin_post_form"):
    access_token = st.text_input("Access Token", type="password")
    post_text = st.text_area("Message", placeholder="Write something to post on LinkedIn...")
    submit = st.form_submit_button("Post")

if submit:
    if not access_token or not post_text:
        st.error("Please fill in both the Access Token and Message fields.")
    else:
        try:
            # Step 1: Get User ID
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = requests.get("https://api.linkedin.com/v2/me", headers=headers)

            if me_response.status_code != 200:
                st.error("Invalid access token or unable to fetch LinkedIn profile.")
            else:
                user_id = me_response.json()["id"]

                # Step 2: Post Message
                post_url = "https://api.linkedin.com/v2/ugcPosts"
                post_data = {
                    "author": f"urn:li:person:{user_id}",
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": post_text},
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }

                post_response = requests.post(
                    post_url,
                    json=post_data,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "X-Restli-Protocol-Version": "2.0.0",
                        "Content-Type": "application/json"
                    }
                )

                if post_response.status_code == 201:
                    st.success("Successfully posted on LinkedIn!")
                else:
                    st.error(f"Failed to post: {post_response.text}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
