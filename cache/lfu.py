from .dict import CacheDict


class FreqNode:

    def __init__(self, key):
        self.key = key
        self.pre = None
        self.next = None
        self.freq_link: FreqLinkNode | None = None

    def remove_from_link(self):
        if self.pre is not None:
            self.pre.next = self.next

        if self.next is not None:
            self.next.pre = self.pre

        self.next = self.pre = None

    def move_forward(self):
        self.freq_link.move_node(self)


class FreqLinkNode:
    def __init__(self, freq):
        self.freq = freq

        self.head = None
        self.tail = None

        self.next_link = None
        self.pre_link = None

    def add(self, node):
        if self.head is None:
            self.tail = node

        else:
            self.head.pre = node

        node.next = self.head
        self.head = node

    def dump_tail(self):
        self.tail = self.tail.pre

        if self.tail is not None:
            self.tail.next = None

        if self.head is self.tail:
            self.head = None

        self.delete_if_empty()

    def move_node(self, freq_node):
        if self.next_link is None:
            self.next_link = FreqLinkNode(self.freq + 1)
            self.next_link.pre_link = self

        elif self.next_link.freq != self.freq + 1:
            link = FreqLinkNode(self.freq + 1)
            link.next_link = self.next_link
            self.next_link.pre_link = link
            self.next_link = link
            link.pre_link = self

        if self.head is freq_node:
            self.head = freq_node.next

        if self.tail is freq_node:
            self.tail = freq_node.pre

        freq_node.remove_from_link()
        self.next_link.add(freq_node)

        self.delete_if_empty()

    def delete_if_empty(self):
        if self.head is None:
            if self.pre_link is not None:
                self.pre_link.next_link = self.next_link
            if self.next_link is not None:
                self.next_link.pre_link = self.pre_link

            self.pre_link = self.next_link = None


class LFUCache:
    def __init__(self, capacity=10, ttl=30000):
        self.capacity = capacity + 1
        self.cache = CacheDict(ttl)
        self.freq_dict = {}
        self.freq_link_head = None

    def set(self, key, value):

        if self.cache.get(key) is not None:
            self.cache[key] = value
            return

        freq = FreqNode(key)
        self.freq_dict[key] = freq

        if self.freq_link_head is None or self.freq_link_head.freq != 1:
            freq_link = FreqLinkNode(1)
            freq_link.next_link = self.freq_link_head
            self.freq_link_head = freq_link

        freq.freq_link = self.freq_link_head
        self.freq_link_head.add(freq)

        if len(self.cache) >= self.capacity:
            self._dump_cache()

        self.cache[key] = key

    def get(self, key):
        item = self.cache.get(key)
        freq_node = self.freq_dict.get(key)
        if item is None:
            return -1

        freq_node.move_forward()

        return item

    def _dump_cache(self):
        key = self.freq_link_head.tail.key
        self.cache.pop(key)
        self.freq_dict.pop(key)
        self.freq_link_head.dump_tail()
