# autoblog

Python 3.11 이상에서 실행하는 한국어 블로그 초안 생성 CLI입니다. 외부 Python 런타임 의존성이 없습니다. 글을 자동 게시하지 않으며, 생성 결과는 게시 전에 사실 확인과 편집이 필요합니다.

## 설치

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

## API 키 없이 사용

```bash
.venv/bin/autoblog '파이썬으로 업무 자동화 시작하기' --offline --output drafts/example.md
```

오프라인 모드는 작성용 개요를 생성합니다. 완성된 글을 생성하려면 API 모드를 사용하세요. `--output`을 생략하면 표준 출력으로 표시합니다. 기존 출력 파일은 덮어쓰지 않습니다.

## AI로 글 생성

보안 환경 설정에 `AUTOBLOG_API_KEY`를 등록하세요. 기존 `OPENAI_API_KEY`도 지원합니다. `.env` 파일을 자동으로 읽지는 않습니다. API 키를 소스나 Git에 저장하지 마세요.

```bash
.venv/bin/autoblog '파이썬으로 업무 자동화 시작하기' --output drafts/article.md
```

OpenAI Responses API(`https://api.openai.com/v1/responses`)를 사용하며 API 호출 비용이 발생합니다. 기본 모델은 `gpt-4.1-mini`이고 `--model` 또는 `AUTOBLOG_MODEL`로 변경할 수 있습니다. 실행 환경에서 `api.openai.com` HTTPS 접근과 모델 사용 권한이 필요합니다. 키 누락 시 오류로 종료하고, API 응답이 미완성이면 파일을 저장하지 않습니다.

## 테스트

```bash
.venv/bin/python -m unittest discover -s tests -v
```

테스트는 오프라인 파일 생성, 기존 파일 보호, 키 누락 처리 및 모의 API 요청/응답을 검증합니다. 실제 API 연결은 유효한 키를 설정한 뒤 별도로 확인해야 합니다.
