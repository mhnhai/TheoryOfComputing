class DFA:
    def __init__ (self, states, alphabet, transition_function, start_state, accept_states, current_state):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state
        return
    
    def transition_to_state_with_input(self, input_value):
        #nếu không tồn tại đường đi từ trạng thái hiện tại trên input_value
        if ((self.current_state, input_value) not in self.transition_function.keys()):
            self.current_state = None
            return
        #tồn tại đường đi từ trạng thái hiện tại trên input_value
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
            continue
        return self.in_accept_state()
class NFAe:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states, epsilon='e'):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.epsilon = epsilon
        self.current_state = self.epsilon_closure({start_state})

    def epsilon_closure(self, states):
        """Trả về tập các trạng thái có thể đạt được từ 'states' qua các epsilon transition."""
        closure = set(states)
        list_e = list(states)

        while list_e:
            state = list_e.pop()
            if (state, self.epsilon) in self.transition_function:
                for next_state in self.transition_function[(state, self.epsilon)]:
                    if next_state not in closure:
                        closure.add(next_state)
                        list_e.append(next_state)
        return closure

    def transition_to_state_with_input(self, input_value):
        next_states = set()
        # đi qua input -> tìm exsilon closure của state mới 
        print("Current states before input:", self.current_state, input_value)
        for state in self.current_state:
        
            if (state, input_value) in self.transition_function:
                next_states.update(self.transition_function[(state, input_value)])
        # Sau khi đi theo input, ta cũng cần tính epsilon-closure
        print ("Next states before epsilon closure:", next_states)
        self.current_state = self.epsilon_closure(next_states)
        print("Current states after epsilon closure:", self.current_state)
        return

    def in_accept_state(self):
        return any(state in self.accept_states for state in self.current_state)

    def go_to_initial_state(self):
        self.current_state = self.epsilon_closure({self.start_state})
        return

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
        return self.in_accept_state()
    
    def transferToDFA(self):
        self.go_to_initial_state()
        return
    
def convert_NFAe_to_DFA(nfae: NFAe):
    """
    Chuyển đổi từ NFAε sang DFA dựa trên thuật toán subset construction có epsilon-closure.
    Trả về: đối tượng DFA
    """

    # --- Khởi tạo ---
    dfa_states = []                # danh sách các tập trạng thái (mỗi phần tử là frozenset)
    dfa_transition = dict()        # bảng chuyển (T, a) -> U
    dfa_accept_states = set()      # tập trạng thái kết thúc trong DFA
    marked = dict()                # trạng thái đã xét hay chưa

    # Bước 1: epsilon-closure(q0)
    start_closure = frozenset(nfae.epsilon_closure({nfae.start_state}))
    dfa_states.append(start_closure)
    marked[start_closure] = False  # chưa được đánh dấu

    # Bước 2: Duyệt từng trạng thái của DFA
    while any(not marked[s] for s in marked):
        # Lấy một trạng thái T chưa đánh dấu
        T = next(s for s in marked if not marked[s])
        marked[T] = True  # đánh dấu
        # Với mỗi ký hiệu nhập a trong alphabet của NFAε 
        for a in nfae.alphabet:
            # δ(T, a): hợp các δ(q, a) với q ∈ T
            move_set = set()
            for q in T:
                if (q, a) in nfae.transition_function:
                    move_set.update(nfae.transition_function[(q, a)])
            # ε-closure(δ(T, a))
            U = frozenset(nfae.epsilon_closure(move_set))
            if not U:
                continue  # nếu rỗng thì bỏ qua

            # Thêm U nếu chưa có trong dfa_states
            if U not in marked:
                dfa_states.append(U)
                marked[U] = False

            # Cập nhật bảng chuyển DFA
            dfa_transition[(T, a)] = U

    # Bước 3: Xác định tập trạng thái kết thúc của DFA
    for state_set in dfa_states:
        if any(s in nfae.accept_states for s in state_set):
            dfa_accept_states.add(state_set)

    # --- Tạo đối tượng DFA ---
    dfa = DFA(
        states=dfa_states,
        alphabet=nfae.alphabet,
        transition_function=dfa_transition,
        start_state=start_closure,
        accept_states=dfa_accept_states,
        current_state=start_closure
    )

    return dfa

# class NFAeToDFA(NFAe):
        
states = {0, 1, 2, 3, 4, 5, 6 ,7 ,8 ,9 ,10}
alphabet = {'a','b'}
start_state = 0
accept_states = {10}

tf = dict()
tf[(0, 'e')] = {1, 7}
tf[(1, 'e')] = {2, 4}
tf[(3, 'e')] = {6}
tf[(5, 'e')] = {6}
tf[(6, 'e')] = {1,7}
tf[(2, 'a')] = {3}
tf[(4, 'b')] = {5}
tf[(7, 'a')] = {8}
tf[(8, 'b')] = {9}
tf[(9, 'b')] = {10}

nfae = NFAe(states, alphabet, tf, start_state, accept_states)
dfa = convert_NFAe_to_DFA(nfae)
# Test
# print(nfae.run_with_input_list(list("aaba")))  # True
print(dfa.states)
