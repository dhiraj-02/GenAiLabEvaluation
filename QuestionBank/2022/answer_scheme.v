//Total (28 marks)
// Final O/P carries 6 marks. Rest 22 marks divided across modules as described before the module definitions below

// d_ff modiule; No marks if only the code for D_FF module is written
module d_ff(q, d, clock, reset);
  input d, clock, reset;
  output  q;
  reg q;
  always @ (posedge clock or posedge reset)
  if(reset)
    q = 1'b0;
  else
    q = d;
endmodule

// 3 marks for REG_8BIT module
module REG_8BIT(reg_out, num_in, clock, reset);
  input [7:0] num_in;
  input clock, reset;
  output  [7:0]  reg_out;
  genvar j;
  generate
    for(j = 0; j < 8; j = j + 1) begin:  d_loop
      d_ff ff(reg_out[j], num_in[j], clock, reset);
    end
  endgenerate
endmodule

//3 marks for EXPANSION_BOX module
module EXPANSION_BOX(in, out);
	input [3:0]in;
	output [7:0]out;
	assign out = {in[3],in[0],in[1],in[2],in[1],in[3],in[2],in[0]};
endmodule

//1 mark for XOR_8BIT module
module XOR_8BIT (xout_8, xin1_8, xin2_8);
	output [7:0] xout_8;
	input [7:0] xin1_8, xin2_8;
	assign xout_8 = xin1_8 ^ xin2_8;
endmodule

//1 mark for XOR_4BIT module 
module XOR_4BIT (xout_4, xin1_4, xin2_4);
	output [3:0] xout_4;
	input [3:0] xin1_4, xin2_4;
	assign xout_4 = xin1_4 ^ xin2_4;
endmodule

// 1-bit MUX required in the CSA_4BIT module; No marks for this 1-bit MUX module independently
module mux2to1_1bit (a,b,s,f); 
	input a,b,s;
	output f;
	assign f = s ? a : b;
endmodule

// 4-bit MUX required in the CSA_4BIT module; No marks for this 4-bit MUX module independently
module mux2to1_4bit (a,b,s,f); 
	input [3:0]a; 
	input [3:0]b;
	input s;
	output [3:0] f;
	assign f = s ? a : b;
endmodule

// 1-bit full adder as fulladd module required in the fulladd4 module;  No marks for this 1-bit fulladdr module independently
module fulladd(sum, c_out, a, b, c_in);
	output sum, c_out;
	input a, b, c_in;
	wire s1, c1, c2;
	
	assign {c_out,sum} = a+b+c_in;
endmodule

// 4-bit full adder as fulladd4 module required in the CSA_4BIT module; No marks for this 4-bit fulladdr module independently; ; As seen here it should instantiate all the modules shown inside it.
module fulladd4(sum, c_out, a, b, c_in);
	output [3:0] sum;
	output c_out;
	input [3:0] a, b;
	input c_in;
	wire c1, c2, c3;
	
	fulladd fa0(sum[0], c1, a[0], b[0], c_in);
	fulladd fa1(sum[1], c2, a[1], b[1], c1);
	fulladd fa2(sum[2], c3, a[2], b[2], c2);
	fulladd fa3(sum[3], c_out, a[3], b[3], c3);
endmodule

//6 marks for CSA_4BIT module; Out of these 6 marks: 3 marks for correctly creating and instantiating fulladd4 module, 1 mark for correctly creating and instantiating fulladd modules inside fulladd4 module, and 2 marks for correctly creating and instantiating 1-bit and 4-bit MUX modules together
module CSA_4BIT(cin, inA, inB, cout, out);
	input cin;
	input [3:0] inA;
	input [3:0] inB;
	output cout;
	output [3:0] out;
	wire [3:0] out1;
	wire [3:0] out2;
	wire cout1, cout2;
	
	fulladd4 f1(out1, cout1, inA, inB, 1'b0);
	fulladd4 f2(out2, cout2, inA, inB, 1'b1);
	mux2to1_4bit m1(out2,out1,cin, out);
	mux2to1_1bit m2(cout2,cout1,cin,cout); 
	
endmodule

//1 mark for module CONCAT
module CONCAT(concat_out, concat_in1, concat_in2);
	output [7:0] concat_out;
	input [3:0] concat_in1, concat_in2;
	assign concat_out = {concat_in1,concat_in2};
endmodule

//4 marks for module ENCRYPT; As seen here it should instantiate all the modules shown inside it.
module ENCRYPT(number, key, clock, reset, enc_number);
	input [7:0] number, key;
	input clock, reset;
	output [7:0] enc_number;
	wire [7:0] reg1_out, reg2_out;
	wire [7:0] d_out, x_or1_out;
	wire [3:0] csa_out, x_or2_out;

	REG_8BIT reg1(reg1_out, number, clock, reset);
	REG_8BIT reg2(reg2_out, key, clock, reset);
	EXPANSION_BOX box(reg1_out[3:0], d_out);
	XOR_8BIT x_or1(x_or1_out, d_out, reg2_out);
	CSA_4BIT csa(reg2_out[0], x_or1_out[7:4], x_or1_out[3:0], cout, csa_out);
	XOR_4BIT x_or2(x_or2_out, csa_out, reg1_out[7:4]);
	CONCAT con1(enc_number, x_or2_out, reg1_out[3:0]);
endmodule

//3 marks for tb_encryption module; Out of these, 1 mark for clock and reset signal together, 1 mark for module instantiation, and 1 mark for correctly writing the monitor statement and the inputs
module tb_encryption; 
	reg [7:0] number;
	reg [7:0] key;
	reg clock,reset;
	wire [7:0] enc_number;
	
	ENCRYPT mod(number, key, clock, reset, enc_number);
	
	initial begin 
		clock=0; 
	end
	always 
		#2 clock=~clock; 
	
	initial begin 
		$monitor($time,"Number=%b Key= %b enc_number=%b \n",number, key, enc_number);
		#0 reset = 1'b0;
		#1 number = 8'b0100_0110; key = 8'b1001_0011;  //enc_number: 0000_0110
		#4 number = 8'b1100_1001; key = 8'b1010_1100;  //enc_number: 0011_1001
		#3 number = 8'b1010_0101; key = 8'b0101_1010;  //enc_number: 0011_0101
		#5 number = 8'b1111_0000; key = 8'b1011_0001;  //enc_number: 0010_0000
		#5 $finish; 
	end

endmodule