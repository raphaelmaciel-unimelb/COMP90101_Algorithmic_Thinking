class CompetitorArray:
    def __init__(self):
        self.A = [None] * (10**6) # Pre-allocated up to 1M items
        self.cnt = 0
        self.i_max = -1

    def getTop(self):
        """Returns the maximum element without removing it."""
        if self.i_max == -1:
            return None
        return self.A[self.i_max]
    
    def push(self, key):
        self.A[self.cnt] = key
        
        # Update i_max if array was empty or new key is larger
        if self.i_max == -1 or key > self.A[self.i_max]:
            self.i_max = self.cnt
            
        self.cnt += 1  # Always increment count on every push
        

    def _find_max_index(self):
        """Scans valid elements from index 0 to cnt - 1 to find the max value's index."""
        max_idx = 0
        for i in range(1, self.cnt):
            if self.A[i] > self.A[max_idx]:
                max_idx = i
        return max_idx

    def pop(self):
        """Removes and returns the maximum element, then rescans to update i_max."""
        # 1. Empty check
        if self.i_max == -1:
            return None
            
        # 2. Save current max value
        key_max = self.A[self.i_max]
        
        # 3. Swap max element with the last valid element in the array
        self.A[self.i_max] = self.A[self.cnt - 1]
        
        # 4. Remove the last element by reducing count
        self.cnt -= 1
        
        # 5 & 6. Update i_max
        if self.cnt == 0:
            self.i_max = -1
        else:
            self.i_max = self._find_max_index()
            
        # 7. Return maximum key
        return key_max