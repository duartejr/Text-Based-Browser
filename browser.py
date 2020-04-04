import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup


def check_url(url):
    if '.' not in url:
        return False
    return True


def is_file(filename, directory):
    files = os.listdir(directory)
    if 'com' in filename:
        return False
    if filename not in files:
        return False
    return True


def save_site(content, url, save_dir):
    site_name = '.'.join(url.split('.')[:-1])
    save_file = os.path.join(save_dir, site_name)

    with open(save_file, 'w') as f:
        for line in content:
            f.write(line + '\n')


def open_site(url):
    url = 'https://' + url
    r = requests.get(url)
    if r.status_code == 200:
        return r.text


def parsing(page):
    soup = BeautifulSoup(page.content, 'html.parser')

    body = soup.find('body')

    paragraphs = body.find_all(['p', 'a', 'ul', 'ol', 'li',
                                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                'title'])
    out = []
    for p in paragraphs:
        text = p.get_text().strip().replace('\n', ' ')
        print(text)
        out.append(text)
    return out

if __name__ == '__main__':

    home = os.getcwd()
    my_stack = deque()
    aux = 0

    if len(sys.argv) == 1:
        dir_out = 'tb_tabs'
    else:
        dir_out = sys.argv[1]

    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    site = ''

    while site != 'exit':
        site = input('> ')

        if site == 'exit':
            break

        if check_url(site):
            page = open_site(site)
            text = parsing(requests.get("https://" + site))
            save_site(text, site, dir_out)
            my_stack.append(site)
            last = site
        elif site == 'back' and len(my_stack):
            m = my_stack.pop()
            if m == last:
                m = my_stack.pop()
            print(open_site(m))
        elif is_file(site, dir_out):
            with open(os.path.join(dir_out, site)) as f:
                for line in f:
                    print(line, end='')
        else:
            print('Error: Incorrect URL')

