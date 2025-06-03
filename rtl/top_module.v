`timescale 1ns/1ns

// Top-level module for Conway's Game of Life logic with periodic boundaries
module top_module #(
    parameter width = 256 // Total number of cells in the grid (must be square)
)(
    input clk,                     // System clock
    input load,                    // Load signal: if high, q is initialized with input data
    input [width-1:0] data,        // Initial state of the grid (1D vectorized)
    output reg [width-1:0] q       // Current grid state (1D vectorized)
); 
    
    // Grid side length (assuming square), calculated as sqrt(width)
    localparam n = 1<<($clog2(width)/2);

    // Array to hold 4-bit sum of alive neighbors for each cell
    reg [3:0] sum [0:(width-1)];

    integer i = 0;

    // Initial reset of q and sum values
    initial begin
        q = 0;
        for (i = 0; i < width; i = i + 1)
            sum[i] = 0;
    end

    // Combinational block to compute neighbor sums
    always @(*) begin
        for (i = 0; i < width; i = i + 1) begin

            // Left boundary (column 0)
            if ((i % n) == 0) begin
                if (i == 0) begin
                    // Top-left corner (cell 0)
                    sum[i] = q[i+1] + q[i+(n-1)] + q[i+n] + q[(i+1)+n] +
                             q[i+((n<<1)-1)] + q[i+(n*(n-1))] +
                             q[i+((n*(n-1))+1)] + q[i+((n+1)*(n-1))];
                end
                else if (i == (n*(n-1))) begin
                    // Bottom-left corner (cell 240 for n=16)
                    sum[i] = q[i+1] + q[i+(n-1)] + q[i-n] + q[(i+1)-n] +
                             q[i-1] + q[i-(n*(n-1))] + q[(i+1)-(n*(n-1))] +
                             q[(i+n-1)-(n*(n-1))];
                end
                else begin
                    // Other left-edge cells
                    sum[i] = q[i+1] + q[i+(n-1)] + q[i+n] + q[(i+1)+n] +
                             q[i+((n<<1)-1)] + q[i-n] + q[(i+1)-n] + q[i-1];
                end

            end
            // Right boundary (column n-1)
            else if ((i % n) == (n-1)) begin
                if (i == (n-1)) begin
                    // Top-right corner (cell 15)
                    sum[i] = q[i-1] + q[(i+1)-n] + q[i+n] + q[(i-1)+n] +
                             q[i+1] + q[i+(n*(n-1))] + q[(i-1)+(n*(n-1))] +
                             q[(i+1)+(n*(n-2))];
                end
                else if (i == ((n-1)*(n+1))) begin
                    // Bottom-right corner (cell 255 for n=16)
                    sum[i] = q[i-1] + q[(i+1)-n] + q[i-n] + q[(i-1)-n] +
                             q[(i+1)-(n<<1)] + q[i-(n*(n-1))] +
                             q[(i-1)-(n*(n-1))] + q[(i+1)-(n*n)];
                end
                else begin
                    // Other right-edge cells
                    sum[i] = q[i-1] + q[(i+1)-n] + q[i+n] + q[(i-1)+n] +
                             q[i+1] + q[i-n] + q[(i-1)-n] + q[(i+1)-(n<<1)];
                end

            end
            // Top edge (excluding corners)
            else if (i > 0 && i < (n-1)) begin
                sum[i] = q[i-1] + q[i+1] + q[(i-1)+n] + q[i+n] + q[(i+1)+n] +
                         q[i+(n*(n-1))] + q[(i-1)+(n*(n-1))] + q[(i+1)+(n*(n-1))];
            end
            // Bottom edge (excluding corners)
            else if (i > (n*(n-1)) && i < (n*n)) begin
                sum[i] = q[i-1] + q[i+1] + q[(i-1)-n] + q[i-n] + q[(i+1)-n] +
                         q[i-(n*(n-1))] + q[(i+1)-(n*(n-1))] + q[(i-1)-(n*(n-1))];
            end
            // Interior cells
            else begin
                sum[i] = q[i-1] + q[i+1] + q[(i-1)+n] + q[i+n] + q[(i+1)+n] +
                         q[(i-1)-n] + q[i-n] + q[(i+1)-n];
            end
        end
    end

    // Sequential block: update q on clock edge
    always @(posedge clk) begin
        if (load)
            q <= data; // Load initial state
        else begin
            for (i = 0; i < width; i = i + 1) begin
                // Game of Life rules:
                if (sum[i] <= 1)
                    q[i] <= 0;            // Underpopulation
                else if (sum[i] == 2)
                    q[i] <= q[i];         // Survival
                else if (sum[i] == 3)
                    q[i] <= 1;            // Birth
                else
                    q[i] <= 0;            // Overpopulation
            end
        end
    end
endmodule
