import time
startTime = time.time()

#####your python script#####

def secilen(isim):
    with open('C:/Users/berke/Desktop/qrapp/secilen.txt','w',encoding='utf-8') as f:
        f.write(isim)
        
secilen('something.png')

executionTime = (time.time() - startTime)
print(executionTime)