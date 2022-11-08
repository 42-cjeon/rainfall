> Password: 71d449df0f960b36e0055eb58c14d0f5d0ddc0b35328d657f91cf0df15910587 

bonus3의 어셈블리 코드를 보자.

먼저 fopen으로 다음 레벨의 패스워드 파일을 열고,

```
8048502:	ba f0 86 04 08       	mov    $0x80486f0,%edx
 8048507:	b8 f2 86 04 08       	mov    $0x80486f2,%eax
 804850c:	89 54 24 04          	mov    %edx,0x4(%esp)
 8048510:	89 04 24             	mov    %eax,(%esp)
 8048513:	e8 f8 fe ff ff       	call   8048410 <fopen("/home/user/end/.pass", "r")@plt>
 8048518:	89 84 24 9c 00 00 00 	mov    %eax,0x9c(%esp)<local:FILE *>
```

스택에 존재하는 버퍼에 그 내용을 읽어온 다음,

```
 804854d:	8d 44 24 18          	lea    0x18(%esp),%eax
 8048551:	8b 94 24 9c 00 00 00 	mov    0x9c(%esp),%edx
 8048558:	89 54 24 0c          	mov    %edx,0xc(%esp)
 804855c:	c7 44 24 08 42 00 00 	movl   $0x42,0x8(%esp)
 8048563:	00 
 8048564:	c7 44 24 04 01 00 00 	movl   $0x1,0x4(%esp)
 804856b:	00 
 804856c:	89 04 24             	mov    %eax,(%esp)
 804856f:	e8 5c fe ff ff       	call   80483d0 <fread(0x18(%esp), byte, 66, local:<FILE *>)@plt>
```

읽어온 버퍼에서 atoi(argv[1])만큼 뒤로 간 위치에 널 문자를 넣은 뒤에

```
 8048574:	c6 44 24 59 00       	movb   $0x0,0x59(%esp)
 8048579:	8b 45 0c             	mov    0xc(%ebp),%eax
 804857c:	83 c0 04             	add    $0x4,%eax
 804857f:	8b 00                	mov    (%eax),%eax
 8048581:	89 04 24             	mov    %eax,(%esp)
 8048584:	e8 a7 fe ff ff       	call   8048430 <atoi(argv[1])@plt>
 8048589:	c6 44 04 18 00       	movb   $0x0,0x18(%esp,%eax,1)
```

처음 읽은 위치에서 0x42만큼 뒤의 위치에 다시 .pass파일의 내용을 읽어오고

```
 804858e:	8d 44 24 18          	lea    0x18(%esp),%eax
 8048592:	8d 50 42             	lea    0x42(%eax),%edx
 8048595:	8b 84 24 9c 00 00 00 	mov    0x9c(%esp),%eax
 804859c:	89 44 24 0c          	mov    %eax,0xc(%esp)
 80485a0:	c7 44 24 08 41 00 00 	movl   $0x41,0x8(%esp)
 80485a7:	00 
 80485a8:	c7 44 24 04 01 00 00 	movl   $0x1,0x4(%esp)
 80485af:	00 
 80485b0:	89 14 24             	mov    %edx,(%esp)
 80485b3:	e8 18 fe ff ff       	call   80483d0 <fread(0x5a(%esp))@plt>
```

처음 읽은 위치에 있는 문자열과 argv[1]을 strcmp로 비교하여 같은 경우 쉘을 실행하는 코드이다.

```
 80485c7:	8b 45 0c             	mov    0xc(%ebp),%eax
 80485ca:	83 c0 04             	add    $0x4,%eax
 80485cd:	8b 00                	mov    (%eax),%eax
 80485cf:	89 44 24 04          	mov    %eax,0x4(%esp)
 80485d3:	8d 44 24 18          	lea    0x18(%esp),%eax
 80485d7:	89 04 24             	mov    %eax,(%esp)
 80485da:	e8 d1 fd ff ff       	call   80483b0 <strcmp@plt>
```

따라서 문제를 해결하려면

.pass 문자열에서 [0, atoi(argv[1])) 구간이 argv[1]과 동일한 어떤 argv[1]을 찾아야 한다.

단순히 빈 문자열을 프로그램에 넘겨줄 경우 atoi("")은 0이므로 .pass문자열에서 [0, 0) 구간 즉 빈 문자열과 빈 문자열을 비교하게 되서 쉘을 획득할 수 있다.

```bash
./bonus3 ""
```