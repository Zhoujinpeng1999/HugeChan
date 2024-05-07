'''
'''

import random as rnd
import copy
import mmh3

def GenerateRandomKey(seed: int):
    rnd.seed(seed)
    return int(rnd.random() * (2**31-1))


import numpy as np
import numpy.random

WORD_SIZE = 32  # The template argument after the type
STATE_SIZE = 624  # The next template argument (Also `len(np.random.MT19937().state['state']['key'])`)
INITIALIZATION_MULTIPLIER = 1812433253  # The last template argument
DEFAULT_SEED = 5489  # A constant

def cpp_seed_mt19937(seed = DEFAULT_SEED):
    state = np.zeros(STATE_SIZE, dtype=np.uint32)
    state[0] = seed
    for j in range(1, STATE_SIZE):
        state[j] = INITIALIZATION_MULTIPLIER * (state[j-1] ^ (state[j-1] >> (WORD_SIZE - 2))) + j
    result = np.random.MT19937()
    result.state = {'bit_generator': 'MT19937', 'state': {'key': state, 'pos': STATE_SIZE - 1}}
    result.random_raw(1)  # Start at index "STATE_SIZE-1" and advance by 1 to advance past the generated state
    return result
    
engine = cpp_seed_mt19937(868041001)

def HashWithXor(xor_base, value):
    return int(xor_base ^ value)

def HashWithMmh3(seed, value):
    return int(mmh3.hash(str(value), signed=False, seed=seed))

from cityhash import CityHash32
def HashWithCityhash(seed, value):
    return CityHash32(str(value^seed))

with open('sids.txt', 'r') as file:
    lines = file.readlines()

# 将数据按照第一列的数值进行排序
sorted_data = sorted(lines, key=lambda x: int(x.split()[0]))
sorted_data = list(map(str.strip, sorted_data))

# 输出排序后的结果
print("排序后的结果: ")
for line in sorted_data:
    # line = str(line.strip())
    print("|{}|".format(line))
score = 0

lines2 = copy.deepcopy(lines)
new_lines2 = []
fixed_value1 = engine.random_raw(1)
for line in lines2:
    a, b = map(int, line.split())
    # result = HashWithXor(a, fixed_value1)
    # result = HashWithMmh3(a, fixed_value1)
    result = HashWithCityhash(a, fixed_value1)
    new_lines2.append("{} {} {} {}".format(result, b, a, sorted_data.index("{} {}".format(a, b))+1))
sorted_data2 = sorted(new_lines2, key=lambda x: int(x.split()[0]))
print("{} 排序后的结果: ".format(fixed_value1))
for line in sorted_data2:
    print(line.strip())

lines3 = copy.deepcopy(lines)
fixed_value2 = engine.random_raw(1)
new_lines3 = []
print("\nxor2:")
for line in lines3:
    a, b = map(int, line.split())
    # result = HashWithXor(a, fixed_value2)
    # result = HashWithMmh3(a, fixed_value2)
    result = HashWithCityhash(a, fixed_value2)
    new_lines3.append("{} {} {} {}".format(result, b, a, sorted_data.index("{} {}".format(a, b))+1))
sorted_data3 = sorted(new_lines3, key=lambda x: int(x.split()[0]))
print("{} 排序后的结果: ".format(fixed_value2))
for line in sorted_data3:
    print(line.strip())