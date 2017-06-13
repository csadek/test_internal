NetSh Advfirewall set allprofiles state off
cd \openssh
powershell.exe -ExecutionPolicy Bypass -File uninstall-sshd.ps1
powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1
net start ssh-agent
net start sshd
sc config sshd start=auto
sc config ssh-agent start=auto
Reg Add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f
Reg Add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d $ecureC0re#13579 /f
shutdown -r -t 10