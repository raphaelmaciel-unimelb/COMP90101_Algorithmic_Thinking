class MaxHeap:
    def __init__(self):
        self.heap = []

    def getTop(self):
        """Returns the root (maximum element) in O(1) without removing it."""
        if not self.heap:
            return None
        return self.heap[0]

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def push(self, key):
        """Inserts a new element and restores heap order upwards."""
        self.heap.append(key)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        """Removes and returns the maximum element (root) in O(log n)."""
        if not self.heap:
            return None
        
        # Save the root value
        max_val = self.heap[0]
        
        # Move the last element to the root
        last_val = self.heap.pop()
        
        if self.heap:  # If heap is not empty, restore structure
            self.heap[0] = last_val
            self._bubble_down(0)
            
        return max_val
        
    def _bubble_up(self, index):
        while index > 0:
            p_idx = self._parent(index)
            # If the current node is greater than its parent, swap them
            if self.heap[index] > self.heap[p_idx]:
                self.heap[index], self.heap[p_idx] = self.heap[p_idx], self.heap[index]
                index = p_idx  # Move up to parent's position
            else:
                break
    
    def _bubble_down(self, index):
        n = len(self.heap)
        while True:
            largest = index
            l_idx = self._left(index)
            r_idx = self._right(index)

            # Check if left child exists AND is larger than current largest
            if l_idx < n and self.heap[l_idx] > self.heap[largest]:
                largest = l_idx

            # Check if right child exists AND is larger than current largest
            if r_idx < n and self.heap[r_idx] > self.heap[largest]:
                largest = r_idx

            # If a child was larger, swap and push down further
            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break # Heap property restored

    def heapify(self, unsorted_list):
        """Converts an unsorted list into a valid Max-Heap in O(n) time."""
        self.heap = unsorted_list[:]  # Make a copy of the input list
        
        n = len(self.heap)
        start_idx = (n // 2) - 1      # Index of the last non-leaf parent
        
        # Sift down each parent from bottom to top
        for i in range(start_idx, -1, -1):
            self._bubble_down(i)