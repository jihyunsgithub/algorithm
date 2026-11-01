# 2026-Q3 코딩 연습

사용자 기억을 바탕으로 조건을 정리하고, 소재와 문장을 새로 작성한 두 문제입니다. 공식 출제문이나 공식 채점 데이터가 아닙니다. 모호한 조건은 문항별 복원 가정에 명시했으며, 이 문제집의 테스트는 그 규칙을 따릅니다.

| 번호 | 문제 | 함수 |
| --- | --- | --- |
| 1 | [완성된 정사각형 타일 묶음](01-square-regions/problem.md) | `solution(board)` |
| 2 | [가장 마음에 드는 체험 부스](02-ticket-exchange/problem.md) | `solution(preferences, requests)` |

## 풀고 PR 보내기

1. 이 저장소를 fork하고 자신의 브랜치를 만듭니다.
2. `submissions/<GitHub ID>/` 아래에 문항 번호에 맞는 `.py` 또는 `.cpp` 답안을 작성합니다.
3. 로컬 채점기로 공개 테스트 10개를 실행합니다.
4. 구현과 테스트 결과를 담아 원래 저장소로 PR을 보냅니다.

자세한 경로, 함수 형식, 명령은 [제출 안내](CONTRIBUTING.md)를 참고하세요. 기준 해설과 정답 코드는 공개하지 않습니다.

## 입출력 테스트

문항마다 **10개**, 총 **20개**의 재현 가능한 입력·기대 출력이 있습니다. [테스트 목록](TESTCASES.md)에서 각 사례가 확인하는 경계 조건과 크기를 볼 수 있습니다.

이 디렉터리에서 다음 명령으로 실제 JSON 입출력 파일을 생성합니다.

```sh
python3 cases.py --output generated-tests
```

`generated-tests/<문항 ID>/01.in.json`부터 `10.in.json`까지 입력을, 같은 이름의 `.out.json`에 기대 반환값을 만듭니다. 백만 칸 격자도 생성되므로 큰 입력 내용을 Markdown에 직접 나열하지 않습니다. 채점기는 같은 생성기를 사용하며 파일을 미리 만들 필요는 없습니다.

```sh
python3 check.py 01-square-regions submissions/YOUR_ID/01-square-regions.py --timeout 5
python3 check.py 02-ticket-exchange submissions/YOUR_ID/02-ticket-exchange.cpp --timeout 5
```

최대 크기 입력과 테스트별 시간제한으로 느린 구현을 점검할 수 있습니다. 기본 제한은 이 문제집의 로컬 실행 기준이며 실제 시험의 시간제한이 아닙니다. 공개 사례 통과가 모든 입력의 정답이나 시간복잡도를 보장하지는 않습니다.

