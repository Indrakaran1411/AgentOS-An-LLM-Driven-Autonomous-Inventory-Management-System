import streamlit as st
import requests

st.set_page_config(page_title="AgentOS Retail", page_icon="📦")
st.title("📦 AgentOS: Smart Inventory")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about inventory or process a return..."):
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call your FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/api/chat", 
            json={"text": prompt}
        )
        res_data = response.json()
        
        # Determine display text based on your status logic
        if res_data.get("status") == "success":
            reply = f"✅ **Success:** {res_data['message']}"
        else:
            reply = res_data.get("message", "I'm not sure how to help with that.")

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")