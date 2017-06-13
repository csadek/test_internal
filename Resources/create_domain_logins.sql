-- This Script needs to be executed after a domain is created on the machine.

-- Functionality:
-- 1) Creates an admin login for 'DomainName\AlarisAdmin' domain account.
-- 2) Gives the created login a 'sysadmin' server role.

-- Usage:
-- This script can be called from a batch file. Example:
-- -- Batch file content:
-- -- -- sqlcmd -i create_domain_logins.sql -v Domain_Name = %1 -o %2
-- -- Executing the batch file:
-- -- -- CallSqlScript.cmd M2Automation E:\SQLLogs\create_domain_logins_log.txt
-- This script can be also called from cmd directly. Example:
-- -- sqlcmd -i create_domain_logins.sql -v Domain_Name = M2Automation -o %2

-----------------------------------------------------------------------------------------------------------

-- Try to create the login. Nothing happens if the login is already created.
BEGIN TRY
	-- Create 'AlarisAdmin' Login
	create login [$(Domain_Name)\AlarisAdmin] from windows;
END TRY
BEGIN CATCH
--Nothing
END CATCH
GO

-- Create 'smautouser' Login
create login smautouser with password = 'password_123456';
GO

-- After the login is created, the server role of 'sysadmin' is assigned.
sp_addsrvrolemember '$(Domain_Name)\AlarisAdmin', 'sysadmin';
GO
sp_addsrvrolemember 'smautouser', 'sysadmin';
GO

