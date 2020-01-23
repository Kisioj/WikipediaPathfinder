# Wikipedia Pathfinder
Finding shortest path between two Wikipedia articles.

## Usage

```
python3 main.py start_word end_word lang
```

## Examples
```
$ python3 main.py Słońce Ziemia pl
...
Run time: 0.63s
Shortest path: Słońce -> Ziemia
```

```
$ python3 main.py Polska Gustaw_III pl
...
Run time: 27.30s
Shortest path: Polska -> Szwecja -> Gustaw_III
```

```
$ python3 main.py Brainfuck Scanline_rendering en
...
Run time: 264.00s
Shortest path: Brainfuck -> Programming_paradigm -> Computer_graphics -> Scanline_rendering
```

## Performance problem

As you can see above, finding paths between two articles is rather slow. The problem is that there isn't much that can be done to fix it. To understand why, you need to know that there are 2 main tasks done for every checked article:
1. HTTP request in order to get article's HTML
2. Extracting and adding to queue urls to other articles from provided HTML

As of now, extracting urls from HTML does use regular expressions and is rather fast (takes `0.01 s` and less). Most of the run time is actually requesting HTML from Wikipedia, and that's beyond our control.

#### Can I make it faster?

Yes. You could make it super fast. In order to do that you need to preprocess Wikipedia's articles or... just download Wikipedia's database and use it for this task. To read more about downloading and running Wikipedia offline, just go to: https://en.wikipedia.org/wiki/Wikipedia:Database_download

