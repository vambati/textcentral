while(<>){
chomp;
# POS	ID	PosScore	NegScore	SynsetTerms	Gloss
my ($tag,$id,$neg,$pos,$set,$gloss) = split(/\t/,$_);
if($pos!=0) { 
	my @arr = split(/\s/,$set); 
	foreach my $x (@arr ) { 
		my ($w,$i) = split(/#/,$x);
		print "$w\t$pos\n";
	}
}
}
