import streamlit as st
import requests
import json

SECRET_CODE = "opensesame123"
API_URL = "http://127.0.0.1:8000/process-email"

def login():
    st.title("Login")
    code = st.text_input("Enter access code:", type="password", key="login_code")
    if st.button("Unlock"):
        if code == SECRET_CODE:
            st.session_state["authenticated"] = True
            st.success("Access granted! Please use the app below. Please press Unlock Again")
        else:
            st.error("Incorrect code. Try again.")

def main_app():
    st.title("Email Support AI Agent")

    email_text = st.text_area("Enter customer email JSON here:", key="email_text", height=200)
    if st.button("Analyze Email"):
        if email_text.strip() == "":
            st.warning("Please enter some email JSON text.")
        else:
            try:
                email_data = json.loads(email_text)
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please fix the input.")
                return
            
            if "from" in email_data and "from_email" not in email_data:
                email_data["from_email"] = email_data.pop("from")

            required_fields = ["id", "from_email", "subject", "body"]
            missing_fields = [field for field in required_fields if field not in email_data]
            if missing_fields:
                st.error(f"Missing required fields: {', '.join(missing_fields)}")
                return

            with st.spinner("Processing..."):
                try:
                    response = requests.post(API_URL, json=email_data)
                    if response.status_code == 200:
                        # print("Response: ",response.content)
                        result = response.json()
                        # print("Result: ",result)
                        st.subheader("Category:")
                        st.write(result.get("category", "N/A"))

                        st.subheader("Urgency:")
                        st.write(result.get("urgency", "N/A"))

                        st.subheader("Agent Reply:")
                        st.write(result.get("reply", "N/A"))
                    else:
                        st.error(f"API error: {response.status_code} {response.text}")
                except Exception as e:
                    st.error(f"Request failed: {e}")

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        if "email_text" in st.session_state:
            del st.session_state["email_text"]
        if "login_code" in st.session_state:
            del st.session_state["login_code"]

def app():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login()
    else:
        main_app()

if __name__ == "__main__":
    app()
