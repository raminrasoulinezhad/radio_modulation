`timescale 1ns/1ps
module from_serial_tb();

	parameter NO_CH = 10;
	parameter BW_IN = 2;
	parameter BW_OUT = 8;

	parameter NO_CYC = int'($ceil(BW_OUT/BW_IN));

	parameter clk_p = 1.0;
	parameter clk_p2= clk_p/2;

	parameter exp_repeats = 2;

	reg clk;
	reg rst;

	reg vld_in;
	reg [NO_CH-1:0][BW_IN-1:0] data_in;
	wire vld_out;
	wire [NO_CH-1:0][BW_OUT-1:0] data_out;
	
	reg signed [NO_CH-1:0][BW_OUT-1:0] A_org;
	reg signed [NO_CH-1:0][BW_OUT-1:0] A;
	
	integer i;
	initial begin
		for (i = 0; i < NO_CH; i = i + 1) begin
			A[i] = $random;
			A_org[i] = A[i];
			data_in[i] = 0;
		end 
	end

	initial begin 
		clk = 0;
		forever #clk_p2 clk= !clk;
	end 

	integer j;
	initial begin
		rst = 1;
		vld_in = 0;

		repeat(4) begin 
			@(posedge clk) begin
				rst = 0;
			end 
		end 

		repeat (NO_CYC) begin
			@(posedge clk) begin
				for (j = 0; j < NO_CH; j = j + 1) begin
					data_in[j] = A[j][BW_IN-1:0];	
					A[j] = {{BW_IN{1'b0}}, {A[j][BW_OUT-1:BW_IN]}};
				end
				vld_in = 1;
			end
		end

		repeat(1) @(posedge clk)
		vld_in = 0;

		repeat(10) begin 
			@(posedge clk) begin
				if (vld_out) begin
					if (A_org != data_out)begin 
						$display("baseline - error");
						$display("A: %b", A_org);
						$display("O: %b", data_out);
					end else begin 
						$display("baseline - OK");
						$display("A: %b", A_org);
						$display("O: %b", data_out);
					end 
					$stop;
				end
			end
		end
	end

	from_serial#(
		NO_CH,
		BW_IN,
		BW_OUT
	)from_serial_inst(
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),
		
		.vld_out(vld_out),
		.data_out(data_out)
	);

endmodule 
