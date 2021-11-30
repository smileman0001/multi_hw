import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from tqdm import tqdm
import timeit
import re
import concurrent.futures

yep = input("Обновить ссылки? (1 - да, 0 - нет)")

url = r'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
def get_links():
    for i in tqdm(range(100)):
        html = urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        for l in links:
            href = l.get('href')
            if href and href.startswith('http') and 'wiki' not in href:
                print(href, file=res)
if(yep == 1):
    try:
        res = open('wiki_links.txt', 'w', encoding='utf8')
        get_links()
    except urllib.error.URLError:
        print("Something went wrong")
        res.close()
else:
    l = len(re.findall(r"[\n']+?", open('wiki_links.txt').read()))
    print('Список ссылок остался прежним(в нем {} строк)'.format(l))


links = open('wiki_links.txt', encoding='utf8').read().split('\n')

def check_links(links):
    for url in links:
        try:
            request = Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 9.0; Win65; x64; rv:97.0) Gecko/20105107 Firefox/92.0'},
            )
            response = urlopen(request, timeout=5)
            code = response.code
            #print(code)
            response.close()
        except Exception as e:
            print("Exception occured. URL: ", url, "Exception:", e)

start = timeit.default_timer()
check_links(links)
elapsed = timeit.default_timer() - start
print("----------------")
print(elapsed) #Стандарт
print("----------------")

#aсинхронная проверка
count = int(input("Введите количество потоков:"))
def split_to_nparts(l, n):
    #https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    k, m = divmod(len(l), n)
    return [l[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

partitioned_links = split_to_nparts(links, count)
worker2links = {worker_id:partitioned_links[worker_id] for worker_id in range(count)}
for k in worker2links:
    print(k, ':', len(worker2links[k]))

async_start = timeit.default_timer()
with concurrent.futures.ThreadPoolExecutor(max_workers=count) as executor:
    future2worker = {executor.submit(check_links, worker2links[w_id]): w_id for w_id in range(count)}
    for future in concurrent.futures.as_completed(future2worker):
        w_id = future2worker[future]
        #print(f"Worker {w_id} finished checking {len(worker2links[w_id])} URLs")
async_elapsed = timeit.default_timer() - async_start
print(f" {async_elapsed} using {count} workers")
#5 потоков - примерно в 3 - 5 раз быстрее стандарта
#10 потоковв - примерно в 6-7.5 раз быстрее
#100 потоков - сильно зависит от количества изначально полученных ссылок