import streamlit as st
import pandas as pd
import os
import requests

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="ConnectHub",
    layout="wide",
    page_icon="🤝"
)

# ----------------------------
# CONSTANTS
# ----------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "qwerty//"
DATA_FILE = "students.csv"
AGENT_API_URL = "http://127.0.0.1:8000/run"

# ----------------------------
# SESSION STATE
# ----------------------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "groups" not in st.session_state:
    st.session_state.groups = None


# ----------------------------
# DATA HELPERS
# ----------------------------
def load_submissions():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(
        columns=["id", "name", "email", "interests", "looking_to_connect_with"]
    )


def save_submission(data):
    df = load_submissions()
    data["id"] = len(df) + 1
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def call_adk_agent(users, query):
    """
    Calls FastAPI backend ONCE.
    """
    try:
        response = requests.post(
            AGENT_API_URL,
            json={
                "users": users,
                "query": query
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ----------------------------
# STYLING
# ----------------------------
st.markdown("""
<style>
body, .stApp {
    background-color: #05010a;
    color: #e5d7ff;
}
h1, h2, h3, h4 {
    color: #c770ff !important;
    text-shadow: 0 0 18px #b43aff;
}
.stButton > button {
    background: linear-gradient(90deg, #b23aff, #7f00ff);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
}
.block-container {
    padding-top: 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR NAV
# ----------------------------
st.sidebar.header("Menu")

if st.session_state.admin_logged_in:
    selection = st.sidebar.radio("Go to", ["Admin Dashboard", "Logout"])
else:
    selection = st.sidebar.radio("Go to", ["Submit Profile", "Admin Login"])


# ----------------------------
# ADMIN LOGIN
# ----------------------------
if selection == "Admin Login":

    st.subheader("Admin Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

    if login:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Logged in")
            st.rerun()
        else:
            st.error("Invalid credentials")


# ----------------------------
# LOGOUT
# ----------------------------
if selection == "Logout":
    st.session_state.admin_logged_in = False
    st.session_state.groups = None
    st.success("Logged out")
    st.rerun()


# ----------------------------
# USER FORM
# ----------------------------
if selection == "Submit Profile" and not st.session_state.admin_logged_in:

    st.subheader("Welcome to ConnectHub 🤝")
    st.write("Meet like-minded people at conferences, workshops, and events.")

    with st.form("user_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        interests = st.text_area("Your Interests")
        looking = st.text_area("Who you'd like to connect with")

        submitted = st.form_submit_button("Join Event")

    if submitted:
        if not name or not email:
            st.error("Name and email are required")
        else:
            save_submission({
                "name": name.strip(),
                "email": email.strip(),
                "interests": interests.strip(),
                "looking_to_connect_with": looking.strip()
            })
            st.success("Profile submitted successfully!")


# ----------------------------
# ADMIN DASHBOARD
# ----------------------------
if selection == "Admin Dashboard" and st.session_state.admin_logged_in:

    st.subheader("Admin Dashboard")

    df = load_submissions()
    st.markdown("### Attendee Data")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.markdown("### Create Groups")

    query = st.text_input(
        "Grouping Query",
        placeholder="Example: Group introverts interested in AI and ML"
    )

    # ---------- SINGLE CALL GUARANTEE ----------
    if st.button("Generate Groups") and st.session_state.groups is None:

        if df.empty:
            st.warning("No data available")
        elif not query:
            st.error("Please enter a query")
        else:
            with st.spinner("Generating groups…"):
                response = call_adk_agent(
                    df[["name", "email", "interests", "looking_to_connect_with"]]
                    .to_dict(orient="records"),
                    query
                )

            if "error" in response:
                st.error(response["error"])
            else:
                st.session_state.groups = response["groups"]
                st.success("Groups generated")

    # ---------- RESET ----------
    if st.button("Reset Groups"):
        st.session_state.groups = None
        st.rerun()

    # ---------- DISPLAY GROUPS ----------
    if st.session_state.groups:
        st.markdown("### 🤝 Generated Groups")

        for group in st.session_state.groups:
            st.markdown(f"#### {group['name']}")
            st.write(group["reason"])
            for m in group["members"]:
                st.write(f"- {m['name']} ({m['email']})")
