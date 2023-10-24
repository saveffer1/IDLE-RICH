class LimitedQueue:
    def __init__(self, max_size:int=5):
        self._queue = []
        self.max_size = max_size
    
    def enqueue(self, item):
        if len(self._queue) >= self.max_size:
            self.dequeue()
        self._queue.append(item)
    
    def dequeue(self):
        self._queue.pop(0)
        
    def queue(self):
        return self._queue
    
    def __getitem__(self, index):
        return self._queue[index]
    
    def __len__(self):
        return len(self._queue)
    
    def __str__(self):
        return str(self._queue)