def heapify(arr):
    """Converts an unsorted list into a Max-Heap in-place in O(n) time."""
    n = len(arr)

    def bubble_down(index):
        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            # Compare with left child
            if left < n and arr[left] > arr[largest]:
                largest = left
            # Compare with right child
            if right < n and arr[right] > arr[largest]:
                largest = right

            # If current node is already larger than both children, stop
            if largest == index:
                break

            # Swap and continue down
            arr[index], arr[largest] = arr[largest], arr[index]
            index = largest


    
    # 1. Identify the last non-leaf node: (n // 2) - 1
    start_index = (n // 2) - 1

    # 2. Iterate backwards from last non-leaf node down to the root
    for i in range(start_index, -1, -1):
        bubble_down(i)

    return arr

# Example
data = [4, 10, 3, 5, 1, 15, 8]
heapify(data)
print("Max-Heap:", data)
# Output: [15, 10, 8, 5, 1, 3, 4]