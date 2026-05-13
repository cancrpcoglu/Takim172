import streamlit as st
from services.api import api_request


def render_chat(endpoint, title):

    st.subheader(title)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Bir şeyler yazın..."):

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        st.chat_message("user").write(prompt)

        res = api_request(
            "POST",
            endpoint,
            {"message": prompt}
        )

        

        # farklı response ihtimalleri
        response_text = (
            res.get("message")
            or res.get("response")
            or res.get("answer")
            or res.get("detail")
            or str(res)
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text
        })

        st.chat_message("assistant").write(response_text)