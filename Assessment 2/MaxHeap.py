class MaxHeap:
    """Max-Heap implementation using a complete binary tree array representation."""

    def __init__(self):
        self.heap = []

    def getTop(self):
        """Returns the maximum element (root) in O(1) without removing it."""
        if not self.heap:
            return None
        return self.heap[0]

    def push(self, key):
        """Inserts a new key and restores max-heap property upwards in O(log N)."""
        self.heap.append(key)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        """Removes and returns the maximum key in O(log N)."""
        if not self.heap:
            return None
        
        max_val = self.heap[0]
        last_val = self.heap.pop()
        
        if self.heap:
            self.heap[0] = last_val
            self._bubble_down(0)
            
        return max_val

    def heapify(self, unsorted_list):
        """Converts an unsorted list into a valid Max-Heap in O(N) using Floyd's algorithm."""
        self.heap = unsorted_list[:]
        n = len(self.heap)
        
        for i in range((n // 2) - 1, -1, -1):
            self._bubble_down(i)

    def _bubble_up(self, index):
        heap = self.heap
        while index > 0:
            p_idx = (index - 1) // 2
            if heap[index] > heap[p_idx]:
                heap[index], heap[p_idx] = heap[p_idx], heap[index]
                index = p_idx
            else:
                break

    def _bubble_down(self, index):
        heap = self.heap
        n = len(heap)
        while True:
            largest = index
            l_idx = 2 * index + 1
            r_idx = 2 * index + 2

            if l_idx < n and heap[l_idx] > heap[largest]:
                largest = l_idx
            if r_idx < n and heap[r_idx] > heap[largest]:
                largest = r_idx

            if largest != index:
                heap[index], heap[largest] = heap[largest], heap[index]
                index = largest
            else:
                break