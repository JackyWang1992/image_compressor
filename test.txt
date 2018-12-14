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
Part2C="python3 compressor.py"
Part2D="python3 decompressor.py"
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
    $Part2C Kodak/"$file.bmp" 8 1
    mv "$file.csv" PART2C/
    $Part2D PART2C/"$file.csv" 8 1
    mv "$file.bmp" PART2D/
    $Part1C PART2C/"$file.csv" 0 0
    mv PART2C/"$file.dat" PART21C/
    $Part1D PART21C/"$file.dat" 0 0
    mv PART21C/"$file.csv" PART211D/
    $Part2D PART211D/"$file.csv" 8 1
    mv "$file.bmp" PART2112D/
    cat PART2C/"$file.csv" | compress > COMPRESS/$file
    cat PART2C/"$file.csv" | gzip > GZIP/$file
    echo "Check $file lossless portion for differences:"; diff PART2C/"$file.csv" PART211D/"$file.csv"
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