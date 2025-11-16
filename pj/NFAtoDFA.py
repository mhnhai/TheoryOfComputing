import itertools
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
    
class NFA:
    def __init__ (self, states, alphabet, transition_function, start_state, accept_states):
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


states = {1, 2, 3}
alphabet = {'0', '1'}
start_state = 1
accept_states = {3}

tf = dict()
tf[(1, '0')] = {2,3}
tf[(2, '0')] = {1,3}
tf[(3, '0')] = {1}
tf[(3, '1')] = {2,3}
nfa = NFA(states, alphabet, tf, start_state, accept_states)

def generate_states(L1):
    concatenated_states = list()
    for i in range(1, len(L1)+1):
        for permutation in itertools.combinations(L1, i):
            concatenated_states.append((permutation))
    return concatenated_states

def convert_NFA_to_DFA(nfa: NFA):
    # --- Tập trạng thái của DFA là tập con của Q ---
    start_state = tuple([nfa.start_state])
    print("Start state of DFA:", start_state)
    
    # tập bảng chữ cái của DFA
    dfa_alphabet = nfa.alphabet
    
    # tập trạng thái của DFA
    dfa_states = generate_states(nfa.states)
    
     # tập trạng thái kết thúc trong DFA
    dfa_accept_states = set() 
    for state in dfa_states:
        # nếu có ít nhất 1 trạng thái con thuộc trạng thái kết thúc của NFA
        if any(s in nfa.accept_states for s in state):
            dfa_accept_states.add(state)
    print("Accept states of DFA:", dfa_accept_states)
    
     # bảng chuyển (T, a) -> U
    dfa_transition = dict()       

    # xây dựng bảng chuyển
    for state in dfa_states:
        # với mỗi kí tự trong bảng chữ cái
        for symbol in dfa_alphabet:
            next_set = set()
            # với mỗi trạng thái con trong tập trạng thái hiện tại
            for sub_state in state:
                if (sub_state, symbol) in nfa.transition_function:
                    next_set.update(nfa.transition_function[(sub_state, symbol)])
            if next_set:
                dfa_transition[(state, symbol)] = tuple((next_set))
    print("Transition function of DFA:")
    for k,v in dfa_transition.items():
        print(k, "->", v)

    dfa = DFA(
        states=dfa_states,
        alphabet=dfa_alphabet,
        transition_function=dfa_transition,
        start_state=start_state,
        accept_states=dfa_accept_states,
        current_state=start_state
    )

    return dfa

dfa = convert_NFA_to_DFA(nfa)

print("\nAccept states:", dfa.accept_states)
