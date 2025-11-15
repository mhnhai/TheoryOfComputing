class NFAe:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states, epsilon='ε'):
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

def nhap_nfae_tu_file(ten_file, epsilon='ε'):
    with open(ten_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Dòng 1: tập trạng thái
    states = set(lines[0].split())
    
    # Dòng 2: bảng chữ cái
    alphabet = set(lines[1].split())
    
    # Dòng 3: trạng thái bắt đầu
    start_state = lines[2]
    
    # Dòng 4: tập accept states
    accept_states = set(lines[3].split())
    
    # Dòng 5+: hàm chuyển
    tf = dict()
    for i in range(4, len(lines)):
        parts = lines[i].split()
        from_state = parts[0]
        symbol = parts[1]
        to_states = set(parts[2:])   # nhiều trạng thái
        
        tf[(from_state, symbol)] = to_states
    
    return NFAe(states, alphabet, tf, start_state, accept_states, epsilon)


states = {1, 2, 3}
alphabet = {'a','b'}
start_state = 1
accept_states = {2}

tf = dict()
tf[(1, 'a')] = {3}
tf[(1, 'ε')] = {2}  # epsilon transition từ 1 -> 2
tf[(2, 'a')] = {1}
tf[(3, 'a')] = {2}
tf[(3, 'b')] = {2, 3}

nfae = NFAe(states, alphabet, tf, start_state, accept_states)
nfae2 = nhap_nfae_tu_file("nfae.txt")

L_input = input("Nhập chuỗi đầu vào: ")
L = list(L_input)

print(nfae2.go_to_initial_state())
print(nfae2.run_with_input_list(L))

# Test
# print(nfae.run_with_input_list(list("aaba")))  # True
