"""Console executable entry point; double-click opens an interactive session."""

from datetime import datetime
from getpass import getpass
import os
from pathlib import Path
import sys
from uuid import uuid4

from autoblog.cli import main


def interactive() -> int:
    print("Autoblog - 한국어 블로그 초안 생성")
    topic = input("글 주제: ").strip()
    if not topic:
        print("글 주제를 입력하세요.")
        return 1
    mode = input("AI로 글 생성: 1 / 무료 오프라인 개요: 2 [기본 2]: ").strip()
    if mode not in ("", "1", "2"):
        print("1 또는 2를 선택하세요.")
        return 1
    args = [topic]
    if mode == "1":
        print("OpenAI API 호출 비용이 발생합니다.")
        if not (os.getenv("AUTOBLOG_API_KEY") or os.getenv("OPENAI_API_KEY")):
            key = getpass("OpenAI API 키 (화면에 표시하거나 파일에 저장하지 않음): ").strip()
            if not key:
                print("API 키가 필요합니다.")
                return 1
            os.environ["AUTOBLOG_API_KEY"] = key
    else:
        args.append("--offline")
    default = Path.home() / "Autoblog" / f"draft-{datetime.now():%Y%m%d-%H%M%S}-{uuid4().hex[:8]}.md"
    chosen = input(f"저장 경로 [Enter: {default}]: ").strip().strip('"')
    output = Path(chosen).expanduser() if chosen else default
    code = main([*args, "--output", str(output)])
    if code == 0:
        print(f"저장 완료: {output.resolve()}")
        print("게시 전에 내용을 편집하고 사실을 확인하세요.")
    return code


def run() -> int:
    if len(sys.argv) > 1:
        return main()
    try:
        return interactive()
    except (EOFError, KeyboardInterrupt):
        print("\n취소했습니다.")
        return 1
    except (OSError, ValueError) as exc:
        print(f"실행 실패: {exc}")
        return 1
    finally:
        try:
            input("Enter를 누르면 종료합니다.")
        except (EOFError, KeyboardInterrupt):
            pass


if __name__ == "__main__":
    raise SystemExit(run())
