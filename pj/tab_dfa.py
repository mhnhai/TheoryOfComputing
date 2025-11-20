import streamlit as st
from graphviz import Digraph

class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states, current_state=None):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = current_state if current_state else start_state

    def transition_to_state_with_input(self, input_value):
        if (self.current_state, input_value) in self.transition_function:
            self.current_state = self.transition_function[(self.current_state, input_value)]
        return

    def in_accept_state(self):
        return self.current_state in self.accept_states

    def go_to_initial_state(self):
        self.current_state = self.start_state
        return

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
        return self.in_accept_state()


def show_dfa_tab():

    st.header("🔹 Kiểm tra DFA")

    # ====== Khởi tạo session_state ======
    if "dfa" not in st.session_state:
        st.session_state.dfa = None

    # ========= Default Example ==========
    default_states = "0 1 2"
    default_alphabet = "0 1"
    default_start = "0"
    default_accept = "0"
    default_tf = """0 0 0
0 1 1
1 0 2
1 1 0 
2 0 1
2 1 2"""

    # ========== Input Section ==========
    st.subheader("⚙️ Cấu hình DFA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Nhập thủ công")
        states_input = st.text_input("Tập trạng thái (cách nhau bằng dấu cách)", default_states, key="dfa_states")
        alphabet_input = st.text_input("Bảng chữ cái (cách nhau bằng dấu cách)", default_alphabet, key="dfa_alphabet")
        start_state_input = st.text_input("Trạng thái bắt đầu", default_start, key="dfa_start")
        accept_states_input = st.text_input("Tập trạng thái kết thúc (cách nhau bằng dấu cách)", default_accept, key="dfa_accept")
        transition_input = st.text_area("Hàm chuyển (vd: s input s')", default_tf, key="dfa_tf", height=150)

        if st.button("Tạo DFA", key="btn_create_dfa_manual"):
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
                    to_state = parts[2]
                    
                    tf[(from_state, symbol)] = to_state

                dfa = DFA(
                    states=states,
                    alphabet=alphabet,
                    transition_function=tf,
                    start_state=start_state_input,
                    accept_states=accept_states,
                    current_state=start_state_input
                )

                st.session_state.dfa = dfa
                st.success("✅ DFA đã được tạo!")

            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
    
    with col2:
        st.subheader("📂 Tải từ file")
        uploaded_file = st.file_uploader("Chọn file DFA (.txt)", type=["txt"], key="dfa_file")
        
        if uploaded_file is not None:
            if st.button("📥 Tải file", key="btn_upload_dfa"):
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
                        to_state = parts[2]
                        
                        tf[(from_state, symbol)] = to_state
                    
                    dfa = DFA(
                        states=states,
                        alphabet=alphabet,
                        transition_function=tf,
                        start_state=start_state,
                        accept_states=accept_states,
                        current_state=start_state
                    )
                    
                    st.session_state.dfa = dfa
                    st.success("✅ Tải file thành công!")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi tải file: {e}")

    # =========== Hiển thị đồ thị DFA ============
    if st.session_state.dfa is None:
        st.info("⬅️ Nhập DFA ở trên để bắt đầu.")
        return

    dfa = st.session_state.dfa

    st.subheader("🔸 Đồ thị DFA")

    dot = Digraph(format="svg")
    dot.attr(rankdir="LR", fontsize="22")

    dot.node("start", shape="none")

    for s in dfa.states:
        if s in dfa.accept_states:
            dot.node(str(s), shape="doublecircle", style="filled", fillcolor="lightgreen")
        else:
            dot.node(str(s), shape="circle")

    dot.edge("start", str(dfa.start_state))

    for (src, sym), dest in dfa.transition_function.items():
        dot.edge(str(src), str(dest), label=sym)

    st.graphviz_chart(dot)

    # ========== Kiểm tra chuỗi ==========
    st.subheader("📝 Kiểm tra chuỗi")

    test_input = st.text_input("Nhập chuỗi cần kiểm tra:", key="dfa_test_input")

    if st.button("Kiểm tra trên DFA", key="btn_check_dfa"):
        dfa.go_to_initial_state()
        result = dfa.run_with_input_list(list(test_input))
        st.success("✔️ DFA chấp nhận!") if result else st.error("❌ DFA từ chối!")