`timescale 1ns/1ps

module windower_serial_ramin_tb();

	parameter PARALLEL_WIDTH = 16;
	parameter SERIAL_WIDTH = 4;
	parameter NO_CH = 4;
	parameter NO_CH_IN = NO_CH * SERIAL_WIDTH;

	parameter LOG2_IMG_SIZE = 5;
	parameter WINDOW_SIZE = 3;
	parameter SER_CYC = PARALLEL_WIDTH/SERIAL_WIDTH;
	localparam LOG2_SER = $clog2(SER_CYC);

	parameter clk_p = 1.0;
	parameter clk_p2 = clk_p / 2;

	reg clk;
	reg rst;

	reg vld_in;
	reg [NO_CH_IN-1:0] data_in;

	wire vld_out;
	wire [NO_CH_IN-1:0] data_out [WINDOW_SIZE-1:0];
	wire ser_rst;


	initial begin 
		clk = 0;
		forever begin
			#clk_p2 clk= !clk;
		end
	end 

	reg [19:0] i;
	reg [SERIAL_WIDTH-1:0] count;
	initial begin

		rst = 1;
		vld_in = 0;
		count = 0;
		i = 0;

		repeat (2)  @(posedge clk) 
		rst = 0;
		
		repeat (2)  @(posedge clk) 
		rst = 0;

		repeat (2**(LOG2_IMG_SIZE+LOG2_SER)) begin 
			@(posedge clk) begin
				data_in = {NO_CH{count}};
				count = count + 1;
				i = i + 1;
				#clk_p2 vld_in = 1;
			end
		end

		@(posedge clk) #clk_p2 vld_in = 0;
		repeat (20)  begin
			@(posedge clk)
			#clk_p2 vld_in = 0;
		end 


		repeat (2**(LOG2_IMG_SIZE+LOG2_SER)) begin 
			@(posedge clk) begin
				data_in = {NO_CH{count}};
				count = count + 1;
				i = i + 1;
				#clk_p2 vld_in = 1;
			end
		end

		@(posedge clk) #clk_p2 vld_in = 0;
		repeat (20)  begin
			@(posedge clk)
			#clk_p2 vld_in = 0;
		end 

		$stop;

	end

	windower_serial_ramin #(
		NO_CH_IN,
		LOG2_IMG_SIZE,
		WINDOW_SIZE,
		SER_CYC
	) dut (
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),

		.vld_out(vld_out),
		.data_out(data_out),
	
		.ser_rst(ser_rst)
	);

endmodule 
