class MemRequest:
    def __init__(self,id,size,typeReq):
        """
        Constructor
        Args:
            id (int): id of request
            size (int): size of memory request
            typeReq ('A'or'D'or'W'): type of the request 'A' for Allocation
                                   'D' for Deallocation 'W' for Write
        Raises:
            TypeError: If the types of the args are wrong
        """
        # type check
        if type(id) is int:
            self.__id = id
        else:
            raise TypeError("Must be of type int")
        # type check
        if type(size) is int and size < 129:
            # make sure requests are less than the max
            self.__size = size
        else:
            raise TypeError("Must be of type int and less than 129")
        # typeReq check
        if typeReq in ["A","D","W"]:
            self.__typeReq = typeReq
        else:
            raise TypeError("Must be of type int")
 
    def getId(self):
        """
        Id Getter
        Returns:
            (int): id of the request
        """
        return self.__id
    id = property(getId)
 
    def getSize(self):
        """
        Size Getter
        Returns:
            (int): size of memory request
        """
        return self.__size
    size = property(getSize)
 
    def getType(self):
        """
        Size Getter
        Returns:
            ("A" or "D" or "W"): type of request
        """
        return self.__typeReq
    typeReq = property(getType)
