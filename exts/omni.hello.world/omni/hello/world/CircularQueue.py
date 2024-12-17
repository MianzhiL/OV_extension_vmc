class CircularQueue:
    def __init__(self, max_size):
        self.queue = [None] * max_size
        self.max_size = max_size
        self.head = -1
        self.tail = -1

    def enqueue(self, data):
        if (self.tail + 1) % self.max_size == self.head:
            print("Queue is full!")
            return False
        elif self.head == -1:  # First element
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 1) % self.max_size
            self.queue[self.tail] = data
        return True

    def dequeue(self):
        if self.head == -1:
            print("Queue is empty!")
            return None
        data = self.queue[self.head]
        if self.head == self.tail:  # Only one element was present
            self.head = -1
            self.tail = -1
        else:
            self.head = (self.head + 1) % self.max_size
        return data

    def front(self):
        if self.head == -1:
            print("Queue is empty!")
            return None
        return self.queue[self.head]

    def is_empty(self):
        return self.head == -1

    def is_full(self):
        return (self.tail + 1) % self.max_size == self.head

    def size(self):
        if self.is_empty():
            return 0
        elif self.tail >= self.head:
            return self.tail - self.head + 1
        else:
            return self.max_size - (self.head - self.tail) + 1


