open(POS,">pos.txt"); 
open(NEG,">neg.txt"); 

while(<>){
chomp();
my ($w,$h,$s) = split(/,/,$_);
$w=~s/^\s+//g;
$w=~s/\s+$//g;

if($h>$s) { 
print POS "1\t$w\n";
}else{
print NEG "0\t$w\n";
}

}
close(POS);
close(NEG);

