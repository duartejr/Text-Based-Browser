import sys
import os
from collections import deque
import requests


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
    site_name = url.split('.com')[0]
    save_file = os.path.join(save_dir, site_name)
    content = content.split('\n')
    with open(save_file, 'w') as f:
        for line in content:
            f.write(line + '\n')


def open_site(url):
    url = 'https://' + url
    r = requests.get(url)
    if r.status_code == 200:
        return r.text


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
            print(open_site(site))
            save_site(open_site(site), site, dir_out)
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

