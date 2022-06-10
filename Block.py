class Block:
    def __init__(self,pages, size,buddy=None):
        """
        Constructor
        Args:
            pages (int): number of pages in the block
            size (int): size of the block
            buddy (Block or None): the buddy of this block
        Raises:
            TypeError: If the types of the args are wrong
        """
        self.pages = pages
        self.size = size
        self.buddy = buddy
        self.requestId = None
        self.amount = 0
        # I judged that I would be implementing global replacement by replacing entire blocks.
        # So I combined the A bits and M bits of the pages in the block into one value.
        # The bits of the individual pages in the block will all change at the same time.
        self.bitA = False
        self.bitM = False
 
    def __str__(self):
        """
        Returns String Version of the ADT
        Returns:
            (String): The pages, and requestId if there is one of the block
        """
        return f"< Block # Size: {self.__size}KB, RequestId: {self.__requestId} >"
 
    #getter setter
    def getPages(self):
        """
        Page Getter
        Returns:
            (int): number of pages in the block
        """
        return self.__pages
 
    def setPages(self,value):
        """
        Page Setter
        Args:
            value (int): number of pages in the block
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) is int:
            self.__pages = value
        else:
            raise TypeError("Must be of type int")
    pages = property(getPages,setPages)
 
    def getSize(self):
        """
        Size Getter
        Returns:
            (int): size of the block in KB
        """
        return self.__size
 
    def setSize(self,value):
        """
        Size Setter
        Args:
            value (int): size of the block to be set
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) is int:
            self.__size = value
        else:
            raise TypeError("Must be of type int")
    size = property(getSize,setSize)
 
    def getBuddy(self):
        """
        Buddy Getter
        Returns:
            (Block): block that is buddy to this block
        """
        return self.__buddy
 
    def setBuddy(self,value):
        """
        Buddy Setter
        Args:
            value (Block or None): The buddy to be set
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) == Block or value == None:
            self.__buddy = value
        else:
            raise TypeError("Must be of type Block")
 
    buddy = property(getBuddy,setBuddy)
 
    def getRequestId(self):
        """
        RequestId Getter
        Returns:
            (int): id of the request which has been allocated this block
        """
        return self.__requestId
 
    def setRequestId(self,value):
        """
        RequestId Setter
        Args:
            value (int or None): id of the request to be set to this block
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) is int or value == None:
            self.__requestId = value
        else:
            raise TypeError("Must be of type int")
    requestId = property(getRequestId,setRequestId)
 
    def getAmount(self):
        """
        Amount Getter
        Returns:
            (int): amount of the data in the block in KB
        """
        return self.__amount
 
    def setAmount(self,value):
        """
        Amount Setter
        Args:
            value (int): amount of dat in the block to be set
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) is int and value <= self.size:
            self.__amount = value
        else:
            raise TypeError("Must be of type int")
    amount = property(getAmount,setAmount)
 
    def getBitA(self):
        """
        BitA Getter
        Returns:
            (bool): bitA of the pages of the block
        """
        return self.__bitA
 
    def setBitA(self, value):
        """
        BitA Setter
        Args:
            value (bool): bitA of the pages of the block
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) is bool:
            self.__bitA = value
        else:
            raise TypeError("Must be of type bool")
    bitA = property(getBitA,setBitA)
 
    def getBitM(self):
        """
        BitM Getter
        Returns:
            (bool): id of the process
        """
        return self.__bitM
 
    def setBitM(self, value):
        """
        BitM Setter
        Args:
            value (bool): bitM of the pages of the block
        Raises:
            TypeError: If the types of the args are wrong
        """
        if type(value) is bool:
            self.__bitM = value
        else:
            raise TypeError("Must be of type bool")
    bitM = property(getBitM,setBitM)
