import random
'''
Main memory size - 64kB
Line size - 64bytes
One word - 1byte

L1 CACHE:
    Size - 8kB
    128 lines

    3bits - tag bits [0,1,2]
    7bits - line offset [3,4,5,6,7,8,9]
    6bits - byte offset [10,11,12,13,14,15]
    
    Victim cache:
        4 lines
        fully associative
    
L2 CACHE:
    Size - 16kB
    256 lines
    4-way set associative

    4 bits - tag bits [0,1,2,3]
    6 bits - set no [4,5,6,7,8,9]
    6 bits - byte offset [10,11,12,13,14,15]
'''

#byte address 16 bytes
#[address, data]

no_mm_lines = 1024
no_of_bytes = 64
L1_no_of_lines = 128

def main_memory_initialisation():
    k = 0
    global main_memory
    main_memory = []
    for i in range(no_mm_lines):
        line = []
        for j in range(no_of_bytes):
            line.append([convert_bin(k),convert_bin(random.randint(0,65536))])
            k+=1
        main_memory.append(line)

def display_main_memory():
    for i in range(2):
        for j in range(no_of_bytes):
            print(main_memory[i][j],end = ' ')
        print("")

def convert_bin(num):
    binary_num = bin(num)[2:]
    while (len(binary_num) < 16):
        binary_num = '0' + binary_num
    return binary_num

def convert_deci(binary):
    binary = int(binary)
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal

def L1_cache_initialization():
    global L1
    L1 = []
    for i in range(L1_no_of_lines):
        line = []
        for j in range(no_of_bytes):
            line.append(["0000000000000000","0000000000000000"])
        L1.append(line)

def display_L1_cache():
    for i in range(2):
        for j in range(no_of_bytes):
            print(L1[i][j], end = " ")
        print("")

def L1_mapping():
    global L1_map
    L1_map = {}
    for i in range(128):
        temp = []
        for j in range(8):
            temp.append((128*j)+i)
        L1_map[i] = temp

def cache_check_L1(address):
    tag = convert_deci(address[:3])
    line = convert_deci(address[3:10])
    byte = convert_deci(address[10:])
    print('\n',tag,'\n',line,'\n',byte,'\n')
    if tag == convert_deci(L1[line][0][0][:3]):
        print("HIT")
    else:
        print("MISS")
        for i in range(64):
            L1[line][i] = main_memory[convert_deci(address[:10])][i]
            
main_memory_initialisation()
L1_cache_initialization()
L2_cache_intialization()

def L2_cache_intialization():
    global L2
    L2=[]
    for i in range(64):
        set= []
        for k in range(0,4):
            line=[]
            for j in range(64):
                line.append(["0000000000000000","0000000000000000"])
            line.extend([0])
            set.append(line)
        L2.append(set)

def L2_mapping(w_address):
    address=convert_deci(w_address[0:10])
    set=convert_deci(address[0][0][4:10])
    min=L2[set][0][-1]
    index=0
    for i in range(0,4):
        if L2[set][i][-1]<min:
            index=i
    victim=L2[set][index]
    L2[set][index]=address
    L2[set][index].extend([1])

def cache_check_L2(w_address):
    address=convert_deci(w_address[0:10])
    set = convert_deci(address[0][0][4:10])
    for i in range(0,4):
        if(L2[set][i][0][0][:4]==address[0][0][:4]):
            print("HIT")
            L2[set][i][-1]+=1
            return address


L2_mapping(main_memory[89])
cache_check_L2(main_memory[89])
