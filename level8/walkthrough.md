> Password: 5684af5cb4c8679958be4abe6373147ab52d95768e047820bf382e44fa8d8fb9 

level8의 어셈블리 코드를 확인해보자

프로그램이 꽤나 복잡한데, 정리해보면 유저의 입력이 각각`auth `, `service`, `login`, `reset`일 때

- `auth <token>`

  받은 token을 비밀번호로 설정한다. 최대 길이는 0x1e이다. 

- `service<token>`

  받은 token을 저장한다

- `reset`

  동적 할당된 auth token을 free한다.

- `login`

  auth token의 0x20번 인덱스 위치의 값을 가져와서 0인지 확인한 이후

  0일 때: password: 라는 문자열을 띄운다

  0이 아닐 때: 쉘을 실행한다.

이때 auth에서 0x20 길이의 문자열을 넣을 수 없지만, login에서 auth token의 길이가 얼마든 무조건 0x20번 위치를 확인한 다는 점을 이용해서 auth명령어 -> service명령어 순서로 명령어를 실행해 메모리에서의 순서가 auth -> service가 되게 만들면 auth token에서 0x20번 위치가 0이 아닌 값이 들어가게 만들 수 있다.

```bash
cat <(printf "auth .\nservice0123456789012345\nlogin\n") - | ./level8
```