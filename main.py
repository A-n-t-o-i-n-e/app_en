from random import choices
import math
import json
from datetime import datetime

def _print(word):
    print(
        word['en'],
        '=',
        word['fr'],
        '\n'
        '==========Definitions==========',
        '\n',
        word['mean'],
        '\n'*10
    )


def flashcard(word):
    while True:
        try:
            ans = int(input(
                '1 : Je sais!' + ' '*5 + str(word['en']) + '(' + str(word['nature']) + ')' + ' '*5 + '2 : Je sais pas!'))
            break 
        except: pass


    if ans == 1:
        return True
    return False


def qcm(word):
    return flashcard(word)
         

def question(word):
    ans = input('What does "' + str(word['en']) + '" mean in french? ')
    for traduction in word['fr']:
        if ans == traduction or ans in traduction.split(','):
            return True
    return False
         

def main():
    
    # loading
    with open('dictionary/dictionary.json', "r", encoding='utf-8') as fp:
        data = json.load(fp)

    with open('user/studied-words.json', "r", encoding='utf-8') as fp:
        studied_words = json.load(fp)
        
    while True:

        # the dict who represent the word to learn
        ## en premier les mots or delai puis...->
        #### rajouter une boucle si le mot apparias trop tot (rappel) comparais date avec vre date et du delta time du long memory
        word = choices(
            [dict for dict in data], 
            weights=[dict['rarity'] for dict in data]
            )[0]

        # add the dict who represent the word to learn in the studied_words list. only if it's not already in it 
        
        is_in_studied_words = False
        for dict in studied_words:
            if word['en'] == dict['en'] and word['nature'] == dict['nature']:
                word = dict
                is_in_studied_words = True
                break
        if not is_in_studied_words:
            word['short_memory'] = 0
            word['long_memory'] = 0
            word['date'] = datetime.today().isoformat()
            studied_words.append(word)

        for i in range(7, -1, -1):
            if word['long_memory'] == i:
                if word['short_memory'] == 0:
                    if flashcard(word):
                        print('flashcard ok')
                        word['short_memory'] += 1
                    else:
                        print('flashcard non')
                        word['short_memory'] = 0
                elif word['short_memory'] == 1:
                    if qcm(word):
                        print('qcm')
                        word['short_memory'] += 1
                    else:
                        print('qcm non')
                        word['short_memory'] = 0
                elif word['short_memory'] == 2:
                    if question(word):
                        print('question')
                        word['long_memory'] +=1
                        word['short_memory'] = 0
                    else:
                        print('question non')
                        word['short_memory'] = 0   
                _print(word)


        # save
        with open('user/studied-words.json', "w", encoding='utf-8') as f:
            json.dump(sorted(studied_words, key=lambda x: x["long_memory"]), f, indent=2)

        with open('user/stats.json', "w", encoding='utf-8') as f:
            json.dump({'words' : len(studied_words)}, f, sort_keys=True, indent=2)
        

if __name__ == '__main__':
    # main()
    print(math.pi)