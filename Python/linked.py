class Node:
    def __init__(self, data, next=None,prev=None):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f'[{self.data}]'

class LinkedList:
    def __init__(self,head=None,tail=None):
        self.head = head
        self.tail = tail

    def generate_from_list(self,lst):
        
        if lst:
            self.head = Node(lst[0])
            curr = self.head
            for idx in range(1,len(lst)):
                curr.next = Node(lst[idx])
                prev = curr
                curr = curr.next
                curr.prev = prev
            self.tail = curr
        else:
            print("Unable to generate. Given empty list!")

    
    def display(self):
        
        if self.head:
            curr = self.head
            while curr:
                print(curr,end=" ")
                curr = curr.next
            print()
        else:
            print("Linked List is empty")

    def print_backwards(self):
        if self.tail:
            curr = self.tail
            while curr:
                print(curr,end=" ")
                curr = curr.prev
            print()
        else:
            print("Linked List is empty")

lst = [112, 42, 83, 119]
LL = LinkedList()
LL.generate_from_list(lst)
LL.display()
LL.print_backwards()

