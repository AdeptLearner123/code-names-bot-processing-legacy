import random

f = open("words.txt", "r")
words = f.read().splitlines()

for i in range(5):
    print(random.sample(words, 2))