#!/usr/bin/env python3
from urllib import parse
import collections
import re
import requests
import sys
import time


class WikipediaPathfinder:
    def __init__(self, start_word, end_word, lang):
        self.start_word = start_word
        self.end_word = end_word
        self.history = {start_word: None}
        self.queue = collections.deque([start_word])
        self.request_id = 0
        self.start_time = None
        self.end_time = None
        self.lang = lang
        self.session = requests.Session()

    def search(self):
        self.start_time = time.time()
        while not self.search_on_next_page():
            pass
        self.end_time = time.time()
        run_time = self.end_time - self.start_time

        chain = []
        word = self.end_word
        while word is not None:
            chain.append(word)
            word = self.history[word]

        chain.reverse()
        print(f'Run time: {run_time:.2f}s')
        print('Shortest path:', ' -> '.join(chain))

    def search_on_next_page(self):
        self.request_id += 1
        word = self.queue.popleft()

        debug_info = f'{len(self.history)}, {self.request_id}, {word}'

        before_request_time = time.perf_counter()
        r = self.session.get(url=f'https://{self.lang}.wikipedia.org/wiki/{word}')
        after_request_time = time.perf_counter()

        pattern = re.compile(r'href="/wiki/([^:#"]+)"')
        links = (parse.unquote_plus(href) for href in pattern.findall(r.text))
        for href in links:
            if href not in self.history:
                self.history[href] = word
                if href == self.end_word:
                    return True
                self.queue.append(href)

        after_extraction_time = time.perf_counter()

        req_time = after_request_time - before_request_time
        run_time = after_extraction_time - after_request_time
        print(f'{debug_info}, request: {req_time:.2f}s, code: {run_time:.2f}s')


def main(start_word, end_word, lang='en'):
    wp = WikipediaPathfinder(start_word, end_word, lang)
    wp.search()


if __name__ == '__main__':
    main(*sys.argv[1:])
