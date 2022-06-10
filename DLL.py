from Queue import *
 
class DLL(Queue):
    def __init__(self):
        """
        Constructer for DLL: The extension of the queue for specfic removes.
        """
        Queue.__init__(self)
        self.__cursor = None
 
    def specficRemove(self, value):
        """
        Remove a specfic node from the list
        Args:
            value (any): item of node to be removed
        """
        # start at start
        self.__cursor = self.head
        # while we havent gotten to the end
        while self.__cursor != None:
            # check if its the item if so remove it
            if self.__cursor._item == value:
                self.__remove_current()
                break
            # otherwise move on the cursor
            else:
                self.__cursor = self.__cursor._nextNode
 
    def __remove_current(self):
        # get prev and next
        nextnode = self.__cursor._nextNode
        prevnode = self.__cursor._prevNode
        # check if it is the head and if it is set the head to the next node
        if prevnode is None:
            self.head = self.head._nextNode
        else:
            prevnode._nextNode = nextnode
        # check if it is the tail
        if nextnode is None:
            # check if list now empty
            if prevnode is None:
                # set the none
                self.head = None
                self.size += -1
                return
        else:
            nextnode._prevNode = prevnode
        # otherwise just set to next node
        self.size += -1
        return
