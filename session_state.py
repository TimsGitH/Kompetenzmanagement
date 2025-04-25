import streamlit as st

def clear_session_states():
    for key in st.session_state.keys():
        del st.session_state[key]

def clear_session_states_except_role_and_debug_mode():
    for key in st.session_state.keys():
        if key != "role" and key != "debug_mode":
            del st.session_state[key]