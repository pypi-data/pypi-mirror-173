#proc AIT::memory_bonding {} {
#    #for {set mem_channel 0} {$mem_channel < [dict get ${::AIT::address_map} "num_banks"]} {incr mem_channel} {
#    #    set mem_channel_bonding [create_bd_cell -type ip -vlnv bsc:ompss:memory_channel_bonding:* mem_channel_bonding_${mem_channel}_[expr ${mem_channel} + 1]]
#
#
#    #}
#
#    #connect_bd_intf_net [get_bd_intf_pins $AXI_port] [get_bd_intf_pins
#    #
#    #
#    
#}
#

proc AIT::bond_QDMA_channels {} {
    set old_num_banks [dict get ${::AIT::address_map} "mem_num_banks"]
    set old_bank_size [dict get ${::AIT::address_map} "mem_bank_size"]
    dict set ::AIT::address_map "mem_num_banks" [expr $old_num_banks/2]
    dict set ::AIT::address_map "mem_bank_size" [expr $old_bank_size*2]

    set_property -dict [list CONFIG.USER_SAXI_14 {true}] [get_bd_cells bridge_to_host/HBM/HBM]
    set axi_fifo [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_data_fifo:* bridge_to_host/HBM/S_AXI_QDMA/AXI_fifo]
    set_property -dict [list CONFIG.READ_FIFO_DEPTH {32}] $axi_fifo
    #create_bd_cell -type ip -vlnv xilinx.com:ip:axi_protocol_converter:* bridge_to_host/HBM/S_AXI_QDMA/HBM_protocol_converter
    #delete_bd_objs [get_bd_cells bridge_to_host/HBM/S_AXI_QDMA/HBM_RAMA]
    delete_bd_objs [get_bd_cells bridge_to_host/HBM/S_AXI_QDMA/HBM_data_width_converter]
    delete_bd_objs [get_bd_intf_nets bridge_to_host/HBM/S_AXI_QDMA]
    delete_bd_objs [get_bd_intf_nets bridge_to_host/HBM/S_AXI_QDMA/HBM_protocol_converter_M_AXI]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA/S_AXI] [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA/HBM_protocol_converter/S_AXI]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA/HBM_protocol_converter/M_AXI] [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA/AXI_fifo/S_AXI]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA/M_AXI] [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA/AXI_fifo/M_AXI]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/QDMA/M_AXI] [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA]
    connect_bd_net [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/AXI_fifo/aclk]
    connect_bd_net [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/AXI_fifo/aresetn]
    delete_bd_objs [get_bd_nets bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_awaddr_2] [get_bd_nets bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_araddr_2] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_awaddr] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_araddr]
    #delete_bd_objs [get_bd_nets bridge_to_host/HBM/S_AXI_QDMA_awaddr_2] [get_bd_nets bridge_to_host/HBM/S_AXI_QDMA_araddr_2] [get_bd_nets bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_awaddr_2] [get_bd_nets bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_araddr_2] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_awaddr] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA/S_AXI_QDMA_araddr] [get_bd_nets bridge_to_host/QDMA_s_axi_araddr] [get_bd_nets bridge_to_host/QDMA_s_axi_awaddr] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA_araddr] [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA_awaddr]
    set_property name S_AXI_QDMA_0 [get_bd_cells bridge_to_host/HBM/S_AXI_QDMA]
    #set_property name S_AXI_QDMA_0 [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA]
    #set_property name S_AXI_QDMA_0 [get_bd_intf_nets bridge_to_host/HBM/S_AXI_QDMA]
    copy_bd_objs bridge_to_host/HBM [get_bd_cells {bridge_to_host/HBM/S_AXI_QDMA_0}]
    connect_bd_net [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA_1/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/HBM/AXI_14_ACLK] [get_bd_pins bridge_to_host/HBM/QDMA_aclk]
    connect_bd_net [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA_1/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/HBM/AXI_14_ARESET_N] [get_bd_pins bridge_to_host/HBM/QDMA_peripheral_aresetn]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA_1/M_AXI] [get_bd_intf_pins bridge_to_host/HBM/HBM/SAXI_14]

    #delete_bd_objs [get_bd_intf_nets bridge_to_host/QDMA_M_AXI]
    set mem_channel_bonding [create_bd_cell -type ip -vlnv bsc:ompss:memory_channel_bonding:* bridge_to_host/HBM/QDMA_mem_channel_bonding]
    set_property -dict [list CONFIG.AXI_ID_WIDTH {4} CONFIG.AXI_ADDR_WIDTH {64} CONFIG.AXI_MASTER_DATA_WIDTH {256} CONFIG.WIDE_BANK_BITS {28} CONFIG.NARROW_BANK_CAPACITY {268435456}] $mem_channel_bonding
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA] [get_bd_intf_pins $mem_channel_bonding/s_axi]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA_0/S_AXI] [get_bd_intf_pins $mem_channel_bonding/m0_axi]
    connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA_1/S_AXI] [get_bd_intf_pins $mem_channel_bonding/m1_axi]
    connect_bd_net [get_bd_pins $mem_channel_bonding/clk] [get_bd_pins bridge_to_host/QDMA/aclk]
    connect_bd_net [get_bd_pins $mem_channel_bonding/rstn] [get_bd_pins bridge_to_host/QDMA/aresetn]
    connect_bd_net [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA_awaddr] [get_bd_pins $mem_channel_bonding/s_axi_awaddr]
    connect_bd_net [get_bd_pins bridge_to_host/HBM/S_AXI_QDMA_araddr] [get_bd_pins $mem_channel_bonding/s_axi_araddr]
}

#update_ip_catalog -add_ip /media/sda2/scratch/joliver/reset/ip-bonding-experiment-10MHz-no-225MHz-16accs-working-qdma-fifos/ip-bonding-experiment/spmv/bsc.es_axi-tools_axi_channel_bonding_1.0.zip -repo_path /media/sda2/scratch/joliver/reset/ip-bonding-experiment-10MHz-no-225MHz-16accs-working-qdma-fifos/ip-bonding-experiment/spmv/spmv_ait/xilinx/HLS
#
#startgroup
#
## Add reset box for APB & connect it properly
#create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 proc_sys_reset_0
#connect_bd_net [get_bd_pins clock_generator/locked] [get_bd_pins proc_sys_reset_0/dcm_locked]
#connect_bd_net [get_bd_pins clock_generator/apb_clk] [get_bd_pins proc_sys_reset_0/slowest_sync_clk]
#connect_bd_net [get_bd_ports pcie_perstn] [get_bd_pins proc_sys_reset_0/ext_reset_in]
#disconnect_bd_net /bridge_to_host/HBM/peripheral_aresetn_1 [get_bd_pins bridge_to_host/HBM/HBM/APB_0_PRESET_N]
#disconnect_bd_net /bridge_to_host/HBM/peripheral_aresetn_1 [get_bd_pins bridge_to_host/HBM/HBM/APB_1_PRESET_N]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/HBM/APB_0_PRESET_N] [get_bd_pins proc_sys_reset_0/peripheral_aresetn]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/APB_0_PRESET_N] [get_bd_pins bridge_to_host/HBM/HBM/APB_1_PRESET_N]
#
#
## ignore reset paths for timing -- this doesn't work here, add it as
## constraint?
##set_false_path -from [get_pins -hier -filter NAME=~spmv_design_i/processor_system_reset*/C]
#
#if {0} {
## reduce QDMA
#set_property -dict [list CONFIG.pl_link_cap_max_link_width {X16} CONFIG.pl_link_cap_max_link_speed {2.5_GT/s} CONFIG.axi_data_width {128_bit} CONFIG.axisten_freq {250} CONFIG.coreclk_freq {250} CONFIG.plltype {CPLL} CONFIG.pf0_device_id {901F} CONFIG.pf2_device_id {921F} CONFIG.pf3_device_id {931F} CONFIG.PF0_SRIOV_VF_DEVICE_ID {A03F} CONFIG.PF1_SRIOV_VF_DEVICE_ID {A13F} CONFIG.PF2_SRIOV_VF_DEVICE_ID {A23F} CONFIG.PF3_SRIOV_VF_DEVICE_ID {A33F}] [get_bd_cells bridge_to_host/QDMA/QDMA]
#create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dwidth_converter:2.1 bridge_to_host/axi_dwidth_converter_0
#connect_bd_net [get_bd_pins bridge_to_host/QDMA/aclk] [get_bd_pins bridge_to_host/axi_dwidth_converter_0/s_axi_aclk]
#connect_bd_net [get_bd_pins bridge_to_host/QDMA/aresetn] [get_bd_pins bridge_to_host/axi_dwidth_converter_0/s_axi_aresetn]
#delete_bd_objs [get_bd_intf_nets bridge_to_host/QDMA_M_AXI]
#connect_bd_intf_net -boundary_type upper [get_bd_intf_pins bridge_to_host/QDMA/M_AXI] [get_bd_intf_pins bridge_to_host/axi_dwidth_converter_0/S_AXI]
#connect_bd_intf_net -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA] [get_bd_intf_pins bridge_to_host/axi_dwidth_converter_0/M_AXI]
#set_property -dict [list CONFIG.MI_DATA_WIDTH.VALUE_SRC USER] [get_bd_cells bridge_to_host/axi_dwidth_converter_0]
#set_property -dict [list CONFIG.MI_DATA_WIDTH {512}] [get_bd_cells bridge_to_host/axi_dwidth_converter_0]
#}
#
## change qdma s_axi box name for simplicity
#set_property name S_AXI_15 [get_bd_intf_nets bridge_to_host/QDMA_M_AXI]
#set_property name S_AXI_15 [get_bd_intf_pins bridge_to_host/HBM/S_AXI_QDMA]
#set_property name S_AXI_15 [get_bd_cells /bridge_to_host/HBM/S_AXI_QDMA]
#set_property name S_AXI_QDMA24 [get_bd_intf_nets bridge_to_host/HBM/S_AXI_QDMA]
#
## Remove addinterleavers
#delete_bd_objs [get_bd_nets -regexp bridge_to_host/HBM/S_AXI_.+/HBM_protocol_converter_S_AXI_m_axi_awaddr]
#delete_bd_objs [get_bd_nets -regexp bridge_to_host/HBM/S_AXI_.+/HBM_protocol_converter_S_AXI_m_axi_araddr]
#
##delete_bd_objs [get_bd_nets -regexp bridge_to_host/HBM/S_AXI_.+/bridge_to_host_addrInterleaver_out_awaddr]
##delete_bd_objs [get_bd_nets -regexp bridge_to_host/HBM/S_AXI_.+/bridge_to_host_addrInterleaver_out_araddr]
#
#delete_bd_objs [get_bd_cells -regexp bridge_to_host/HBM/S_AXI_.+/bridge_to_host_addrInterleaver]
#
#delete_bd_objs [get_bd_nets -regexp bridge_to_host/HBM/S_AXI_.+_out_araddr]
#delete_bd_objs [get_bd_nets -regexp bridge_to_host/HBM/S_AXI_.+_out_awaddr]
#delete_bd_objs [get_bd_pins -regexp bridge_to_host/HBM/S_AXI_.+/out_awaddr]
#delete_bd_objs [get_bd_pins -regexp bridge_to_host/HBM/S_AXI_.+/out_araddr]
#
## Remove width converters
#delete_bd_objs [get_bd_intf_nets -regexp bridge_to_host/HBM/S_AXI_.+/S_AXI_1] [get_bd_intf_nets -regexp bridge_to_host/HBM/S_AXI_.+/HBM_data_width_converter_S_AXI_M_AXI] [get_bd_cells -regexp bridge_to_host/HBM/S_AXI_.+/HBM_data_width_converter_S_AXI]
#
## Connect input pins to protocol converter. This code assumes (probably wrong)
## that pairs are retrieved in the same order, so no need to do "manual
## pairing". FIXME
##
#set left_pins [get_bd_intf_pins -regexp bridge_to_host/HBM/S_AXI_.+/S_AXI]
#set right_pins [get_bd_intf_pins -regexp bridge_to_host/HBM/S_AXI_.+/HBM_protocol_converter_S_AXI/S_AXI]
#foreach left $left_pins right $right_pins { connect_bd_intf_net -boundary_type upper $left $right}
#
#
#set max_axi 32
#set smart_connect_on_qdma 0
#for {set i 0; set j 1} {$i < $max_axi} {incr i 2; incr j 2} {
#	set high_slave [get_bd_cells -regexp /bridge_to_host/HBM/S_AXI_$i];
#	set low_slave [get_bd_cells -regexp /bridge_to_host/HBM/S_AXI_$j];
#	set source_item "";
#	set dest_item "";
#	set both_connected 0;
#	if {$high_slave ne "" && $low_slave eq ""} {
#		set source_item $high_slave;
#		set dst_item $j;
#	} elseif {$low_slave ne "" && $high_slave eq ""} {
#		set source_item $low_slave;
#		set dst_item $i;
#	} elseif {$low_slave ne "" && $high_slave ne ""} {
#		set both_connected 1;
#	}
#
#	if {$both_connected eq 1 && $i eq 14 && $j eq 15} {
#		set smart_connect_on_qdma 1
#	}
#
#	if {$high_slave ne "" } {
#		#Rename existing QDMA_x wires/pins
#		set index [expr (($i / 2) + 1)+(16*($i%2))]
#		puts "Index for $i is $index"
#		set_property name S_AXI_$i [get_bd_intf_nets bridge_to_host/HBM/S_AXI_QDMA$index]
#	}
#	if {$low_slave ne "" } {
#		#Rename existing QDMA_x wires/pins
#		set index [expr (($j / 2) + 1)+(16*($j%2))]
#		puts "Index for $j is $index"
#		set_property name S_AXI_$j [get_bd_intf_nets bridge_to_host/HBM/S_AXI_QDMA$index]
#	}
#
#	if {$source_item ne ""} {
#		# copy s_axi_I into s_axi_J (or J into I)
#		puts "would create a new block from $source_item for $dst_item:"
#		set source_name [get_property name $source_item]
#		set new_copy "copia_$source_name"
#		puts "new_copy: $new_copy"
#		set new_name "S_AXI_$dst_item"
#		puts "new_name: $new_name"
#
#		copy_bd_objs -prefix "copia_" /bridge_to_host/HBM  [get_bd_cells $source_item];
#		set_property name $new_name [get_bd_cells /bridge_to_host/HBM/$new_copy]
#		set dst_index $dst_item
#		if {$dst_index < 10} {
#			set dst_index "0$dst_index"
#		}
#
#		# Enable HBM pseudo-channel
#		set_property -dict [list CONFIG.USER_SAXI_$dst_index {true}] [get_bd_cells bridge_to_host/HBM/HBM]
#
#		# Connect pins
#		connect_bd_intf_net -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_$dst_item/M_AXI] [get_bd_intf_pins bridge_to_host/HBM/HBM/SAXI_$dst_index]
#		connect_bd_net [get_bd_pins bridge_to_host/HBM/aclk] [get_bd_pins bridge_to_host/HBM/S_AXI_$dst_item/aclk]
#		connect_bd_net [get_bd_pins bridge_to_host/HBM/peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/S_AXI_$dst_item/peripheral_aresetn]
#		connect_bd_net [get_bd_pins bridge_to_host/HBM/aclk] [get_bd_pins bridge_to_host/HBM/HBM/AXI_${dst_index}_ACLK]
#		connect_bd_net [get_bd_pins bridge_to_host/HBM/peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/HBM/AXI_${dst_index}_ARESET_N]
#	}
#
#	if {$low_slave ne "" || $high_slave ne ""} {
#
#		# Create bonding IP
#		set bonding_ip_name "/bridge_to_host/HBM/axi_channel_bonding_${i}_${j}"
#		puts "bonding ip name: $bonding_ip_name"
#		create_bd_cell -type ip -vlnv bsc.es:axi-tools:axi_channel_bonding:1.0 $bonding_ip_name
#		set_property -dict [list CONFIG.AXI_MASTER_DATA_WIDTH {256} CONFIG.WIDE_BANK_BITS {28} CONFIG.NARROW_BANK_CAPACITY {268435456}] [ get_bd_cells $bonding_ip_name ]
#		set_property -dict [list CONFIG.AXI_ID_WIDTH {4} CONFIG.AXI_ADDR_WIDTH {64}] [ get_bd_cells $bonding_ip_name ]
#		connect_bd_net [get_bd_pins bridge_to_host/HBM/aclk] [get_bd_pins $bonding_ip_name/clk]
#		connect_bd_net [get_bd_pins bridge_to_host/HBM/peripheral_aresetn] [get_bd_pins $bonding_ip_name/rstn]
#
#		# Disconnect slaves and connect to
#		if {$high_slave ne ""} {
#			delete_bd_objs [get_bd_intf_nets bridge_to_host/HBM/S_AXI_$i]
#		}
#		if {$low_slave ne ""} {
#			delete_bd_objs [get_bd_intf_nets bridge_to_host/HBM/S_AXI_$j]
#		}
#		connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_${i}_${j}/m1_axi] -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_${i}/S_AXI]
#		connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_${i}_${j}/m0_axi] -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_${j}/S_AXI]
#
#		# Now connect masters from qdma & accels to wide slave. Two cases: only one
#		# s_axi was being used or both. In the latter case, we need an interconnect 
#		# or smartconnect
#		if {$both_connected eq 0} {
#			#connect_bd_intf_net -boundary_type upper [get_bd_intf_pins $source_item ] [get_bd_intf_pins $bonding_ip_name ]
#			#connect_bd_intf_net -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_2] [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_${i}_${j}/s_axi]
#			connect_bd_intf_net -boundary_type upper [get_bd_intf_pins $source_item] [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_${i}_${j}/s_axi]
#		} else {
#			set sc_name bridge_to_host/HBM/smartconnect_${i}_${j}
#			create_bd_cell -type ip -vlnv xilinx.com:ip:smartconnect:1.0 $sc_name
#			connect_bd_intf_net [get_bd_intf_pins ${sc_name}/M00_AXI] [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_${i}_${j}/s_axi]
#			connect_bd_intf_net -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_${i}] [get_bd_intf_pins ${sc_name}/S00_AXI]
#			connect_bd_intf_net -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_${j}] [get_bd_intf_pins ${sc_name}/S01_AXI]
#			connect_bd_net [get_bd_pins bridge_to_host/HBM/aclk] [get_bd_pins ${sc_name}/aclk]
#			connect_bd_net [get_bd_pins bridge_to_host/HBM/peripheral_aresetn] [get_bd_pins ${sc_name}/aresetn]
#		}
#	}
#}
##for {set i 0} {$i < $max_axi} {incr i } {
##for {set i 0} {$i < 0} {incr i } {
##	set i_idx $i
##	if {$i < 10} {
##		set i_idx "0${i}"
##	}
##	for {set j 0} {$j < 32} {incr j } {
##		set j_idx $j
##		if {$j < 10} {
##			set j_idx "0${j}"
##		}
##		assign_bd_address [get_bd_addr_segs {bridge_to_host/HBM/HBM/SAXI_${i_idx}/HBM_MEM${j_idx} }]
##	}
##}
#
## Disconnect / reconnect & configure addresses
#delete_bd_objs [get_bd_addr_segs -regexp .+b8c.+]
##NO: delete_bd_objs [get_bd_addr_segs bridge_to_host/QDMA/QDMA/M_AXI ]
#delete_bd_objs [get_bd_addr_segs -regexp /bridge_to_host/QDMA.+M_AXI.+HBM.+]
#assign_bd_address
#include_bd_addr_seg [ get_bd_addr_segs -excluded -regexp .+b8c.+ ]
##NO include_bd_addr_seg [ get_bd_addr_segs bridge_to_host/QDMA/QDMA/M_AXI ]
#
## Set correct clock domains for AXI/bonding/smartconnect/HBM on pseudochannels
## 14 & 15, since QDMA is configured @250MHz and our design is @225MHz
#
## Add a second clock to smartconnect, if it exists
#if {$smart_connect_on_qdma eq 1} {
#	set_property -dict [list CONFIG.NUM_CLKS {2}] [get_bd_cells bridge_to_host/HBM/smartconnect_14_15]
#	connect_bd_net [get_bd_pins bridge_to_host/HBM/smartconnect_14_15/aclk1] [get_bd_pins bridge_to_host/QDMA/QDMA/axi_aclk]
#}
#
## Disconnect/connect clocks & reset signals on the rest of the AXI14/15 path
#disconnect_bd_net /bridge_to_host/HBM/aclk_1 [get_bd_pins bridge_to_host/HBM/S_AXI_14/aclk]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/S_AXI_14/aclk]
#
#disconnect_bd_net /bridge_to_host/HBM/aclk_1 [get_bd_pins bridge_to_host/HBM/axi_channel_bonding_14_15/clk]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/axi_channel_bonding_14_15/clk]
#
#disconnect_bd_net /bridge_to_host/HBM/aclk_1 [get_bd_pins bridge_to_host/HBM/HBM/AXI_14_ACLK]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/HBM/AXI_14_ACLK]
#
#disconnect_bd_net /bridge_to_host/HBM/peripheral_aresetn_1 [get_bd_pins bridge_to_host/HBM/HBM/AXI_14_ARESET_N]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/HBM/AXI_14_ARESET_N]
#
#disconnect_bd_net /bridge_to_host/HBM/peripheral_aresetn_1 [get_bd_pins bridge_to_host/HBM/axi_channel_bonding_14_15/rstn]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/axi_channel_bonding_14_15/rstn]
#
#disconnect_bd_net /bridge_to_host/HBM/peripheral_aresetn_1 [get_bd_pins bridge_to_host/HBM/S_AXI_14/peripheral_aresetn]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/S_AXI_14/peripheral_aresetn]
#
#
## Add register slices
##
#for {set i 0} {$i < 32} {incr i} {
#	set s_axi [get_bd_intf_nets S_AXI_${i}_1]
#	if {$s_axi ne ""} {
#		delete_bd_objs [get_bd_intf_nets S_AXI_${i}_1]
#		create_bd_cell -type ip -vlnv xilinx.com:ip:axi_register_slice:2.1 axi_register_slice_${i}
#
#		if {$i eq 0} {
#			connect_bd_intf_net -boundary_type upper [get_bd_intf_pins spmv_b8c_fpga_0/m_axi_mcxx_wrapper_data_V] [get_bd_intf_pins axi_register_slice_${i}/S_AXI]
#		} else {
#			#set ii [expr $i * 2]
#			#set ii [expr $i - 1]
#			set ii [expr (($i / 2) - 1)+(16*($i%2))]
#			puts "for $i is $ii"
#			connect_bd_intf_net -boundary_type upper [get_bd_intf_pins block_spmv_b8c_fpga_${ii}/m_axi_mcxx_wrapper_data_V] [get_bd_intf_pins axi_register_slice_${i}/S_AXI]
#		}
#		connect_bd_net [get_bd_pins axi_register_slice_${i}/aclk] [get_bd_pins clock_generator/clk_out1]
#		connect_bd_net [get_bd_pins axi_register_slice_${i}/aresetn] [get_bd_pins Hardware_Runtime/managed_aresetn]
#		connect_bd_intf_net [get_bd_intf_pins axi_register_slice_${i}/M_AXI] -boundary_type upper [get_bd_intf_pins bridge_to_host/S_AXI_${i}]
#		set_property -dict [list CONFIG.REG_AW {15} CONFIG.REG_AR {15} CONFIG.REG_W {15} CONFIG.REG_R {15} CONFIG.REG_B {15} CONFIG.USE_AUTOPIPELINING {1}] [get_bd_cells axi_register_slice_${i}]
#	}
#}
#if {0} {
#	# QDMA axi register slice
#	create_bd_cell -type ip -vlnv xilinx.com:ip:axi_register_slice:2.1 axi_register_slice_qdma
#	move_bd_cells [get_bd_cells bridge_to_host] [get_bd_cells axi_register_slice_qdma]
#	connect_bd_net [get_bd_pins bridge_to_host/QDMA/aclk] [get_bd_pins bridge_to_host/axi_register_slice_qdma/aclk]
#	connect_bd_net [get_bd_pins bridge_to_host/QDMA/aresetn] [get_bd_pins bridge_to_host/axi_register_slice_qdma/aresetn]
#	delete_bd_objs [get_bd_intf_nets bridge_to_host/S_AXI_15]
#	connect_bd_intf_net [get_bd_intf_pins bridge_to_host/axi_register_slice_qdma/S_AXI] -boundary_type upper [get_bd_intf_pins bridge_to_host/QDMA/M_AXI]
#	connect_bd_intf_net [get_bd_intf_pins bridge_to_host/axi_register_slice_qdma/M_AXI] -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_15]
#	set_property -dict [list CONFIG.REG_AW {15} CONFIG.REG_AR {15} CONFIG.REG_W {15} CONFIG.REG_R {15} CONFIG.REG_B {15} CONFIG.USE_AUTOPIPELINING {1}] [get_bd_cells bridge_to_host/axi_register_slice_qdma]
#}
#
## enable timing optimizations ?
#set_property STEPS.SYNTH_DESIGN.ARGS.RETIMING true [get_runs synth_1]           
#set_property STEPS.POST_ROUTE_PHYS_OPT_DESIGN.IS_ENABLED true [get_runs impl_1]
#
#
## Debugging
#if {0} {
#	set_property HDL_ATTRIBUTE.DEBUG true [get_bd_intf_nets { axi_register_slice_0_M_AXI block_spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V bridge_to_host/HBM/axi_channel_bonding_0_1_m0_axi bridge_to_host/HBM/axi_channel_bonding_14_15_m0_axi bridge_to_host/HBM/axi_channel_bonding_2_3_m0_axi bridge_to_host/HBM/axi_channel_bonding_0_1_m1_axi bridge_to_host/S_AXI_15 spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V bridge_to_host/HBM/axi_channel_bonding_2_3_m1_axi axi_register_slice_2_M_AXI bridge_to_host/HBM/axi_channel_bonding_14_15_m1_axi}]
#	apply_bd_automation -rule xilinx.com:bd_rule:debug -dict [list \
#                                                          [get_bd_intf_nets axi_register_slice_0_M_AXI] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets axi_register_slice_2_M_AXI] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets block_spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_0_1_m0_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_0_1_m1_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_2_3_m0_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_2_3_m1_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_14_15_m0_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/bridge_to_host/QDMA/QDMA/axi_aclk" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_14_15_m1_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/bridge_to_host/QDMA/QDMA/axi_aclk" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/S_AXI_15] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/bridge_to_host/QDMA/QDMA/axi_aclk" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                         ]
#	set_property -dict [list CONFIG.C_DATA_DEPTH {4096}] [get_bd_cells system_ila_0]
#	set_property -dict [list CONFIG.C_DATA_DEPTH {4096}] [get_bd_cells system_ila_1]
#}
#if {0} {
#	set_property HDL_ATTRIBUTE.DEBUG true [get_bd_intf_nets {axi_register_slice_0_M_AXI block_spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V bridge_to_host/HBM/axi_channel_bonding_0_1_m0_axi bridge_to_host/HBM/axi_channel_bonding_14_15_m0_axi bridge_to_host/HBM/axi_channel_bonding_2_3_m0_axi bridge_to_host/HBM/axi_channel_bonding_0_1_m1_axi bridge_to_host/S_AXI_15 spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V bridge_to_host/HBM/axi_channel_bonding_2_3_m1_axi axi_register_slice_2_M_AXI bridge_to_host/HBM/axi_channel_bonding_14_15_m1_axi}]
#	set_property HDL_ATTRIBUTE.DEBUG true [get_bd_intf_nets {axi_register_slice_0_M_AXI block_spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V bridge_to_host/HBM/axi_channel_bonding_0_1_m0_axi bridge_to_host/HBM/axi_channel_bonding_14_15_m0_axi bridge_to_host/HBM/axi_channel_bonding_2_3_m0_axi bridge_to_host/HBM/axi_channel_bonding_0_1_m1_axi bridge_to_host/S_AXI_15 spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V bridge_to_host/HBM/axi_channel_bonding_2_3_m1_axi axi_register_slice_2_M_AXI bridge_to_host/HBM/axi_channel_bonding_14_15_m1_axi}]
#	apply_bd_automation -rule xilinx.com:bd_rule:debug -dict [list \
#                                                          [get_bd_intf_nets axi_register_slice_0_M_AXI] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets axi_register_slice_2_M_AXI] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets block_spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_0_1_m0_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_0_1_m1_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_2_3_m0_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_2_3_m1_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_14_15_m0_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/bridge_to_host/QDMA/QDMA/axi_aclk" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_14_15_m1_axi] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/bridge_to_host/QDMA/QDMA/axi_aclk" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets bridge_to_host/S_AXI_15] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/bridge_to_host/QDMA/QDMA/axi_aclk" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                          [get_bd_intf_nets spmv_b8c_fpga_0_m_axi_mcxx_wrapper_data_V] {AXI_R_ADDRESS "Data and Trigger" AXI_R_DATA "Data and Trigger" AXI_W_ADDRESS "Data and Trigger" AXI_W_DATA "Data and Trigger" AXI_W_RESPONSE "Data and Trigger" CLK_SRC "/clock_generator/clk_out1" SYSTEM_ILA "Auto" APC_EN "0" } \
#                                                         ]
#	set_property -dict [list CONFIG.C_DATA_DEPTH {4096}] [get_bd_cells system_ila_0]
#	set_property -dict [list CONFIG.C_DATA_DEPTH {4096}] [get_bd_cells system_ila_1]
#}
#
#
#create_bd_cell -type ip -vlnv xilinx.com:ip:axi_data_fifo:2.1 bridge_to_host/HBM/axi_data_fifo_0
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/axi_data_fifo_0/aresetn]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/axi_data_fifo_0/aclk]
#delete_bd_objs [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_14_15_m1_axi]
#connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_14_15/m1_axi] [get_bd_intf_pins bridge_to_host/HBM/axi_data_fifo_0/S_AXI]
#connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/axi_data_fifo_0/M_AXI] -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_14/S_AXI]
#
#create_bd_cell -type ip -vlnv xilinx.com:ip:axi_data_fifo:2.1 bridge_to_host/HBM/axi_data_fifo_1
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_aclk] [get_bd_pins bridge_to_host/HBM/axi_data_fifo_1/aclk]
#connect_bd_net [get_bd_pins bridge_to_host/HBM/QDMA_peripheral_aresetn] [get_bd_pins bridge_to_host/HBM/axi_data_fifo_1/aresetn]
#delete_bd_objs [get_bd_intf_nets bridge_to_host/HBM/axi_channel_bonding_14_15_m0_axi]
#connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/axi_data_fifo_1/S_AXI] [get_bd_intf_pins bridge_to_host/HBM/axi_channel_bonding_14_15/m0_axi]
#connect_bd_intf_net [get_bd_intf_pins bridge_to_host/HBM/axi_data_fifo_1/M_AXI] -boundary_type upper [get_bd_intf_pins bridge_to_host/HBM/S_AXI_15/S_AXI]
#
#set_property -dict [list CONFIG.READ_FIFO_DEPTH {32}] [get_bd_cells bridge_to_host/HBM/axi_data_fifo_0]
#set_property -dict [list CONFIG.READ_FIFO_DEPTH {32}] [get_bd_cells bridge_to_host/HBM/axi_data_fifo_1]
#
#
#validate_bd_design
#save_bd_design
#
#endgroup
