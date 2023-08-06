import os
FILENAME=os.path.join(os.path.split(os.path.realpath(__file__))[0],'list.txt')
with open(FILENAME) as f:
    words = tuple(i.strip() for i in f.readlines())
