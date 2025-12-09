import csv
#from collections import deque

def parse_csv(file_path): #dictionary for TM 
    with open(file_path, 'r') as file: #read in csv file 
        reader = csv.reader(file) 
        machine_name = next(reader)[0] 
        string_read = next(reader)[0] #input string
        states = next(reader)[0].split(',') #seperate states by comma
        alphabet = next(reader)[0].split(',') #inputs
        tape_symbols = next(reader)[0].split(',') #tape symbols
        start_state = next(reader)[0] 
        accept_state = next(reader)[0]
        reject_state = next(reader)[0]
        transitions = {} #state, char -> list of (next_state, write_char, move_dir)
        
        for row in reader:
            if not row: #skip empty rows
                continue
            state, char, next_state, write_char, move_dir = row
            transitions.setdefault((state, char), []).append((next_state, write_char, move_dir)) #ad possible transistions
    
    return { #retrun dictionary of TM components
        'name': machine_name,
        'states': states,
        'alphabet': alphabet,
        'tape_symbols': tape_symbols,
        'start_state': start_state,
        'accept_state': accept_state,
        'reject_state': reject_state,
        'transitions': transitions,
        'string_read': string_read  # list of strings to process
    }

def simulate_ntm(machine, input_string, max_depth=None): #BFS simulation of NTM/endds with accept or tries everything
    print(f'Running machine -  {machine["name"]}\nstring -  {input_string}')
    start_config = (machine['start_state'], input_string, 0)  # (state, tape, head_pos)
    tree = [[start_config]] #levels of configurations
    transitions = machine['transitions']
    accept_state = machine['accept_state']
    reject_state = machine['reject_state']

    #variables to keep track
    total_transitions = 0
    non_leaves = 0
    total_configurations = 0
    accepted_configurations = 0
    rejected_configurations = 0
    transition_log = []
    current_depth = 0

    while tree:
        current_level = tree.pop(0) #get current level of configurations
        next_level = []
        print(f"Depth {current_depth}, Current Level: {len(current_level)} configurations")

        for state, tape, head_pos in current_level:
            total_configurations += 1  # Increment for each configuration processed

            if state == accept_state:
                accepted_configurations += 1 #count accepted 
                print(f"String accepted in {current_depth} steps.")
                print(f"Level of nondeterminism: {total_transitions / (non_leaves or 1):.2f}") #averge #of transistions 
                print(f"Configurations explored: {total_configurations}")
                print(f"Accepted configurations: {accepted_configurations}")
                print(f"Rejected configurations: {rejected_configurations}")
                print("Transition Log:")
                for log in transition_log:
                    print(log)
                return current_depth #return depth of accepted string

            if state == reject_state: #end
                rejected_configurations += 1
                continue
            
            #read characters if off tape then blank symbols '_'
            head_char = tape[head_pos] if 0 <= head_pos < len(tape) else '_'
            possible_transitions = transitions.get((state, head_char), [])

            if len(possible_transitions) > 1: #branchings 
                non_leaves += 1

            for next_state, write_char, move_dir in possible_transitions:
                new_tape = list(tape) 
                if 0 <= head_pos < len(new_tape):
                    new_tape[head_pos] = write_char
                else:
                    new_tape.append(write_char)

                new_head_pos = head_pos + (1 if move_dir == 'R' else -1)
                next_config = (next_state, ''.join(new_tape), new_head_pos)
                next_level.append(next_config)

                transition_log.append(
                    f"({state}, {head_char}) -> ({next_state}, {write_char}, {move_dir})"
                )

            total_transitions += len(possible_transitions)

        if next_level:
            tree.extend([next_level])
            current_depth += 1
        else:
            print(f"String rejected in {current_depth} steps.")
            print(f"Level of nondeterminism: {total_transitions / (non_leaves or 1):.2f}")
            print(f"Configurations explored: {total_configurations}")
            print(f"Accepted configurations: {accepted_configurations}")
            print(f"Rejected configurations: {rejected_configurations}")
            print("Transition Log:")
            for log in transition_log:
                print(log)
            return False

    print(f"Execution stopped after reaching max depth of {max_depth}.")
    print(f"Level of nondeterminism: {total_transitions / (non_leaves or 1):.2f}")
    print(f"Configurations explored: {total_configurations}")
    print(f"Accepted configurations: {accepted_configurations}")
    print(f"Rejected configurations: {rejected_configurations}")
    print("Transition Log:")
    for log in transition_log:
        print(log)
    return None 


