`timescale 1ns/1ps
module to_serial_tb();

	parameter NO_CH = 4;
	parameter BW_IN = 10;
	parameter BW_OUT = 2;

	localparam NO_CYC = int'($ceil(BW_IN/BW_OUT));

	parameter clk_p = 1.0;
	parameter clk_p2= clk_p/2;

	parameter exp_repeats = 2;

	reg clk;
	reg rst;

	reg vld_in;
	reg [NO_CH-1:0][BW_IN-1:0] data_in;
	wire vld_out;
	wire [NO_CH-1:0][BW_OUT-1:0] data_out;
	
	
	reg [NO_CH-1:0] count;

	initial begin 
		clk = 0;
		forever #clk_p2 clk= !clk;
	end 

	integer i, j;
	initial begin
		rst = 1;
		vld_in = 0;
		count = 1024;

		repeat(2) @(posedge clk) 
		rst = 0;
		repeat(2) @(posedge clk) 
		rst = 0;
		
		vld_in = 1;
		for (i = 0; i < NO_CH; i = i + 1) begin
			data_in[i] = $random;
		end 
		
		repeat(NO_CYC+10) begin 
			@(posedge clk)
			vld_in = 0;		
		end 	

		$stop;

	end

	to_serial#(
		NO_CH,
		BW_IN,
		BW_OUT
	)to_serial_inst(
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),
		
		.vld_out(vld_out),
		.data_out(data_out)
	);

endmodule 
