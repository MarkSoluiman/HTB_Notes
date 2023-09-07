from pwn import *

key=list(b"SUPERSECURE")
flag=[]

encrypt=read("login.xlsx.enc")

#print (encrypt)

count=0

for byte in encrypt :
	flag.append(byte-key[count%len(key)])
	count+=1


print(flag)

