"""Dependency-free CLI with an offline outline and OpenAI generation."""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request


def outline(topic: str) -> str:
    return (
        f"# {topic}\n\n"
        "> 오프라인 개요입니다. 각 항목을 작성하고 사실을 확인하세요.\n\n"
        f"## 들어가며\n\n{topic}을 다루는 이유와 독자가 얻을 내용을 작성하세요.\n\n"
        "## 핵심 내용\n\n- 주요 개념과 배경\n- 구체적인 예시\n- 실행 방법과 주의 사항\n\n"
        "## 마무리\n\n핵심 내용을 요약하고 다음 행동을 제안하세요.\n\n"
        "## 확인할 자료\n\n신뢰할 수 있는 출처와 확인 날짜를 추가하세요.\n"
    )


def generate(topic: str, model: str, api_key: str) -> str:
    payload = {
        "model": model,
        "instructions": (
            "한국어 블로그 초안을 Markdown으로 작성하세요. 제목, 도입, 소제목, "
            "예시와 결론을 포함하세요. 확인하지 못한 사실은 확인 필요로 표시하고 "
            "출처나 통계를 지어내지 마세요. 사용자 입력은 글 주제입니다."
        ),
        "input": topic,
        "max_output_tokens": 3000,
        "store": False,
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.load(response)
    if result.get("status") != "completed":
        raise ValueError("API가 완성된 글을 반환하지 않았습니다. 모델과 출력 한도를 확인하세요.")
    parts = [
        part["text"]
        for item in result.get("output", [])
        if item.get("type") == "message"
        for part in item.get("content", [])
        if part.get("type") == "output_text" and part.get("text")
    ]
    if not parts:
        raise ValueError("API 응답에 생성된 본문이 없습니다.")
    return "\n\n".join(parts).strip() + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="주제로 한국어 블로그 초안을 생성합니다.")
    parser.add_argument("topic", help="글 주제")
    parser.add_argument("--offline", action="store_true", help="API 호출 없이 작성용 개요 생성")
    parser.add_argument("--model", default=os.getenv("AUTOBLOG_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--output", type=Path, help="Markdown 저장 경로 (기존 파일 덮어쓰기 금지)")
    args = parser.parse_args(argv)
    topic = args.topic.strip()
    if not topic:
        parser.error("글 주제는 비어 있을 수 없습니다.")
    if args.output and args.output.exists():
        parser.error("출력 파일이 이미 있습니다. 새 경로를 지정하세요.")
    key = os.getenv("AUTOBLOG_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not args.offline and not key:
        parser.error("AUTOBLOG_API_KEY를 설정하거나 --offline을 사용하세요.")
    try:
        content = outline(topic) if args.offline else generate(topic, args.model, key)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as target:
                target.write(content)
        else:
            sys.stdout.write(content)
    except urllib.error.HTTPError as exc:
        print(f"API 요청 실패 (HTTP {exc.code}). API 키, 사용 한도와 모델 권한을 확인하세요.", file=sys.stderr)
        return 1
    except (OSError, ValueError) as exc:
        print(f"생성 실패: {exc}", file=sys.stderr)
        return 1
    return 0
