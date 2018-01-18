Name: continue-line

%define foo %if 1 \
x: foo \
%else \
x: bar \
%endif
