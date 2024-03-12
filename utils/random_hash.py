import random as rnd

def GenerateRandomKey(seed: int):
    rnd.seed(seed)
    return int(rnd.random() * (2**31-1))
