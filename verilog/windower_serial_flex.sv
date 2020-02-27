`timescale 1ns / 1ps
/* This module windows the data
 It assumes that after a vld_in signal, the entire image will be sent for 2^(LOG2_IMG_SIZE) cycles
 This windower is used to produce multiple convolutional windows depending on the THROUGHPUT
 */
module windower_serial_flex
#(
	parameter NO_CH = 2,
	parameter LOG2_IMG_SIZE = 10,
	parameter WINDOW_SIZE = 3,
	parameter SER_CYC = 1 		// must be a power of 2
) (
	input clk,
	input rst,

	input vld_in,
	input [NO_CH-1:0] data_in,
	
	output logic vld_out,
	output reg [NO_CH-1:0] data_out [WINDOW_SIZE-1:0],
	
	output ser_rst
);

	localparam LOG2_SER = $clog2(SER_CYC);
	localparam LOG2_W_S = $clog2(WINDOW_SIZE);
	localparam CNTR_MAX = 2**(LOG2_IMG_SIZE+LOG2_SER);

	localparam PAD = SER_CYC * ((WINDOW_SIZE-1)/2);

	reg [1:0] state;
	localparam state_wait = 2'b00;
	localparam state_run = 2'b01;
	localparam state_autorun = 2'b10;

	reg [NO_CH-1:0] window_mem_a;
	reg [NO_CH-1:0] window_mem [WINDOW_SIZE-2:0][SER_CYC-1:0];
	
	reg [LOG2_IMG_SIZE+LOG2_SER-1:0] cntr;
	
	reg [LOG2_SER+LOG2_W_S-1:0] remaining;


	//assign ser_rst = (cntr[LOG2_SER-1:0] == 0);
	assign ser_rst = (cntr[LOG2_SER-1:0] == (SER_CYC-1));
	//assign ser_rst = (((SER_CYC-1) == cntr) && ((vld_in)||(state == state_autorun)));

	wire cond0;
	//wire cond1;

	assign cond0 = (state == state_autorun) && (remaining != 0);
	//assign cond1 = vld_in && ((state == state_wait)|| (state == state_run));

	integer i, j;
	always @( posedge clk ) begin
		if (rst) begin
			window_mem_a <= 0;
			for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
				for (j = 0; j < SER_CYC; j = j + 1) begin
					window_mem[i][j] <= 0;
				end
			end
		end else begin
			if (cond0) begin 
				window_mem_a <= 0;
				for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
					if (i == 0) begin
						window_mem[i][0] <= window_mem_a;
					end else begin 
						window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
					end
					window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
				end
			end else if (vld_in) begin
				window_mem_a <= data_in;
				for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
					if (i == 0) begin
						window_mem[i][0] <= window_mem_a;
					end else begin 
						window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
					end
					window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
				end
			end 

		end
	end

	/*integer i, j;
	always @( posedge clk ) begin
		if (rst) begin
			window_mem_a <= 0;
			for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
				for (j = 0; j < SER_CYC; j = j + 1) begin
					window_mem[i][j] <= 0;
				end
			end
		end else if (vld_in && ((state == state_wait)|| (state == state_run))) begin
			window_mem_a <= data_in;
			for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
				if (i == 0) begin
					window_mem[i][0] <= window_mem_a;
				end else begin 
					window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
				end
				window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
			end
		end else if (state == state_autorun) begin
			if (remaining != 0) begin
				window_mem_a <= 0;
				for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
					if (i == 0) begin
						window_mem[i][0] <= window_mem_a;
					end else begin 
						window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
					end
					window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
				end	
			end else if (vld_in) begin  
				window_mem_a <= data_in;
				for (i = 0; i < WINDOW_SIZE - 1; i = i + 1) begin
					if (i == 0) begin
						window_mem[i][0] <= window_mem_a;
					end else begin 
						window_mem[i][0] <= window_mem[i-1][SER_CYC-1];
					end
					window_mem[i][SER_CYC-1:1] <= window_mem[i][SER_CYC-2:0];
				end
			end
		end
	end*/

	// output manager
	integer k;
	always @(*) begin
		for (k = 0; k < WINDOW_SIZE; k = k + 1) begin
			if (k == 0) begin
				data_out[k] = window_mem_a;
			end else begin
				data_out[k] = window_mem[k-1][SER_CYC-1];
			end
		end	
	end

	// State machine 
	always @( posedge clk ) begin
		if ( rst ) begin
			cntr <= 0;
			remaining <= PAD; 
			vld_out <= 0;
			state <= 0;
		end else begin
			
			unique if (state == state_run) begin
				if (vld_in)begin
					vld_out <= 1;
					if (cntr == (CNTR_MAX-PAD-2)) begin
						state <= state_autorun;
						remaining = PAD;
					end 
					cntr <= cntr + 1;
				end else begin
					vld_out <= 0;
				end
			end else if (state == state_autorun) begin
				if (remaining != 0) begin
					remaining <= remaining - 1;
					vld_out <= 1;
					cntr <= cntr + 1;
				end else begin  
					vld_out <= 0;
					state <= state_wait;
					cntr <= 0;
					if (vld_in) begin
						remaining <= PAD - 1;
					end else begin
						remaining <= PAD;
					end
				end
			end else if (state == state_wait) begin 
				if (vld_in) begin
					if (remaining == 0) begin
						state <= state_run;
						vld_out <= 1;
						cntr <= 0;
					end else begin
						remaining <= remaining - 1;
					end
				end
			end
		end
	end

endmodule
