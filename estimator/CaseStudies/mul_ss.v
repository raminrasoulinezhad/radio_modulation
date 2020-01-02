module mul_ss(

	clk,

	a,
	b,

	c
);
	parameter a_s = 16;
	parameter b_s = 8;
	input clk;

	input signed [a_s-1:0] a;
	input signed [b_s-1:0] b;

	output reg signed [a_s+b_s-1:0] c;

	always @(posedge clk)begin
		c <= a * b;
	end

endmodule 

