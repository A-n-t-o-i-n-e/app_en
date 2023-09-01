from string import digits, punctuation, whitespace
import os, json

def dict_f():
    ''' 
    This function create a dictionnary that sort the english words per apparition frenquency 
    
    '''

    rootdir = 'books'
    word_frenquency = {}
    for path in os.listdir(rootdir):
        with open(rootdir + '/' + path) as book:
            # delete space / lower letter
            book = book.read().lower().split()
            # delete punctuation
            _dict = str.maketrans("", "", punctuation + digits)
            for i in range(len(book)):
                book[i] = book[i].translate(_dict)
                if book[i] not in word_frenquency:
                    word_frenquency[book[i]] = 1
                else:
                    word_frenquency[book[i]] = word_frenquency.get(book[i], 0) + 1
    return dict(reversed(sorted(word_frenquency.items(), key=lambda item:item[1])))



def first_word(str, i=0):
    word = ''
    for char in str[i:]:
        if char not in whitespace:
            word += char
        else:
            return word


def before_char(str, punc):
    before_char = ''
    for char in str:
        if char == punc:
            return before_char
        else: before_char += char


def in_char(str, punc):
    in_char, right_str = '', False
    for char in str:
        if char == punc[0]:
            right_str = True
        elif char == punc[1]:
            return in_char
        elif right_str:
            in_char += char


# {
#     "en": "the",
#     "fr": "le , la , les , l' (before a vowel or a mute h)",
#     "mean": "article",
#     "nature": "article",
#     "rarity": 5.94
# }

time = 0

dictionary = []
info_word = {
    'en' : 'demo', 
    'fr' : ['demo'], 
    'nature' : 'demo', 
    'mean' : ['demo'], 
    'rarity' : 0,
}
word_frenquency = dict(list(dict_f().items())[:8000])
nb_total_word = sum(dict_f().values())
for key in word_frenquency:
    with open("dictionary/en-fr-enwiktionary.txt", encoding='utf-8') as en_fr_enwiktionary:
        for line in en_fr_enwiktionary:
            if first_word(line) > key:
                break
            elif before_char(line, '{') != first_word(line) + ' ':
                continue
            elif first_word(line) == key:
                # add the word (dict) to the dictionary
                if not first_word(line) == info_word['en'] and not in_char(line, '{}') == info_word['nature']:
                    # find where is '::' (iteration)
                    i = len(line) - line[::-1].find(':')
                    fr = line[i+1:].replace('{m}', '').replace('{f}', '').replace('{p}', '').replace('{f-p}', '').replace('\n', '').replace('{n}', '')
                    
                    nature = in_char(line, '{}')
                    mean = in_char(line, '()')

                    info_word = {
                        'en' : key, 
                        'fr' : [fr], 
                        'nature' : nature, 
                        'mean' : [mean], 
                        'rarity' : float(format(word_frenquency[key]/nb_total_word*100, '.3g')),
                        }
        
                    dictionary.append(info_word)
                    continue
                else:
                    # the word is already in dictionary : fusionne les doublons
                    if dictionary[-1]['mean'] == None:
                        dictionary[-1]['mean'] = []
                    elif dictionary[-1]['fr'] == None:
                        dictionary[-1]['fr'] = []

                    i = len(line) - line[::-1].find(':')
                    fr = line[i+1:].replace('{m}', '').replace('{f}', '').replace('{p}', '').replace('{f-p}', '').replace('\n', '').replace('{n}', '')
                    if fr != None:
                        dictionary[-1]['fr'].append(fr)

                    mean = in_char(line, '()')
                    if mean != None and not mean in dictionary[-1]['mean']:
                        dictionary[-1]['mean'].append(mean)
                    else: dictionary[-1]['fr'].pop()
    print(time)
    time +=1



with open('dictionary/dictionary.json', "w", encoding='utf-8') as f:
    json.dump(dictionary, f, sort_keys=True, indent=2)


'''
# code a utiliser dans le main pour avoir acces a tout le dico
with open('dictionary/dictionary.json', "r", encoding='utf-8') as fp:
    data = json.load(fp)'''


'''
# view
d =  dict(list(dict_f().items())[:20])
end = [1, ' '*15]
for k in d:
    if end[0] == 3:
        end[0], end[1] = 0, "\n"
    print(k, d[k], end=end[1])
    end[1] = ' '*15
    end[0] += 1

print(len(dict_f()))
'''
