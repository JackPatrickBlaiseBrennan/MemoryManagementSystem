from DLL import *
class HashTable:
    def __init__(self):
        """
        Constructor: for the Hashtable with repeats
        """
        # decided to use a python dictionary as I wouldn't beat it's complexity
        self.__dict = dict()
        self.__size = 0
 
    def getBlocksOf(self,key):
        """
        Get the DLL List at a Key
        Args:
            key (any): the key of the DLL to be gotten
 
        Returns:
            DLL: the DLL at the key
        """
        return self.__dict.get(key)
 
    def addItem(self,key,value):
        """
        Add Item to the Hashtable
        Args:
            key (any): the key of the item
            value (any): the value to be added at the key
        """
        self.__size += 1
        # if there isn't a DLL at the key create one with the item in it
        # otherwise append the item to the list.
        self.__dict.setdefault(key,DLL()).add_last(value)
        # I decided to use a DLL list to enable adding muiltible values with the same key
        # as taking from the top() is low still complexity as well as making clock  replacement
        # easier to implement
 
    def takeItem(self,key):
        """
        Take an item from the top of a DLL and return it
        Args:
            key (any): the key of the item
        Returns:
            any: the item that was at the top of the list
        """
        # take the item and return it
        item = self.__dict[key].remove_first()
        # only alter size if somethings returned
        if item is not None:
            self.__size += -1
        return item
 
    def removeSpecfic(self,key,value):
        """
        Remove a specfic node from the Hashtable
        Args:
            key (any): the key of the item
            value (any): the item to be removed at the key
 
        Returns:
            any: the item that was specfically removed
        """
        self.__size += -1
        return self.getBlocksOf(key).specficRemove(value)
 
    def __str__(self):
        """
        Returns String Version of the ADT
        Returns:
            string: a string represtation of the HashTable
        """
        keystr = "Blocks of Size: '"
        string = ''
        # print every key and it's values
        for key in self.__dict:
            string += keystr + str(key) + "KB' : "
            string += str(self.__dict[key]) + ' \n'
        return string
 
    def getSize(self):
        """
        Size Getter
        Returns:
            int: the size of the Hashtable
        """
        return self.__size
    size = property(getSize)
