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
	for my $i (1..$level) {
		my $rand = int(rand(@mas_op));
		if($mas_op[$#mas_op] eq 'tfold') {
			$rand = $#mas_op;
			$mas_op[$#mas_op] = 'fold';
		}
		my $count_ex_pre = 0;
		while($result =~ /Ex/g) {
			$count_ex_pre++;
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
		my $exp;
		if (($i == $level) and ($count + 2 + $count_ex_pre == $level)) {
			if($operators->{$mas_op[$rand]}->{'w'} != 1) {
				for (@mas_op) {
					if (exists $unar_operators->{$_}) {
						$exp = $unar_operators->{$_}->{'exp'};
					}
				}	
			}
		} else {
			$exp = $operators->{$mas_op[$rand]}->{'exp'};
		}
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
	#	if($level < $count + $count_ex) {
	#		print "\n";
	#		next LINE;
	#	}
		if (($level-1 <= $count + $count_ex) or (not @mas_op)) {
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
