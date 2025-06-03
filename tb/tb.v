`timescale 1ns / 1ns

module tb;

parameter width = 256; // Total number of cells (must be a perfect square)
localparam r_c_w = 1 << ($clog2(width)/2); // Grid side length (sqrt of width)

reg clk = 0, load = 0;              // Clock and load signals
reg [width-1:0] d;                  // Input data vector (initial grid state)
wire [width-1:0] q;                // Output data vector (current grid state)

reg [6:0] stable_count = 0;        // Counter to check for stable (unchanging) state
reg [width-1:0] prv_q = 0;         // Stores previous value of q to compare with current
integer i = 0, j = 0;              // Loop indices for printing grid (if needed)

reg [255:0] d_mem [0:0];           // Memory to hold initial data read from file

// Instantiate the DUT (Device Under Test)
top_module DUT(clk, load, d, q);

// Generate clock: 100 MHz (10 ns period)
always #5 clk = ~clk;

// Initial block to load pattern and trigger load signal
initial begin
    d <= 256'd0;
    $readmemh("F:/conway_gol/run/user_input.txt", d_mem); // Load initial state from file
    #100;                             // Wait for 100 ns
    @(posedge clk) load = 1;         // Set load high
    @(posedge clk) d = d_mem[0];     // Drive input data
    @(posedge clk) load = 0;         // Lower load after one cycle
end 

// Monitor for convergence (no change in state for 16 consecutive cycles)
reg flag = 0;
always @(posedge clk) begin
    if (!load) prv_q <= q;              // Store previous output
    if (prv_q == q) begin               // If current output matches previous
        if (stable_count == 15) begin   // If stable for 16 cycles
            flag <= 1;                  // Set flag to end simulation
        end else begin
            stable_count <= stable_count + 1; // Increment stability counter
        end
    end else begin
        stable_count <= 0;              // Reset if change is observed
    end
end

/*
Optional grid printing for visual debug
Uncomment to see 16x16 formatted output
*/
always @(posedge clk) begin
    if (!load && d) begin
        for (i = 0; i < r_c_w; i = i + 1) begin
            $write("[ ");
            for (j = 0; j < r_c_w; j = j + 1) begin
                $write("%0d ", q[i * r_c_w + j]);
            end
            $write("]\n");
        end
        $write("\n"); // Separate frames
    end
end


// File handle to write simulation output
integer outfile;
initial begin
    outfile = $fopen("sim_output.txt", "w"); // Open output file
    if (outfile == 0) begin
        $display("Failed to open output file!");
        $finish;
    end
end

// Write current grid state to file on each clock cycle, until system stabilizes
always @(posedge clk) begin
    if (!flag && outfile && !load) begin
        $fwrite(outfile, "%b\n", q); // Log grid as binary row
    end
    
    if (flag) begin
        $fclose(outfile);            // Close output file
        $finish;                     // End simulation
    end
end

// Simulation timeout to prevent infinite loop (in case no stability is reached)
initial begin
    #500000;
    $display("Simulation timed out.");
    $fclose(outfile);
    $finish;    
end

endmodule
