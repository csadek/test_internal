for /f %%i in ('qwinsta ^| findstr ">rdp-tcp#"') do set RDP_SESSION=%%i
:: Strip the >
set RDP_SESSION=%RDP_SESSION:>=%
tscon %RDP_SESSION% /dest:console
echo y | rwinsta 65536