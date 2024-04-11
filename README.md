# PageWalk
Implementation of a Page Walk algorithm used in virtualization that is written in Python. It takes an input of various parameters, however it is meant to simply translate a virtual address to its physical counterpart.

Test case:
  Input:
    python ./PageWalk_Alg.py 0x535385a4871e43d1 0x6520e289eea2a5c8 ept_tables.csv 0x0000EF0123456789
                                   ^                    ^                ^                ^
                                   |                    |                |                |
                                  CR3               EPT_Pointer     adress table   virtual address
  Expected Output: 
    0x1a49a56db789
          ^
          |
   Physical address
  

