from easyselect import Sel
import time
import sys

a = Sel(
    list(range(10))
).choose('''
[red]adsasa?
''')


# print('aaa')
# sys.stdout.write("\033[F")
# print('b')

input('press enter')
