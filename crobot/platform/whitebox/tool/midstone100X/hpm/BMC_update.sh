#!/usr/local/bin/expect

set BMC_ip [lindex $argv 0]
set File_name [lindex $argv 1]
set timeout 300

	spawn ipmitool -I lanplus -H $BMC_ip -U admin -P admin hpm upgrade $File_name force -z 0x7fff
	expect "Do you wish to continue? (y/n):"
	send "y\r"
	expect "Firmware upgrade procedure successful"
	send "echo \"BMC FW upgrade successful!!\"\r "
