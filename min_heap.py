def heapify(arr, n, i): 
	samallest = i # Initialize samallest as root 
	l = 2 * i + 1
	r = 2 * i + 2

	if l < n and arr[i] > arr[l]:
		samallest = l

	if r < n and arr[samallest] > arr[r]:
		samallest = r

	if samallest != i:
		arr[i],arr[samallest] = arr[samallest],arr[i]

		heapify(arr, n, samallest)

def minHeap(arr, n):
    for i in range(n, -1, -1):
	    heapify(arr, n, i)

def heapPop(arr):
    min_ = arr.pop(0)
    minHeap(arr, len(arr))
    return min_

# a = [1,23,4,5,3,2,5,6,2,4,-1]
# minHeap(a, len(a))
# print(heapPop(a))
