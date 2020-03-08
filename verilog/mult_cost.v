module mult_cost(
		a, 
		b, 
		
		a_v,
		b_v,

		c
	);

	parameter a_size = 16;
	parameter b_size = 2;

	parameter a_v_en = 1'b0;
	parameter b_v_en = 1'b0;
	
	input signed [a_size-1 : 0] a;
	input signed [b_size-1 : 0] b;
		
	input a_v;
	input b_v;

	output signed [a_size+b_size-1 : 0] c;


	reg signed [a_size-1 : 0] a_temp;
	reg signed [b_size-1 : 0] b_temp;
	always @(*) begin
		if ( a_v_en == 1 ) begin 
			if (a_v == 1) begin
				a_temp = a;
			end else begin
				a_temp = 0;
			end 
		end else begin
			a_temp = a;
		end 
	end 
	always @(*) begin
		if ( b_v_en == 1 ) begin 
			if (b_v == 1) begin
				b_temp = b;
			end else begin
				b_temp = 0;
			end 
		end else begin
			b_temp = b;
		end 
	end 

	assign c = a_temp * b_temp;

endmodule 
