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
