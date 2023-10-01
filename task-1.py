import numpy as np
import numpy.linalg
import math
import random

# initializing consts

# alphabet dict
abc = ["А","Б","В","Г","Д",
       "Е","Ё","Ж","З","И",
       "Й","К","Л","М","Н",
       "О","П","Р","С","Т",
       "У","Ф","Х","Ц","Ч",
       "Ш","Щ","Ъ","Ы","Ь",
       "Э","Ю","Я"]

# alphabet length
n = len(abc)
print('n =', n)

# alphabet codes
codes = [0,1,2,3,4,
         5,6,7,8,9,
         10,11,12,13,14,
         15,16,17,18,19,
         20,21,22,23,24,
         25,26,27,28,29,
         30,31,32]

# hash matrices
hash_m_2x2 = [[7, 24],
              [15, 16]]

hash_m_3x3 = [[7, 24, 1],
              [13, 16, 10],
              [20, 17, 15]]

hash_m_4x4 = [[7, 2, 1, 1],
              [3, 16, 10, 1],
              [20, 7, 5, 1],
              [1, 2, 3, 4]]

np_2x2 = np.array(hash_m_2x2)
np_3x3 = np.array(hash_m_3x3)
np_4x4 = np.array(hash_m_4x4)

# checking determinants
print('det2x2 =', math.floor(np.linalg.det(np_2x2)))
print('det3x3 =', math.floor(np.linalg.det(np_3x3)))
print('det4x4 =', math.floor(np.linalg.det(np_4x4)))


# initializing functions
# check determinant for a matrix (unused for now)
# def check_det(m):
#     det = math.floor(numpy.linalg.det(m))
#     if det != 0:
#         return True
#     else: return False


# encoding the message (message, str -> encoded message, array of ints)
def encode_msg(msg, codes, dict):
    coded_msg = []
    for i in range(len(msg)):
        coded_msg.append(codes[dict.index(msg[i])])
    return coded_msg


# encrypting the message (encoded msg, array of ints -> encrypted msg, array of ints)
def encrypt(en_msg, matrix, dim):
    match dim:
        case 2:
            encrypted_msg = []
            for i in range(0, len(en_msg)-1, 2):
                vector = [en_msg[i], en_msg[i+1]]
                # matrix.dot is a matrix multiplication function in numpy
                vector_matrix = matrix.dot(vector)
                for k in range(len(vector_matrix)):
                    j = int(vector_matrix[k])
                    while j >= 33:
                        j -= 33
                    encrypted_msg.append(j)
            return encrypted_msg
        case 3:
            encrypted_msg = []
            for i in range(0, len(en_msg) - 1, 3):
                vector = [en_msg[i], en_msg[i + 1], en_msg[i + 2]]
                vector_matrix = matrix.dot(vector)
                for k in range(len(vector_matrix)):
                    j = int(vector_matrix[k])
                    while j >= 33:
                        j -= 33
                    encrypted_msg.append(j)
            return encrypted_msg
        case 4:
            encrypted_msg = []
            for i in range(0, len(en_msg) - 1, 4):
                vector = [en_msg[i], en_msg[i + 1], en_msg[i + 2], en_msg[i + 3]]
                vector_matrix = matrix.dot(vector)
                for k in range(len(vector_matrix)):
                    j = int(vector_matrix[k])
                    while j >= 33:
                        j -= 33
                    encrypted_msg.append(j)
            return encrypted_msg
        case _:
            print('Wrong dim factor')


# decoding the message (encoded msg, array of ints -> decoded msg, array of str)
def decode(msg, dict):
    decoded_msg = []
    for char in msg:
        decoded_msg.append(dict[int(char)])
    return decoded_msg


# join the message (array of str -> str)
def msg_join(msg):
    msg_n = ''
    for char in msg:
        msg_n += str(char)
    return msg_n


# decrypt the message (str -> array of str)
def decrypt(msg, inv_matrix, dim):
    new_encoded = encode_msg(msg, codes, abc)
    new_encrypted = encrypt(new_encoded, inv_matrix, dim)
    return decode(new_encrypted, abc)


# task 1, Hill Cipher
encoded = encode_msg('ПРАКЛИНАЛГБР', codes, abc)
print('encoded:', encoded)

by_m2x2 = encrypt(encoded, np_2x2, 2)
by_m3x3 = encrypt(encoded, np_3x3, 3)
by_m4x4 = encrypt(encoded, np_4x4, 4)

print('encrypted:', by_m4x4)
print('decoded:', decode(by_m4x4, abc))

# invert modular matrices (sry I can't code it)
# https://planetcalc.ru/3324/
np_2x2_inv = np.array([[1,15],
                       [30,19]])

np_3x3_inv = np.array([[25,26,14],
                       [23,28,15],
                       [0,4,4]])

np_4x4_inv = np.array([[28,7,20,11],
                       [12,31,25,16],
                       [1,21,3,2],
                       [11,0,5,21]])

message = msg_join(decode(by_m4x4, abc))
print('joined:', message)
print('decrypted:',decrypt(message, np_4x4_inv, 4))

# imitating interference
# message = ВКЬЬЭЪЪПЮТОВ
message = 'ШЫФЫКЦЙЦИЛТЦ'
print('jammed: ', message)
print('decrypted jammed:',decrypt(message, np_4x4_inv, 4))
