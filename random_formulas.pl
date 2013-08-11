#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper;

my $level = shift @ARGV;
my @mas_op = split(', ', shift @ARGV);
my $num_variants = shift @ARGV;
print $num_variants, "\n";
my @mas_const = ('1' , '0' , 'id');
unless (@mas_op) {
	@mas_op = ('xor', 'not', 'shr1', 'or', 'plus', 'shr4', 'shr16', 'shl1', 'if0', 'fold');
}
my $operators = {
	'fold' => {
		'exp' => '(fold Ex Ex ( lambda ( id1 id2 ) Ex ) )',
		'flag' => 0,
		'w' => 2,
	},
	'if0' => {
		'exp' => '(if0 Ex Ex Ex)',
		'flag' => 0,
		'w' => 2,
	},
	'or' => {
		'exp' => '(or Ex Ex)',
		'flag' => 0,
		'w' => 2,
	},
	'shr1' => { 
		'exp' => '(shr1 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'shr4' => { 
		'exp' => '(shr4 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'shr16' => { 
		'exp' => '(shr16 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'shl1' => { 
		'exp' => '(shl1 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'not' => {
		'exp' => '(not Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'plus' => {
		'exp' => '(plus Ex Ex)',
		'flag' => 0,
		'w' => 2,
	},
	'xor' => {
		'exp' => '(xor Ex Ex)',
		'flag' => 0,
		'w' => 2,
	},
};
=qw
my $unar_operators = {
	'shr1' => { 
		'exp' => '(shr1 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'shr4' => { 
		'exp' => '(shr4 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'shr16' => { 
		'exp' => '(shr16 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'shl1' => { 
		'exp' => '(shl1 Ex)',
		'flag' => 0,
		'w' => 1,
	},
	'not' => {
		'exp' => '(not Ex)',
		'flag' => 0,
		'w' => 1,
	},

};
=cut
my $const = {
	'1' => {
		'exp' => '1',
		'num' => '1'
	},
	'0' => {
		'exp' => '0',
		'num' => '1'
	},
	'id' => {
		'exp' => 'id',
		'num' => '1'
	},

};
LINE:
for (1..$num_variants) {
	my $count = 0;
	my $count_ex = 0;
	my $result = '(lambda (id) ';
	my @parametrs = @mas_op;
	for my $i (1..$level) {
		my $rand = int(rand(@parametrs));
		if($parametrs[$#parametrs] eq 'tfold') {
			$rand = $#parametrs;
			$parametrs[$#parametrs] = 'fold';
		}
		my $count_ex_pre = 0;
		while($result =~ /Ex/g) {
			$count_ex_pre++;
		}
		my $exp = $operators->{$parametrs[$rand]}->{'exp'};
		if ($result =~ /Ex/) {
			$result =~ s/Ex/$exp/;
		} else {
			$result =~ s/(.*)$/$1 $exp/;
		}
		if($parametrs[$rand]  eq 'fold') {
			pop(@parametrs);
			$count++;
		} else {
			$operators->{$parametrs[$rand]}->{'flag'} = 1;
		}
		$count++;
		$count_ex = 0;
		while($result =~ /Ex/g) {
			$count_ex++;
		}
		if ($level-1 <= $count + $count_ex) {
			last;
		}
	}

	for my $i (1..$count_ex) {
		my $rand = int(rand(@mas_const));
		my $exp = $const->{$mas_const[$rand]}->{'exp'};
		if ($exp eq 'id' and $result =~ /[^(Ex)]\(fold [\S]* [\S]* \( lambda \( id1 id2 \) Ex \) \)/) {
			$exp .= 1+int(rand(2));	 
		}
		if($result =~ /\(Ex\)/) {
			$result =~ s/\(Ex\)/$exp/;
		} elsif ($result =~ /Ex/) {
			$result =~ s/Ex/$exp/;
		}
	}

	print "$result)\n";
}
