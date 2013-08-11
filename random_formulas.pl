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
		'flag' => 0,
	},
	'if0' => {
		'exp' => '(if0 Ex Ex Ex)',
		'flag' => 0,
	},
	'or' => {
		'exp' => '(or Ex Ex)',
		'flag' => 0,
	},
	'shr1' => { 
		'exp' => '(shr1 Ex)',
		'flag' => 0,
	},
	'shr4' => { 
		'exp' => '(shr4 Ex)',
		'flag' => 0,
	},
	'shr16' => { 
		'exp' => '(shr16 Ex)',
		'flag' => 0,
	},
	'shl1' => { 
		'exp' => '(shl1 Ex)',
		'flag' => 0,
	},
	'not' => {
		'exp' => '(not Ex)',
		'flag' => 0,
	},
	'plus' => {
		'exp' => '(plus Ex Ex)',
		'flag' => 0,
	},
	'xor' => {
		'exp' => '(xor Ex Ex)',
		'flag' => 0,
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
		if($level < 7) {
			print "\n";
			exit(0);
		}
		$rand = $#mas_op;
		$mas_op[$#mas_op] = 'fold';
	}
	if($operators->{$mas_op[$rand]}->{'flag'} == 1) {
		my $flag = 0;
		for my $oper (@mas_op) {
			if ($operators->{$oper}->{'flag'} == 0) {
				$flag = 1;
			}
		}
		redo if $flag;
	}
	my $exp = $operators->{$mas_op[$rand]}->{'exp'};
	if ($result =~ /Ex/) {
		$result =~ s/Ex/$exp/;
	} else {
		
		$result =~ s/(.*)$/$1 $exp/;
	}
	if($mas_op[$rand]  eq 'fold') {
		pop(@mas_op);
		$count++;
	} else {
		$operators->{$mas_op[$rand]}->{'flag'} = 1;
	}
	$count++;
	$count_ex = 0;
	while($result =~ /Ex/g) {
		$count_ex++;
	}
	if($level < $count + $count_ex) {
		print "\n";
		exit(0)
	}
	if (($level-1 <= $count + $count_ex) or (not @mas_op)) {
		last;
	}
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
