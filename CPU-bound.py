import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from tqdm import tqdm
import timeit
import re
import concurrent.futures
from hashlib import md5
from random import choice

def get_coins():
    while True:
        s = "".join([choice("0123456789") for i in range(50)])
        h = md5(s.encode('utf8')).hexdigest()

        if h.endswith("00000"):
            print(s, h)

start = timeit.default_timer()
get_coins()
elapsed = timeit.default_timer() - start
print("----------------")
print(elapsed) #Стандарт
print("----------------")

count = int(input("Введите количество процессов:"))

async_start = timeit.default_timer()
with concurrent.futures.ProcessPoolExecutor(max_workers=count) as executor:
    for i in range(1, count + 1):
        executor.submit(get_coins(), i)
async_elapsed = timeit.default_timer() - async_start
print("----------------")
print(async_elapsed)
print("----------------")