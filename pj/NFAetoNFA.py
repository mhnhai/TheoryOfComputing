class NFA:
    def __init__ (self, states, alphabet, transition_function, start_state, accept_states, current_state):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = {start_state}

    def transition_to_state_with_input(self, input_value):
        #nếu không tồn tại đường đi từ trạng thái hiện tại trên input_value
        next_states = set()
        for state in self.current_state:
          if (state, input_value) in self.transition_function:
              next_states.update(self.transition_function[(state, input_value)])
        self.current_state = next_states
        return

    def in_accept_state(self):
        return any(state in self.accept_states for state in self.current_state)

    def go_to_initial_state(self):
        self.current_state = {self.start_state}
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

def convert_NFAe_to_NFA(nfae: NFAe):
    # Trạng thái bắt đầu của NFA
    start_state = nfae.start_state
    
    # tập bảng chữ cái của NFA
    nfa_alphabet = nfae.alphabet
    
    # tập trạng thái của NFA
    nfa_states = nfae.states
    
     # tập trạng thái kết thúc trong NFA
    # F’ = F U q0 nếu E-CLOSURE(q0) chứa một trạng thái thuộc F. 
    # Ngược lại, F’ = F
    nfa_accept_states = set() 
    print(nfae.accept_states)
    epsilon_start_state = nfae.epsilon_closure({nfae.start_state})
    if any(s in epsilon_start_state for s in nfae.accept_states ):
        nfae_start_state = nfae.start_state
        nfa_accept_states.add(nfae_start_state)
    # bảng chuyển (T, a) -> U
    nfa_transition = dict()       
    for state in nfa_states:
        # với mỗi kí tự trong bảng chữ cái
        epsilon_state = nfae.epsilon_closure({state})
        for symbol in nfa_alphabet:
            # tìm tập trạng thái đích
            #  • δ’(q, a) = δ*(q, a) = E-CLOSURE(δ(δ*(q, e),a))
            next_states = set()
            for e_state in epsilon_state:
                if (e_state, symbol) in nfae.transition_function:
                    next_states.update(nfae.transition_function[(e_state, symbol)])
            if next_states:
                nfa_transition[(state, symbol)] = nfae.epsilon_closure(next_states)

    nfa = NFA(
        states=nfa_states,
        alphabet=nfa_alphabet,
        transition_function=nfa_transition,
        start_state=start_state,
        accept_states=nfa_accept_states,
        current_state=start_state
    )

    return nfa


states = {0, 1, 2}
alphabet = {'0','1', '2'}
start_state = 0
accept_states = {2}

tf = dict()
tf[(0, 'e')] = {1}
tf[(1, 'e')] = {2}
tf[(0, '0')] = {0}
tf[(1, '1')] = {1}
tf[(2, '2')] = {2}


nfae = NFAe(states, alphabet, tf, start_state, accept_states)
nfa = convert_NFAe_to_NFA(nfae)
print(nfa.transition_function)