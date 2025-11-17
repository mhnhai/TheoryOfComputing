import streamlit as st
from graphviz import Digraph
from NFAtoDFA import convert_NFA_to_DFA, NFA, DFA

def show_nfa_to_dfa_tab():

    st.header("🔹 Chuyển đổi NFA → DFA")

    # ========= Default Example ==========
    default_states = "1 2 3"
    default_alphabet = "0 1"
    default_start = "1"
    default_accept = "3"
    default_tf = """1 0 2 3
2 0 1 3
3 0 1
3 1 2 3"""

    # ========== Input Section ==========
    st.subheader("⚙️ Cấu hình NFA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Nhập thủ công")
        states_input = st.text_input("Tập trạng thái (cách nhau bằng dấu cách)", default_states, key="nfa_states")
        alphabet_input = st.text_input("Bảng chữ cái (cách nhau bằng dấu cách)", default_alphabet, key="nfa_alphabet")
        start_state_input = st.text_input("Trạng thái bắt đầu", default_start, key="nfa_start")
        accept_states_input = st.text_input("Tập trạng thái kết thúc (cách nhau bằng dấu cách)", default_accept, key="nfa_accept")
        transition_input = st.text_area("Hàm chuyển (vd: s input s1 s2)", default_tf, key="nfa_tf", height=150)

        if st.button("Tạo NFA", key="btn_create_nfa_to_dfa"):
            try:
                states = set(states_input.split())
                alphabet = set(alphabet_input.split())
                accept_states = set(accept_states_input.split())

                tf = {}
                for line in transition_input.strip().splitlines():
                    if not line.strip():
                        continue
                    parts = line.split()
                    if len(parts) < 3:
                        continue
                    
                    from_state = parts[0]
                    symbol = parts[1]
                    to_states = set(parts[2:])
                    
                    tf[(from_state, symbol)] = to_states

                nfa = NFA(
                    states=states,
                    alphabet=alphabet,
                    transition_function=tf,
                    start_state=start_state_input,
                    accept_states=accept_states
                )

                dfa = convert_NFA_to_DFA(nfa)

                st.session_state.nfa = nfa
                st.session_state.dfa = dfa

                st.success("✅ NFA đã được tạo!")

            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
    
    with col2:
        st.subheader("📂 Tải từ file")
        uploaded_file = st.file_uploader("Chọn file NFA (.txt)", type=["txt"], key="nfa_file")
        
        if uploaded_file is not None:
            if st.button("📥 Tải file", key = 'file_upload'):
                try:
                    content = uploaded_file.read().decode("utf-8").strip().splitlines()
                    
                    states = set(content[0].split())
                    alphabet = set(content[1].split())
                    start_state = content[2].strip()
                    accept_states = set(content[3].split())
                    
                    tf = {}
                    for line in content[4:]:
                        if not line.strip():
                            continue
                        parts = line.split()
                        if len(parts) < 3:
                            continue
                        
                        from_state = parts[0]
                        symbol = parts[1]
                        to_states = set(parts[2:])
                        tf[(from_state, symbol)] = to_states
                    
                    nfa = NFA(
                        states=states,
                        alphabet=alphabet,
                        transition_function=tf,
                        start_state=start_state,
                        accept_states=accept_states
                    )
                    
                    dfa = convert_NFA_to_DFA(nfa)
                    
                    st.session_state.nfa = nfa
                    st.session_state.dfa = dfa
                    
                    st.success("✅ Tải file thành công!")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi tải file: {e}")

    # =========== Hiển thị đồ thị NFA ============
    if "nfa" in st.session_state:
        nfa = st.session_state.nfa
        dfa = st.session_state.dfa

        st.subheader("🔸 Đồ thị NFA")

        dot = Digraph(format="svg")
        dot.attr(rankdir="LR", fontsize="22")

        dot.node("start", shape="none")

        for s in nfa.states:
            if s in nfa.accept_states:
                dot.node(str(s), shape="doublecircle", style="filled", fillcolor="lightblue")
            else:
                dot.node(str(s), shape="circle")

        dot.edge("start", str(nfa.start_state))

        for (src, sym), dests in nfa.transition_function.items():
            for d in dests:
                dot.edge(str(src), str(d), label=sym)

        st.graphviz_chart(dot)

        # =========== Hiển thị DFA ============
        st.subheader("🔸 Đồ thị DFA")

        dot2 = Digraph(format="svg")
        dot2.attr(rankdir="LR")

        dot2.node("start", shape="none")

        for s in dfa.states:
            label = str(s)
            if s in dfa.accept_states:
                dot2.node(label, shape="doublecircle", style="filled", fillcolor="lightgreen")
            else:
                dot2.node(label, shape="circle")

        dot2.edge("start", str(dfa.start_state))

        for (src, sym), dest in dfa.transition_function.items():
            dot2.edge(str(src), str(dest), label=sym)

        st.graphviz_chart(dot2)

        # ========== Kiểm tra chuỗi ==========
        st.subheader("📝 Kiểm tra chuỗi")

        test_input = st.text_input("Nhập chuỗi cần kiểm tra:")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Kiểm tra trên DFA", key = "dfa_checker"):
                dfa.go_to_initial_state()
                result = dfa.run_with_input_list(list(test_input))
                st.success("✔️ DFA chấp nhận!") if result else st.error("❌ DFA từ chối!")

        with col2:
            if st.button("Kiểm tra trên NFA", key = "nfa_checker"):
                nfa.go_to_initial_state()
                result = nfa.run_with_input_list(list(test_input))
                st.success("✔️ NFA chấp nhận!") if result else st.error("❌ NFA từ chối!")