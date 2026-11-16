# Connect to Security & Compliance PowerShell

This article contains instructions for how to connect to Security & Compliance PowerShell using the Exchange Online PowerShell module with or without multifactor authentication (MFA).

The Exchange Online PowerShell module uses modern authentication for connecting to Exchange Online PowerShell and Security & Compliance PowerShell. For more information about the Exchange Online PowerShell module, see [About the Exchange Online PowerShell module](exchange-online-powershell-v2?view=exchange-ps).

To connect to Security & Compliance PowerShell for automation, see [App-only authentication for unattended scripts](app-only-auth-powershell-v2?view=exchange-ps).

## What do you need to know before you begin?

- The requirements for installing and using the module are described in [Prerequisites for the Exchange Online PowerShell module](exchange-online-powershell-v2?view=exchange-ps#prerequisites-for-the-exchange-online-powershell-module) and [Supported operating systems for the Exchange Online PowerShell module](exchange-online-powershell-v2?view=exchange-ps#supported-operating-systems-for-the-exchange-online-powershell-module).
- After you connect, role-based access control (RBAC) controls the cmdlets and parameters that you have or don't have access to. For more information, see [Permissions in the Microsoft Defender portal](/en-us/defender-office-365/mdo-portal-permissions) and [Permissions in the Microsoft Purview portal](/en-us/purview/purview-permissions).

## Step 1: Load the Exchange Online PowerShell module

Note

If the module is already installed, you can typically skip this step and run **Connect-IPPSSession** without manually loading the module first.

After you [install the module](exchange-online-powershell-v2?view=exchange-ps#install-and-update-the-exchange-online-powershell-module), open a PowerShell window and load the module by running the following command:

```
Import-Module ExchangeOnlineManagement
```

## Step 2: Connect and authenticate

Note

- Connect commands likely fail if the profile path of the account that you used to connect contains special PowerShell characters (for example, `$`). The workaround is to connect using a different account that doesn't have special characters in the profile path.
- If you plan on running eDiscovery cmdlets (**\*-ComplianceSearch** or **New-ComplianceSearchAction**), the connection must meet the following requirements:

  - Version 3.9.0 (August 2025) or later of the Exchange Online PowerShell module.
  - The connect command must include the *EnableSearchOnlySession* switch.

    If your Security & Compliance PowerShell connection doesn't meet these requirements, you receive the following error when you try to run eDiscovery cmdlets:

    `Please close the current PowerShell session and open a new session using Connect-IPPSSession with the -EnableSearchOnlySession flag. This requires using ExchangeOnlineManagement v3.9.0 or higher.`

    The minimum module version 3.9.0 described in this section applies to connections that use interactive sign-in. App-only authentication for eDiscovery cmdlets is unsupported. For existing app-only automations that continue to use this configuration, use module version 3.10.1 or later, include the *EnableSearchOnlySession* switch, and follow the best-effort guidance in [Configure app-only authentication for eDiscovery PowerShell](/en-us/purview/edisc-permissions#configure-app-only-authentication-for-ediscovery-powershell).

The command that you need to run uses the following syntax:

```
Connect-IPPSSession -UserPrincipalName <UPN> [-ConnectionUri <URL>] [-AzureADAuthorizationEndpointUri <URL>] [-DelegatedOrganization <String>] [-PSSessionOption $ProxyOptions] [-EnableSearchOnlySession]
```

For detailed syntax and parameter information, see [Connect-IPPSSession](/en-us/powershell/module/exchangepowershell/connect-ippssession).

- *<UPN>* is your account in user principal name format (for example, `navin@contoso.onmicrosoft.com`).
- The required *ConnectionUri* and *AzureADAuthorizationEndpointUri* values depend on the nature of your Microsoft 365 organization. Common values are described in the following list:

  - **Microsoft 365 or Microsoft 365 GCC**:
    - *ConnectionUri*: None. The required value `https://ps.compliance.protection.outlook.com/powershell-liveid/` is also the default value, so you don't need to use the *ConnectionUri* parameter in Microsoft 365 or Microsoft 365 GCC environments.
    - *AzureADAuthorizationEndpointUri*: None. The required value `https://login.microsoftonline.com/organizations`, but it is also the default value, so you don't need to use the *AzureADAuthorizationEndpointUri* parameter in Microsoft 365 or Microsoft 365 GCC environments.
  - **Microsoft 365 GCC High**:
    - *ConnectionUri*: `https://ps.compliance.protection.office365.us/powershell-liveid/`
    - *AzureADAuthorizationEndpointUri*: `https://login.microsoftonline.us/organizations`\*
  - **Microsoft 365 DoD**:
    - *ConnectionUri*: `https://l5.ps.compliance.protection.office365.us/powershell-liveid/`
    - *AzureADAuthorizationEndpointUri*: `https://login.microsoftonline.us/organizations`\*
  - **Office 365 operated by 21Vianet**:
    - *ConnectionUri*: `https://ps.compliance.protection.partner.outlook.cn/powershell-liveid`
    - *AzureADAuthorizationEndpointUri*: `https://login.chinacloudapi.cn/organizations`\*

  \* The *AzureADAuthorizationEndpointUri* value ending in `/organizations` allows only work or school accounts. The older URI value ending in `/common` still works, but might prompt you to choose between a personal account and a work or school account. We recommend the `/organizations` URI value in enterprise scenarios where consumer accounts should be excluded.
- If you're behind a proxy server, you can use the *PSSessionOption* parameter in the connection command. First, run this command: `$ProxyOptions = New-PSSessionOption -ProxyAccessType <Value>`, where <Value> is `IEConfig`, `WinHttpConfig`, or `AutoDetect`. Then, use the value `$ProxyOptions` for the *PSSessionOption* parameter. For more information, see [New-PSSessionOption](/en-us/powershell/module/microsoft.powershell.core/new-pssessionoption).
- Depending on the nature of your organization, you might be able to omit the *UserPrincipalName* parameter in the next step. Instead, you enter the username and password or select stored credentials after you run the **Connect-IPPSSession** command. If it doesn't work, then you need to use the *UserPrincipalName* parameter.
- If you aren't using MFA, you should be able to use the *Credential* parameter instead of the *UserPrincipalName* parameter. First, run the command `$Credential = Get-Credential`, enter your username and password, and then use the variable name for the *Credential* parameter (`-Credential $Credential`). If it doesn't work, then you need to use the *UserPrincipalName* parameter.

### Connect to Security & Compliance PowerShell with an interactive sign in prompt

1. The following examples work in Windows PowerShell 5.1 and PowerShell 7 for accounts with or without MFA:

   - **This example connects to Security & Compliance PowerShell in a Microsoft 365 or Microsoft 365 GCC organization**:

     ```
     Connect-IPPSSession -UserPrincipalName navin@contoso.onmicrosoft.com
     ```
   - **This example connects to Security & Compliance PowerShell in a Microsoft GCC High organization**:

     ```
     Connect-IPPSSession -UserPrincipalName chris@govt.us -ConnectionUri https://ps.compliance.protection.office365.us/powershell-liveid/ -AzureADAuthorizationEndpointUri https://login.microsoftonline.us/organizations
     ```
   - **This example connects to Security & Compliance PowerShell in a Microsoft 365 DoD organization**:

     ```
     Connect-IPPSSession -UserPrincipalName michelle@govt.mil -ConnectionUri https://l5.ps.compliance.protection.office365.us/powershell-liveid/ -AzureADAuthorizationEndpointUri https://login.microsoftonline.us/organizations
     ```
   - **This example connects to Security & Compliance PowerShell in an Office 365 operated by 21Vianet organization**:

     ```
     Connect-IPPSSession -UserPrincipalName li@fabrikam.cn -ConnectionUri https://ps.compliance.protection.partner.outlook.cn/powershell-liveid -AzureADAuthorizationEndpointUri https://login.chinacloudapi.cn/organizations
     ```
2. In the sign-in window that opens, enter your password, and then select **Sign in**.

   ![Enter your password in the Sign in to your account window.](../docs-conceptual/media/connect-exo-password-prompt.png?view=exchange-ps)

   Note

   In PowerShell 7, browser-based single sign-on (SSO) is used by default, so the sign in prompt opens in your default web browser instead of a standalone dialog.
3. **MFA only**: A verification code is generated and delivered based on the response option configured for your account (for example, a text message or the Microsoft Authenticator app on your device).

   In the verification window that opens, enter the verification code, and then select **Verify**.

   ![Enter your verification code in the Sign in to your account window.](../docs-conceptual/media/connect-exo-mfa-verify-prompt.png?view=exchange-ps)

### Connect to Security & Compliance PowerShell without a sign in prompt (unattended scripts)

For complete instructions, see [App-only authentication for unattended scripts in Exchange Online PowerShell and Security & Compliance PowerShell](app-only-auth-powershell-v2?view=exchange-ps).

### Connect to Security & Compliance PowerShell in customer organizations

The procedures in this section require version 3.0.0 or later of the module.

In Security & Compliance PowerShell, you need to use the *AzureADAuthorizationEndpointUri* with the *DelegatedOrganization* parameter.

For more information, about partners and customer organizations, see the following articles:

- [What is the Cloud Solution Provider (CSP) program?](/en-us/partner-center/csp-overview).
- [Introduction to granular delegated admin privileges (GDAP)](/en-us/partner-center/gdap-introduction)

This example connects to customer organizations in the following scenarios:

- Connect to a customer organization using a CSP account.
- Connect to a customer organization using a GDAP.
- Connect to a customer organization as a guest.

  ```
  Connect-IPPSSession -UserPrincipalName navin@contoso.onmicrosoft.com -DelegatedOrganization adatum.onmicrosoft.com -AzureADAuthorizationEndpointUri https://login.microsoftonline.com/adatum.onmicrosoft.com
  ```

## Step 3: Disconnect when you're finished

Be sure to disconnect the session when you're finished. If you close the PowerShell window without disconnecting the session, you could use up all the sessions available to you, and you need to wait for the sessions to expire. To disconnect the session, run the following command:

```
Disconnect-ExchangeOnline
```

To silently disconnect without a confirmation prompt, run the following command:

```
Disconnect-ExchangeOnline -Confirm:$false
```

Note

The disconnect command likely fails if the profile path of the account that you used to connect contains special PowerShell characters (for example, `$`). The workaround is to connect using a different account that doesn't have special characters in the profile path.

## How do you know you connected successfully?

The Security & Compliance PowerShell cmdlets are imported into your local Windows PowerShell session and tracked by a progress bar. If you don't receive any errors, you connected successfully. A quick test is to run a Security & Compliance PowerShell cmdlet, for example, **Get-RetentionCompliancePolicy**, and see the results.

If you receive errors, check the following requirements:

- A common problem is an incorrect password. Run the three steps again and pay close attention to the username and password that you use.
- The account that you use to connect must be enabled for PowerShell. For more information, see [Enable or disable access to Exchange Online PowerShell](disable-access-to-exchange-online-powershell?view=exchange-ps).
- TCP port 80 traffic needs to be open between your local computer and Microsoft 365. It's probably open, but it's something to consider if your organization has a restrictive internet access policy.
- REST-based connections to Security & Compliance PowerShell require the PowerShellGet module. By dependency, the PowerShellGet module requires the PackageManagement module. You get errors if you try to connect without having both modules installed. For example, you might see the following error:

  > The term 'Update-ModuleManifest' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.

  For more information about the PowerShellGet and PackageManagement module requirements, see [PowerShellGet for REST-based connections in Windows](exchange-online-powershell-v2?view=exchange-ps#powershellget-for-rest-api-connections-in-windows).
- You might fail to connect if your client IP address changes during the connection request. The failure occurs if your organization uses a source network address translation (SNAT) pool with multiple IP addresses. The connection error looks like this:

  > The request for the Windows Remote Shell with ShellId <ID> failed because the shell was not found on the server. Possible causes are: the specified ShellId is incorrect or the shell no longer exists on the server. Provide the correct ShellId or create a new shell and retry the operation.

  To fix the issue, do either of the following steps:

  - Use an SNAT pool that contains a single IP address.
  - Force the use of a specific IP address for connections to the Security & Compliance PowerShell endpoint.
