class CompetitorArray:
    """Competitor implementation using a flat pre-allocated array tracking cnt and i_max."""

    def __init__(self, capacity=1_000_000):
        self.A = [0] * capacity  # Array A of length 10^6
        self.cnt = 0             # Counter initialized to 0
        self.i_max = -1          # Index of largest element initialized to -1

    def push(self, key):
        """Pushes an element key into array A."""
        # A[cnt] <- key
        self.A[self.cnt] = key

        # if i_max == -1 or A[i_max] < A[cnt], i_max <- cnt
        if self.i_max == -1 or self.A[self.i_max] < self.A[self.cnt]:
            self.i_max = self.cnt

        # cnt <- cnt + 1
        self.cnt += 1

    def pop(self):
        """Removes and returns the maximum element keymax."""
        # if i_max == -1, return null
        if self.i_max == -1:
            return None

        # keymax <- A[i_max]
        keymax = self.A[self.i_max]

        # swap element A[i_max] with A[cnt - 1]
        self.A[self.i_max], self.A[self.cnt - 1] = self.A[self.cnt - 1], self.A[self.i_max]

        # delete A[cnt - 1] by setting cnt <- cnt - 1
        self.cnt -= 1

        # if cnt == 0, set i_max <- -1
        if self.cnt == 0:
            self.i_max = -1
        else:
            # find new maximum element by scanning array A from index 0 to cnt - 1
            new_max_idx = 0
            for i in range(1, self.cnt):
                if self.A[i] > self.A[new_max_idx]:
                    new_max_idx = i
            self.i_max = new_max_idx

        # return keymax
        return keymax

    def getTop(self):
        """Returns the maximum element keymax without removing it."""
        # if i_max == -1, return null
        if self.i_max == -1:
            return None

        # keymax <- A[i_max]
        keymax = self.A[self.i_max]

        # return keymax
        return keymax