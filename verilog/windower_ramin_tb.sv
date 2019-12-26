`timescale 1ns/1ps
module windower_tb();

	parameter NO_CH = 16;
	parameter LOG2_IMG_SIZE = 10;
	parameter THROUGHPUT = 1;
	parameter WINDOW = 3;
	parameter PADDDING = 1 ;

	reg clk;
	reg rst;

	reg vld_in;
	reg [NO_CH-1:0] data_in [THROUGHPUT-1:0];

	wire vld_out;
	wire [NO_CH-1:0] data_out [THROUGHPUT+1:0];
	
	integer i;

	initial begin 
		clk = 0;
		forever begin
			#0.5 clk= !clk;
		end
	end 
	initial begin
		rst = 1;
		vld_in = 0;

		#10 rst = 0;
		for (i = 0; i < THROUGHPUT; i = i + 1)begin
			data_in[i] = $urandom;
		end
		#10 vld_in = 1; 
		@(posedge clk)
		for (i = 0; i < THROUGHPUT; i = i + 1)begin
			data_in[i] = $urandom;
		end
		@(posedge clk)
		for (i = 0; i < THROUGHPUT; i = i + 1)begin
			data_in[i] = $urandom;
		end
		@(posedge clk)
		for (i = 0; i < THROUGHPUT; i = i + 1)begin
			data_in[i] = $urandom;
		end
		@(posedge clk)
		for (i = 0; i < THROUGHPUT; i = i + 1)begin
			data_in[i] = $urandom;
		end

	end

	windower #(
		NO_CH,
		LOG2_IMG_SIZE,
		THROUGHPUT,
		WINDOW,
		PADDDING
	) windower_inst (
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),

		.vld_out(vld_out),
		.data_out(data_out)
	);


endmodule 
