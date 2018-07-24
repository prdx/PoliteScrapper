import heapq
import time

class Heap(object):
    """Max heap (Priority queue) implementation by inversing the value in min heap
    To simplify, we will be using heapq. But heapq supports only min-heap.
    Then we just simply multiply the value by -1
    """

    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, value)
    
    def pop(self):
        if self.heap == []: return None
        else: return heapq.heappop(self.heap)

    def heapify(self):
        heapq.heapify(self.heap)
        return self.heap

    def size(self):
        return len(self.heap)


class Link(object):
    def __init__(self, url):
            self.url = url
            self.inlinks_count = -1
            self.inlinks = []
            self.timestamp = time.time()

    def add_inlinks(self, link):
            self.inlinks.append(link)
            self.inlinks_count -= 1

    def __lt__(self, other):
        if self.inlinks == other.inlinks:
            return self.timestamp < other.timestamp
        return self.inlinks_count < other.inlinks_count

