#!/usr/local/bin/expect
set port [lindex $argv 0]

spawn telnet 10.10.10.9
expect "User Name :"
send "apc\r"
expect "Password  :"
send "apc\r"
expect ">"
sleep 1
set timeout -1
send "olOFF $port\r"
expect ">"
sleep 3
send "\r"
expect ">"
