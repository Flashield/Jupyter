from random import shuffle as sl
from random import randint as rd
def gn():   #生成1到1000的一个随机数
    num = rd(1,1000)  
    return num  
def w2f(f,num,fg):  #将num写入文件f，并根据fg的值决定是否换行
    f.write(str(num))  
    if fg==True:  
        f.write('\n')  
    else:  
        f.write(' ')  
  
def DataMake(c):  #生成DAG，存入以c命名的文件内
    MAXL =100000;  
    f = open('data'+str(c)+'.in','w')  
    n = 1000  #设置图中节点数量
    node = range(1,n+1)  #生成1到n的一个序列
    node=list(node) #将格式转换成list，便于下一步随机重排
    sl(node)  #随机重排
    sl(node)  #随机重排，生成节点的序号。在这里，node[i]的值表示节点，i表示当前节点的拓扑序。
    m = rd(1,min(n*n,5000))  #设置图中边的数量
    w2f(f,n,0);w2f(f,m,1)  #将节点数量n和边的数量m写入文件f
    for i in range(0,m):  #随机生成m条边
        p1 = rd (1,n-1)  #选择第一个节点
        p2 = rd (p1+1,n)  #选择第二个节点，这个节点的拓扑序必须大于第一个节点
        x = node[p1-1]  #读取拓扑序为p1的节点
        y = node[p2-1]  #读取拓扑序为p2的节点
        l = rd(1,MAXL)  #生成一个1到MAXL的随机数
        w = gn()  #生成一个1到1000的随机数
        w2f(f,x,0);w2f(f,y,0);w2f(f,l,0);w2f(f,w,1)  #将x,y,l,w写入文件
    k = gn()  #生成一个1到1000的随机数k
    w2f(f,k,1)  #将k写入文件
    for i in range(0,k):  #生成k个1到1000的随机数
        w2f(f,gn(),1)  
    print(n,' node',m,' edges',k,'Queries')  
    f.close()  
  
DataMake(1)  #生成一个名为data1.in的文件，里面存储的就是一个DAG
print('Done')