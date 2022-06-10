class Node():
    def __init__(self, item, nextnode=None, prevnode=None):
        """
        Constructor
        Args:
            item (any): item of the Node
            nextnode (Node or None): reference to the next Node
            prevnode (Node or None): reference to previous Node
        """
        #protected attributes
        self._item = item
        self._nextNode = nextnode
        self._prevNode = prevnode
 
class Queue():
    def __init__(self):
        """
        Constructor
        """
        # ADT attributes
        self.__head = None
        self.__tail = None
        self.__size = 0
 
    def __iter__(self):
        """
        Implements Iteration For The Queue
        """
        item = self.top()
        while item is not None:
            yield item._item
            item = item._nextNode
 
    def _getHead(self):
        """
        Protected head Getter method
        Returns:
            Node or None: the head of the queue
        """
        return self.__head
 
    def _setHead(self,value):
        """
        Protected head Setter method
        Args:
            value (Node or None): the head of the queue
        """
        self.__head = value
    head = property(_getHead,_setHead)
 
    def _getSize(self):
        """
        Protected size Getter method
        Returns:
            int: size of the queue
        """
        return self.__size
 
    def _setSize(self,value):
        """
        Protected size Setter Method 
        Args:
            value (int): size of the queue
        """
        self.__size = value
    size = property(_getSize,_setSize)
 
    def __str__(self):
        """
        Returns String Version of the ADT
        Returns:
            (String): Queue formatted similar to a list
        """
        string = '['
        # print the list
        if self.__head is not None:
            curNode = self.__head
            for each in range(self.__size):
                string = string + str(curNode._item)  + ", "
                curNode = curNode._nextNode
            string = string[:-2]
            return string + ']'
        return 'None'
 
    def add_last(self,item):
        """
        Add to end of Queue
        Args:
            item (any): thing to be added
        """
        newNode = Node(item)
        #if empty set head
        if self.__head == None:
            self.__head = newNode
        # set tail next
        else:
            self.__tail._nextNode = newNode
            newNode._prevNode = self.__tail
        #set tail to next
        self.__tail = newNode
        self.__size += 1
 
    def top(self):
        """
        Get the item at the top of the Queue
        Returns:
            (any): item at top of the Queue
        """
        return self.__head
 
    def remove_first(self):
        """
        Remove the first item from the Queue
        Returns:
            (any): the first item from the queue
        """
        # only remove if there is something to remove
        if self.__size == 0:
            return None
        # get item
        item = self.__head._item
        # delete head
        __headNext = self.__head._nextNode
        if __headNext is not None:
            __headNext._prevNode = None
        del(self.__head)
        # move head to next
        self.__head = __headNext
        self.__size = self.__size - 1
        return item
