> Password: level0

level0 파일을 objdump를 사용해서 main함수를 확인하면

```
08048ec0 <main>:
8048ec0:	55                   	push   %ebp
8048ec1:	89 e5                	mov    %esp,%ebp
8048ec3:	83 e4 f0             	and    $0xfffffff0,%esp
8048ec6:	83 ec 20             	sub    $0x20,%esp
8048ec9:	8b 45 0c             	mov    0xc(%ebp),%eax
8048ecc:	83 c0 04             	add    $0x4,%eax
8048ecf:	8b 00                	mov    (%eax),%eax
8048ed1:	89 04 24             	mov    %eax,(%esp)
8048ed4:	e8 37 08 00 00       	call   8049710 <atoi>
8048ed9:	3d a7 01 00 00       	cmp    $0x1a7,%eax
8048ede:	75 78                	jne    8048f58 <main+0x98>
```

이러한 초반 부분을 볼 수 있다.

중요한 부분을 정리하면 

8048ec9에서 main의 2번째 인자(argv)를 eax에 넣고

그 뒤 두 줄을 보면 eax = 0x4(eax)와 같은 일을 진행하는데, 결국 argv[1]을 eax에 넣는 내용이다.

이후 부분은 eax를 스택 맨 위에 넣고, atoi를 호출하며, 결과를 0x1a7(423)과 비교하여 jump하는 부분이다.

이때 결과가 0x1a7과 같을 경우에는 shell을 실행하고, 아닐 경우에는 프로그램이 종료된다.

따라서 첫번째 인자를 423으로 주어 프로그램을 실행시키면 다음 레벨의 쉘을 얻을 수 있다.

```bash
./level0 423
```