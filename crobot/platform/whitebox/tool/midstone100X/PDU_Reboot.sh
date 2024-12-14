#!/usr/local/bin/expect
set port [lindex $argv 0]

# spawn telnet 10.10.10.9
spawn telnet 192.168.0.105
expect "User Name :"
send "apc\r"
expect "Password  :"
send "apc\r"
expect ">"
sleep 1
set timeout -1
send "olReboot $port\r"
expect ">"
sleep 3
send "\r"
expect ">"
