'timescale 1ns / 1ps;

module simple_cpu(
    clk, 
    rst, 
    instruction
);

    parameter DATA_WIDTH = 8; // 8-bit wide data
    parameter ADDR_BITS = 5; // 32 addresses
    parameter INSTR_WIDTH = 20; // 20b instruction

    input clk;
    input rst;
    input [INSTR_WIDTH-1:0] instruction;

    // CU wires
    wire [DATA_WIDTH-1:0] offset_i;
    wire sel1_i, sel3_i;
    wire [DATA_WIDTH-1:0] operand_1_i, operand_2_i;

    // Data memory wires
    wire [ADDR_BITS-1:0] addr_i;
    wire [DATA_WIDTH-1:0] data_in_i, data_out_i, result2_i;
    wire wen_i;

    // ALU wires
    wire [DATA_WIDTH-1:0] operand_a_i, operand_b_i, result1_i;
    wire [3:0] opcode_i;