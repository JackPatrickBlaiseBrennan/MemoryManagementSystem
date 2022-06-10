from HashTable import *
from MemRequest import *
from Block import *
 
class Manager:
    def __init__(self):
        """
        Constructer: Sets up memory paritions and the freeMemory tracker
        """
        # Set Up A Hash Table for freeMem memory management and a Queue for requests
        self.__freeMem = HashTable()
        self.__requests = Queue()
        # setup main and inMemory as just a representation of the hardware
        # main is how the memory is currently paritioned contains all blocks
        # inMemory is what blocks are currently being used
        self.__main = HashTable()
        self.__inMemory = HashTable()
        # end string for printing results
        self.__endString = "#######################################################"
        # varaibles for printing fragmentation
        self.__internalFrag = 0
        # internal fragmentation starts at 4MB as no memory is being used
        self.__externalFrag = 4000
        # set up inital memory paritions
        self.__blockArray = [16,16,16,16,16,8]
        self.__pageArray = [32,16,8,4,2,1]
        for i in range(len(self.__blockArray)):
          for b in range(self.__blockArray[i]):
            block = Block(self.__pageArray[i],self.__pageArray[i]*4)
            self.__freeMem.addItem(block.size,block)
            self.__main.addItem(block.size,block)
        #print INITIALISED string
        print(f"# MANAGER INITIALISED #\n# FREE MAIN MEMORY #\n{self.__freeMem}\n# ALL MAIN MEMORY #\n{self.__main}{self.__endString}")
 
    def addRequest(self,request):
        """
        Adds requests to the Request Queue
        Args:
            request (MemRequest): The request to be added
        Raises:
            TypeError: if it is not a Request
        """
        # check if it is a request
        if type(request) is MemRequest:
            # add to Queue
            self.__requests.add_last(request)
        else:
            # if not raise error
            raise TypeError("Must be of type MemRequest")
 
    def run(self):
        """
        Run the management system.
        """
        # print that the system is running
        print(f"# RUNNING MEMORY MANGEMENT SYSTEM #\n{self.__endString}")
        # for each in the queue
        for request in self.__requests:
            # if the request is allocation/replacement
            if request.typeReq == "A":
                #choose wether it should be for allocation or replacement
                self.__choose(request)
            # if its a deallocation deallocate
            elif request.typeReq == "D":
                self.__deAllocate(request)
            # otherwise must be a write
            else:
                self.__write(request)
 
    def __choose(self, request):
        # check if any freeMemory left
        if self.__freeMem.size > 0:
            # store the outcome as we want to print the freeMem after
            keepOutcome = self.__allocate(request)
            print(f"# FREE MAIN MEMORY #\n{self.__freeMem}\n{self.__endString}")
            # we return the outcome as write uses it to determine if a deffer has occured
            return keepOutcome
        # if no free replace
        else:
            # return reason same as above
            return self.__replacement(request)
 
    def __allocate(self,request):
        # check if request inMemory
        check = self.__inMemory.getBlocksOf(request.id)
        if check and check.top() is not None:
            # if so set A bit and print string
            check.top()._item.bitA = True
            print(f"# MEMEORY ALREADY ALLOCATED FOR {check.top()._item} #\n# SETTING A BIT #\n{self.__endString}")
            return
        # otherwise select size
        nSize = self.__selectSize(request)
        # get a block of that size
        block = self.__freeMem.takeItem(nSize)
        # if no block found split some
        if block is None:
            biggerFinder = nSize
            while block is None:
                # get next block size
                biggerFinder = biggerFinder * 2
                # if this size is bigger than max replacement must be used instead
                if biggerFinder > 128:
                    return self.__replacement(request)
                # check if there is a block of this size
                block = self.__freeMem.takeItem(biggerFinder)
            # when ones found split it to the size needed
            block = self.__split(block,nSize)
        # set the blocks requestId and add to inMemory(the hardware would just know this)
        block.requestId = request.id
        self.__inMemory.addItem(request.id, block)
        # set the A bit to 1 and set the amount of the block used
        block.bitA = True
        block.amount = request.size
        # print allocation and do fragmentaion
        print(f"# MEMEMORY ALLOCATED #\n{block} For {request.size}KB\n{self.__endString}")
        self.__internalFrag += (block.size - block.amount)
        self.__externalFrag -= block.size
        print(f"# TOTAL CURRENT FRAGMENTAION #\n# EXTERNAL {self.__externalFrag} + INTERNAL {self.__internalFrag} = {self.__externalFrag + self.__internalFrag}KB\n{self.__endString}")
 
    def __selectSize(self, request):
        nSize = request.size
        # check if it's below min allocation if so return that
        if nSize < 4:
            return 4
        else:
            # bitwise method to round nSize up to the closest power of two
            # method only works for 32 bit numbers but since we know none of my base parition
            # sizes are not above that this method is suitable
            nSize -= 1
            nSize |= nSize >> 1
            nSize |= nSize >> 2
            nSize |= nSize >> 4
            nSize |= nSize >> 8
            nSize |= nSize >> 16
            nSize += 1
            # return size of the block needed
            return nSize
 
    def __replacement(self, request, sizeN=None):
        # if no size is given
        if sizeN is None:
            # calculate one
            sizeN = self.__selectSize(request)
        # get the blocks of that size
        clock = self.__main.getBlocksOf(sizeN)
        # if there is some
        if clock and clock.top() is not None:
            # create two hands handA is looking for the replacee the other is saving
            handA = clock.top()
            handM = clock.top()
            # set the second half way through
            for i in range(clock.size//2):
                handM = handM._nextNode
            # while the main hand points to something other than 00, each loop is a fault
            while (handA._item.bitA or handA._item.bitM) is True:
                # set the replacee A to False if True
                if handA._item.bitA is True:
                    handA._item.bitA = False
                # if the handM is pointing to something not saved save it
                if handM._item.bitM is True:
                    # save write to disk
                    print(f"# HAND SAVING BLOCK OF {handM._item.size}KB #\n{handM._item}\n{self.__endString}")
                    handM._item.bitM = False
                # move the hands on
                handA = handA._nextNode
                handM = handM._nextNode
                # if at the end of the clock move to start
                if not handA:
                    handA = clock.top()
                if not handM:
                    handM = clock.top()
            # print what is to be replaced and remove it from memory
            print(f"# MEMORY REPLACED #\n{handA._item}IS REPLACED BY", end = '')
            self.__inMemory.removeSpecfic(handA._item.requestId,handA._item)
            # add on to fragmentation
            self.__internalFrag += (handA._item.amount - request.size)
            # give the block the new request and amount and add it to memory
            handA._item.requestId = request.id
            handA._item.amount = request.size
            self.__inMemory.addItem(handA._item.requestId,handA._item)
            handA._item.bitA = True

            # print the requestId with replaced it and exit the method
            print(f"{handA._item}\n{self.__endString}")
            # print fragmentation
            print(f"# TOTAL CURRENT FRAGMENTAION #\n# EXTERNAL {self.__externalFrag} + INTERNAL {self.__internalFrag} = {self.__externalFrag + self.__internalFrag}KB\n{self.__endString}")
            return
        # otherwise there isn't any blocks of that size
        # As the allocation and deallocation of requests is dictated by the cpu
        # And all blocks of a size must be split to a lower size for this to occur.
        # I've deemed this unlikely to happen so, I've just deffered the request.
        print(f"# NO MEMORY BLOCKS OF REQUIRED SIZE AVAILABLE #\n# RECOMMENEDED DEALLOCATION # REQUEST DEFFERED #\n{self.__endString}")
        self.__requests.add_last(request)
        # return True to tell the write that allocation/replacement was unsuccessful
        return True
 
    def __write(self, request):
        # check if the request is in memeory
        blocks = self.__inMemory.getBlocksOf(request.id)
        if blocks and blocks.top() is not None:
            #if so write
            blocks.top()._item.bitM = True
            print(f"# WRITITNG TO BLOCK #\n{blocks.top()._item}\n{self.__endString}")
            return
        # if not try to allocate
        if self.__choose(request):
            # if it fails (None is exspected, so True is a fail) print the deffer
            print(f"# WRITE DEFFERED DUE TO ALLOCATION PROBLEM # \n{self.__endString}")
        else:
            # otherwise write to the memory
            block = self.__inMemory.getBlocksOf(request.id).top()._item
            block.bitM = True
            print(f"# NOW IN MEMEORY WRITITNG TO BLOCK #\n{block}\n{self.__endString}")
 
    def __deAllocate(self, request):
        # check if the block needs to be saved
        if self.__inMemory.getBlocksOf(request.id) and self.__inMemory.getBlocksOf(request.id).top():
            block = self.__inMemory.takeItem(request.id)
            if block.bitM:
                # save
                print(f"# DEALLOCATION IS SAVING BLOCK OF {block.size}KB #\n{self.__endString}")
                block.bitM = False
            # deallocate
            block.requestId = None
            # fragmentation update
            self.__internalFrag -= (block.size - block.amount)
            self.__externalFrag += block.size
            # print deallocation and fragmentation
            print(f"# DEALLOCATED BLOCK OF {block.size}KB #\n{self.__endString}")
            print(f"# TOTAL CURRENT FRAGMENTAION #\n# EXTERNAL {self.__externalFrag} + INTERNAL {self.__internalFrag} = {self.__externalFrag + self.__internalFrag}KB\n{self.__endString}")
            # check if pair available
            self.__pair(block)
            # add to free memory
            self.__freeMem.addItem(block.size,block)
        else:
            # if theres none in memory print that theres nothing in memory
            print(f'# NO BLOCK IN MEMORY TO DEALLOCATE #\n{self.__endString}')
 
    def __addBlockFreeMainMem(self,block):
        # add block to the main and freeMem
        self.__freeMem.addItem(block.size,block)
        self.__main.addItem(block.size,block)
 
    def __removeBlockFreeMainMem(self,block):
        # remove block from main and frreMem
         self.__freeMem.removeSpecfic(block.size,block)
         self.__main.removeSpecfic(block.size,block)
 
    def __split(self, block, sizeN):
        # have the orginal size
        orgi = block.size
        # loop until split the block to the required size
        while block.size != sizeN:
            # print split
            print(f"# Splitting Block Of {block.size}KB #\n{self.__endString}" )
            # adjust pages and size and make the buddy
            block.pages = block.pages//2
            block.size = block.size//2
            bud = Block(block.pages,block.size, block)
            block.buddy = bud
            # maintain free and main
            self.__addBlockFreeMainMem(bud)
        # split done
        print(f"# SPLIT DONE #\n{self.__endString}")
        # maintain the key being the blocks size in the main
        self.__main.removeSpecfic(orgi, block)
        self.__main.addItem(block.size, block)
        return block
 
    def __pair(self, block):
        # check if the block has a buddy and if that body is not allocated and if its the same size as itself
        if block.buddy != None and block.buddy.requestId == None and block.buddy.size == block.size:
            bud = block.buddy
            print(f"# PAIRED #\n# {block} with {bud} #")
            # update the block pages and sizes
            block.pages = block.pages * 2
            block.size = block.size * 2
            # remove the buddy
            block.buddy = None
            # take out from free and main
            self.__removeBlockFreeMainMem(bud)
            # delete the buddy
            del(bud)
            print(f"# NEW BLOCK : {block} #\n{self.__endString}")
 
