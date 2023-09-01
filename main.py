from random import choices
from time import time
import json
from datetime import datetime


def flashcard(word):
    print(
        '1 : Je sais!', 
        ' '*5, 
        word['en'], 
        '(', 
        word['nature'], 
        ')', 
        ' '*5,
        '2 : Je sais pas!'

    )
    print('\n'*10)
    while True:
        try:
            choice = int(input())
            break 
        except: pass
    print('\n'*10)
    print(
        word['en'],
        '=',
        word['fr'],
        '\n'
        '==========Definitions==========',
        '\n',
        word['mean']
    )

    if choice == 1:
        return True
    return False


def qcm(word):
    return flashcard(word)
         

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
                            word['short_memory'] = 1
                        else:
                            word['short_memory'] = 0
                    elif word['short_memory'] == 1:
                        if qcm(word):
                            word['long_memory'] +=1
                            word['short_memory'] = 0
                        else:
                            word['short_memory'] = 0

        # save
        with open('user/studied-words.json', "w", encoding='utf-8') as f:
            json.dump(sorted(studied_words, key=lambda x: x["long_memory"]), f, indent=2)

        with open('user/stats.json', "w", encoding='utf-8') as f:
            json.dump({'words' : len(studied_words)}, f, sort_keys=True, indent=2)
        

if __name__ == '__main__':
    main()