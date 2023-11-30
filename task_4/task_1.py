import statistics
import random
from fractions import Fraction as F
from decimal import Decimal as D
from prettytable import PrettyTable

print("task 1")

table = PrettyTable()
table.field_names = ["Statistic", "Result"]
table.align = "l"

table.add_row(["statistics.mean([56, 122, 60, 15])", f'{statistics.mean([56, 122, 60, 15])}'])
table.add_row(["statistics.mean([F(10, 15), F(22, 93), F(15, 1)])", f'{statistics.mean([F(10, 15), F(22, 93), F(15, 1)])}'])

table.add_row(['statistics.mean([D("3.2"), D("1.2"), D("9.5"), D("1.7")])', f'{statistics.mean([D("3.2"), D("1.2"), D("9.5"), D("1.7")])}'])


table.add_row(["statistics.mean([random.randint(1, 100) for x in range(1, 1001)])", f'{statistics.mean([random.randint(1, 100) for x in range(1, 1001)])}'])
table.add_row(["statistics.mean([random.triangular(1, 100, 70) for x in range(1, 1001)])", f'{statistics.mean([random.triangular(1, 100, 70) for x in range(1, 1001)])}'])

table.add_row(["statistics.mode([random.randint(1, 100) for x in range(1, 1001)])", f'{statistics.mode([random.randint(1, 100) for x in range(1, 1001)])}'])
table.add_row(["statistics.mode([random.randint(1, 100) for x in range(1, 1001)])", f'{statistics.mode([random.randint(1, 100) for x in range(1, 1001)])}'])
table.add_row(["statistics.mode([random.randint(1, 100) for x in range(1, 1001)])", f'{statistics.mode([random.randint(1, 100) for x in range(1, 1001)])}'])

table.add_row(['statistics.mode(["tiger", "lion", "zebra", "lion", "cat"])', f'{statistics.mode(["tiger", "lion", "zebra", "lion", "cat"])}'])

table.add_row(["statistics.median([random.randint(1, 100) for x in range(1, 50)", f'{statistics.median([random.randint(1, 100) for x in range(1, 51)])}'])

table.add_row(["statistics.median_grouped([random.randint(1, 100) for x in range(1, 50)", f'{statistics.median_grouped([random.randint(1, 100) for x in range(1, 51)])}'])

table.add_row(["statistics.median_high([random.randint(1, 100) for x in range(1, 50)", f'{statistics.median_high([random.randint(1, 100) for x in range(1, 51)])}'])
table.add_row(["statistics.median_low([random.randint(1, 100) for x in range(1, 50)", f'{statistics.median_low([random.randint(1, 100) for x in range(1, 51)])}'])

data = [10, 5, 7, 23, 1, 8, 14, 6, 9]
table.add_row(["data", f'{data}'])
table.add_row(["statistics.pvariance(data)", f'{statistics.pvariance(data)}'])
table.add_row(["statistics.pstdev(data)", f'{statistics.pstdev(data)}'])
table.add_row(["statistics.variance(data)", f'{statistics.variance(data)}'])


more_data = [3, 4, 5, 5, 5, 5, 5, 6, 6]
table.add_row(["more_data", f'{more_data}'])
table.add_row(["statistics.pvariance(more_data)", f'{statistics.pvariance(more_data)}'])
table.add_row(["statistics.pstdev(more_data)", f'{statistics.pstdev(more_data)}'])
table.add_row(["statistics.variance(more_data)", f'{statistics.variance(more_data)}'])

some_fractions = [F(15, 6), F(2, 4), F(5, 66)]
table.add_row(["some_fractions", f'{some_fractions}'])
table.add_row(["statistics.pvariance(some_fractions)", f'{statistics.pvariance(some_fractions)}'])
table.add_row(["statistics.pstdev(some_fractions)", f'{statistics.pstdev(some_fractions)}'])
table.add_row(["statistics.variance(some_fractions)", f'{statistics.variance(some_fractions)}'])

print(table)
