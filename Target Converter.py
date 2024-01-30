#GET_INT_STATE
def get_int_state(self):
    state = []
    for pin in self._component:
        state.append(pin.value)
    #ex: state = [F,T,T,F
    value = []
    for s in state:
        #changes bit to boolean
        value.append(str(int(s)))
    #ex: value = ["0","1","1","0"]
    #prints the string without spaces
    value = "".join(value)
    #ex: value = "0110"
    value = int(value,2)
    #ex: value = 6
    return value






target = 13
print(target)
#bin changes to binary; 2: cuts off 0b; zfill makes it as long as the number you enter
b_target = bin(target)[2:].zfill(5)
print(b_target)

l_target = []
for bit in b_target:
    #changes bit to boolean
    l_target.append(bool(int(bit)))
print(l_target)

bitstring = []
for bit in l_target:
    #changes boolean to string
    bitstring.append(str(int(bit)))
print(bitstring)

#prints the string without spaces
bitstring = "".join(bitstring)
print(bitstring)

#changes to integer
value = int(bitstring)
print(value)