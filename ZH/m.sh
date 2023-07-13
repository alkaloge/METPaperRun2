
while read line 
do
echo "        self.t.Branch('"$line"', self.$line, '$line /F) '"
done<$1
