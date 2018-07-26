import heapq
import time
from engine.topic_focus import keywords

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
    def __init__(self, url, depth, text):
            self.url = url
            self.inlinks_count = -1
            self.inlinks = []
            self.text = text
            self.depth = depth
            self.timestamp = time.time()

    def add_inlinks(self, link):
            self.inlinks.append(link)
            self.inlinks_count -= 1

    def __lt__(self, other):
        self_priority_count = self.priority_count(self.text)
        other_priority_count = other.priority_count(other.text)

        # Give higher priority for a link that has keyword in the anchor text
        # Then if they are equal, we give higher priority if they have more inkilings
        if self_priority_count == other_priority_count:
            if self.inlinks_count == other.inlinks_count:
                return self.timestamp < other.timestamp
            return self.inlinks_count < other.inlinks_count
        return self_priority_count < other_priority_count 

    def priority_count(self, text):
        n = 0
        for keyword in keywords:
            if keyword in text.lower():
                n += 1
        return -1 * n



