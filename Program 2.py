import re
import csv

genre = input('Какой жанр игр Вас интересует?\n').capitalize().lstrip().split(',')
category = input('Какая категория игр Вас интересует?\n').title().lstrip().split(',')
developer = input('Игры какого разработчика Вас интересуют?\n').title().lstrip().split(',')
platform = input('На какой платформе вы собираетесь играть?\n').lower().lstrip().split(',')

year = (input('Какой год выхода Вас интересует? (Можно ввести промежуток)\n'))
if '-' in year:
    year = year.split('-')
    period = True
else:
    period = False

cost = input('Выберите допустимую цену игры в долларах (используйте < или >)\n')
if cost == '':
    cost = [0.0, 422.0]
elif cost[0] == '<':
    k = float(re.findall(r'[\d.]+', cost)[0])
    cost = [0.0, k]
else:
    cost = [float(cost), float(cost)]

ratings = input('Положительных отзывов должно быть больше, чем отрицательных? (Введите \'да\' или \'нет\')\n').lower()
if ratings == 'да':
    good = True
else:
    good = False

with open('steam.csv', encoding='utf-8') as f, \
        open('result.txt', 'w', encoding='utf-8') as f1:
    reader = csv.reader(f)
    for line in reader:
        if line[0] == 'appid':
            continue

        if period:
            if year[0] <= line[2].split('-')[0] <= year[1]:
                date = True
            else:
                date = False
        else:
            date = (line[2].split('-')[0] == year) | (year == '')

        if ((any(genre in line[9].split(';') and line[10].split(';') for genre in genre) | (genre == [''])) and
                date and
                (any(category in line[8].split(';') for category in category) | (category == [''])) and
                (any(developer in line[4].split(';') for developer in developer) | (developer == [''])) and
                (any(platform in line[6].split(';') for platform in platform) | (platform == [''])) and
                (cost[0] <= float(line[17]) <= cost[1]) and
                (((good is True) & (int(line[12]) > int(line[13]))) | (ratings == ''))):
            f1.write(line[1] + '\n')