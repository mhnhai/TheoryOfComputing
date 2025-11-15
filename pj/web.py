import streamlit as st
from graphviz import Digraph
from NFAetoDFA import convert_NFAe_to_DFA, NFAe, DFA

def nhap_nfae_tu_file(file, epsilon='ε'):
    content = file.read().decode("utf-8").strip().splitlines()

    # Dòng 1 – states
    states = set(content[0].split())

    # Dòng 2 – alphabet
    alphabet = set(content[1].split())

    # Dòng 3 – start state
    start_state = content[2].strip()

    # Dòng 4 – accept states
    accept_states = set(content[3].split())

    # Dòng 5 trở đi – transitions
    tf = {}
    for line in content[4:]:
        parts = line.split()
        from_state = parts[0]
        symbol = parts[1]
        to_states = set(parts[2:])

        tf[(from_state, symbol)] = to_states

    return NFAe(states, alphabet, tf, start_state, accept_states, epsilon)


# ====== Cấu hình Streamlit ======
st.set_page_config(page_title="Mô phỏng NFAε và DFA", layout="wide")
st.title("🔹 Mô phỏng NFAε và chuyển đổi sang DFA")

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
default_states = "0,1,2,3,4,5,6,7,8,9,10"
default_alphabet = "a,b"
default_start = "0"
default_accept = "10"
default_transitions = """0,e->1,7
1,e->2,4
3,e->6
5,e->6
6,e->1,7
2,a->3
4,b->5
7,a->8
8,b->9
9,b->10"""

# ====== Nhập dữ liệu ======
st.sidebar.header("Cấu hình NFAε")
states_input = st.sidebar.text_input("Tập trạng thái", default_states)
alphabet_input = st.sidebar.text_input("Bảng chữ cái", default_alphabet)
start_state = st.sidebar.text_input("Trạng thái bắt đầu", default_start)
accept_states_input = st.sidebar.text_input("Trạng thái kết thúc", default_accept)
transition_input = st.sidebar.text_area("Hàm chuyển (dạng: state,input -> state,state,...)", default_transitions)

st.sidebar.subheader("📂 Tải file NFAε (.txt)")
uploaded_file = st.sidebar.file_uploader("Chọn file...", type=["txt"])

if uploaded_file is not None and st.sidebar.button("📥 Đọc từ file"):
    try:
        nfae = nhap_nfae_tu_file(uploaded_file, epsilon='ε')

        # Lưu vào session
        st.session_state.nfae = nfae
        st.session_state.dfa = convert_NFAe_to_DFA(nfae)
        st.session_state.states = nfae.states
        st.session_state.accept_states = nfae.accept_states
        st.session_state.tf = nfae.transition_function

        st.success("✅ Đọc file thành công! NFAε đã được tạo.")
    except Exception as e:
        st.error(f"❌ Lỗi đọc file: {e}")

# ====== Tạo NFAε ======
if st.sidebar.button("Tạo NFAε"):
    states = set(states_input.replace(" ", "").split(","))
    alphabet = set(alphabet_input.replace(" ", "").split(","))
    accept_states = set(accept_states_input.replace(" ", "").split(","))

    tf = {}
    for line in transition_input.splitlines():
        if "->" not in line:
            continue
        left, right = line.split("->")
        s, a = left.split(",")
        tf[(s.strip(), a.strip())] = set(right.replace(" ", "").split(","))

    # Lưu vào session_state
    st.session_state.nfae = NFAe(states, alphabet, tf, start_state, accept_states, epsilon='e')
    st.session_state.dfa = convert_NFAe_to_DFA(st.session_state.nfae)
    st.session_state.tf = tf
    st.session_state.states = states
    st.session_state.accept_states = accept_states

    st.success("✅ NFAε đã được tạo!")

# ===================================================================
#                    HIỂN THỊ NFAε + DFA + KIỂM TRA
# ===================================================================

if st.session_state.nfae is not None:

    nfae = st.session_state.nfae
    dfa = st.session_state.dfa
    tf = st.session_state.tf
    states = st.session_state.states
    accept_states = st.session_state.accept_states

    # ====== Vẽ NFAε ======
    st.subheader("🔸 Đồ thị NFAε")
    dot_nfa = Digraph(format='svg')
    dot_nfa.attr(rankdir='LR', fontsize='24')

    # Arrow start
    dot_nfa.node('start', shape='none', label='')

    # States
    for s in states:
        if s in accept_states:
            dot_nfa.node(s,
                         shape='doublecircle',
                         style='filled',
                         fillcolor='lightblue',
                         fontsize='22')
        else:
            dot_nfa.node(s,
                         shape='circle',
                         style='filled',
                         fillcolor='white',
                         fontsize='22')

    # Start edge
    dot_nfa.edge('start', nfae.start_state)

    # Transitions
    for (src, sym), dests in tf.items():
        for d in dests:
            label = sym if sym != 'e' else 'ε'
            dot_nfa.edge(src, d, label=label, fontsize='20')

    st.graphviz_chart(dot_nfa)


    # ====== Vẽ DFA ======
    st.subheader("🔸 Đồ thị DFA")
    dot_dfa = Digraph(format='png')
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

    # ====== KIỂM TRA CHUỖI ======
    st.subheader("📝 Kiểm tra chuỗi đầu vào")

    test_input = st.text_input("Nhập chuỗi cần kiểm tra (VD: abbb, abb...)")

    col1, col2 = st.columns(2)

    # --- Button 1: kiểm tra trên DFA ---
    with col1:
        if st.button("Kiểm tra trên DFA"):
            dfa.go_to_initial_state()
            result = dfa.run_with_input_list(list(test_input))
            if result:
                st.success(f"✅ DFA: Chuỗi '{test_input}' được chấp nhận!")
            else:
                st.error(f"❌ DFA: Chuỗi '{test_input}' bị từ chối.")

    # --- Button 2: kiểm tra trên NFAε ---
    with col2:
        if st.button("Kiểm tra trên NFAε"):
            nfae.go_to_initial_state()
            result = nfae.run_with_input_list(list(test_input))
            if result:
                st.success(f"✅ NFAε: Chuỗi '{test_input}' được chấp nhận!")
            else:
                st.error(f"❌ NFAε: Chuỗi '{test_input}' bị từ chối.")
