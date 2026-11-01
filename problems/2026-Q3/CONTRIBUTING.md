# 풀이 제출하기

이 폴더의 두 연습 문제는 공개 테스트를 직접 실행한 뒤 Pull Request로 풀이를 제출할 수 있습니다. 공개 테스트는 문항별 10개이며, 작은 경계 입력과 제한 크기의 입력을 포함합니다. 모두 통과해도 모든 입력에 대한 정답이나 특정 시간 복잡도가 보장되지는 않으므로, 알고리즘의 타당성과 복잡도도 확인해 주세요.

## 1. Fork와 작업 브랜치

[zinee-u/algorithm](https://github.com/zinee-u/algorithm)을 Fork하고 본인 저장소를 clone합니다. 풀이를 작성할 브랜치를 만듭니다.

```sh
git switch -c solve/2026-Q3
```

## 2. 풀이 파일 추가

저장소 루트 기준으로 아래 경로에 본인 GitHub 아이디의 폴더를 만들고, 제출할 문항의 파일을 추가합니다. Python과 C++ 중 하나만 제출하거나 둘 다 제출해도 됩니다.

```text
problems/2026-Q3/submissions/<github-id>/
├── 01-square-regions.py
├── 01-square-regions.cpp
├── 02-ticket-exchange.py
└── 02-ticket-exchange.cpp
```

문항 1은 **완성된 정사각형 타일 묶음**, 문항 2는 **가장 마음에 드는 체험 부스**입니다. [문항 1의 problem.md](01-square-regions/problem.md)와 [문항 2의 problem.md](02-ticket-exchange/problem.md)에 있는 공개 규칙을 기준으로 구현합니다. 필요하면 같은 폴더에 접근 방법과 시간·공간 복잡도를 설명한 `README.md`를 추가하세요.

Python은 `solution` 함수를 정의하고 값을 반환합니다. 입력을 직접 읽거나 실행 코드를 추가할 필요는 없습니다.

```python
# 01-square-regions.py: int 반환
def solution(board):
    ...

# 02-ticket-exchange.py: str 반환
def solution(preferences, requests):
    ...
```

C++은 필요한 표준 헤더와 아래 형식의 함수를 작성합니다. `main` 함수는 채점기가 제공합니다. 매개변수는 값으로 받고, 반환 형식은 정확히 맞춰 주세요.

```cpp
#include <string>
#include <vector>
using namespace std;

// 01-square-regions.cpp
int solution(vector<vector<int>> board);

// 02-ticket-exchange.cpp
string solution(vector<string> preferences, vector<vector<string>> requests);
```

각 `.cpp`에는 해당 문항의 함수 정의를 포함해야 합니다. 외부 라이브러리나 다른 파일 없이 하나의 풀이 파일로 실행 가능하게 작성하세요. 반환값을 화면에 출력하지 마세요. 특히 C++의 `cout`/`printf` 디버깅 출력은 오답으로 처리됩니다. Python의 일반적인 디버깅 출력은 반환값 판정에 섞이지 않지만 제출 전 제거하는 것을 권장합니다.

## 3. 공개 테스트 실행

Python 3와 표준 라이브러리만으로 채점기를 실행할 수 있습니다. C++ 풀이를 검사할 때는 C++17을 지원하는 `clang++` 또는 `g++`도 필요합니다.

저장소 루트에서 다음과 같이 실행합니다. `<github-id>`는 본인 아이디로 바꿉니다.

```sh
python3 problems/2026-Q3/check.py 01-square-regions problems/2026-Q3/submissions/<github-id>/01-square-regions.py --timeout 5
python3 problems/2026-Q3/check.py 02-ticket-exchange problems/2026-Q3/submissions/<github-id>/02-ticket-exchange.cpp --timeout 5
```

문제 폴더 안에서는 더 짧게 실행할 수 있습니다. 풀이 파일의 절대 경로도 지원합니다.

```sh
cd problems/2026-Q3
python3 check.py 01-square-regions /path/to/solution.py --timeout 5
python3 check.py 02-ticket-exchange /path/to/solution.cpp --timeout 5
```

`--timeout`의 기본값은 테스트당 5초입니다. 테스트마다 새로운 프로세스에서 실행하므로 전역 변수 상태가 다음 테스트로 이어지지 않습니다. 표시되는 시간에는 프로세스 시작, Python 모듈 로딩, 입력 읽기, 함수 실행이 포함됩니다. 테스트 생성과 입력 파일 준비 시간은 포함하지 않습니다. 실행 환경의 성능에 따라 걸리는 시간은 달라질 수 있습니다.

컴파일러는 `CXX` 환경 변수, `clang++`, `g++` 순서로 선택합니다. 컴파일에는 `-std=c++17 -O2 -Wall -Wextra -pedantic`을 적용하며, 컴파일 제한 시간은 60초입니다. 예를 들어 `CXX=g++ python3 check.py ...`로 컴파일러를 지정할 수 있습니다. C++ 컴파일 시간은 개별 테스트 제한 시간과 별개입니다.

결과는 테스트별 실행 시간과 다음 상태로 표시됩니다.

| 상태 | 의미 |
| --- | --- |
| `PASS` | 반환값과 형식이 기대값과 일치함 |
| `FAIL` | 반환값이 다르거나 C++ 표준 출력에 다른 내용이 섞임 |
| `ERROR` | 예외, 비정상 종료, 잘못된 반환 형식 또는 결과 누락 |
| `TIMEOUT` | 해당 테스트의 제한 시간 초과 |

마지막 줄에 상태별 개수를 집계합니다. 모두 통과하면 종료 코드 `0`, 테스트 실패 또는 컴파일 실패는 `1`, 잘못된 명령이나 컴파일러·테스트 파일 등 실행 환경 문제는 `2`를 반환합니다. Python의 `bool`은 문항 1의 `int` 반환값으로 인정하지 않습니다.

공개 테스트는 `cases.py`에서 재현 가능하게 생성합니다. 테스트와 채점기를 바꾸어서 본인 풀이를 통과시키지 마세요. 이 도구는 신뢰하는 로컬 풀이를 실행하기 위한 도구이며 보안 샌드박스가 아닙니다.

## 4. Pull Request 열기

본인 풀이 파일과 선택적인 해설만 커밋하여 Fork 저장소의 브랜치에 push하고, 원본 저장소의 `main`을 대상으로 PR을 엽니다. 문제·공개 테스트·채점기 변경은 풀이 제출 PR에 포함하지 않습니다.

PR 제목은 다음 형식을 사용합니다.

```text
[풀이] 2026-Q3 / 01-square-regions / Python / github-id
```

PR 본문에는 제출 문항과 언어, 알고리즘의 핵심 아이디어, 시간·공간 복잡도, 실행한 검사 명령과 결과를 적어 주세요. Python 버전 또는 C++ 컴파일러 버전, `--timeout` 값도 함께 남기면 실행 결과를 비교하기 좋습니다.

```text
문항: 01-square-regions
언어: Python 3
아이디어 및 복잡도: ...
검사 명령: python3 problems/2026-Q3/check.py ... --timeout 5
검사 결과: PASS 10 | FAIL 0 | ERROR 0 | TIMEOUT 0
실행 환경: ...
```

이 공개 묶음에는 자동 CI 채점이 연결되어 있지 않습니다. PR 작성자가 로컬 검사 결과를 첨부하고, 리뷰어가 코드와 결과를 확인하는 방식입니다.
