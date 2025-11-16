import streamlit as st
from graphviz import Digraph
from NFAetoDFA import convert_NFAe_to_DFA, NFAe, DFA


def show_nfae_dfa_tab():

    st.header("🔹 Chuyển đổi NFAε → DFA")
    
    # ====== Khởi tạo session_state ======
    if "nfae" not in st.session_state:
        st.session_state.nfae = None
    if "dfa" not in st.session_state:
        st.session_state.dfa = None
    if "tf" not in st.session_state:
        st.session_state.tf = None
    if "states" not in st.session_state:
        st.session_state.states = None
    if "accept_states" not in st.session_state:
        st.session_state.accept_states = None

    # ====== Ví dụ mặc định ======
    default_states = "0 1 2 3 4 5 6 7 8 9 10"
    default_alphabet = "a b"
    default_start = "0"
    default_accept = "10"
    default_transitions = """0 e 1 7
1 e 2 4
3 e 6
5 e 6
6 e 1 7
2 a 3
4 b 5
7 a 8
8 b 9
9 b 10"""

    # ==========================
    #        INPUT SECTION
    # ==========================
    st.subheader("⚙️ Cấu hình NFAε")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Nhập thủ công")
        states_input = st.text_input("Tập trạng thái (cách nhau bằng dấu cách)", default_states, key="nfae_states")
        alphabet_input = st.text_input("Bảng chữ cái (cách nhau bằng dấu cách)", default_alphabet, key="nfae_alphabet")
        start_state = st.text_input("Trạng thái bắt đầu", default_start, key="nfae_start")
        accept_states_input = st.text_input("Trạng thái kết thúc (cách nhau bằng dấu cách)", default_accept, key="nfae_accept")
        transition_input = st.text_area("Hàm chuyển (vd: s input s1 s2)", default_transitions, key="nfae_tf", height=150)

        if st.button("Tạo NFAε"):
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

                st.session_state.nfae = NFAe(states, alphabet, tf, start_state, accept_states, epsilon='e')
                st.session_state.dfa = convert_NFAe_to_DFA(st.session_state.nfae)
                st.session_state.tf = tf
                st.session_state.states = states
                st.session_state.accept_states = accept_states

                st.success("✅ NFAε đã được tạo!")
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
    
    with col2:
        st.subheader("📂 Tải từ file")
        uploaded_file = st.file_uploader("Chọn file NFAε (.txt)", type=["txt"], key="nfae_file")
        
        if uploaded_file is not None:
            if st.button("📥 Tải file"):
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

                    nfae = NFAe(states, alphabet, tf, start_state, accept_states, epsilon='e')

                    st.session_state.nfae = nfae
                    st.session_state.dfa = convert_NFAe_to_DFA(nfae)
                    st.session_state.states = nfae.states
                    st.session_state.accept_states = nfae.accept_states
                    st.session_state.tf = nfae.transition_function

                    st.success("✅ Tải file thành công!")
                except Exception as e:
                    st.error(f"❌ Lỗi tải file: {e}")

    # ==================================================
    #            HIỂN THỊ NFAε / DFA / CHECKER
    # ==================================================
    if st.session_state.nfae is None:
        st.info("⬅️ Nhập NFAε ở trên để bắt đầu.")
        return

    nfae = st.session_state.nfae
    dfa = st.session_state.dfa
    tf = st.session_state.tf
    states = st.session_state.states
    accept_states = st.session_state.accept_states

    # =======================
    #       VẼ NFAε
    # =======================
    st.subheader("🔸 Đồ thị NFAε")

    dot_nfa = Digraph(format='svg')
    dot_nfa.attr(rankdir='LR', fontsize='24')
    dot_nfa.node('start', shape='none', label='')

    for s in states:
        if s in accept_states:
            dot_nfa.node(s, shape='doublecircle', style='filled', fillcolor='lightblue')
        else:
            dot_nfa.node(s, shape='circle', style='filled', fillcolor='white')

    dot_nfa.edge('start', nfae.start_state)

    for (src, sym), dests in tf.items():
        for d in dests:
            label = sym if sym != 'e' else 'ε'
            dot_nfa.edge(src, d, label=label)

    st.graphviz_chart(dot_nfa)

    # =======================
    #        VẼ DFA
    # =======================
    st.subheader("🔸 Đồ thị DFA")

    dot_dfa = Digraph(format='svg')
    dot_dfa.attr(rankdir='LR')

    for s in dfa.states:
        label = str(s)
        if s in dfa.accept_states:
            dot_dfa.node(label, shape='doublecircle', style='filled', fillcolor='lightgreen')
        else:
            dot_dfa.node(label, shape='circle', style='filled', fillcolor='white')

    dot_dfa.node('', shape='none')
    dot_dfa.edge('', str(dfa.start_state))

    for (src, sym), dest in dfa.transition_function.items():
        dot_dfa.edge(str(src), str(dest), label=sym)

    st.graphviz_chart(dot_dfa)

    # =======================
    #   KIỂM TRA CHUỖI
    # =======================
    st.subheader("📝 Kiểm tra chuỗi")

    test_input = st.text_input("Nhập chuỗi cần kiểm tra:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Kiểm tra trên DFA"):
            dfa.go_to_initial_state()
            result = dfa.run_with_input_list(list(test_input))
            st.success("Chuỗi hợp lệ!" if result else "Chuỗi bị từ chối!")

    with col2:
        if st.button("Kiểm tra trên NFAε"):
            nfae.go_to_initial_state()
            result = nfae.run_with_input_list(list(test_input))
            st.success("✔️ NFAε chấp nhận!") if result else st.error("❌ NFAε từ chối!")
