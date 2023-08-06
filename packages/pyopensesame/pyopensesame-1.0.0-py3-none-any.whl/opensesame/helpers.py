def infinite_loop():
    it=0
    while True:
        yield it
        it+=1
def get_loop(n,i):
    if i:
        return infinite_loop()
    return range(n)
def force_bytes(o):
    if isinstance(o,str):
        return o.encode()
    elif isinstance(o,bytes):
        return o
    raise TypeError
