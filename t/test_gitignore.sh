#!/bin/bash
# Test for .gitignore integration in 20-files-present-and-referenced

set -e

# Path to the script to test
VALIDATOR="./20-files-present-and-referenced"
TEST_DATA_DIR="t/data/gitignore_test"

# Create test data directory if it doesn't exist
mkdir -p "$TEST_DATA_DIR"
trap 'rm -rf "$TEST_DATA_DIR"' EXIT

# Create a dummy spec file
cat > "$TEST_DATA_DIR/test.spec" <<EOF
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

# Create a .gitignore and an ignored file
echo "ignored.txt" > "$TEST_DATA_DIR/.gitignore"
touch "$TEST_DATA_DIR/ignored.txt"

# Create an extra file that should NOT be ignored and NOT in spec
touch "$TEST_DATA_DIR/extra.txt"

echo "Running validator on $TEST_DATA_DIR..."
OUTPUT=$(./20-files-present-and-referenced --batchmode "$TEST_DATA_DIR" 2>&1)

echo "Output:"
echo "$OUTPUT"

# Verification
RET=0

if echo "$OUTPUT" | grep -q "ignored.txt"; then
    echo "FAIL: ignored.txt should have been ignored but was mentioned in output"
    RET=1
fi

if ! echo "$OUTPUT" | grep -q "extra.txt"; then
    echo "FAIL: extra.txt should have been mentioned in output but was not"
    RET=1
fi

if [ $RET -eq 0 ]; then
    echo "SUCCESS: gitignore filtering works correctly"
else
    echo "FAILURE: gitignore filtering test failed"
fi

exit $RET
