`timescale 1ns / 1ps

// IMPORTANT Note about parameter section: 

module pipelined_accumulator
#(
	parameter IN_BITWIDTH = 8,
	// OUT_BITWIDTH = IN_BITWIDTH + LOG2_NO_IN + loops_of_MAC
	parameter OUT_BITWIDTH = 10,
	parameter LOG2_NO_IN = 1
) (
	input clk,

	input new_sum,
	input signed [(1<<LOG2_NO_IN)-1:0][IN_BITWIDTH-1:0] data_in,

	output signed [OUT_BITWIDTH-1:0] data_out
);

	localparam INCR_BW = (IN_BITWIDTH<OUT_BITWIDTH) ?  IN_BITWIDTH + 1  :  IN_BITWIDTH;
	localparam NO_IN = 1 << LOG2_NO_IN;

	genvar i;
	generate
		if (LOG2_NO_IN <= 0) begin

			reg signed [OUT_BITWIDTH-1:0] data_out_reg;
			always @( posedge clk ) begin
	   			if ( new_sum ) begin
					data_out_reg <= $signed( data_in[0] ) + $signed( 0 );
				end else begin
					data_out_reg <= $signed( data_in[0] ) + $signed( data_out_reg );
				end
			end

			assign data_out = data_out_reg;

		end else begin

			reg signed [(NO_IN/2)-1:0][INCR_BW-1:0] intermediate_results;
			for (i = 0; i < (NO_IN/2); i = i + 1) begin
				always @( posedge clk ) begin
					intermediate_results[i] <= $signed(data_in[2*i]) + $signed(data_in[(2*i)+1]);
				end
			end
			
			reg new_sum_reg;
			always @( posedge clk ) begin
	   			new_sum_reg <= new_sum;
			end

			pipelined_accumulator
  			#(
				.IN_BITWIDTH( INCR_BW ),
				.OUT_BITWIDTH( OUT_BITWIDTH ),
				.LOG2_NO_IN( LOG2_NO_IN - 1 )
			) summation	(
				.clk( clk ),
				.new_sum( new_sum_reg ),
				.data_in( intermediate_results ),
				.data_out( data_out )
			);
		end
	endgenerate   

endmodule
