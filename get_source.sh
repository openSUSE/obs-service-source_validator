#!/bin/bash

rm -rf obs-service-source_validator
mkdir obs-service-source_validator
for i in /work/cd/lib/source_validators/* ; do
   test -f $i || continue
   case $i in *abuild*) continue ;; esac
   sed -e "s@/work/cd/lib@/usr/lib/obs/service" $i > obs-service-source_validator/`basename $i`
   chmod 755 obs-service-source_validator/`basename $i`
done
mkdir obs-service-source_validator/helpers
for i in /work/cd/lib/source_validators/helpers/* ; do
   test -f $i || continue
   sed -e "s@/work/cd/lib@/usr/lib/obs/service" -e "s@/work/src/bin/tools/release_2_pdb_release@echo@" -e "s@/work/abuild/lib/abuild/modules@/usr/lib/build@" -e "s@use dateparse@use Date::Parse@" -e "s@use timezone@use Time::Zone@" $i > obs-service-source_validator/helpers/`basename $i`
   chmod 755 obs-service-source_validator/helpers/`basename $i`
done
rm -rf t
mkdir t
cd t
tar xjfp ../obs-service-source_validator.tar.bz2
cd ..
diff -urN t/obs-service-source_validator obs-service-source_validator
rm -rf t
tar cjfp obs-service-source_validator.tar.bz2 obs-service-source_validator

