﻿import socket, sys
from struct import *
 
def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8) + (ord(msg[i+1]) )
        s = s + w   
    s = (s>>16) + (s & 0xffff);
    s = ~s & 0xffff
    return s
 
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) +' Message ' + msg[1]
    sys.exit()
 
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
seq = 0

for i in range(1,100):
	packet = '';
	source_ip = '192.168.154.130'
	dest_ip = '192.168.154.128' 
	#ip head
	ihl = 5
	version = 4
	tos = 0
	tot_len = 20 + 20
	id = 54321  
	frag_off = 0
	ttl = 255
	protocol = socket.IPPROTO_TCP
	check = 10  
	daddr = socket.inet_aton(dest_ip)
	saddr =socket.inet_aton(source_ip) 
	ihl_version = (version << 4) + ihl
 	ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
	#tcp head
	source = 1234  
	dest = 80+i   
	seq = i
	ack_seq = 0
	doff = 5    
	fin = 0
	syn = 1
	rst = 0
	psh = 0
	ack = 0
	urg = 0
	window = socket.htons (5840)    
	check = 0
	urg_ptr = 0
	offset_res = (doff << 4) + 0
	tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) +(ack << 4) + (urg << 5)
	tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags,  window, check, urg_ptr)
	#tcp pseudo 
	dest_address = socket.inet_aton(dest_ip)
	source_address = socket.inet_aton(source_ip)
	placeholder = 0
	protocol = socket.IPPROTO_TCP
	tcp_length = len(tcp_header) 
	psh = pack('!4s4sBBH', source_address , dest_address , placeholder , protocol , tcp_length);
	psh = psh + tcp_header; 
	tcp_checksum = checksum(psh)
	tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags,  window, tcp_checksum , urg_ptr)
	packet = ip_header + tcp_header
	s.sendto(packet, (dest_ip , 0))
