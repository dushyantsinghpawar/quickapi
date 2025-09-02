import os

import requests
import streamlit as st

st.set_page_config(page_title="QuickAPI UI", page_icon="⚡")
API_BASE = st.sidebar.text_input("API base URL", os.getenv("API_BASE", "http://127.0.0.1:8000"))

if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None

st.title("QuickAPI UI")

# ---------- Auth ----------
with st.expander("Register (first time only)"):
    r_email = st.text_input("Email", value="me@example.com", key="reg_email")
    r_pwd = st.text_input(
        "Password (≥12 chars; upper/lower/digit/symbol)", type="password", key="reg_pwd"
    )
    if st.button("Register"):
        try:
            res = requests.post(
                f"{API_BASE}/auth/register",
                json={"email": r_email, "password": r_pwd},
                timeout=10,
            )
            st.write(
                res.status_code,
                (
                    res.json()
                    if res.headers.get("content-type", "").startswith("application/json")
                    else res.text
                ),
            )
        except Exception as e:
            st.error(f"Register failed: {e}")

st.subheader("Login")
email = st.text_input("Email", value=st.session_state.email or "me@example.com")
pwd = st.text_input("Password", type="password")
if st.button("Login"):
    try:
        res = requests.post(
            f"{API_BASE}/auth/login",
            data={"username": email, "password": pwd},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )
        if res.ok:
            token = res.json()["access_token"]
            st.session_state.token = token
            st.session_state.email = email
            st.success("Logged in!")
        else:
            st.error(f"Login failed: {res.status_code} {res.text}")
    except Exception as e:
        st.error(f"Login error: {e}")

authed = st.session_state.token is not None
if authed:
    st.info(f"Logged in as **{st.session_state.email}**")
    if st.button("Logout"):
        st.session_state.token = None
        st.experimental_rerun()

# ---------- Health ----------
col1, col2 = st.columns(2)
with col1:
    if st.button("Health check"):
        try:
            res = requests.get(f"{API_BASE}/health", timeout=5)
            st.write(res.status_code, res.json())
        except Exception as e:
            st.error(e)

# ---------- ML: Iris predict ----------
st.header("ML · Iris Prediction")
if not authed:
    st.warning("Login to use ML prediction.")
else:
    s1 = st.number_input("sepal_length", 0.0, 10.0, 5.1, 0.1)
    s2 = st.number_input("sepal_width", 0.0, 10.0, 3.5, 0.1)
    p1 = st.number_input("petal_length", 0.0, 10.0, 1.4, 0.1)
    p2 = st.number_input("petal_width", 0.0, 10.0, 0.2, 0.1)
    if st.button("Predict"):
        try:
            res = requests.post(
                f"{API_BASE}/ml/predict",
                json={
                    "sepal_length": s1,
                    "sepal_width": s2,
                    "petal_length": p1,
                    "petal_width": p2,
                },
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                timeout=10,
            )
            st.write(
                res.status_code,
                (
                    res.json()
                    if res.headers.get("content-type", "").startswith("application/json")
                    else res.text
                ),
            )
        except Exception as e:
            st.error(f"Predict error: {e}")

# ---------- Items ----------
st.header("Items")
colA, colB = st.columns(2)
with colA:
    if st.button("List items"):
        try:
            res = requests.get(f"{API_BASE}/items", timeout=10)
            st.write(res.status_code, res.json())
        except Exception as e:
            st.error(f"List error: {e}")

with colB:
    st.text("Create (requires login)")
    name = st.text_input("Item name", "sample-item")
    desc = st.text_input("Description", "hello world")
    if st.button("Create item"):
        if not authed:
            st.warning("Login first.")
        else:
            try:
                res = requests.post(
                    f"{API_BASE}/items",
                    json={"name": name, "description": desc},
                    headers={
                        "Authorization": f"Bearer {st.session_state.token}",
                        "Content-Type": "application/json",
                    },
                    timeout=10,
                )
                st.write(
                    res.status_code,
                    (
                        res.json()
                        if res.headers.get("content-type", "").startswith("application/json")
                        else res.text
                    ),
                )
            except Exception as e:
                st.error(f"Create error: {e}")
