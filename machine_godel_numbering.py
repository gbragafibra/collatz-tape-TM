from sympy import prime

def godel_num(tm_string):
    machine_parts = tm_string.split("_")

    # fixed symbol map (without k states which will vary)
    symbol_map = {
        "0": 1,
        "1": 2,
        "L": 3,
        "R": 4,
        "H": 5,
    }

    # get all states
    state_symbols = set()
    for part in machine_parts:
        for i in range(0, 6, 3):
            s = part[i+2]  #get states
            if s not in symbol_map: #somewhat redundant (but just making sure)
                state_symbols.add(s)

    # assign num values to corresponding states (A, B, ...) in state_symbols
    # and add them to symbol_map
    for i, s in enumerate(sorted(state_symbols), start=6):
        symbol_map[s] = i

    # get all vals for corresponding symbols in machine string
    vals = []
    for part in machine_parts:
        for i in range(0, 6, 3):
            vals.append(symbol_map[part[i]])     
            vals.append(symbol_map[part[i+1]]) 
            vals.append(symbol_map[part[i+2]])  
    # compute Gödel number
    godel_num = 1
    for i, val in enumerate(vals, start=1):
        godel_num *= prime(i) ** val

    return godel_num

if __name__ == "__main__":
    tm_str = "1RB0LA_1LH0LA"
    print(godel_num(tm_str))
