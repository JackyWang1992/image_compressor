# image_compressor
__Contributors:__
- __[Jiaqi Wang](https://github.com/JackyWang1992)__ - wangjiaqi2017@brandeis.edu 

## how to compile my code?

1. the part1 part is a java program, you need to compile the java file first, all you need to do is the 
    simple command below:
    ```bash
    javac *.java
    ```
    
2. the part2 compressor and decompressor are python project, some packages may not available with your computer, 
    here I use [Numpy](http://www.numpy.org/) for matrix computation and [PIL](https://pillow.readthedocs.io/en/5.3.x/)
    to install them, you can use terminal to type:
    ```bash
    pip install numpy
    ```
    ```bash
    pip install Pillow
    ```
3. also there is another program called psnr_analysis.py to calculate the PSNR of our compression
   it's also a python project and don't have to compile

## how to use it? 
###(all files in the example are in the same folder with program and need to uncomment the complete mode in the main at the bottom and comment the test script mode)

1. follow this instruction to play with this tool! :)

2. to compress(lossy) the image file, just type like below:
  the first parameter is the filename, the second parameter is block size (8 * 8) or (16 * 16), the last 
  parameter is the quality, (0 - low (PSNR = 30), 1-medium(PSNR=40), 2-high (PSNR = 50))
  to simplicity in the test script, by default, I commented this function in the main and just use filename as 
  the only parameter.
    ```bash
    python3 compressor.py Kodak08gray.bmp 8 1 # complete mode
    ```
    ```bash
    python3 compressor.py Kodak08gray.bmp  # test script mode
    ```
3. after compression, the compressed file is called: XXXout.csv
    
4. then you can use XXXout.csv to do the loss compress the file follow the same way of compression
      ```bash
    python3 decompressor.py Kodak08grayout.csv 8 1 # complete mode
    ```
    ```bash
    python3 compressor.py Kodak08grayout.csv  # test script mode
    ```
    
5. the decompressed file is called: XXXrestore.bmp

6. then you can use psnr to compare the quality of compression, the first parameter is the original image file and the
    second filename is the compressed image file after lossy compression
    ```bash
     sudo python3 psnr_analysis.py Kodak08gray.bmp Kodak08grayoutrestore.bmp
    ```
7. to use the part1 compressor, just type below, the first parameter is the filename and the second parameter is the compression mode (0-FC, 1-AP),
 and the third parameter is the deletion mode (0- freeze, 1-restart, 2-LRU)
    ```bash
    java Part1Compress Kodak22grayout.csv 0 0
    ```
8. the part1 decompress is the same as compress:
     ```bash
    java Part1Decompress Kodak22grayout-compressed.dat 0 0
    ```

6. below is the example about how to use it to compress Kodak08gray.bmp and decompress from compressed file.

Example:
```bash
python3 compressor.py Kodak08gray.bmp 8 1
python3 decompressor.py Kodak08grayout.csv 8 1
python3 psnr_analysis.py Kodak08gray.bmp Kodak08grayoutrestore.bmp
java Part1Compress Kodak08grayout.csv 0 0
java Part1Decompress Kodak08grayout-compressed.dat 0 0
```

### How my program works and data structure I used

1. for this assignment, I mainly follow the compression steps of JPEG: the goal of compression is to produce a file of 
    string line by line, every line represents a block（8 * 8 or 16 * 16)
    the decompression goal is to restore a bmp file from file produced from part2 compressor or after part1 compression

2. for DCT and inverse function, I used matrix multiplication: 
   ```
   2DCT(A) = D * A * D' 
   i2DCT(A) = D' * A * D 
   ```   
   first, I compute the matrix of D for DCT use python function `construct_dct()` and then apply this formula with the 
   help from `numpy.matmul()` which apply matrix multiplication.
   
3. also in decompressor to restore the matrix from compression, I store the matrix width * length in the output file of compression
   as the title of output.csv and use it to stack the blocks to restore the matrix, other functions are just the inverse of compression

4. to control the PSNR for different qualities (low = 30, medium = 40, high = 50), I choose different quantization matrix, when tuned to different
  PSNR, I found that the restored image lose a lot of details when I just change the matrix without reference.
  To solve this problem, I found a fantastic website [ImpulseAdventures](https://www.impulseadventure.com/photo/jpeg-quantization.html) for references
  . From here, you can find a lot of quantization tables optimized for jpeg compression.
  For convenience, I used **Adobe PhotoShop CS** standard for reference since it can provide a wide range of PSNR.
  Unfortunately, I cannot find a suitable quantization matrix for PSNR = 30 for many pictures, so I just scaled the given 
  quantization table(not a good idea though)...
  
5. I used psnr_analysis.py to analyse the psnr and then fill the tables.

