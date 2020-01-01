# /usr/bin/env python3
# -*- coding: utf-8 -*-

'A personal execution point recording tool with a reward mechanism as its core.'

__author__ = 'QidiLiu'

from json import load, dumps
from fractions import Fraction
from time import sleep, strftime, localtime
import csv

print("Bonus:\n"
      "- Get up at 6 o'clock                   ==>  1\n"
      "- Mobile phone data used less than 15MB ==>  1\n"
      "- Study extra content for an hour       ==>  1\n"
      "- Away from mobile phone for 13 hours   ==>  2\n"
      "- Get up after 9 o'clock                ==> -2\n"
      "- Skip class                            ==> -2")

with open('data.json', 'r') as f:
    data = load(f)

# Score is added here


def fraction_converter(fra_str):
    fra_list = list(fra_str)
    fra = False
    for i in fra_list:
        if(i == '/'):
            fra = True
            break
    if(fra):
        return Fraction(fra_str)
    else:
        return fra_str


score = data['score']
sport = input('Sport:')
if(sport != ''):
    sport = fraction_converter(sport)
    study = fraction_converter(input('Study:'))
    others = fraction_converter(input('Others:'))
    bonus = input('Bonus:')
    add = round(float(study)*5+float(sport)*2.5 +
                float(others)*2.5+float(bonus), 1)
    score += add
print('')
print('*****************************')
print('Your score now:', score)
print('*****************************')
print('')

# Gift-list is shown here
print('Gift list:')
print('=============================')
print('{:12} {:4} {:1}'.format('Gift name', 'No.', 'Cost'))
print('-----------------------------')
del data['score']
for i in data:
    print('{:12} {:4} {:1}'.format(data[i]['name'], i, data[i]['score']))
print('=============================')
print('')

# Choose a gift (number)
gift_code = input('Which gift do you want today?')
print('')
print('*****************************')
if(gift_code == ''):
    sub = 0
    gift_code = '0'
    print('Well, have a nice day! :)')
else:
    sub = data[gift_code]["score"]
    if(score-sub < 0):
        print("You don't have enough score.")
    else:
        score = round(score-sub, 1)
        print('Your score now:', score)
        print("What you've got today:", data[gift_code]['name'])
print('*****************************')

data['score'] = score
with open('data.json', 'w') as f:
    f.write(dumps(data))

# Record today's archivement and my choice, then save the record in csv file "history.csv"
if(sport != ''):
    date = strftime('%Y-%m-%d', localtime())  # Get the date
    point = add
    record = [date, point, gift_code]
    with open('history.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        lines = list(reader)
        lines.append(record)
    with open('history.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)

sleep(5)
