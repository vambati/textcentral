open(N,">neg.txt");
open(P,">pos.txt");
open(B,">both.txt");
open(O,">neutral.txt");

# Format 
# type=weaksubj len=1 word1=wreck pos1=noun stemmed1=n priorpolarity=negative
while(<>) { 
$_=~/word1=(.+?) /;
$word = $1;
$_=~/priorpolarity=(.+?)$/;
$polar = $1; 

if($polar eq "negative"){
	print N $word."\n"
}elsif($polar eq "positive")  { 
	print P $word."\n";
}elsif($polar eq "both")  { 
	print P $word."\n";
	print N $word."\n";
	print B $word."\n";
}elsif($polar eq "neutral")  { 
	print O $word."\n";
}

}
