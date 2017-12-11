package DebianSourceChangesValidator;

use strict;
use warnings;

sub validate {
  my ($fname) = @_;
  my @mandatory = qw/Format Date Source Binary Architecture Version Distribution Maintainer Description Changes Checksums-Sha1 Checksums-Sha256 Files/;
  my $re    = '^('.join('|',@mandatory).'):.*';
  my $result = {};

  open(my $fh,$fname) || die "Could not open '$fname': $!\n";
  while (my $line = <$fh>) { $line =~ m/$re/ && $result->{$1}++ }
  close $fh;

  for my $key (@mandatory) { return 1 if (! $result->{$key} ) }

  return 0
}

1;
