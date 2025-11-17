import streamlit as st
from graphviz import Digraph
import itertools
from NFAetoNFA import NFAe, convert_NFAe_to_NFA

def show_nfae_to_nfa_tab():
    st.header("🔹 Chuyển đổi NFAε → NFA")

    # ====== Ví dụ mặc định ======
    default_states = "0 1 2"
    default_alphabet = "0 1 2"
    default_start = "0"
    default_accept = "2"
    default_transitions = """0 e 1
1 e 2
0 0 0
1 1 1
2 2 2"""

    # ==========================
    #        INPUT SECTION
    # ==========================
    st.subheader("⚙️ Cấu hình NFAε")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Nhập thủ công")
        states_input = st.text_input("Tập trạng thái (cách nhau bằng dấu cách)", default_states, key="nfae2nfa_states")
        alphabet_input = st.text_input("Bảng chữ cái (cách nhau bằng dấu cách)", default_alphabet, key="nfae2nfa_alphabet")
        start_state = st.text_input("Trạng thái bắt đầu", default_start, key="nfae2nfa_start")
        accept_states_input = st.text_input("Trạng thái kết thúc (cách nhau bằng dấu cách)", default_accept, key="nfae2nfa_accept")
        transition_input = st.text_area("Hàm chuyển (vd: s input s1 s2)", default_transitions, key="nfae2nfa_tf", height=150)

        if st.button("Tạo NFAε", key="btn_create_nfae2nfa"):
            try:
                states = set(states_input.split())
                alphabet = set(alphabet_input.split())
                accept_states = set(accept_states_input.split())

                tf = {}
                for line in transition_input.strip().splitlines():
                    if not line.strip():
                        continue
                    parts = line.split()
                    if len(parts) < 2:
                        continue

                    from_state = parts[0]
                    symbol = parts[1]
                    to_states = set(parts[2:]) if len(parts) > 2 else set()

                    if to_states:
                        tf[(from_state, symbol)] = to_states

                nfae = NFAe(states, alphabet, tf, start_state, accept_states, epsilon='e')
                nfa = convert_NFAe_to_NFA(nfae)

                st.session_state.nfae_to_nfa = nfae
                st.session_state.nfa_result = nfa

                st.success("✅ NFAε đã được tạo!")

            except Exception as e:
                st.error(f"❌ Lỗi: {e}")

    with col2:
        st.subheader("📂 Tải từ file")
        uploaded_file = st.file_uploader("Chọn file NFAε (.txt)", type=["txt"], key="nfae2nfa_file")

        if uploaded_file is not None:
            if st.button("📥 Tải file", key="btn_upload_nfae2nfa"):
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
                        if len(parts) < 2:
                            continue

                        from_state = parts[0]
                        symbol = parts[1]
                        to_states = set(parts[2:]) if len(parts) > 2 else set()

                        if to_states:
                            tf[(from_state, symbol)] = to_states

                    nfae = NFAe(states, alphabet, tf, start_state, accept_states, epsilon='e')
                    nfa = convert_NFAe_to_NFA(nfae)

                    st.session_state.nfae_to_nfa = nfae
                    st.session_state.nfa_result = nfa

                    st.success("✅ Tải file thành công!")

                except Exception as e:
                    st.error(f"❌ Lỗi tải file: {e}")

    # ==================================================
    #            HIỂN THỊ NFAε / NFA
    # ==================================================
    if "nfae_to_nfa" not in st.session_state:
        st.info("⬅️ Nhập NFAε ở trên để bắt đầu.")
        return

    nfae = st.session_state.nfae_to_nfa
    nfa = st.session_state.nfa_result

    # =======================
    #       VẼ NFAε
    # =======================
    st.subheader("🔸 Đồ thị NFAε")

    dot_nfae = Digraph(format='svg')
    dot_nfae.attr(rankdir='LR', fontsize='22')
    dot_nfae.node('start', shape='none', label='')

    for s in nfae.states:
        if s in nfae.accept_states:
            dot_nfae.node(str(s), shape='doublecircle', style='filled', fillcolor='lightblue')
        else:
            dot_nfae.node(str(s), shape='circle', style='filled', fillcolor='white')

    dot_nfae.edge('start', str(nfae.start_state))

    for (src, sym), dests in nfae.transition_function.items():
        for d in dests:
            label = 'ε' if sym == 'e' else sym
            dot_nfae.edge(str(src), str(d), label=label)

    st.graphviz_chart(dot_nfae)

    # =======================
    #        VẼ NFA
    # =======================
    st.subheader("🔸 Đồ thị NFA (sau loại bỏ epsilon)")

    dot_nfa = Digraph(format='svg')
    dot_nfa.attr(rankdir='LR', fontsize='22')
    dot_nfa.node('start', shape='none', label='')

    for s in nfa.states:
        if s in nfa.accept_states:
            dot_nfa.node(str(s), shape='doublecircle', style='filled', fillcolor='lightgreen')
        else:
            dot_nfa.node(str(s), shape='circle', style='filled', fillcolor='white')

    dot_nfa.edge('start', str(nfa.start_state))

    for (src, sym), dests in nfa.transition_function.items():
        dot_nfa.edge(str(src), str(dests), label=sym)

    st.graphviz_chart(dot_nfa)

    # =======================
    #   KIỂM TRA CHUỖI
    # =======================
    st.subheader("📝 Kiểm tra chuỗi")

    test_input = st.text_input("Nhập chuỗi cần kiểm tra:", key="nfae2nfa_test_input")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Kiểm tra trên NFAε", key="btn_check_nfae2nfa"):
            nfae.go_to_initial_state()
            result = nfae.run_with_input_list(list(test_input))
            st.success("✔️ NFAε chấp nhận!") if result else st.error("❌ NFAε từ chối!")

    with col2:
        if st.button("Kiểm tra trên NFA", key="btn_check_nfa2nfa"):
            nfa.go_to_initial_state()
            result = nfa.run_with_input_list(list(test_input))
            st.success("✔️ NFA chấp nhận!") if result else st.error("❌ NFA từ chối!")