#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import parse
import collections
import re
import requests
import sys
import time


class WikipediaPathfinder:
    def __init__(self, start_word, end_word):
        self.start_word = start_word
        self.end_word = end_word
        self.history = {start_word: None}
        self.queue = collections.deque([start_word])
        self.request_id = 0
        self.start_time = None
        self.end_time = None

    def search(self):
        self.start_time = time.time()
        while not self.search_on_next_page():
            pass
        self.end_time = time.time()
        run_time = self.end_time - self.start_time

        chain = []
        word = self.end_word
        while True:
            chain.append(word)
            word = self.history[word]
            if not word:
                break

        chain.reverse()
        print('Run time: {:.2f}s'.format(run_time))
        print('Shortest path:', ' -> '.join(chain))

    def search_on_next_page(self):
        self.request_id += 1
        word = self.queue.popleft()
        print(len(self.history), self.request_id, word)
        before = time.time()
        r = requests.get(url='https://en.wikipedia.org/wiki/{}'.format(word))
        start = time.time()

        pattern = re.compile(r'href="/wiki/([^:#"]+)"')
        links = (parse.unquote_plus(href) for href in pattern.findall(r.text))
        for href in links:
            if href not in self.history:
                self.history[href] = word
                if href == self.end_word:
                    return True
                self.queue.append(href)

        end = time.time()
        req_time = start - before
        run_time = end - start
        print('request: {:.2f}s, code: request: {:.2f}s'.format(req_time, run_time))


def main(start_word='Brainfuck', end_word='Scanline_rendering'):
    wp = WikipediaPathfinder(start_word, end_word)
    wp.search()

if __name__ == '__main__':
    main(*sys.argv[1:])
