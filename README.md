# autoblog

## Windows 실행파일

GitHub 저장소의 **Actions → Windows executable → 성공한 최신 실행 → Artifacts → Autoblog-Windows-x64**에서 ZIP을 다운로드하고 압축을 푸세요. GitHub 로그인이 필요할 수 있습니다. `Autoblog.exe`를 더블클릭하면 주제, 생성 모드, 저장 경로를 묻습니다. Python 설치는 필요 없습니다. Windows x64용입니다.

기본 모드는 비용이 없는 오프라인 개요입니다. AI 모드에서는 OpenAI API 키와 인터넷이 필요하며 호출 비용이 발생합니다. 키는 입력 시 숨겨지고 파일에 저장되지 않습니다. 기본 결과 저장 위치는 사용자 폴더 아래 `Autoblog` 폴더이며, 프로그램이 실제 경로를 표시합니다.

PowerShell에서도 실행할 수 있습니다.

```powershell
.\Autoblog.exe '파이썬 업무 자동화' --offline --output draft.md
```

직접 빌드하려면 Windows에서 Python 3.12를 설치한 뒤 저장소 루트에서 실행하세요. 빌드는 Windows 환경에서 해야 합니다.

```powershell
python -m pip install pyinstaller==6.16.0
python -m unittest discover -s tests -v
python -m PyInstaller --noconfirm --clean --onefile --console --name Autoblog windows_entry.py
```

결과 파일은 `dist/Autoblog.exe`입니다. 현재 빌드는 코드 서명이 없어 Windows에서 알 수 없는 게시자로 표시될 수 있습니다.

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
