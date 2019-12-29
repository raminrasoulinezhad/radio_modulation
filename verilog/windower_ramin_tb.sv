`timescale 1ns/1ps
module windower_ramin_tb();

	parameter NO_CH = 16;
	parameter LOG2_IMG_SIZE = 6;
	parameter THROUGHPUT = 1;
	parameter WINDOW = 3;
	parameter PADDDING = 1;

	parameter clk_p = 1.0;
	parameter clk_p2= clk_p/2;

	reg clk;
	reg rst;

	reg vld_in;
	reg [NO_CH-1:0] data_in [THROUGHPUT-1:0];

	wire vld_out;
	wire [NO_CH-1:0] data_out [WINDOW-1:0];
	
	integer i;
	reg [NO_CH-1:0] count;

	initial begin 
		clk = 0;
		forever begin
			#clk_p2 clk= !clk;
		end
	end 
	initial begin

		rst = 1;
		vld_in = 0;
		count = 1024;

		repeat (2)  @(posedge clk) 
		rst = 0;
		
		repeat (2)  @(posedge clk) 
		rst = 0;

		repeat (2**LOG2_IMG_SIZE) begin 
			@(posedge clk) begin
				for (i = 0; i < THROUGHPUT; i = i + 1)begin
					data_in[i] = count;
					count = count + 1;
				end
				#clk_p2 vld_in = 1;
			end
		end

		@(posedge clk) #clk_p2 vld_in = 0;

		repeat (10)  begin
			@(posedge clk)
			#clk_p2 vld_in = 0;
		end 
		$stop;

	end

	windower_ramin #(
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
