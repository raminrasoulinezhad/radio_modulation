module mux_w(
	a,
	b,

	s,
	c 
);
	parameter width = 2;

	input [width-1:0] a;
	input [width-1:0] b;

	input s;

	output [width-1:0] c;

	assign c = (s)? a : b;

endmodule
