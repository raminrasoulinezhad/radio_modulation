`timescale 1ns/1ps
module maxpool_flex_tb();

	parameter NO_CH = 10;
	// "BW_IN" should be dividable by "SER_BW"
	parameter BW_IN = 4;
	parameter SER_BW = 2;

	parameter clk_p = 1.0;
	parameter clk_p2= clk_p/2;

	localparam CYC = BW_IN / SER_BW;

	reg clk;
	reg rst;

	reg vld_in;
	reg [NO_CH-1:0][SER_BW-1:0] data_in;

	wire vld_out;
	wire [NO_CH-1:0][BW_IN-1:0] data_out;
	wire vld_out_flex;
	wire [NO_CH-1:0][BW_IN-1:0] data_out_flex;
	
	reg signed [NO_CH-1:0][BW_IN-1:0] A_org;
	reg signed [NO_CH-1:0][BW_IN-1:0] B_org;
	reg signed [NO_CH-1:0][BW_IN-1:0] A;
	reg signed [NO_CH-1:0][BW_IN-1:0] B;
	reg signed [NO_CH-1:0][BW_IN-1:0] M;

	reg [NO_CH-1:0] count;

	initial begin 
		clk = 0;
		forever begin
			#clk_p2 clk= !clk;
		end
	end 

	integer i, j;

	initial begin
		for (i = 0; i < NO_CH; i = i + 1) begin
			A[i] = $random;
			A_org[i] = A[i];
			B[i] = $random;
			B_org[i] = B[i];
			if ($signed(A[i]) > $signed(B[i]))begin
				M[i] = A[i];
			end else begin 
				M[i] = B[i];
			end 
		end 

		for (j = 0; j < NO_CH; j = j + 1) begin
			data_in[j] = 0;	
		end

	end
		
	initial begin
		rst = 1;
		vld_in = 0;
		count = 0;

		repeat(2) @(posedge clk) 
		rst = 0;
		repeat(2) @(posedge clk) 
		rst = 0;

		repeat (CYC) begin
			@(posedge clk) begin
				for (j = 0; j < NO_CH; j = j + 1) begin
					data_in[j] = A[j][SER_BW-1:0];	
					A[j] = {{SER_BW{1'b0}}, {A[j][BW_IN-1:SER_BW]}};
				end
				vld_in = 1;
			end
		end

		repeat (CYC) begin
			@(posedge clk) begin
				for (j = 0; j < NO_CH; j = j + 1) begin
					data_in[j] = B[j][SER_BW-1:0];
					B[j] = {{SER_BW{1'b0}}, {B[j][BW_IN-1:SER_BW]}};
				end
			end
		end

		repeat(1) @(posedge clk)
		vld_in = 0;

		repeat(10) begin 
			@(posedge clk) begin
				if (vld_out || vld_out_flex) begin
					if (M != data_out)begin 
						$display("baseline - error");
						$display("A: %b", A_org);
						$display("B: %b", B_org);
						$display("M: %b", M);
						$display("O: %b", data_out);
					end else begin 
						$display("baseline - OK");
						$display("A: %b", A_org);
						$display("B: %b", B_org);
						$display("M: %b", M);
						$display("O: %b", data_out);
					end 

					if (M != data_out_flex)begin 
						$display("flex - error");
						$display("A: %b", A_org);
						$display("B: %b", B_org);
						$display("M: %b", M);
						$display("O: %b", data_out_flex);
					end else begin 
						$display("flex - OK");
						$display("A: %b", A_org);
						$display("B: %b", B_org);
						$display("M: %b", M);
						$display("O: %b", data_out_flex);
					end 
					$stop;
				end
			end
		end
	end

	maxpool_flex #(
		NO_CH,
		BW_IN,
		SER_BW
	) maxpool_flex_inst (
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),

		.vld_out(vld_out_flex),
		.data_out(data_out_flex)
	);

	maxpool #(
		NO_CH,
		BW_IN,
		SER_BW
	) maxpool_inst (
		.clk(clk),
		.rst(rst),

		.vld_in(vld_in),
		.data_in(data_in),

		.vld_out(vld_out),
		.data_out(data_out)
	);

endmodule 
