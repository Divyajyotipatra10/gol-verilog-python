#DO FILE FOR AXB UART MODULE
#WORK LIBRARY
vlib work 
#vmap work dev
#COMPILING ALL RTL DESIGN FILES
vlog ../rtl/top_module.v

#COMPILING THE TESTBENCH

vlog ../tb/tb.v

#ELABORATION

vsim work.tb

add wave -divider "OUTPUT"
add wave sim:/tb/clk
add wave sim:/tb/load
add wave sim:/tb/d
add wave sim:/tb/q

# Run simulation
run -all
