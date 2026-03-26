import random

def merge_sort(array, low, high):
    if low < high:
        split = (high - low) // 3
        low_mid = low + split; 
        high_mid = low +2 * split; 
        merge_sort(array, low, low_mid)
        merge_sort(array, low_mid + 1, high_mid)
        merge_sort(array, high_mid + 1, high)
        merge(array, low, low_mid, high_mid, high)

def merge(array, low, low_mid, high_mid, high):
    temp = [0] * (high - low + 1)       
    i = low
    j = low_mid + 1
    p = high_mid + 1
    k = 0
    while i <= low_mid and j <= high_mid and p <= high: 
        if array[i] < array[j] and array[i] < array[p]:     # If the value in A is lower than the value in B
            temp[k] = array[i]          # Increment A
            i += 1
        elif array[j] < array[p] and array[j] < array[i]:   # If the value in B is lower than the value in C
            temp[k] = array[j]          # Increment B
            j += 1
        else:                           # If the value in C is lower than B
            temp[k] = array[p]          # Increment C
            p += 1
        k += 1
    while i <= low_mid and j <= high_mid:    # A and B remain
        if array[i] <= array[j]: temp[k] = array[i]; i += 1
        else:                     temp[k] = array[j]; j += 1
        k += 1
    while i <= low_mid and p <= high:        # A and C remain
        if array[i] <= array[p]: temp[k] = array[i]; i += 1
        else:                     temp[k] = array[p]; p += 1
        k += 1
    while j <= high_mid and p <= high:       # B and C remain
        if array[j] <= array[p]: temp[k] = array[j]; j += 1
        else:                     temp[k] = array[p]; p += 1
        k += 1
    while i <= low_mid:                 # Handle remaining in A
        temp[k] = array[i]
        i += 1
        k += 1
    while j <= high_mid:                # Handle remaining in B
        temp[k] = array[j]
        j += 1
        k += 1
    while p <= high:                    # Handle remaining in C
        temp[k] = array[p]
        p += 1
        k += 1
    for i in range(high - low + 1):     # Copy temp to array
        array[low + i] = temp[i] 


array = [0] * 10
for i in range(10):
    # Generate random number between 0 and 100
    array[i] = random.randint(0, 99)
    print(array[i], end=" ")

print()
merge_sort(array, 0, 9)

# Print array
for i in range(10):
    print(array[i], end=" ")
print()
