rem Open TCP Port 12986 inbound and outbound
netsh advfirewall firewall add rule name="NSPV TCP Port 25435" dir=in action=allow protocol=TCP localport=25435
netsh advfirewall firewall add rule name="NSPV TCP Port 25435" dir=out action=allow protocol=TCP localport=25435
start "" /B nspv.exe %CHAIN%  ^1^> log.txt ^2^>^&^1
PING -n 10 127.0.0.1>nul
start "" /B /wait python.exe -m pytest rpctest\test_nspv.py -s
