def job():
    f = open('terms.txt')
    words = f.read().splitlines()
    print(words)
    f2 = open('terms_formatted.txt', 'w')
    words_formmatted = map(lambda word: '"{0}",\n'.format(word), words)
    f2.writelines(words_formmatted)