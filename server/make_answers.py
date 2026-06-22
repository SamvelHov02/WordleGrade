'''
A Python script for the word of the day list, which the server can use to make assesments.
'''
from wordfreq import zipf_frequency
from datetime import date, timedelta
import random
import json

def main():
    words = []
    with open('valid-wordle-words.txt', 'r') as file:
        for word in file.readlines():
            words.append(word.strip())
    
    words.sort(key=lambda w: zipf_frequency(w, 'en'), reverse=True) 

    answers = words[:2000]
    answers = random.choices(answers, k=2000)
    

    answers_dict = {}
    today = date.today()

    for i, ans in enumerate(answers):
        day = today + timedelta(days=i)
        answers_dict[day.strftime("%Y-%m-%d")] = ans
        

    with open('answers.json', 'w') as file:
        json.dump(answers_dict, file, indent=2)
        

if __name__ == '__main__':
    main()