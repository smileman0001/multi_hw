import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from tqdm import tqdm
import timeit
import re
import concurrent.futures
from hashlib import md5
from random import choice


def get_coins_single():
    res = open('coins_single.txt', 'w', encoding='utf8')
    ii = 0
    for i in tqdm(range(1000000000000)):
        s = "".join([choice("0123456789") for i in range(50)])
        h = md5(s.encode('utf8')).hexdigest()

        if h.endswith("00000"):
            print('{}     {}'.format(s, h), file=res)
            ii += 1
        #скорость +- 24000 итераций в секунду
        # if(len(re.findall(r"[\n']+?", open('coins_single.txt').read())) == 1):
        #     break
        #+- 6450 итераций в секнду
        #if (sum(1 for line in open('coins_single.txt').read()) == 1):
        #    break
        #+-6600
        if(ii > 0):
            break
        #+-23200
        # if (ii == 1):
        #     break
        #+-21500
    res.close()

def get_coins_multi():
    ii = 0
    for i in tqdm(range(1000000000)):
        s = "".join([choice("0123456789") for i in range(50)])
        h = md5(s.encode('utf8')).hexdigest()

        if h.endswith("00000"):
            print(s, h)
            ii += 1
        if (ii > 0):
            break

start = timeit.default_timer()
get_coins_single()
elapsed = timeit.default_timer() - start
print("----------------")
print(elapsed) #Стандарт
print("----------------")

count = int(input("Введите количество процессов:"))

worker2links = {worker_id:str(100/count) for worker_id in range(count)}
async_start = timeit.default_timer()
with concurrent.futures.ProcessPoolExecutor(max_workers=count) as executor:
    future2worker = {executor.submit(get_coins_multi): w_id for w_id in range(count)}
    for future in concurrent.futures.as_completed(future2worker):
        w_id = future2worker[future]
async_elapsed = timeit.default_timer() - async_start
print("----------------")
print(async_elapsed)
print("----------------")