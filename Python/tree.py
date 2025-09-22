# from typing import List, Optional

# class ListNode:
#     def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
#         self.val = val
#         self.next = next

# def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
#     if not lists or len(lists) == 0:
#         return None

#     while len(lists) > 1:
#         merged_lists = []

#         for i in range(0, len(lists), 2):
#             l1 = lists[i]
#             l2 = lists[i+1] if (i+1) < len(lists) else None
#             merged_lists.append(mergeLists(l1, l2))

#         lists = merged_lists

#     return lists[0]

# def mergeLists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
#     dummy = ListNode()
#     tail = dummy

#     while l1 and l2:
#         if l1.val <= l2.val:
#             tail.next = l1  # reuse node
#             l1 = l1.next
#         else:
#             tail.next = l2
#             l2 = l2.next
#         tail = tail.next

#     tail.next = l1 if l1 else l2  # append the remainder
#     return dummy.next

from typing import List, Optional
import heapq

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

    # Required for comparison in heap
    def __lt__(self, other):
        return self.val < other.val

def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    min_heap = []

    # Step 1: Add head of each non-empty list to the heap
    for idx, node in enumerate(lists):
        if node:
            heapq.heappush(min_heap, node)

    # Dummy head and current pointer
    dummy = ListNode(0)
    current = dummy

    # Step 2: Pop the smallest element and add its next to heap
    while min_heap:
        smallest = heapq.heappop(min_heap)
        current.next = smallest
        current = current.next
        if smallest.next:
            heapq.heappush(min_heap, smallest.next)

    return dummy.next

def build_linked_list(values):
    dummy = ListNode()
    curr = dummy
    for val in values:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def print_linked_list(head):
    while head:
        print(head.val, end=' → ' if head.next else '\n')
        head = head.next

lists = [
    build_linked_list([1, 4, 5]),
    build_linked_list([1, 3, 4]),
    build_linked_list([2, 6])
]

result = mergeKLists(lists)
print_linked_list(result)
