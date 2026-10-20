#!/bin/bash
# Test Git ignore handling, including checkouts with a .git file.

set -eu

VALIDATOR="$PWD/20-files-present-and-referenced"
TEST_ROOT=$(mktemp -d)
trap 'rm -rf "$TEST_ROOT"' EXIT

# Keep user and system ignore settings out of these tests.
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null

fail() {
    echo "FAIL: $*" >&2
    printf '%s\n' "${OUTPUT:-}" >&2
    exit 1
}

assert_mentioned() {
    grep -Fq -- "$1" <<< "$OUTPUT" || fail "$1 should be mentioned"
}

assert_ignored() {
    if grep -Fq -- "$1" <<< "$OUTPUT"; then
        fail "$1 should be ignored"
    fi
}

for layout in directory gitfile; do
    TEST_DATA_DIR="$TEST_ROOT/$layout"
    if [ "$layout" = gitfile ]; then
        # The same .git indirection is used by submodules and worktrees.
        git init -q --separate-git-dir="$TEST_ROOT/metadata" "$TEST_DATA_DIR"
        [ -f "$TEST_DATA_DIR/.git" ] || fail "expected a .git file"
        # An osc checkout using Git must not require .osc/_osclib_version.
        mkdir "$TEST_DATA_DIR/.osc"
    else
        git init -q "$TEST_DATA_DIR"
    fi

    cat > "$TEST_DATA_DIR/test.spec" <<'EOF'
Name: test
Version: 1.0
Release: 0
Summary: test
License: MIT
Source0: test.tar.gz
%description
test
%prep
%setup -q
%build
%install
%files
EOF
    touch "$TEST_DATA_DIR/test.tar.gz"
    git -C "$TEST_DATA_DIR" add test.tar.gz

    printf 'ignored.txt\nignored-dir/\nextra.txt\n!extra.txt\n' > "$TEST_DATA_DIR/.gitignore"
    touch "$TEST_DATA_DIR/ignored.txt" "$TEST_DATA_DIR/extra.txt"
    mkdir "$TEST_DATA_DIR/ignored-dir"
    touch "$TEST_DATA_DIR/ignored-dir/file"

    echo "Testing .gitignore with $layout checkout"
    OUTPUT=$("$VALIDATOR" --batchmode "$TEST_DATA_DIR" 2>&1)
    assert_ignored ignored.txt
    assert_ignored ignored-dir
    assert_mentioned extra.txt

    # No root .gitignore is needed for repository-local excludes.
    rm "$TEST_DATA_DIR/.gitignore"
    EXCLUDE=$(git -C "$TEST_DATA_DIR" rev-parse --path-format=absolute --git-path info/exclude)
    printf 'ignored.txt\nignored-dir/\n' >> "$EXCLUDE"
    echo "Testing info/exclude with $layout checkout"
    OUTPUT=$("$VALIDATOR" --batchmode "$TEST_DATA_DIR" 2>&1)
    assert_ignored ignored.txt
    assert_ignored ignored-dir
    assert_mentioned extra.txt

    # Global ignore rules must work without a root .gitignore too.
    printf 'global-ignored.txt\n' > "$TEST_ROOT/global-ignore"
    git -C "$TEST_DATA_DIR" config core.excludesFile "$TEST_ROOT/global-ignore"
    touch "$TEST_DATA_DIR/global-ignored.txt"
    OUTPUT=$("$VALIDATOR" --batchmode "$TEST_DATA_DIR" 2>&1)
    assert_ignored global-ignored.txt

    # An ignored, untracked source required by the spec is still an error.
    git -C "$TEST_DATA_DIR" rm -q --cached test.tar.gz
    printf 'test.tar.gz\n' >> "$EXCLUDE"
    if OUTPUT=$("$VALIDATOR" --batchmode "$TEST_DATA_DIR" 2>&1); then
        fail "ignored required source should fail validation"
    fi
    git -C "$TEST_DATA_DIR" add -f test.tar.gz

done

# Provide the validator's external tools, but deliberately omit Git.
mkdir "$TEST_ROOT/bin"
for tool in bash dirname perl mktemp uname sed grep sort rm find cat touch cpio patch unzip xmllint diff cmp; do
    if TOOL_PATH=$(command -v "$tool"); then
        ln -s "$TOOL_PATH" "$TEST_ROOT/bin/$tool"
    fi
done

echo "Testing fallback without Git"
OUTPUT=$(PATH="$TEST_ROOT/bin" "$VALIDATOR" --batchmode "$TEST_DATA_DIR" 2>&1)
assert_mentioned ignored.txt
assert_mentioned ignored-dir
assert_mentioned extra.txt
if grep -Eq 'command not found|No such file or directory' <<< "$OUTPUT"; then
    fail "fallback should not invoke missing commands"
fi

echo "SUCCESS: Git ignore handling works with both checkout layouts and without Git"
