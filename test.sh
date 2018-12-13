#!/usr/bin/env bash
#Shell script to test Assignments Part 1 and 2 used together.
#This script should be run in a folder containing this script, named test.txt,
#a folder named "Kodak" that contains the 6 Kodak gray scale test files for Assignment Part 2,
#and executables for a Part 1 encoder, a Part 1 decoder, a Part 2 encoder, and a Part 2 decoder.
#To run, type ./test.txt in a UNIX terminal window using the bash shell (as on a Mac in the COSCI lounge).
#
#These names are set to do nothing for Part 2 (cat just passed the bytes through)
#and use bzip2 for part 1.
#Change cat to your Part 2 encoder and decoder and bzip2 to your Part 1 encoder and decoder.
Part1C="java Part1Compress"
Part1D="java Part1Decompress"
Part2C="python3 compressor"
Part2D="python3 decompressor"
#
#Creat sub-sirectories to store results:
mkdir COMPRESS
mkdir UNCOMPRESS
mkdir GZIP
mkdir GUNZIP
mkdir PART2C
mkdir PART2D
mkdir PART21C
mkdir PART211D
mkdir PART2112D
#
echo ''; echo 'Compress, decompress, check lossless portion for differences:'
for file in Kodak08gray Kodak09gray Kodak12gray Kodak18gray Kodak21gray Kodak22gray
do
cat Kodak/"$file.bmp" | $Part2C > PART2C/$file
cat PART2C/$file | $Part2D > PART2D/"$file.bmp"
cat PART2C/$file | $Part1C > Part21C/$file
cat PART21C/$file | $Part1D > PART211D/$file
cat PART211D/$file | $Part2D > PART2112D/"$file.bmp"
cat Part2C/$file | compress > COMPRESS/$file
cat Part2C/$file | gzip > GZIP/$file
echo "Check $file lossless portion for differences:"; diff Part2C/$file Part211D/$file
done
#
echo''; echo 'Original file sizes:'
ls -l Kodak
#
echo ''; echo 'Compressed file sizes using Part2 followed by Part 1:'
ls -l PART21C
#
echo ''; echo 'Compressed file sizes using Part2 followed by Unix compress:'
ls -l COMPRESS
#
echo ''; echo 'Compressed file sizes using Part2 followed by Unix gzip:'
ls -l GZIP