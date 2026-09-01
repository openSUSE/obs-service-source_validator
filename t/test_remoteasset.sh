#!/bin/bash
# Test for .gitignore integration in 20-files-present-and-referenced

set -e

# Path to the script to test
VALIDATOR="./20-files-present-and-referenced"
TEST_DATA_DIR="t/data/remoteasset_test"

# Create test data directory if it doesn't exist
rm -rf "$TEST_DATA_DIR"
mkdir -p "$TEST_DATA_DIR"

# Create a dummy spec file
cat > "$TEST_DATA_DIR/test.spec" <<EOF
%define llama_cpp_version main
Name: test
Version: 1.0
Release: 0
Summary: test
License: MIT
#!RemoteAsset: git+https://github.com/ggml-org/llama.cpp#%{llama_cpp_version}
#!CreateArchive
Source10:       llama.cpp-main.tar.xz
%description
test
%prep
%setup -q
%build
%install
%files
EOF

# to be obsoleted, the current policy of factory requires that the remoteasset
# is also committed together wit the sources
touch "$TEST_DATA_DIR/llama.cpp-main.tar.xz"

# additional sources not needed for re-building the source rpm
touch "$TEST_DATA_DIR/build.obscpio"

echo "Running validator on $TEST_DATA_DIR..."
./20-files-present-and-referenced --batchmode "$TEST_DATA_DIR" || exit 1

rm "$TEST_DATA_DIR/llama.cpp-main.tar.xz"
./20-files-present-and-referenced --batchmode "$TEST_DATA_DIR" 2>/dev/null | grep -q "ERROR: Current policy is to submit some part of a remote asset" || exit 1

exit 0


