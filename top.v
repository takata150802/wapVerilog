module top (
clk,
in0,
in1,
out0,
out1
);

input clk;
input in0;
input in1;
output out0;
output out1;

wire w0;
m0 i0 (.clk(clk), .in0(w0),.in1(in0), .out0(out0),.out1(w1));
m1 #(77) i1 (
.clk(clk), .in0(w1),.in1(in1), .out0(out1),.out1(w0)
);
endmodule
