"""
 Data structures useful for implementing SearchAgents
"""
import math
import random

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        Queue.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = Queue.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))


def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def euclidianDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return ( xy1[0] - xy2[0] )**2 + ( xy1[1] - xy2[1] )**2

def countVisited(visited):
    size = len(visited)
    count = 0
    for y in range(size):
        for x in range(size):
            if visited[y][x]:
                count += 1

    return count

def nodeHash(k1,k2):
    return ((k1+k2)*(k1+k2+1))/2 + k2


def unHash(z):
    w = math.floor((math.sqrt(8 * z + 1) - 1)/2)
    t = (w**2 + w) / 2
    y = int(z - t)
    x = int(w - y)
    # assert z != pair(x, y, safe=False):
    return x, y


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, x=0, y=0):
        self.parent = parent
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + self.x + ", " + self.y + ")"

def uniqify(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)

       if marker in seen:
            continue

       seen[marker] = 1
       result.append(item)
   return result

def insertionSortLoc(pprint, arr, loc):
  
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)): 
  
        key = arr[i]
        # pprint(str(arr))
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and euclidianDistance(key,loc) < euclidianDistance(arr[j],loc) : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key


def insertionSort(pprint, arr):
  
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)): 
  
        key = arr[i]
        # pprint(str(arr))
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key


def quadrant(x,y):
    if x >= 0:
        if y >= 0:
            return 1
        else:
            return 4
    else:
        if y >= 0:
            return 2
        else:
            return 3

def quadSplit(arr):
    quadrantSplits = [[],[],[],[]]

    for element in arr:
        quadrantSplits[quadrant(*element)-1].append(element)

    # flat_list = [item for sublist in quadrantSplits for item in sublist]

    return quadrantSplits

def crossScale():
    return 1/3

def crossBranch():
    return random.randint(1,4)

def crossLength():
    return 27

def crossAngle(branch):
    return math.pi*branch / 2

def dec2bin(n):
    if n < 0:
        return 'Must be a positive integer'
    elif n == 0:
        return '0'
    else:
        return dec2bin(n//2) + str(n%2)


def dec2Bin(num,width):
    binRepr = dec2bin(num)
    while len(binRepr) < width:
        binRepr = "0" + binRepr
    if len(binRepr) > width:
        binRepr = binRepr[len(binRepr) - width:]
    return binRepr

def bin2dec(binary):
    decimal = 0 
    for digit in binary: 
        decimal = decimal*2 + int(digit) 
    return decimal

def isclose(a,b,abs_tol=0):
    return abs(a-b) <= abs_tol



    
    
