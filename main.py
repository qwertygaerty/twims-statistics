import math
import random
import pandas as pd
import matplotlib.pyplot as mplt
from statistics import mean, variance, median, mode
from scipy.stats import poisson

arr = random.choices(range(0, 10), k=100)
options = range(0, 10)

counts = []
odds = []
relative_odds = []
arr_density = []
arr_distribution = []
count_of_range = []
odds_range = []
intervals = []
intervals_average = []

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_sheet(array):
    for i in options:
        counts.append(array.count(i))
        odds.append(counts[i] / len(array))

    relative_odds.append(odds[0])

    for i in options[1:]:
        relative_odds.append(round((relative_odds[i - 1] + odds[i]) * 100) / 100)

    df = pd.DataFrame({'частота': counts, 'wi': odds, 'w2': relative_odds})
    df = df.set_index([pd.Index(options)])

    print(df)


def get_plot():
    figure = mplt.figure(figsize=(10, 6))
    ax = figure.add_subplot()
    for i in options[1:]:
        mplt.plot(options[i - 1:i + 1], [relative_odds[i - 1], relative_odds[i - 1]])
    mplt.plot([-1, 0], [0, 0])
    mplt.plot([9, 10], [1, 1])
    ax.grid()
    mplt.show()


def get_distribution_position():
    arr_distribution.append(poisson.pmf(k=0, mu=4))
    for i in options[:-1]:
        arr_distribution.append(arr_distribution[i] + poisson.pmf(k=i, mu=4))

    for i in options:
        arr_density.append(poisson.pmf(k=i, mu=4))

    df = pd.DataFrame({'функция распределения': arr_distribution, 'плотность': arr_density})
    df = df.set_index([pd.Index(options)])
    print(df, '\n')


def get_theoretical_plot():
    mplt.plot(options, arr_distribution, label="функция распределения", c='blue')
    mplt.bar(options, arr_density, label='плотность')
    mplt.grid(axis='y')
    mplt.legend()
    mplt.show()


def get_frequency_polygon():
    mplt.plot(options, odds, c='yellow', marker="o")
    mplt.grid()
    mplt.show()


def get_intervals(array):
    a = round(round(1 + 3.222 * math.log(100, 10), 3) - round(1 + 3.222 * math.log(100, 10), 2), 3)
    i = 0
    count = 0
    while i <= 9:
        intervals.append(f'[{round(i - a, 3)};{round((i + 1.3) - a, 3)}]')
        intervals_average.append(round((i - a + i + 1.3 - a) / 2, 3))
        i += 1.3

    for j in intervals:
        for i in array:
            if float(j.split(';')[0].replace('[', '')) <= i <= float(j.split(';')[1].replace(']', '')):
                count += 1
        count_of_range.append(count)
        odds_range.append(count_of_range[-1] / 100)
        count = 0

    df = pd.DataFrame(
        {'Интервалы': intervals, 'Середина': intervals_average, 'Частота': count_of_range, 'Wi': odds_range})
    df = df.set_index(
        [pd.Index(['', '', '', '', '', '', ''])])
    print(df)


def get_histogram_relative():
    mplt.figure(figsize=(10, 5))
    mplt.bar(intervals, odds_range)
    mplt.title('Гистрогамма')
    mplt.grid(axis='y', color='black', linestyle='-')
    mplt.show()


def get_polygon_relative_odds():
    mplt.plot(intervals_average, count_of_range, c='orange')
    mplt.title('Полигон относительных частот')
    mplt.show()


def start():
    print('Массив из 100 элементов:')
    for i in range(10):
        print(arr[i * 10:(i + 1) * 10])
    print('\nТаблица исследования выборки:')
    get_sheet(arr)
    print(f'\nОбъём выборки - {len(arr)}')
    print(f'Сумма относительных частот - {sum(odds)}')
    print('\nЭмпирическая функция распределения:')
    get_plot()
    print(f'\nВыборочная оценка математического ожидания:\n{mean(arr)}')
    print(f'\nОценка дисперсии:\n{round(variance(arr) * 100) / 100}')
    print(f'\nМедиана:\n{median(arr)}')
    print(f'\nМода:\n{mode(arr)}')
    print('\nФункция распределения и плотности через функция распределения Пуассона:\n')
    print('\nПри лямбда равное 4:')
    get_distribution_position()
    get_theoretical_plot()
    print('\nПолигон Частот:\n')
    get_frequency_polygon()
    print(f'\nМаксимальный элемент выборки:{max(arr)}\n')
    print(f'\nМинимальный элемент выборки:{min(arr)}\n')
    print(f'\nКоличество интервалов:{round(1 + 3.222 * math.log(100, 10))}\n')
    print(f'\nh:{round(max(arr) / round(1 + 3.222 * math.log(100, 10)) * 10) / 10}\n')
    get_intervals(arr)
    get_histogram_relative()
    get_polygon_relative_odds()


start()
