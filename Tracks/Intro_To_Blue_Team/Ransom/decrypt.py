from pwn import *

key= list(b"SUPERSECURE") #b is for byte string

encrypted=read('login.xlsx.enc')

count=0

decrypted=[]


for byte in encrypted:
	decrypted.append(byte- key[count %len(key)])
	count+=1

print(decrypted)

