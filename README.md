## 👋 들어가며

> [!question] 
> **Boilerplate?**
> 
> In computer programming, **boilerplate code**, or simply **boilerplate**, are ==sections of code that are repeated in multiple places with little to no variation.== * From Wikipedia

* 프로젝트를 여러 번 하다보면 모든 프로젝트에서 공통적으로 활용할만한 코드를 갖게 됨
	* 주로 유틸리티 함수, 테스트 코드 설정, 로그 설정
		* 테스트 코드는 [`pytest`](https://docs.pytest.org/en/stable/)
		* 로그 설정은 [`structlog`](https://www.structlog.org/en/stable/)
	* 개인적으론 Git 설정 스크립트도 보일러플레이트로 사용 중
* 이런 코드는 굳이 다시 처음부터 작성할 필요가 없음
	* 프로젝트 내용과 독립적으로 어디에서도 사용할 수 있기 때문
* 보일러플레이트 코드를 갖고 있으면 결국 프로젝트 구조도 기본값을 갖게 됨
	* 진행하는 프로젝트의 일관성을 갖게 됨
		* 나만의 방식이 생기면 다른 사람으로 하여금 *'아, 이거 저 사람이 작성한 코드구나?'* 라는 반응을 이끌어낼 수 있음
		* 다른 사람이 내 코드를 이해하기 쉬워짐
	* 일관성이 생산성을 올려줌
		* 협업의 가이드라인이 될 수 있음

> [!caution] 
> * AI센터도 조직에서 사용하는 보일러플레이트 코드가 있긴 함
> 	* 있다고 다 좋은게 아님 → 상황에 맞는 보일러플레이트를 써야 함
> 	* **FastAPI에 Django에서 사용하는 트랜잭션 관리 데코레이터를 쓰는건 무지에서 비롯되었다고 생각**
> 		* FastAPI는 의존성 주입 시스템을 통해서 세션을 주입하고 컨텍스트 매니저로 유연하게 트랜잭션을 관리할 수 있는게 장점인데, Django에서 사용하는 트랜잭션 관리 데코레이터 방식은 장점을 모두 포기하는 것

* 보일러플레이트 코드와 더불어서 기본 개발 환경 설정을 통해 어떤 상황에서도 일관성 있게 효율적인 작업 환경을 구축하는 기회를 가지고자 함
	* 어떤 환경에서 개발을 하는지
	* 어떤 보일러플레이트 코드를 통해 전체 프로젝트의 품질을 올릴 수 있는지
	* 어떤 도구를 통해서 일을 더 쉽게 할 수 있는지

## 💻 기본 환경

* 무조건 VS Code
	* 꽤 많은 Extension을 설치함
		* Themes: [Catppuccin](https://github.com/catppuccin)
			* 가독성을 위해 반드시 폰트를 바꿈 ([JetBrains Mono + D2Coding](https://github.com/Jhyub/JetBrainsMonoHangul))
		* **Syntax (Language Server)** → 문법 하이라이트 + 자동 완성
			* Docker
				* Dockerfile
			* Dotenv
			* Even Better TOML
			* gitignore
			* Markdown All in One
			* Path Intellisense
			* Pylance (Python)
			* shell-format
			* YAML
		* For Python 
			* **autoDocstring**
			* Jupyter
			* Paste and Indent
			* **Static analysis tools**
				* [ruff](https://github.com/astral-sh/ruff)
				* [ty](https://github.com/astral-sh/ty)
		* Utils
			* Error Lens
			* **Git Graph**
			* Output Colorizer
			* SQLTools
			* TODO Highlight
			* Todo Tree
	* 여러 환경에서 작업을 하는 경우 **Settings Sync**를 통해 동기화 가능
* Windows가 아니었으면 좋겠음
	* 최소 WSL을 쓰는게 맞다고 생각함
		* Ubuntu, Debian 컨테이너 안에서 개발할게 아니라면 WSL 설치해서 리눅스의 장점을 모두 활용하면서 개발하는게 100% 맞다고 생각
	* **이제부터 모든 내용은 모두 Windows를 배제함**

## 🌐 가상 환경 설정 * `uv`

<figure>
<img src="https://i.imgur.com/chwrngn.png">
<figcaption>uv, an extremely fast Python package and project manager, written in Rust.</figcaption>
</figure>

* 무조건 [`uv`](https://github.com/astral-sh/uv) 사용
	* 현존하는 모든 Python 가상 환경 도구(`pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv` 등)를 모두 대체할 수 있음
	* ~~이걸 알고 있는데도 다른 이유 없이 안쓴다면 직무 유기에 태업이라고 생각함~~
* 설치부터 간단함
	```bash
	# On macOS and Linux.
	curl -LsSf https://astral.sh/uv/install.sh | sh
	```

* 가상 환경 생성도 간단함
	```bash
	uv init --python <PYTHON_VERSION>
	uv venv --python <PYTHON_VERSION>
	source .venv/bin/activate
	```

## 🔄 Git

* 아쉽지만 브랜치 전략(branch strategy)을 강제할 순 없음
	* 가벼운 프로젝트는 GitHub Flow, 규모가 조금 있으면 Git Flow
	* [SK Devocean 글](https://devocean.sk.com/blog/techBoardDetail.do?ID=165571&boardType=techBlog)
* 대신 커밋 메시지와 코드 스타일은 강제할 수 있음
	* 코드 스타일은 프리커밋, 커밋 메시지는 Hooks

### ✅  프리커밋(Pre-commit)

<figure>
<img src="https://i.imgur.com/Dj3w8Qx.png">
<figcaption>Pre-commit pipeline with <code>black</code> and <code>flake8</code>. Image from <a href="https://kdheepak.com/blog/using-precommit-hooks/">here</a>.</figcaption>
</figure>

* 커밋 시 설정한 도구를 이용해 코드의 품질을 체크할 수 있음
	* 위 이미지는 `black`과 `flake8`을 사용하지만, 이제는 `ruff` 하나로 해결 가능

> [!warning] 
> * 개인적으로 프리커밋에 타입 체커(type checker)와 단위 테스트는 넣지 않음
> 	* 타입 체커를 넣을 수 있지만 간혹 너무 strict한 규칙 때문에 프리커밋을 통과하지 못하는 경우가 있음
> 		* 커밋 전에 `ty`를 따로 실행해서 타입 체킹을 수행
> 	* 단위 테스트는 프로젝트 규모가 커짐에 따라 수행 시간이 매우 길어짐
> 		* 로직이 복잡할 수록 단위 테스트 수행 시간이 길어짐
> 		* 프리커밋에 추가할 경우 커밋 완료까지 긴 시간이 필요해 커밋 경험이 나빠짐

* 다음 명령어로 `pre-commit`, `ruff` 설치
	
	```bash
	uv add --dev pre-commit ruff
	```

* 프로젝트 루트 폴더에 `.pre-commit-config.yaml` 생성 후 다음 코드 추가

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.7
    hooks:
      - id: ruff
        name: "Ruff Linter"
        entry: ruff check
        types_or: [python, pyi]
        require_serial: true
        args: [--fix, --config=ruff.toml]
      - id: ruff-format
        name: "Ruff Format"
        entry: ruff format
        types_or: [python, pyi]
        require_serial: true
        args: ["--line-length", "80"]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-ast
        name: check python ast
        description: simply checks whether the files parse as valid python.
        entry: check-ast
        types: [python]
      - id: check-case-conflict
        name: check for case conflicts
        description: checks for files that would conflict in case-insensitive filesystems.
        entry: check-case-conflict
      - id: check-docstring-first
        name: check docstring is first
        description: checks a common error of defining a docstring after code.
        entry: check-docstring-first
        types: [python]
      - id: check-executables-have-shebangs
        name: check that executables have shebangs
        description: ensures that (non-binary) executables have a shebang.
        entry: check-executables-have-shebangs
        types: [text, executable]
      - id: check-json
        name: check json
        description: checks json files for parseable syntax.
        entry: check-json
        types: [json]
      - id: check-merge-conflict
        name: check for merge conflicts
        description: checks for files that contain merge conflict strings.
        entry: check-merge-conflict
        types: [text]
      - id: check-yaml
        name: check yaml
        description: checks yaml files for parseable syntax.
        entry: check-yaml
        types: [yaml]
      - id: detect-private-key
        name: detect private key
        description: detects the presence of private keys.
        entry: detect-private-key
        types: [text]
      - id: end-of-file-fixer
        name: fix end of files
        description: ensures that a file is either empty, or ends with one newline.
        entry: end-of-file-fixer
        types: [text]
        stages: [pre-commit, pre-push, manual]
        minimum_pre_commit_version: 3.2.0
      - id: fix-byte-order-marker
        name: fix utf-8 byte order marker
        description: removes utf-8 byte order marker.
        entry: fix-byte-order-marker
        types: [text]
      - id: mixed-line-ending
        name: mixed line ending
        description: replaces or checks mixed line ending.
        entry: mixed-line-ending
        types: [text]
      - id: trailing-whitespace
        name: trim trailing whitespace
        description: trims trailing whitespace.
        entry: trailing-whitespace-fixer
        types: [text]
        stages: [pre-commit, pre-push, manual]
        minimum_pre_commit_version: 3.2.0
```

> [!Tip]
> * 위 프리커밋 설정은 네트워크가 가능한 환경에서 사용할 수 있음
> * 네트워크 사용이 불가능한 환경에선 `pre-commit`과 `ruff`를 어떻게든 설치한 후 다음 설정 파일을 사용
> ```yaml
> repos:
>  - repo: local
>    hooks:
>      - id: ruff
>        name: "Ruff Linter"
>        entry: ruff check
>        language: system
>        types_or: [python, pyi]
>        require_serial: true
>        args: [--fix, --config=ruff.toml]
>      - id: ruff-format
>        name: "Ruff Format"
>        entry: ruff format
>        language: system
>        types_or: [python, pyi]
>        require_serial: true
>       args: ["--line-length", "80"]
>  - repo: local
>    hooks:
>      - id: check-ast
>        name: check python ast
>        description: simply checks whether the files parse as valid python.
>        entry: check-ast
>        language: system
>        types: [python]
>      - id: check-case-conflict
>        name: check for case conflicts
>        description: checks for files that would conflict in case-insensitive filesystems.
>        entry: check-case-conflict
>        language: system
>      - id: check-docstring-first
>        name: check docstring is first
>        description: checks a common error of defining a docstring after code.
>        entry: check-docstring-first
>        language: system
>        types: [python]
>      - id: check-executables-have-shebangs
>        name: check that executables have shebangs
>        description: ensures that (non-binary) executables have a shebang.
>        entry: check-executables-have-shebangs
>        language: system
>        types: [text, executable]
>      - id: check-json
>        name: check json
>        description: checks json files for parseable syntax.
>        entry: check-json
>        language: system
>        types: [json]
>      - id: check-merge-conflict
>        name: check for merge conflicts
>        description: checks for files that contain merge conflict strings.
>        entry: check-merge-conflict
>        language: system
>        types: [text]
>      - id: check-yaml
>        name: check yaml
>        description: checks yaml files for parseable syntax.
>        entry: check-yaml
>        language: system
>        types: [yaml]
>      - id: detect-private-key
>        name: detect private key
>        description: detects the presence of private keys.
>        entry: detect-private-key
>        language: system
>        types: [text]
>      - id: end-of-file-fixer
>        name: fix end of files
>        description: ensures that a file is either empty, or ends with one newline.
>        entry: end-of-file-fixer
>        language: system
>        types: [text]
>        stages: [pre-commit, pre-push, manual]
>        minimum_pre_commit_version: 3.2.0
>      - id: fix-byte-order-marker
>        name: fix utf-8 byte order marker
>        description: removes utf-8 byte order marker.
>        entry: fix-byte-order-marker
>        language: system
>        types: [text]
>      - id: mixed-line-ending
>        name: mixed line ending
>        description: replaces or checks mixed line ending.
>        entry: mixed-line-ending
>        language: system
>        types: [text]
>      - id: trailing-whitespace
>        name: trim trailing whitespace
>        description: trims trailing whitespace.
>        entry: trailing-whitespace-fixer
>        language: system
>        types: [text]
>        stages: [pre-commit, pre-push, manual]
>        minimum_pre_commit_version: 3.2.0
> ```

* 파일 작성을 완료하였으면 프로젝트 루트 폴더에서 다음 명령어 실행
	```bash
	pre-commit install
	```

### 📄 커밋 메시지 템플릿

* 커밋 메시지는 작업에 관여하는 모두가 메시지만 확인하고 **어떤 수정 사항을 왜 적용하였는지** 알 수 있어야 함
	* 생각보다 커밋 메시지 작성에 많은 고민이 필요하지만 우리는 대부분 `git commit -m <MESSAGE>`로 단순 버전 관리 용도로 커밋을 수행함
	* [좋은 커밋 메시지를 쓰는 법](https://cbea.ms/git-commit/) 이란 좋은 블로그 글이 있지만 영어인게 아쉬움
		* 그래서 조금 더 편하게, 편하니까 자세하게 쓸 수 있는 커밋 메시지 템플릿을 개인적으로 사용해왔음
* 아래 코드는 `.gitmessage` 파일로 프로젝트 루트 폴더나 `scripts` 폴더 내에서 관리

	```text
	# 아래에 제목을 작성합니다. (50글자 미만)
	
	
	# 설명을 작성합니다.
	# 글머리 '-'를 붙여서 개조식으로 작성합니다. (72글자 미만)
	
	
	# 필요하다면 관련 코드 리뷰 및 이슈 링크를 글머리를 붙여 추가해주세요.
	
	
	# 커밋 규칙
	#   - 제목은 최대한 커밋 내용을 잘 요약해서 작성합니다.
	#   - 제목의 끝에 마침표를 쓰지 않습니다.
	#   - 제목과 설명 사이에 반드시 공백 한 줄을 추가해주세요.
	#   - 설명에는 이 커밋 내용을 "왜" 작성했고, "어떻게" 작성했는지 써주세요.
	#   - 설명은 여러 줄 쓸 수 있습니다.
	# ------------------
	
	```

* 다음 명령어로 커밋 메시지 템플릿 적용
	```bash
	# .gitmessage가 scripts 안에 있을 때
	git config --local commit.template ./scripts/.gitmessage
	```

* 다음의 규칙이 있음
	* 제목은 반드시 50글자 미만으로
		* 커밋의 작업 내용을 짧게 요약할 수 있도록
		* 제목이 길어진다면 혹시 하나의 커밋이 너무 큰건 아닐지?
	* 설명은 개조식으로, 글머리 포함 72글자 미만
		* 왜, 어떻게 중심으로 작성
* 문제는 *이 규칙을 어떻게 강제로 지키게 하는가*임
	* Git Hook 사용

### 🪝 Hooks

* Git의 몇몇 작업을 자동화하도록 돕는 도구들
* 프로젝트 루트 폴더 내에 `.git/hooks` 폴더에 관련 파일이 있음
* 위의 커밋 메시지 규칙을 검증하는 로직을 Python 코드로 작성하여 `.git/hooks` 폴더 내에 `commit-msg` 라는 훅으로 처리할 예정
	* 하나하나 하기엔 번거롭기에 한 번에 작업해주는 스크립트를 만들어 쓰고 있음
		* 보통 이 스크립트는 `scripts` 폴더 내에 `git_hooks.sh` 라는 파일명으로 저장하여 쓰는 중

```shell
#!/bin/bash

# .git/hooks 디렉터리가 없으면 생성
HOOKS_DIR="$PWD/.git/hooks"

mkdir -p "$HOOKS_DIR"

echo "[Git Hook] Creating rules for writing commit messages..."
# 커밋 메시지 검증 로직 생성
COMMIT_VERIFY_PYTHON_FILE="$HOOKS_DIR/verify_commit_msg.py"
cat >"$COMMIT_VERIFY_PYTHON_FILE" <<'EOF'
import sys


class bcolors:
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    WARNING = "\033[93m"


def print_error(message, details=""):
    """Helper function to print formatted error messages."""
    sys.stderr.write(
        f"\n{bcolors.FAIL}Commit failed: {bcolors.ENDC}{message}\n"
    )
    if details:
        sys.stderr.write(f"{bcolors.WARNING}  -> {details}{bcolors.ENDC}\n\n")
    sys.exit(1)


def is_valid_commit_message():
    commit_file_path = sys.argv[1]
    with open(commit_file_path) as commit:
        lines = commit.readlines()

    # Remove comment lines
    lines = [line for line in lines if not line.startswith("#")]

    # Remove trailing blank lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    # Detect empty commit message
    if not lines:
        print_error("Empty commit message.")

    subject = lines[0].strip()

    # Check subject line length (50 characters)
    # NOTE: We use strip() to remove the trailing newline before checking length.
    if len(subject) > 50:
        print_error(
            "Subject line is too long.",
            f"It should be 50 characters or less, but it's {len(subject)}.",
        )

    # A commit must have a body unless it's a trivial change.
    # This enforces a blank line and a description.
    if len(lines) < 3:
        print_error(
            "Description is missing.",
            "Add a blank line after the subject, followed by a description.",
        )

    # The second line must be blank
    if lines[1].strip() != "":
        print_error(
            "Missing a blank line after the subject.",
            "Separate subject from body with a blank line.",
        )

    # Check description lines
    for i, line in enumerate(lines[2:]):
        line = line.strip()
        if not line:
            continue

        # Check description line length (72 characters)
        if len(line) > 72:
            print_error(
                f"Description line {i+1} is too long.",
                f"It should be 72 characters or less, but it's {len(line)}.",
            )

	sys.exit(0)

if __name__ == "__main__":
	is_valid_commit_message()

EOF

echo "[Git Hook] Allow the verification of commit messages..."
# commit-msg 생성
COMMIT_MSG_FILE="$HOOKS_DIR/commit-msg"
cat >"$COMMIT_MSG_FILE" <<'EOF'
#!/bin/sh

exec < /dev/tty
python ./.git/hooks/verify_commit_msg.py $1
EOF

chmod +x "$COMMIT_MSG_FILE"

echo "[Setup] Git hooks intalled successfully!"

```

* 프로젝트 루트 폴더에서 `./scripts/git_hooks.sh` 실행하면 끝
	* 이후 커밋에서는 작성 규칙에 맞지 않는 경우 커밋이 안됨

### 🔧 Git 설정

* Git은 수많은 설정을 할 수 있지만 자세히 알아보지 않으면 편의성을 높일 수 있는 많은 설정을 놓칠 수 있음
	* [관련 글](https://news.hada.io/topic?id=19441)

#### 🎓 기본적인 설정

##### Git 기본 에디터를 VS Code로 변경

* Git 커밋 메시지 작성이나 충돌 해결은 보통 기본 에디터(vim, nano 등)을 사용하게 됨
	-당연히 vim, nano보단 VS Code가 편할테니 VS Code로 바꾸는 것이 좋음

	```bash
	git config --global core.editor "code --wait"
	```

##### Git CLI 명령어 자동 교정

<figure>
<img src="https://i.imgur.com/LH1qlWa.png" width='50%'>
<figcaption>Git을 쓰면서 오타가 발생했을 때의 짜증이란 정말…</figcaption>
</figure>

* Git CLI를 사용하다보면 빈번하게 오타를 내게 됨
	* Git 기본 설정을 통해 이런 오타를 수정할 수 있음

	```bash
	git config --global help.autocorrect prompt
	```

<figure>
<img src="https://i.imgur.com/sQGSJDr.png" width='75%'>
<figcaption>간단한 설정으로 의도한 명령어를 재질의하여 자동교정을 할 수 있다.</figcaption>
</figure>

##### 브랜치 목록 정렬

* 기본적으로 Git은 브랜치를 알파벳 순으로 정렬함
	* 최근 커밋 날짜 순으로 정렬하는게 더 유용하지 않을까?

	```bash
	git config --global column.ui auto
	git config --golbal branch.sort -committerdate
	```

##### 기본 브랜치 이름 설정

* 새로운 저장소를 초기화할 때 기본 브랜치 이름을 `main`으로 설정할 수 있음

	```bash
	git config --global init.defaultBranch main
	```

##### 직관적인 Push

* 새로운 브랜치를 만들고 push를 하면 remote에 없는 브랜치라며 추가 명령을 요구함
	* 알아서 remote에 브랜치 생성하면 되는데 왜 귀찮게 하는지 모르겠음

	```bash
	git config --global push.default simple  
	git config --global push.autoSetupRemote true  
	git config --global push.followTags true  
	```

##### Fetch 시 불필요한 브랜치나 태그 자동 제거

* Fetch 시 불필요한 브랜치나 태그가 많은데, 이걸 자동으로 제거할 수 있음

	```bash
	git config --global fetch.prune true  
	git config --global fetch.pruneTags true  
	git config --global fetch.all true
	```

##### 커밋할 때 변경 사항 커밋 메시지에 포함 

* 커밋 메시지 작성 시 변경된 내용을 함께 표시하여 사용자 경험을 높일 수 있음

	```bash
	git config --global commit.verbose true
	```


##### 충돌 해결 정보의 재사용

* 이전에 수행했던 충돌 해결을 자동으로 재사용할 수 있음

	```bash
	git config --global rerere.enabled true
	git config --global rerere.autoupdate true
	```

#### 🔺 Delta

* 우선 [`delta`](https://github.com/dandavison/delta) 설치
	* `delta` 를 쉽게 설치하기 위해선 [Homebrew](https://brew.sh/) 필요
	```bash
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	```
	* Homebrew 설치 후 `delta` 설치
	```bash
	brew install git-delta
	```

* Git에 `delta` 관련 설정 수행

	```bash
	git config --global core.pager delta
	git config --global interactive.diffFilter 'delta --color-only'
	git config --global delta.navigate true
	git config --global delta.line-numbers true
	git config --global delta.side-by-side true
	git config --global merge.conflictStyle zdiff3
	```


<figure>
<img src="https://i.imgur.com/hwcn2jz.png">
<figcaption>Before : Delta를 사용하기 전엔 수정사항 확인이 쉽지 않다.</figcaption>
</figure>

<figure>
<img src="https://i.imgur.com/pUrTxc3.png">
<figcaption>After : Side-by-side 뷰와 줄 번호, 음영 처리 등으로 가독성이 훨씬 좋음</figcaption>
</figure>

## 🛠️ Linux 도구

* 깡통 Linux (Ubuntu, Debian)가 개발하기 편한건 솔직히 아님
	* 흑백 화면에 하얀 글씨가 많은 정보를 주지도 않음
* 기본 명령어도 좋지만 훨씬 더 나은 도구가 많음
	* 특히 쉘(shell)은 무조건 바꾸는게 맞다고 생각함

### 🐚 zsh + ohmyzsh + powerlevel10k

* Linux의 기본 쉘인 `bash`보단 `zsh` 사용을 적극 권장
* 더 나아가 `zsh`을 더 강력하게 사용하기 위해 `ohmyzsh` 설치

	```bash
	# sudo apt update
	# sudo apt install curl git
	sudo apt install zsh
	sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
	```

* `ohmyzsh` 설치와 동시에 기본 쉘을 `zsh`로 바꾸고 나면 아래와 같은 화면이 뜸

<figure>
<img src="https://i.imgur.com/svHcBRL.png">
<figcaption>꽤 화려한 oh-my-zsh</figcaption>
</figure>

* 여기에 여러 정보를 제공해주는 테마인 `powerlevel10k`까지 설치하면 충분함
	* `powerlevel10k`을 올바르게 사용하기 위해서는 Nerd font가 필요함
	* 자세한 내용은 [README](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#getting-started) 확인

	```bash
	git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
	```

* 위 명령어 실행 후 `~/.zshrc` 파일에 `ZSH_THEME`의 값을 `"powerlevel10k/powerlevel10k`로 변경
* 그 후 `exec zsh`를 실행해서 쉘을 재실행하면 `powerlevel10k` 설정창이 뜸

<figure>
<img src="https://i.imgur.com/jDA7jD9.png">
<figcaption><code>powerlevel10k</code> 설정 완료!</figcaption>
</figure>

### 🦇 bat

* `cat`은 파일 내용을 그대로 출력해주지만 문법 하이라이트, 줄 번호 등이 없어 아쉬운 점이 많음
* [`bat`](https://github.com/sharkdp/bat)으로 대체 가능
	* 문법 하이라이트, 줄 번호, Git 통합, 프린트 불가능 문자 출력 등 다양한 기능이 있음
* Homebrew로 쉽게 설치 가능

	```bash
	brew install bat
	```


### 🧭 yazi

* 터미널에서 파일 탐색이 쉬운 일은 아님
* 작업 효율성을 크게 높여줄 수 있는 탐색기 같은 툴이 바로 [`yazi`](https://yazi-rs.github.io/)
	```bash
	brew install yazi
	```

* 단축키가 매우 많으므로 [문서](https://yazi-rs.github.io/docs/quick-start) 참고

### 🔍 fzf

* 리눅스에서 파일 검색 및 탐색은 느리고 귀찮음
* Fuzzy finding 기능을 탑재한 [`fzf`](https://github.com/junegunn/fzf)를 이용하면 훨씬 빠르고 쉽게 원하는 파일, 폴더를 찾을 수 있음 
	* ~~놀랍게도 한국인이 만듦 (라인 재직 중)~~

	```bash
	brew install fzf
	```

* 아래 내용을 `~/.zshrc`에 추가

	```bash
	# Set up fzf key bindings and fuzzy completion
	source <(fzf --zsh)
	```

* 설정 후 `exec zsh`로 쉘 재실행 후 제대로 사용 가능
* 개인적으로 가장 편한 기능은 `kill`할 프로세스 찾는 것
	* 아래와 같이 `kill -9 **`까지 입력 후 TAB 키를 누르면 프로세스를 검색할 수 있음

	```bash
	kill -9 **<TAB>
	```

<figure>
<img src="https://i.imgur.com/p55z4Fs.png">
<figcaption>매번 귀찮게 <code>ps -ef | grep</code>를 치지 않아도 된다!</figcaption>
</figure>

## 🚀 코드 품질

* 생각보다 코드 품질을 높이기는 어렵지 않음
	* 과거에는 `black`, `isort`, `mypy` 조합을 많이 사용했음
		* 하지만 속도가 그렇게 빠르지 않음
* 최근 Python의 대부분 툴킷은 [Astral](https://github.com/astral-sh)에서 Rust 기반으로 만든 것들
	* `uv`
		* `pipenv`, `poetry`, `pyenv` 대체
	* `ruff`
		* `black`, `flake8`, `autopep8`, `isort` 등 대체
	* `ty`
		* `mypy`, `pyright` 대체
* 위에서 언급한 모든 도구는 VS Code에서 확장 프로그램으로도 설치할 수 있음

### Ruff

<figure>
<img src="https://i.imgur.com/AOM8Sjf.png">
<figcaption>Ruff의 압도적인 속도</figcaption>
</figure>

* [깃허브 저장소](https://github.com/astral-sh/ruff)
* Rust로 작성된 Python 린터이자 코드 포매터

	```bash
	uv add --dev ruff 
	```

* 프로젝트 루트 폴더에 `ruff.toml`에 환경설정을 하거나 `uv`로 생성된 `pyproject.toml`에 환경설정을 할 수 있음
* 아래 설정은 `ruff.toml`에 추가하여 사용하는 값임
	* 기본 레이아웃은 80글자 이내
	* FastAPI에서 발생할 수 있는 의존성 주입 관련 린팅 설정 추가

	```toml
	lint.select = [
	    "E",   # Pycodestyle 오류 (들여쓰기, 공백 등)
	    "F",   # Pyflakes 오류 (미사용 변수, 임포트 등)
	    "I",   # 임포트 정렬
	    "UP",  # pyupgrade
	    "N",   # PEP8 명명 규칙
	    "Q",   # 따옴표 스타일 
	    "S",   # 보안 이슈
	    "SIM", # 코드 단순화
	    "ARG", # 미사용 함수 인자 (flake8-unused-arguments)
	    "W",   # Pycodestyle 경고
	    "B",   # 잠재적 버그 검출
	    "C4",  # 컴프리헨션 최적화
	]
	
	line-length = 80
	indent-width = 4
	target-version = "py312"
	
	[lint.isort]
	case-sensitive = true
	
	[format]
	quote-style = "double"
	line-ending = "auto"
	
	[lint.flake8-bugbear]
	extend-immutable-calls = [
	    "fastapi.Depends",
	    "fastapi.parmas.Depends",
	    "fastapi.Query",
	    "fastapi.params.Query",
	]
	```

* 이미 프리커밋에 추가되어 있지만, 프리커밋과 상관 없이 VS Code에 확장 프로그램으로 설치하여 설정하면 파일 저장 시 알아서 포맷팅이 실행됨
* 코드 베이스에 린팅과 포맷팅을 다음 명령어로 수행할 수 있음
	```bash
	ruff check --fix --config=ruff.toml path/to/code/ 
	ruff format --line-length 80 path/to/code/
	```

### Ty

* [깃허브 저장소](https://github.com/astral-sh/ty)
* 역시 Rust로 작성된 Python 타입 체커이자 랭귀지 서버(language server)
	* 아직 프리뷰 버전이지만 `mypy`, `pyright` 대비 압도적 속도로 자주 사용
* 다음 명령어로 타입 체킹
	```bash
	ty check path/to/code/
	```

* VS Code에서 확장 프로그램으로 설치하여 에디터 내에서도 바로 타입 체킹 가능

## 🐍 Python 보일러플레이트 코드 및 구조

* 이 내용을 설명하기 위해 지금까지 굉장히 많은 설정을 했음
	* 여기서부턴 실제 개발 단계라고 생각하면 됨

> [!note] 
> * 지금까지의 설정이 정말 필요한가 의문을 가질 수 있음
> 	* 왜냐면 배보다 배꼽이 더 커보이니까
> 	* 하지만 이런 설정을 통해 **앞으로 벌어질 수많은 휴먼 에러와 유지보수의 어려움으로부터 벗어날 수 있음**
> * 이런 규칙이 없이 진행되는 프로젝트를 보면…
> 	* 처음에는 꽤 빠르게 개발이 진행됨
> 	  → *왜?* : **프로토타입처럼 만드니까**
> 	* 하지만 구현이 복잡해지고 요구사항이 많아지면
> 		* 필연적으로 문제가 발생함
> 		* 마치 정리되지 않은 바탕화면에서 원하는 파일을 찾아야 하는 느낌
> 			* *바탕화면을 정리하는 나만의 규칙이 있었다면?*

### 🧱 프로젝트 구조

* 일반적인 GenAI 백엔드 개발 프로젝트라고 가정
	* 가정하는 시나리오
		* FastAPI 사용
		* 단위테스트 수행 (`pytest`)
		* DB와 연계
			* Alembic으로 데이터베이스 이관 및 관리
			* ORM은 SQLAlchemy 사용
		* vLLM으로 직접 클라이언트를 구현
		* [리포지토리 패턴(Repository pattern)](https://medium.com/@kmuhsinn/the-repository-pattern-in-python-write-flexible-testable-code-with-fastapi-examples-aa0105e40776) 사용
* 위 시나리오에서 개인적으로 사용하는 프로젝트 구조는 아래와 같음
	* `.gitignore`에 다음 경로 및 파일을 제외하도록 설정
		* `data/`
		* `logs/`
		* `notebooks/`

```
 .
├──  alembic                  # 데이터베이스 이관 및 관리를 위한 alembic 관련 파일
├──  assets                   # 프로젝트에서 사용하는 에셋 (정적 파일 등)    
├──  configs                  # 설정 관련 파일 (Pydantic 설정, 기타 설정)
│   └──  settings.py          # pydantic-settings 기반 설정
├──  data                     # 데이터 관리
├──  logs                     # 로그 적재
├──  notebooks                # Jupyter 노트북 파일 관리
├──  scripts                  # 프로젝트 스크립트 (Git 설정 등)
│   ├──  .gitmessage          # Git 커밋 메시지 템플릿
│   └──  git_hooks.sh         # Git Hooks 스크립트
├── 󰣞 src                      # 소스 코드
│   ├──  api                  # API 계층 (라우터 및 의존성)
│   │   ├──  middleware       # 미들웨어 (인증 등)
│   │   ├──  routers          # 라우터 레이어 (표현 레이어)
│   │   └──  dependencies.py  # 의존성 파일 (DB 세션 등)
│   ├──  clients              # LLM 클라이언트 관리
│   ├──  core                 # 프로젝트 코어 파일 (커스텀 예외 처리, 로깅 모듈 등)
│   │   └──  logging.py       # structlog 기반 로깅 모듈
│   ├──  database             # 데이터베이스 세션, 엔진 등
│   ├──  models               # 모든 SQLAlchemy ORM 모델
│   ├──  repositories         # 데이터 접근 계층 (CRUD 관련)
│   ├──  resources            # 리소스 (커스텀 에러 메시지, 프롬프트 등)
│   ├──  schemas              # 모든 Pydantic 스키마 (요청/응답 유효성 검사)
│   ├──  services             # 서비스 레이어 (비즈니스 로직 계층)
│   └──  utils                # 공통 사용 유틸리티 함수
├──  tests                    # 단위테스트 관리 (src 폴더 미러링)
│	├──  api                  # API 관련 테스트
│	│   └──  routers          # 라우터 테스트
│	├──  clients              # 클라이언트 테스트
│	├──  repositories         # 리포지토리 CRUD 테스트
│	├──  services             # 서비스 레이어 테스트
│	├──  utils                # 유틸리티 함수 테스트
│   └──  conftest.py          # 단위테스트 설정 함수 (API 설정 등)
├── 󰊢 .gitignore               # Git에서 트래킹하지 않을 파일/폴더 목록
├── 󰛢 .pre-commit-config.yaml  # 프리커밋 설정
├──  .python-version          # 프로젝트 파이썬 버전
├──  Dockerfile               # Dockerfile
├──  main.py                  # FastAPI 앱 인스턴스화 및 라우터 포함
├── 󰂺 README.md                # Readme
├──  pyproject.toml           # 프로젝트 메타데이터 및 의존성
├──  ruff.toml                # Ruff 설정
└──  uv.lock                  # 프로젝트 의존성 Lock 파일
```

* 모든 코드 관련 폴더엔 `__init__.py`를 포함해야 함
	* 위 구조에선 생략
* 단위테스트 관련
	* 단위테스트의 폴더 구조는 소스 폴더 구조와 거의 같음
	* 테스트 파일 앞에 `test_` 라는 접두사를 붙이는 것을 권장
		* ex) 채팅 서비스에 대한 테스트 파일은 `test_chat_service.py`가 될 것
* 위 구조가 항상 정답은 아님
	* 어떤 패턴이냐에 따라 많이 달라질 것
		* UoW Pattern, Onion Architecture, CQRS Pattern 등
	* 이런게 궁금하다면 DDD에 대해 공부해보는게 좋음
		* <https://www.cosmicpython.com/>

### ⚙️ 설정 관리 (`pydantic-settings`)

* 모든 설정 관리는 `pydantic-settings`를 이용
* 장점이 많음
	* 자동 타입 변환 및 유효성 검사 가능
	* 명확한 우선 순위를 갖고 있음
		* 직접 코드에서 설정 > 환경 변수 > `.env` 파일 > 모델의 기본값
	* 중앙화된 관리 가능
	* IDE 자동 완성 및 타입 힌팅 가능
	* 시크릿 관리 기능 내장
		* `secrets_dir` 인자 사용
* 개인적으로 아래 코드를 사용함

```python
# configs/settings.py

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    log_path = Field(
        Path(__file__).parent.parent.joinpath("logs").joinpath("app.log")
    )


settings = Settings()

```

* 다른 코드에서 `from configs.settings import settings`를 임포트하여 설정을 불러옴

### 🪵 로그 설정 (`structlog`)

* 스탠다드 라이브러리도 충분히 좋음
	* 하지만 이런 점이 매번 아쉬움
		* 밋밋한 색깔 때문에 가독성이 좋지 못함
		* **구조화된 출력이 어려움**
* 스탠다드 라이브러리를 대체할 수 있는 선택지는 많음
	* `rich`
	* `loguru`
	* `structlog`
* `structlog`를 선택했음
	* `loguru`도 충분히 좋은 선택지
	* 왜?
		* 로그 가독성이 높음 (에러에 대한 traceback도 충분히 좋음)
		* 조금 어렵지만 커스터마이징이 자유로움
		* **구조화된 출력이 가능함**
			* 특히 JSON 형태로 출력하는 것에 강점이 있음 → 나중에라도 테이블로 적재하는 것도 용이
		* 비동기 로깅도 지원
* 아래 보일러플레이트를 주로 사용함

```python
# src/core/logging.py

import logging
import logging.handlers
import sys

import structlog
from structlog.processors import CallsiteParameter

from configs.settings import settings

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=True),
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False
            ),
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    CallsiteParameter.FILENAME,
                    CallsiteParameter.LINENO,
                    CallsiteParameter.FUNC_NAME,
                ],
            ),
        ],
    )
)

# 파일 핸들러 설정
file_handler = logging.handlers.RotatingFileHandler(
    settings.log_path, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
)
file_handler.setFormatter(
    structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(ensure_ascii=False),
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False
            ),
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    CallsiteParameter.FILENAME,
                    CallsiteParameter.LINENO,
                    CallsiteParameter.FUNC_NAME,
                ],
            ),
        ],
    )
)

# 루트 로거에 핸들러 추가
root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.INFO)

# structlog 공통 설정
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.dict_tracebacks,
        structlog.stdlib.render_to_log_kwargs,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """
    처리되지 않은 예외를 로깅하기 위한 함수.
    sys.excepthook의 표준 인자를 그대로 받음.
    """
    # 사용자가 Ctrl+C로 종료한 경우는 무시합니다.
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # structlog 로거를 가져옵니다.
    log = structlog.get_logger("uncaught_exception")

    # exc_info에 튜플을 전달하여 에러를 로깅합니다.
    log.error(
        "처리되지 않은 예외가 발생했습니다.",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

# --* 테스트 ---
# main.py

import sys

import structlog

from src.core import logging  # noqa: F401

logger = structlog.get_logger(__name__)
sys.excepthook = logging.handle_uncaught_exception

logger.info("애플리케이션 시작")
try:
    x = 1 / 0
except ZeroDivisionError:
    logger.exception("계산 중 오류 발생")

```

* 이 코드의 사용법이 약간 독특할 수 있음
	* 직접 무언가를 임포트해서 사용하는게 아니라 `src/core/logging.py` 를 불러오기만 하면 됨
		* 불러오는 것만으로도 내부 로거 설정이 적용됨
* `handle_uncaught_exception` 함수를 `sys.excepthook`에 저장함으로써 `try ... except` 으로 처리하지 못한 예기치 않은 오류도 로깅할 수 있음

### 🗃️ DB 연동 코드

* FastAPI에서 DB 연동 시 세션 팩토리를 의존성 주입하여 사용함
	* 동기/비동기 방식이 조금 다름

```python
# 동기 방식
# src/database/postgres.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "your_database_url"
engine = create_engine(
	DATABASE_URL,
	pool_size=10,
	max_overflow=10,
	pool_recycle=3600,
	pool_pre_ping=True,
	echo=False
)

SessionLocal = sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine,
	expire_on_commit=False
)

# src/api/dependencies.py
from src.database.postgres import SessionLocal

def get_db():
    session = SessionLocal()
    try:
	    yield session
	finally:
	    session.close()

# 비동기 방식

# src/database/postgres.py
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
ASYNC_DATABASE_URL = "your_async_database_url"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# src/api/dependencies.py
	from src.database.postgres import AsyncSessionLocal

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

```

- DB의 특성에 따라서 동기/비동기 시나리오가 나뉘고, 사용하는 라이브러리에 따라 달라질 수 있지만 결국 위 코드를 사용하게 됨
- 사용은 아래와 같이 엔드포인트를 정의하는 라우터에 인자로 넣으면 됨

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    item = result.scalars().first()
    return item
```

### 📝 테스트 기본 코드

* 일반적으로 `conftest.py`에 단위테스트에 사용할 것들을 정의함
	* 여기에서 정의한 fixture는 다른 단위테스트에 공통적으로 사용
	* 특히 FastAPI를 직접 실행하지 않고 클라이언트를 사용할 수 있도록 FastAPI의 테스트 클라이언트 기능을 미리 정의하는 것 추천

```python
# tests/conftest.py
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app() -> FastAPI:
    from main import app as actual_app

	return actual_app


@pytest.fixture(scope="session")
def client(app: FastAPI):
    with TestClient(app) as client:
        yield client

```

* 위처럼 정의한 `client`는 다른 단위테스트 파일에서 공통적으로 사용됨
	* FastAPI 앱을 띄우지 않고서도 단위테스트 가능
