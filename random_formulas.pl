#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper;

my $level = shift @ARGV;
my @mas_op = split(', ', shift @ARGV);

my @mas_const = ('1' , '0' , 'id');
#my @mas_op = ('not', 'shr1', 'or', 'plus', 'shr4', 'shr16', 'shl1', 'if0', 'fold');
my $operators = {
	'fold' => {
		'exp' => '(fold Ex Ex ( lambda ( id1 id2 ) Ex ) )',
	},
	'if0' => {
		'exp' => '(if0 Ex Ex Ex)',
	},
	'or' => {
		'exp' => '(or Ex Ex)',
	},
	'shr1' => { 
		'exp' => '(shr1 Ex)',
	},
	'shr4' => { 
		'exp' => '(shr4 Ex)',
	},
	'shr16' => { 
		'exp' => '(shr16 Ex)',
	},
	'shl1' => { 
		'exp' => '(shl1 Ex)',
	},
	'not' => {
		'exp' => '(not Ex)',
	},
	'plus' => {
		'exp' => '(plus Ex Ex)',
	},
};
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
my $count = 0;
my $count_ex = 0;
my $result = '(lambda (id) ';
for my $i (0..$level) {
	my $rand = int(rand(@mas_op));
	if($mas_op[$#mas_op] eq 'tfold') {
		$rand = $#mas_op;
		$mas_op[$#mas_op] = 'fold';
	}
	print "$rand\n";
	my $exp = $operators->{$mas_op[$rand]}->{'exp'};
	if ($result =~ /Ex/) {
		$result =~ s/Ex/$exp/;
	} else {
		
		$result =~ s/(.*)$/$1 $exp/;
	}
	if($mas_op[$rand]  eq 'fold') {
		#splice(@mas_op, -1);
		pop(@mas_op);
		$count++;
	}
	$count++;
	$count_ex = 0;
	while($result =~ /Ex/g) {
		$count_ex++;
	}
	last if ($level-1 == $count + $count_ex);
}

for my $i (0..$count_ex) {
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
