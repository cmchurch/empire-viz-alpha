#!/bin/bash 
#CHRISTOPHER M CHURCH
#ASSISTANT PROFESSOR
#DEPARTMENT OF HISTORY
#UNIVERSITY OF NEVADA, RENO

echo "Starting..."
cd ~/jdv-txt-fw-sol/
for x in *.txt; do
echo "Reading: " $x
iconv -c -f "windows-1252" -t "UTF-8" $x -o $x.cleaned
echo "Cleaned: " $x.cleaned
cat $x.cleaned | language-identifier | tokenizer | pos-tagger | ner > ~/share/$x.NER.kaf
echo "Recognized: " $x.NER.kaf
mv $x finished/$x
mv $x.cleaned finished/$x.cleaned
echo "Moved: " $x
	 
done
