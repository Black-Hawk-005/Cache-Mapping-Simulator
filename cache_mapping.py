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
    for i in range(4):
        for j in range(no_of_bytes):
            print(main_memory[i][j],end = ' ')
        print("")

def convert_bin(num):
    num=int(num)
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

def L1_victim_cache_initialization():
    global L1_victim, victim_count
    L1_victim = []
    victim_count = [0,0,0,0]
    for i in range(4):
        line = []
        for j in range(no_of_bytes):
            line.append(["0000000000000000","0000000000000000"])
        L1_victim.append(line)

def display_L1_cache():
    for i in range(4):
        for j in range(no_of_bytes):
            print(L1[i][j][0]," ",L1[i][j][1])
        print("")

def cache_check_L1(address):
    tag = convert_deci(address[:3])
    line = convert_deci(address[3:10])
    byte = convert_deci(address[10:])
    if tag == convert_deci(L1[line][0][0][:3]):
        print("HIT")
        return 1
    else:
        print("MISS")
        return 0

def cache_check_L1_victim(address):
    for i in range(4):
        for j in range(64):
            if L1_victim[i][j][0][:10] == address[:10]:
                print("VICTIM CACHE HIT")
                victim_count[i] += 1
                return 1
    return 0

def cache_store_L1(address):
    tag = convert_deci(address[:3])
    line = convert_deci(address[3:10])
    byte = convert_deci(address[10:])
    prev_data = L1[line].copy()
    for i in range(64):
        L1[line][i] = main_memory[convert_deci(address[:10])][i]
    return prev_data

def cache_store_victim(address):
    least_recently_used_line = 0
    least_recently_used_count = victim_count[0]
    for i in range(4):
        if(L1_victim[i][0]==['0000000000000000','0000000000000000']):
            least_recently_used_line = i
            replaced_data = L1_victim[least_recently_used_line]
            L1_victim[least_recently_used_line] = address
            return replaced_data

        elif(victim_count[i] < least_recently_used_count):
            least_recently_used_line = i
            least_recently_used_count = victim_count[i]
    replaced_data = L1_victim[least_recently_used_line]
    L1_victim[least_recently_used_line] = address
    return replaced_data

def display_L1_victim():
    for i in range(4):
        for j in range(64):
            print(L1_victim[i][j][0]," ",L1_victim[i][j][1])
        print("count-",victim_count[i])
        print("\n")

def cache_check_L1_victim(address):
    for i in range(4):
        for j in range(64):
            if L1_victim[i][j][0][:10] == address[:10]:
                print("VICTIM CACHE HIT")
                victim_count[i] += 1
                return 1
    return 0

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

def display_L2_cache():
    for i in range(1):
        for k in range(0,4):
            for j in range(64):
                print(L2[i][k][j][0]," ",L2[i][k][j][1])
            print("count -",L2[i][k][-1])

def L2_mapping(address):
    set=convert_deci(address[0][0][4:10])
    min=L2[set][0][-1]
    index=0
    for i in range(0,4):
        if(L2[set][i][0]==['0000000000000000','0000000000000000']):
            index=i
            victim=L2[set][index]
            L2[set][index]=address
            L2[set][index].extend([1])

        elif L2[set][i][-1]<min:
            index=i
    victim=L2[set][index]
    L2[set][index]=address
    L2[set][index].extend([1])
    return victim

def cache_check_L2(w_address):
    address=main_memory[convert_deci(w_address[0:10])]
    set = convert_deci(address[0][0][4:10])
    for i in range(0,4):
        if(L2[set][i][0][0][:4]==address[0][0][:4]):
            print("HIT")
            L2[set][i][-1]+=1
            return 1
    return 0

main_memory_initialisation()
L1_cache_initialization()
L1_victim_cache_initialization()
L2_cache_intialization()

while(1):
    choice = int(input("1 - Display Main Memory\n2 - Display L1 cache\n3 - Display the victim cache\n4 - Display L2 cache\n5 - Fetch the address\n6 - Exit\nEnter choice: "))
    
    if choice == 1:
        display_main_memory()
    
    elif choice == 2:
        display_L1_cache()
    
    elif choice == 3:
        display_L1_victim()

    elif choice==4:
        display_L2_cache()
    
    elif choice == 5:
        w_number=int(input("enter the word number to be fetched: "))
        w_address=convert_bin(w_number)
        if (cache_check_L1(w_address) == 1):
            print("HIT")
        else:
            print("Memory not found in L1 cache. ")
            print("Checking in Victim Cache")
            if (cache_check_L1_victim(w_address) == 1):
                print("HIT")

            else:
                print("Memory not found in Victim cache. ")
                print("Checking in L2 Cache")
                if(cache_check_L2(w_address)):
                    print("HIT")
                else:
                    print("Memory not found in L2 cache")
                    prev_data = cache_store_L1(w_address)
                    removed_data = cache_store_victim(prev_data)
                    L2_mapping(removed_data)

    elif choice == 6:
        exit(0)
    
    else:
        print("Invalid option number")

'''
for i in range(1024):
    test_address = convert_bin(i)
    test_address = test_address[6:]+"000000"
    cache_check_L1(test_address)
    if (cache_check_L1(test_address) == 1):
        print("HIT")
    else:
        if (cache_check_L1_victim(test_address) == 1):
            print("VICTIM HIT")

        else:
            if(cache_check_L2(test_address)):
                print("HIT")
            else:
                prev_data = cache_store_L1(test_address)
                removed_data = cache_store_victim(prev_data)
                L2_mapping(removed_data)'''
