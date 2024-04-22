# Automated Verilog Code Generator
## Digital Systems Project                          
*(Course : ES 204, Professor : Joycee M. Mekie, Place : IIT Gandhinagar)*

Python based Automated Verilog Code Generator for adder and multipliers (Kogge-stone adder, Wallace tree multiplier and Booth Multiplier)

*Team Members*:

Sneha Gautam                                      
Kumkum Raj                                                     
Oruganti Dheekshitha                                                                           

## Step 1
Download the scratch.py and index.html file from the code section. 

Create a new folder in your device. Save main Python file 'scratch.py' in the folder. The code for website is contained in this file. Make a new folder named "templates" in the created folder. Inside the templates folder save 'index.html' HTML file. This file contain the structure of the website. 

![Screenshot 2024-04-20 190212](https://github.com/SG00428/Digital-Systems-Project/assets/130676806/f612f140-5f58-4a04-af90-60371510a147)
![Screenshot 2024-04-20 190224](https://github.com/SG00428/Digital-Systems-Project/assets/130676806/65434d04-25d4-4109-af9c-55d600a65d00)

## Step 2
Open any python code editor/compiler and add the created folder in it. Now run the scratch.py file. (NOTE : make sure to install Flask in your device)

![Screenshot 2024-04-20 190340](https://github.com/SG00428/Digital-Systems-Project/assets/130676806/6141a111-6f61-4fe5-9cb6-cc83892bf8cd)

## Step 3
Generated code will render a website link, go to the link to open the website.

![Screenshot 2024-04-20 190429](https://github.com/SG00428/Digital-Systems-Project/assets/130676806/7596059f-f39f-41b3-bf71-02a7b2a9d8ec)

## Step 4
Choose from the adder or multipliers and number of bits. Hence the desired verilog code is generated.

![Screenshot 2024-04-20 190457](https://github.com/SG00428/Digital-Systems-Project/assets/130676806/9499aac3-e8c3-40b9-99e8-744e99e5818a)
![Screenshot (214)](https://github.com/SG00428/Digital-Systems-Project/assets/130676806/8fe4ed0d-8650-4a2f-b425-ad45358f1cb1)

## DESCRIPTION:

## KOGGE STONE ADDER:

Like all other carry-lookahead adders, the Kogge-stone adder internally tracks "generate" and
"propagate" bits for spans of bits. We begin with 1-bit spans and perform addition on a single
column, propagating a carry bit (logical XOR) if exactly one input is 1 and creating a carry bit
(logical AND) if both inputs are 1. Next, by merging nearby spans together, bits for wider spans
are produced and disseminated.
The more major, full-width spans are always used in the Kogge-Stone design, whereas the less
significant ones are truncated. All neighbouring spans are combined to create 2-bit spans,
starting with the 1-bit spans. Since no propagation is possible, the least significant span is given
special treatment. It is combined with the carry into the addition and only generates a generate
bit. In the following step, each 2-bit wide span is combined with the 2-bit span that came before
it to create a 4-bit span. Except for the three least important spans, this is the case. The next
two are combined with the carry-in and the previously calculated least significant span,
respectively, to provide generate bits for 3- and 4-bit spans that include the carry-in. The least
significant span has already been calculated.
Since each span is merged with at most two other spans in the next stage (one more significant
and one less significant), fan-out is minimal. [1]


## WALLACE MULTIPLIER:

A Wallace multiplier is a hardware implementation of a binary multiplier, a digital circuit that multiplies two integers. It uses a selection of full and half adders (the Wallace tree or Wallace reduction) to sum partial products in stages until two numbers are left. [3] 
The Wallace tree has three steps: 
1. Multiply each bit of one of the arguments by each bit of the other. 
2. Reduce the number of partial products to two by layers of full and half adders. 3. Group the wires in two numbers and add them with a conventional adder. 

## BOOTH MULTIPLIER:

Booth's algorithm examines adjacent pairs of bits of the 'N'-bit multiplier Y in signed two's complement representation, including an implicit bit below the least significant bit, y−1 = 0. For each bit yi, for i running from 0 to N − 1, the bits yi and yi−1 are considered. Where these two bits are equal, the product accumulator P is left unchanged. Where yi = 0 and yi−1 = 1, the multiplicand times 2i is added to P; and where yi = 1 and yi−1 = 0, the multiplicand times 2i is subtracted from P. The final value of P is the signed product.

The representations of the multiplicand and product are not specified; typically, these are both also in two's complement representation, like the multiplier, but any number system that supports addition and subtraction will work as well. As stated here, the order of the steps is not determined. Typically, it proceeds from LSB to MSB, starting at i = 0; the multiplication by 2i is then typically replaced by incremental shifting of the P accumulator to the right between steps; low bits can be shifted out, and subsequent additions and subtractions can then be done just on the highest N bits of P.[2] There are many variations and optimizations on these details.

The algorithm is often described as converting strings of 1s in the multiplier to a high-order +1 and a low-order −1 at the ends of the string. When a string runs through the MSB, there is no high-order +1, and the net effect is interpretation as a negative of the appropriate value.

