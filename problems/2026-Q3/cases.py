"""복원 연습 문제의 고정 테스트 10개씩을 생성한다.

정답 풀이를 호출하지 않는다. 각 입력의 구조로 알 수 있는 기대값을 고정한다.
입력 파일: {"args": [함수의 첫 번째 인자, ...]}
출력 파일: 기대 반환값을 나타내는 JSON 정수 또는 문자열
"""

import argparse
import json
from pathlib import Path


PROBLEMS = ("01-square-regions", "02-ticket-exchange")


def _case(case_id, name, args, expected):
    return {"id": case_id, "name": name, "args": args, "expected": expected}


def _booth_name(index):
    """0~2999를 서로 다른 소문자 네 글자로 만든다: baaa부터 belj까지."""
    return "b" + "".join(
        chr(ord("a") + index // divisor % 26) for divisor in (676, 26, 1)
    )


def _square_cases():
    return [
        _case("01", "최소 격자의 한 칸짜리 묶음", [[[1, 2], [3, 4]]], 0),
        _case(
            "02", "서로 다른 네 정사각형 묶음",
            [[
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [2, 2, 3, 3],
                [2, 2, 3, 3],
            ]],
            4,
        ),
        _case("03", "큰 묶음의 부분 정사각형 제외", [[[7] * 3 for _ in range(3)]], 1),
        _case(
            "04", "꼭짓점으로 이어진 추가 타일",
            [[[1, 1, 2], [1, 1, 3], [4, 5, 1]]],
            0,
        ),
        _case(
            "05", "가운데가 다른 번호인 묶음",
            [[[1, 1, 1], [1, 0, 1], [1, 1, 1]]],
            0,
        ),
        _case("06", "직사각형 묶음 제외", [[[6, 6, 6], [6, 6, 6]]], 0),
        _case("07", "번호 영의 최소 완성품", [[[0, 0], [0, 0]]], 1),
        _case(
            "08", "최대 크기의 단일 정사각형",
            [[[1] * 1000 for _ in range(1000)]],
            1,
        ),
        _case(
            "09", "최대 높이의 긴 직사각형",
            [[[9] * 999 for _ in range(1000)]],
            0,
        ),
        _case(
            "10", "최대 개수의 독립 완성품",
            [[
                [2 * ((row // 2) % 2) + ((col // 2) % 2) for col in range(1000)]
                for row in range(1000)
            ]],
            250000,
        ),
    ]


def _ticket_cases():
    chain_names = [_booth_name(index) for index in range(3000)]
    # 역순으로 배치해 입력을 한 차례만 순회하는 풀이는 연쇄를 놓치게 한다.
    reverse_chain = [
        ["00:00", "23:59", chain_names[index], chain_names[index - 1]]
        for index in range(2999, 0, -1)
    ]
    reverse_chain.append(["00:00", "23:59", chain_names[0], chain_names[-1]])

    branch_names = [_booth_name(index) for index in range(3000)]
    branches = [
        ["23:58", "23:59", branch_names[1], branch_names[0]],
        ["00:00", "00:01", branch_names[1], branch_names[0]],
        ["09:00", "09:01", branch_names[-1], branch_names[1]],
    ]
    branches.extend(
        ["00:00", "23:59", branch_names[index], branch_names[0]]
        for index in range(2, 2999)
    )

    return [
        _case(
            "01", "기억 예제의 부스 이름 변경",
            [
                ["art", "robot", "space", "ocean"],
                [
                    ["09:00", "18:00", "space", "robot"],
                    ["10:00", "11:00", "robot", "art"],
                    ["10:30", "10:31", "ocean", "space"],
                ],
            ],
            "ocean",
        ),
        _case(
            "02", "마감 시각과 정확히 같은 도착",
            [
                ["art", "robot", "space"],
                [
                    ["10:00", "11:00", "robot", "art"],
                    ["09:00", "10:00", "space", "robot"],
                ],
            ],
            "space",
        ),
        _case(
            "03", "마감 초과와 미등록 부스 경유",
            [
                ["art", "robot", "space", "ocean"],
                [
                    ["10:01", "11:00", "robot", "art"],
                    ["09:00", "10:00", "space", "robot"],
                    ["00:00", "23:59", "ghost", "art"],
                    ["00:00", "23:59", "ocean", "ghost"],
                ],
            ],
            "robot",
        ),
        _case(
            "04", "같은 시각의 역순 연쇄",
            [
                ["art", "clay", "light", "music", "robot", "space", "ocean"],
                [
                    ["12:00", "12:01", "ocean", "space"],
                    ["12:00", "12:01", "space", "robot"],
                    ["12:00", "12:01", "robot", "music"],
                    ["12:00", "12:01", "music", "light"],
                    ["12:00", "12:01", "light", "clay"],
                    ["12:00", "12:01", "clay", "art"],
                ],
            ],
            "ocean",
        ),
        _case(
            "05", "선호도가 낮아지는 중간 교환",
            [
                ["art", "robot", "space", "ocean"],
                [
                    ["09:00", "10:00", "space", "art"],
                    ["09:00", "10:00", "robot", "space"],
                    ["09:00", "10:00", "ocean", "robot"],
                ],
            ],
            "ocean",
        ),
        _case(
            "06", "자정 시작과 대기 및 순환",
            [
                ["art", "robot", "space", "ocean"],
                [
                    ["23:58", "23:59", "ocean", "space"],
                    ["12:00", "13:00", "space", "robot"],
                    ["00:00", "00:01", "robot", "art"],
                    ["00:00", "01:00", "art", "robot"],
                ],
            ],
            "ocean",
        ),
        _case(
            "07", "늦은 직행을 빠른 우회로로 갱신",
            [
                ["art", "robot", "space", "ocean"],
                [
                    ["18:00", "18:01", "robot", "art"],
                    ["09:00", "10:00", "space", "art"],
                    ["09:00", "10:00", "robot", "space"],
                    ["10:00", "10:01", "ocean", "robot"],
                ],
            ],
            "ocean",
        ),
        _case(
            "08", "최소 입력의 방향과 대소문자",
            [
                ["art", "Art"],
                [
                    ["00:00", "23:59", "art", "Art"],
                ],
            ],
            "art",
        ),
        _case("09", "최대 길이의 역순 연쇄와 순환", [chain_names, reverse_chain], "belj"),
        _case("10", "최대 규모의 분기와 평행 제안", [branch_names, branches], "belj"),
    ]


def make_cases(problem):
    """문항 ID에 해당하는 테스트 열 개를 새 목록으로 반환한다."""
    if problem == "01-square-regions":
        return _square_cases()
    if problem == "02-ticket-exchange":
        return _ticket_cases()
    raise ValueError("지원하지 않는 문항 ID: " + str(problem))


def main():
    parser = argparse.ArgumentParser(description="문항별 JSON 입력/기대 출력 10쌍 생성")
    parser.add_argument("--output", required=True, type=Path, help="생성할 파일의 상위 디렉터리")
    args = parser.parse_args()

    for problem in PROBLEMS:
        destination = args.output / problem
        destination.mkdir(parents=True, exist_ok=True)
        cases = make_cases(problem)
        for case in cases:
            files = (
                (destination / (case["id"] + ".in.json"), {"args": case["args"]}),
                (destination / (case["id"] + ".out.json"), case["expected"]),
            )
            for path, content in files:
                with path.open("w", encoding="utf-8") as stream:
                    json.dump(content, stream, ensure_ascii=False, separators=(",", ":"))
                    stream.write("\n")
        print(str(destination) + ": 입력/출력 " + str(len(cases)) + "쌍 생성")


if __name__ == "__main__":
    main()
