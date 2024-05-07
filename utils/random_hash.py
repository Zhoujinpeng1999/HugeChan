import random as rnd

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
    
engine = cpp_seed_mt19937(2)
print(*engine.random_raw(10), sep='\n')