#!/bin/bash
# Test source references handling in 20-files-present-and-referenced

set -e

# Path to the script to test
VALIDATOR="./20-files-present-and-referenced"
TEST_DATA_DIR="t/data/libksba_test"

# Create test data directory if it doesn't exist
rm -rf "$TEST_DATA_DIR"
mkdir -p "$TEST_DATA_DIR"

cp t/data/libksba/libksba.spec $TEST_DATA_DIR

touch "$TEST_DATA_DIR"/libksba-1.8.1.tar.bz2
touch "$TEST_DATA_DIR"/libksba-1.8.1.tar.bz2.sig
touch "$TEST_DATA_DIR"/libksba.keyring
touch "$TEST_DATA_DIR"/libksba.changes

echo "Running validator on $TEST_DATA_DIR..."
./20-files-present-and-referenced --batchmode "$TEST_DATA_DIR" || exit 1

exit 0


