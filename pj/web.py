import streamlit as st
from graphviz import Digraph
from NFAetoDFA import convert_NFAe_to_DFA, NFAe, DFA

# ====== Cấu hình Streamlit ======
st.set_page_config(page_title="Mô phỏng NFAε và DFA", layout="wide")
st.title("🔹 Mô phỏng NFAε và chuyển đổi sang DFA")

# ====== Ví dụ mặc định (của bạn) ======
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

# --- Nhập dữ liệu ---
st.sidebar.header("Cấu hình NFAε (bạn có thể sửa nếu muốn)")
states_input = st.sidebar.text_input("Tập trạng thái", default_states)
alphabet_input = st.sidebar.text_input("Bảng chữ cái", default_alphabet)
start_state = st.sidebar.text_input("Trạng thái bắt đầu", default_start)
accept_states_input = st.sidebar.text_input("Trạng thái kết thúc", default_accept)
transition_input = st.sidebar.text_area("Hàm chuyển (dạng: state,input -> state,state,...)", default_transitions)

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

    nfae = NFAe(states, alphabet, tf, start_state, accept_states, epsilon='e')
    st.success("✅ NFAε đã được tạo!")

    # ====== Vẽ NFAε bằng Graphviz ======
    st.subheader("🔸 Đồ thị NFAε")
    dot_nfa = Digraph(format='png')
    dot_nfa.attr(rankdir='LR')

    for s in states:
        if s in accept_states:
            dot_nfa.node(s, shape='doublecircle', style='filled', fillcolor='lightblue')
        else:
            dot_nfa.node(s, shape='circle', style='filled', fillcolor='white')

    dot_nfa.node('', shape='none')
    dot_nfa.edge('', start_state)

    for (src, sym), dests in tf.items():
        for d in dests:
            label = sym if sym != 'e' else 'ε'
            dot_nfa.edge(src, d, label=label)

    st.graphviz_chart(dot_nfa)

    # ====== Chuyển sang DFA ======
    dfa = convert_NFAe_to_DFA(nfae)
    st.subheader("🔹 Kết quả DFA:")
    st.write("Trạng thái DFA:")
    for s in dfa.states:
        st.write(s)

    # ====== Vẽ DFA bằng Graphviz ======
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

    # ====== Kiểm tra chuỗi ======
    test_input = st.text_input("Nhập chuỗi cần kiểm tra (VD: abbb, abb...)")
    if st.button("Kiểm tra trên DFA"):
        accepted = dfa.run_with_input_list(list(test_input))
        if accepted:
            st.success(f"✅ Chuỗi '{test_input}' được chấp nhận!")
        else:
            st.error(f"❌ Chuỗi '{test_input}' bị từ chối.")
