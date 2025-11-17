import streamlit as st
from tab_nfae_to_dfa import show_nfae_dfa_tab
from tab_nfa_to_dfa import show_nfa_to_dfa_tab
from tab_nfae_to_nfa import show_nfae_to_nfa_tab

st.title("🔷 Công cụ mô phỏng Automata")


tab1, tab2, tab3 = st.tabs([
    "✨ NFAε → DFA",
    "🔰 NFA → DFA",
    "🔄 NFAε → NFA"
])

with tab1:
    show_nfae_dfa_tab()

with tab2:
    show_nfa_to_dfa_tab()

with tab3:
    show_nfae_to_nfa_tab()
