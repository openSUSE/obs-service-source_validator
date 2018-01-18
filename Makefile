PRJ=openSUSE:Tools
PKG=obs-service-source_validator

prefix = /usr

servicedir = ${prefix}/lib/obs/service

all:

install:
	install -d $(DESTDIR)$(servicedir)
	install -m 0755 source_validator $(DESTDIR)$(servicedir)
	install -m 0644 source_validator.service $(DESTDIR)$(servicedir)
	install -d $(DESTDIR)$(servicedir)/source_validators
	install -m 0755 [0-9]* $(DESTDIR)$(servicedir)/source_validators
	install -d $(DESTDIR)$(servicedir)/source_validators/helpers
	install -m 0755 helpers/* $(DESTDIR)$(servicedir)/source_validators/helpers

package:
	@if test -d $(PKG); then cd $(PKG) && osc up && cd -; else osc co -c $(PRJ) $(PKG); fi
	@./mkchanges | tee $(PKG)/.changes
	@test ! -s $(PKG)/.changes || git push
	@test -z "`git rev-list remotes/origin/master..master`" || { echo "unpushed changes"; exit 1; }
	@f=(*bz2); test -z "$f" || /bin/rm -vi *.bz2
	@./mktar
	@mv *bz2 $(PKG)

test:
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/github_issue_64.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/python-libmount.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/util-linux.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/util-linux-systemd.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/coreutils-testsuite.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/coreutils.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/continue-line.spec
	./helpers/spec_query --no-conditionals --keep-name-conditionals --disambiguate-sources --specfile t/data/cross-aarch64-gcc7.spec


.PHONY: all install package test
