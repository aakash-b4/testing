import random
ran="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
def randomString(length=16):
    s=""
    for i in range(length):
      no=random.randint(0,len(ran)-1)
      s=s+ran[no]
    return s

def randomNumber(length=16):
    s=""
    count=0
    for i in range(length):
      if count ==0:
        no = random.randint(1,9)
      else:
       no=random.randint(0,9)
      s=s+str(no)
      count+=1
    return s


