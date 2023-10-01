import numpy as np

abc = ["А","Б","В","Г","Д",
       "Е","Ё","Ж","З","И",
       "Й","К","Л","М","Н",
       "О","П","Р","С","Т",
       "У","Ф","Х","Ц","Ч",
       "Ш","Щ","Ъ","Ы","Ь",
       "Э","Ю"]

codes = []
for i1 in range(2):
    for i2 in range(2):
        for i3 in range(2):
            for i4 in range(2):
                for i5 in range(2):
                    code = str(i1) + str(i2) + str(i3) + str(i4) + str(i5)
                    codes.append(code)

word = 'МЕТН'


def encode(msg, codes, dict):
    encoded = ''
    for char in msg:
        encoded += codes[dict.index(char)]
    return encoded


encoded = encode(word,codes,abc)
print('encoded:', encoded)

G_matrix = [[1,1,0,1],
            [1,0,1,1],
            [1,0,0,0],
            [0,1,1,1],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]]

H_matrix = [[1,0,1,0,1,0,1],
            [0,1,1,0,0,1,1],
            [0,0,0,1,1,1,1]]

G_matrix = np.array(G_matrix)
H_matrix = np.array(H_matrix)

v = [1,0,1,1]
vector = [0, 1, 1, 0, 0, 1, 1]


print(G_matrix.dot(v))
print('-')
print(H_matrix.dot(vector))


def encrypt(G,encoded):
    encoded_arr = []
    encrypted_arr = []
    for i in range(0, len(encoded),4):
        encoded_arr.append((str(encoded[i])+str(encoded[i+1])+str(encoded[i+2])+str(encoded[i+3])))
    for v in encoded_arr:
        vector = []
        for vi in v:
            vector.append(int(vi))
        vector = np.array(vector)
        en_vector = G.dot(vector)
        for k in range(len(en_vector)):
            if en_vector[k] % 2 != 0:
                en_vector[k] = 1
            else: en_vector[k] = 0
        encrypted_arr.append(en_vector)
    return encrypted_arr


def parity_check(H,vector):
    checked_arr = []
    for v in vector:
        checked = H.dot(v)
        for i in range(len(checked)):
            if checked[i] % 2 == 0:
                checked[i] = 0
            else: checked[i] = 1
        checked_arr.append(reversed(checked))
    damaged_bits = []
    for i in range(len(checked_arr)):
        e = list(checked_arr[i])
        if e != [0, 0, 0]:
            print('error in bit', e, ' in vector', vector[i], ' #', i)
            damaged_bits.append([e,i])
    damaged_dec = []
    # print('damaged bits:',damaged_bits)
    if len(damaged_bits) != 0:
        for bit in damaged_bits:
            # print('bit:', bit)
            e = bit[0]
            # print('e:',e)
            bit_dec = 0
            for i in range(len(e)):
                bit_dec += e[i]*2**(2-i)
            damaged_dec.append(bit_dec-1)
            # print('bit[0]:',bit[0])
            bit[0] = bit_dec-1
    print('damaged bits:', damaged_bits)
    return damaged_bits


def decrypt(encrypted):
    R_matrix = np.array([[0,0,1,0,0,0,0],
                        [0,0,0,0,1,0,0],
                        [0,0,0,0,0,1,0],
                        [0,0,0,0,0,0,1]])
    decrypted_arr = []
    for v in encrypted:
        decrypted_arr.append(R_matrix.dot(v))
    return decrypted_arr


def decode(msg, codes, dict):
    decoded_arr = []
    code = ''
    for i in msg:
        for char in i:
            code += str(char)
    for i in range(0, len(code), 5):
        code_5 = code[i:i+5]
        decoded_arr.append(abc[codes.index(code_5)])
    return decoded_arr


def fix(damaged_arr, encr_arr):
    for bit in damaged_arr:
        d_bit = bit[0]
        d_vec = bit[1]
        encr_arr[d_vec][d_bit] = (encr_arr[d_vec][d_bit]+1) % 2
    return encr_arr

# encrypted:
# [1 1 0 0 1 1 0]
# [0 0 1 1 0 0 1]
# [1 1 0 0 1 1 0]
# [1 1 0 0 1 1 0]
# [0 0 1 0 1 1 0]

print('encrypted:')
encrypted = encrypt(G_matrix, encoded)
encrypted[1][2] = 0
encrypted[2][4] = 0
encrypted[3][3] = 1
# encrypted[0][4] = 0
encrypted[4][6] = 1
for i in encrypted:
    print(i)


print('decrypted:')
decrypted = decrypt(encrypted)
for i in decrypted:
    print(i)

decoded = decode(decrypted, codes, abc)
print(decoded)

checked = parity_check(H_matrix, encrypted)

fixed = fix(checked, encrypted)
for i in range(len(fixed)):
    print(fixed[i])

fix_decr = decrypt(fixed)
fix_deco = decode(fix_decr, codes, abc)
print(fix_deco)

H_matrix_15 = np.array([[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
                        [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
                        [0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
                        [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]])

vector_15 = [1,0,1,0,0,1,1,1,0,1,1,1,1,0,1]

check_15 = H_matrix_15.dot(vector_15)
print(check_15)



