#!/usr/local/bin/expect
	
set cfu_path [lindex $argv 0]	
set BMC_ip [lindex $argv 1]
set primary_backup [lindex $argv 2]
set ima_path [lindex $argv 3]
set timeout 300

	spawn $cfu_path -nw -ip $BMC_ip -U admin -P admin -d 1 -mse $primary_backup $ima_path
	expect "Enter your Option :"
	send "y\r"
	expect "Resetting the firmware.........."
	send "echo \"Upgrade by lan was successful\"\r "
	