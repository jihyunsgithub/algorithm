#!/usr/bin/env python3
"""Run ten public cases against a trusted, local Python or C++ solution file."""

import argparse
import importlib.util
import json
import math
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time


sys.dont_write_bytecode = True
PROBLEMS = ("01-square-regions", "02-ticket-exchange")
COMPILE_TIMEOUT = 60
PYTHON_WORKER = r'''
import importlib.util
import json
from pathlib import Path
import sys

source, input_path, result_path, problem = sys.argv[1:]
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(source).parent))
spec = importlib.util.spec_from_file_location("_submitted_solution", source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
function = getattr(module, "solution", None)
if not callable(function):
    raise TypeError("solution 함수를 찾을 수 없습니다.")
with open(input_path, encoding="utf-8") as stream:
    arguments = json.load(stream)["args"]
value = function(*arguments)
expected_type = int if problem == "01-square-regions" else str
if type(value) is not expected_type:
    raise TypeError(
        f"solution 반환 형식은 {expected_type.__name__}이어야 합니다. "
        f"실제: {type(value).__name__}"
    )
with open(result_path, "w", encoding="utf-8") as stream:
    json.dump({"value": value}, stream, ensure_ascii=False)
'''


class EnvironmentErrorForChecker(Exception):
    """The checker could not start or read its own resources."""


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("제한 시간은 0보다 큰 유한한 초 단위 값입니다.")
    return seconds


def load_cases(problem):
    path = Path(__file__).resolve().with_name("cases.py")
    try:
        spec = importlib.util.spec_from_file_location("_public_cases", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        cases = list(module.make_cases(problem))
        if len(cases) != 10:
            raise ValueError(f"공개 테스트는 10개여야 합니다. 실제: {len(cases)}개")
        expected_type = int if problem == PROBLEMS[0] else str
        for case in cases:
            if not {"id", "name", "args", "expected"}.issubset(case):
                raise ValueError("테스트에 id/name/args/expected 필드가 필요합니다.")
            if not isinstance(case["args"], list):
                raise ValueError("테스트 args는 배열이어야 합니다.")
            if type(case["expected"]) is not expected_type:
                raise ValueError("테스트 기대값의 형식이 문제와 맞지 않습니다.")
        return cases
    except Exception as error:
        raise EnvironmentErrorForChecker(f"cases.py를 불러올 수 없습니다: {error}") from error


def tail(path, limit=3000):
    with path.open("rb") as stream:
        stream.seek(0, os.SEEK_END)
        size = stream.tell()
        stream.seek(max(0, size - limit))
        text = stream.read().decode("utf-8", errors="replace").strip()
    return ("…\n" if size > limit else "") + text


def run_process(command, directory, timeout, input_path=None):
    stdout_path = directory / "stdout.log"
    stderr_path = directory / "stderr.log"
    start = time.perf_counter()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        with (input_path or Path(os.devnull)).open("rb") as stdin:
            try:
                completed = subprocess.run(
                    command, stdin=stdin, stdout=stdout, stderr=stderr,
                    cwd=directory, timeout=timeout, check=False,
                )
                return completed.returncode, time.perf_counter() - start, False
            except subprocess.TimeoutExpired:
                return None, time.perf_counter() - start, True
            except OSError as error:
                raise EnvironmentErrorForChecker(f"프로세스를 시작하지 못했습니다: {error}") from error


def cpp_harness(problem):
    prefix = '''#include <iostream>
#include <string>
#include <vector>
#include <utility>
using namespace std;
#include "submission.cpp"
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
'''
    if problem == PROBLEMS[0]:
        body = '''    int n, m;
    if (!(cin >> n >> m)) return 2;
    vector<vector<int>> board(n, vector<int>(m));
    for (auto& row : board)
        for (int& value : row)
            if (!(cin >> value)) return 2;
    int (*submitted_solution)(vector<vector<int>>) = &solution;
    cout << submitted_solution(std::move(board));
'''
    else:
        body = '''    int p, r;
    if (!(cin >> p >> r)) return 2;
    vector<string> preferences(p);
    for (auto& subject : preferences)
        if (!(cin >> subject)) return 2;
    vector<vector<string>> requests(r, vector<string>(4));
    for (auto& request : requests)
        for (auto& field : request)
            if (!(cin >> field)) return 2;
    string (*submitted_solution)(vector<string>, vector<vector<string>>) = &solution;
    cout << submitted_solution(std::move(preferences), std::move(requests));
'''
    return prefix + body + "    return 0;\n}\n"


def compile_cpp(problem, source, directory):
    configured = os.environ.get("CXX")
    if configured:
        try:
            compiler = shlex.split(configured)
        except ValueError as error:
            raise EnvironmentErrorForChecker(f"CXX 설정을 해석할 수 없습니다: {error}") from error
        available = shutil.which(compiler[0]) if compiler else None
        if not available:
            raise EnvironmentErrorForChecker(f"CXX 컴파일러를 찾을 수 없습니다: {configured}")
        compiler[0] = os.path.abspath(available)
    else:
        found = shutil.which("clang++") or shutil.which("g++")
        if not found:
            raise EnvironmentErrorForChecker("C++17 컴파일러가 없습니다. clang++/g++를 설치하거나 CXX를 지정하세요.")
        compiler = [found]
    shutil.copyfile(source, directory / "submission.cpp")
    harness = directory / "harness.cpp"
    harness.write_text(cpp_harness(problem), encoding="utf-8")
    executable = directory / ("solution.exe" if os.name == "nt" else "solution")
    command = compiler + [
        "-std=c++17", "-O2", "-Wall", "-Wextra", "-pedantic",
        str(harness), "-o", str(executable),
    ]
    returncode, elapsed, timed_out = run_process(command, directory, COMPILE_TIMEOUT)
    if timed_out:
        print(f"ERROR: C++ 컴파일 시간 초과 ({elapsed:.3f}s, 제한 {COMPILE_TIMEOUT}s)")
        return None
    diagnostics = tail(directory / "stderr.log")
    if returncode != 0:
        print(f"ERROR: C++ 컴파일 실패 (종료 코드 {returncode}, {elapsed:.3f}s)")
        if diagnostics:
            print(diagnostics)
        return None
    print(f"C++17 컴파일 완료 ({elapsed:.3f}s)")
    if diagnostics:
        print(diagnostics)
    return executable


def write_cpp_input(problem, arguments, path):
    with path.open("w", encoding="utf-8") as stream:
        if problem == PROBLEMS[0]:
            board = arguments[0]
            stream.write(f"{len(board)} {len(board[0])}\n")
            for row in board:
                stream.write(" ".join(map(str, row)) + "\n")
        else:
            preferences, requests = arguments
            stream.write(f"{len(preferences)} {len(requests)}\n")
            stream.write("\n".join(preferences) + "\n")
            for request in requests:
                stream.write(" ".join(request) + "\n")


def run_case(problem, source, executable, case, directory, timeout):
    if executable is None:
        input_path = directory / "input.json"
        result_path = directory / "result.json"
        with input_path.open("w", encoding="utf-8") as stream:
            json.dump({"args": case["args"]}, stream, ensure_ascii=False)
        command = [
            sys.executable, "-B", "-c", PYTHON_WORKER,
            str(source), str(input_path), str(result_path), problem,
        ]
        returncode, elapsed, timed_out = run_process(command, directory, timeout)
    else:
        input_path = directory / "input.txt"
        write_cpp_input(problem, case["args"], input_path)
        returncode, elapsed, timed_out = run_process([str(executable)], directory, timeout, input_path)
    if timed_out:
        return "TIMEOUT", elapsed, f"제한 {timeout:g}s 초과"
    if returncode != 0:
        diagnostics = tail(directory / "stderr.log")
        return "ERROR", elapsed, f"종료 코드 {returncode}" + (f"\n{diagnostics}" if diagnostics else "")
    if executable is None:
        try:
            with result_path.open(encoding="utf-8") as stream:
                actual = json.load(stream)["value"]
            if type(actual) is not type(case["expected"]):
                return "ERROR", elapsed, "반환값의 형식이 올바르지 않습니다."
        except (OSError, ValueError, KeyError, TypeError) as error:
            return "ERROR", elapsed, f"solution 반환값을 읽을 수 없습니다: {error}"
    else:
        stdout_path = directory / "stdout.log"
        expected_output = str(case["expected"]).encode("utf-8")
        with stdout_path.open("rb") as stream:
            actual_output = stream.read(max(200, len(expected_output) + 1))
        if actual_output != expected_output:
            actual = actual_output.decode("utf-8", errors="replace")
            return "FAIL", elapsed, f"기대 {case['expected']!r}, 실제 stdout {actual!r}"
        return "PASS", elapsed, ""
    if actual != case["expected"]:
        return "FAIL", elapsed, f"기대 {case['expected']!r}, 실제 {str(actual)[:200]!r}"
    return "PASS", elapsed, ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", choices=PROBLEMS)
    parser.add_argument("source", type=Path, help="solution 함수가 들어 있는 .py 또는 .cpp 파일")
    parser.add_argument("--timeout", type=positive_seconds, default=5.0, help="테스트별 제한 시간(초), 기본 5")
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    if not source.is_file() or source.suffix.lower() not in (".py", ".cpp"):
        parser.error("존재하는 .py 또는 .cpp 풀이 파일을 지정하세요.")
    try:
        cases = load_cases(args.problem)
        with tempfile.TemporaryDirectory(prefix="q3-check-") as temporary:
            directory = Path(temporary)
            executable = None
            if source.suffix.lower() == ".cpp":
                executable = compile_cpp(args.problem, source, directory)
                if executable is None:
                    return 1
            print(f"{args.problem}: 공개 테스트 {len(cases)}개, 테스트별 제한 {args.timeout:g}s")
            counts = dict.fromkeys(("PASS", "FAIL", "ERROR", "TIMEOUT"), 0)
            for index, case in enumerate(cases, 1):
                case_directory = directory / f"case-{index:02d}"
                case_directory.mkdir()
                status, elapsed, detail = run_case(
                    args.problem, source, executable, case, case_directory, args.timeout,
                )
                counts[status] += 1
                print(f"{status:7s} {case['id']} {case['name']} ({elapsed:.3f}s)", flush=True)
                if detail:
                    print("  " + detail.replace("\n", "\n  "), flush=True)
            print(" | ".join(f"{status} {count}" for status, count in counts.items()))
            return 0 if counts["PASS"] == len(cases) else 1
    except (EnvironmentErrorForChecker, OSError) as error:
        print(f"환경 오류: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
