import streamlit as st
from tab_nfae import show_nfae_dfa_tab
from tab_nfa import show_nfa_to_dfa_tab

st.title("🔷 Công cụ mô phỏng Automata")

tab1, tab2 = st.tabs(["NFAε → DFA", "NFA → DFA"])

with tab1:
    show_nfae_dfa_tab()

with tab2:
    show_nfa_to_dfa_tab()
