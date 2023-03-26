def superfoo(n):
    res = 0
    for m in range(n ** 4 // 2):
        res += res * m
    print(res)
    return res

def ultrabar(t):
    res = 0
    while res < 10 ** 10 // 2:
        res += t
    print(res)
    return res
