#!/bin/bash

rm -rf osc-source_validator
mkdir osc-source_validator
for i in /work/cd/lib/source_validators/* ; do
   test -f $i || continue
   case $i in *abuild*) continue ;; esac
   sed -e "s@/work/cd/lib@/usr/lib/osc@" $i > osc-source_validator/`basename $i`
   chmod 755 osc-source_validator/`basename $i`
done
mkdir osc-source_validator/helpers
for i in /work/cd/lib/source_validators/helpers/* ; do
   test -f $i || continue
   sed -e "s@/work/cd/lib@/usr/lib/osc@" -e "s@/work/src/bin/tools/release_2_pdb_release@echo@" -e "s@/work/abuild/lib/abuild/modules@/usr/lib/build@" -e "s@use dateparse@use Date::Parse@" -e "s@use timezone@use Time::Zone@" $i > osc-source_validator/helpers/`basename $i`
   chmod 755 osc-source_validator/helpers/`basename $i`
done
rm -rf t
mkdir t
cd t
tar xjfp ../osc-source_validator.tar.bz2
cd ..
diff -urN t/osc-source_validator osc-source_validator
rm -rf t
tar cjfp osc-source_validator.tar.bz2 osc-source_validator

