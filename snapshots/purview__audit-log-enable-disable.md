# Turn auditing on or off

Audit logging is on by default for Microsoft 365 organizations. However, when you set up a new Microsoft 365 organization, verify the auditing status for your organization. For instructions, see [Verify the auditing status for your organization](#verify-the-auditing-status-for-your-organization).

When you turn on auditing in the Microsoft Purview portal, the audit log records user and admin activity from your organization and automatically retains it for 180 days. The retention (lifetime) for audit data starts when it's added to the auditing log and is retained based on [audit log retention policies](audit-log-retention-policies) and the license assigned to users.

Important

Auditing isn't enabled by default for [Small and Medium Business (SMB) licenses](https://adoption.microsoft.com/small-and-medium-business/), including Microsoft 365 Business Basic, Business Standard, and Business Premium. Additionally, unmanaged tenants that use free trials of enterprise licenses don't have auditing enabled by default. In both these cases, you must manually enable auditing for your organization.

Changes to the user licensing or retention policies also change the expiration date of audit data.

Your organization might have reasons for not wanting to record and retain audit log data. In these cases, a global admin can turn off auditing in Microsoft 365 for your organization. For instructions, see [Turn off auditing](#turn-off-auditing).

Important

If you turn off auditing in Microsoft 365, you can't use the [Office 365 Management Activity API](/en-us/office/office-365-management-api/office-365-management-activity-api-reference) or [Microsoft Sentinel](/en-us/azure/sentinel/overview) to access auditing data or logs for your organization. When you turn off auditing, searches of the audit log in Microsoft Purview return no results. Running the **Search-UnifiedAuditLog** cmdlet in Exchange Online PowerShell also returns no results.

## Before you turn auditing on or off

You must be assigned the *Audit Logs* role in Exchange Online to turn auditing on or off. By default, the *Compliance Management* and *Organization Management* role groups on the **Permissions** page in the Exchange admin center have this role.

- For step-by-step instructions on searching the audit log, see [Search the audit log](audit-search).
- For more information about the Microsoft 365 Management Activity API, see [Get started with Microsoft 365 Management APIs](/en-us/office/office-365-management-api/get-started-with-office-365-management-apis).

## Verify the auditing status for your organization

To verify that auditing is turned on for your organization, run the following command in [Exchange Online PowerShell](/en-us/powershell/exchange/connect-to-exchange-online-powershell):

```
Get-AdminAuditLogConfig | Format-List UnifiedAuditLogIngestionEnabled
```

A value of `True` for the *UnifiedAuditLogIngestionEnabled* property indicates that auditing is turned on. A value of `False` indicates that auditing isn't turned on.

Important

Be sure to run the previous command in Exchange Online PowerShell. Although the **Get-AdminAuditLogConfig** cmdlet is also available in Security & Compliance PowerShell, the *UnifiedAuditLogIngestionEnabled* property is always `False`, even when auditing is turned on.

## Turn on auditing

If auditing isn't turned on for your organization, turn it on in the Microsoft Purview portal or by using Exchange Online PowerShell. Audit events might take several hours after you turn on auditing before they become searchable in the audit log.

Complete the following steps to turn on auditing:

1. Sign in to the [Microsoft Purview portal](https://purview.microsoft.com).
2. Select the **Audit** solution card. If the **Audit** solution card isn't displayed, select **View all solutions** and then select **Audit** from the **Core** section.
3. If auditing isn't turned on for your organization, a banner is displayed prompting you to start recording user and admin activity.
4. Select the **Start recording user and admin activity** banner.

Enabling auditing might take up to 60 minutes to take effect.

### Use PowerShell to turn on auditing

Complete the following steps to turn on auditing by using Exchange Online PowerShell:

1. [Connect to Exchange Online PowerShell](/en-us/powershell/exchange/connect-to-exchange-online-powershell).
2. Run the following PowerShell command to turn on auditing.

   ```
   Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true
   ```

   A message is displayed saying that enabling auditing might take up to 60 minutes to take effect.

## Turn off auditing

Use Exchange Online PowerShell to turn off auditing.

1. [Connect to Exchange Online PowerShell](/en-us/powershell/exchange/connect-to-exchange-online-powershell).
2. Run the following PowerShell command to turn off auditing.

   ```
   Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $false
   ```
3. After a while, verify that auditing is turned off (disabled). You can do this in two ways:

   - In Exchange Online PowerShell, run the following command:

     ```
     Get-AdminAuditLogConfig | FL UnifiedAuditLogIngestionEnabled
     ```

     The value of `False` for the *UnifiedAuditLogIngestionEnabled* property indicates that auditing is turned off.
   - Go to the **Audit** page in the Microsoft Purview portal.

     If auditing isn't turned on for your organization, a banner prompts you to start recording user and admin activity.

## Audit records when auditing status is changed

Your organization audits changes to the auditing status. Audit records are logged when auditing is turned on or turned off. You can search the Exchange admin audit log for these audit records.

To search the Exchange admin audit log for audit records that are generated when turning auditing on or off, run the following command in [Exchange Online PowerShell](/en-us/powershell/exchange/connect-to-exchange-online-powershell):

```
Search-UnifiedAuditLog -Operations Set-AdminAuditLogConfig
```

Audit records for turning auditing on or off contain information about when the auditing status was changed, the admin who changed it, and the IP address of the computer that was used to make the change. The following screenshots show audit records that correspond to changing the auditing status in your organization.

### Audit record for Set-AdminAuditLogConfig

![Screenshot of an audit record showing that auditing settings were changed.](media/auditadminenableanddisable.png)

Look for the result value of `UnifiedAuditLogIngestionEnabled` in the *AuditData* property. The `UnifiedAuditLogIngestionEnabled` value indicates whether unified audit logging was turned on or off in the Microsoft Purview portal or by running the **Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true/false** cmdlet.

For more information about searching the Exchange admin audit log, see [Search-UnifiedAuditLog](/en-us/powershell/module/exchange/search-unifiedauditlog).

## Next steps

- [Get started with auditing solutions](audit-get-started): Complete the remaining setup steps after enabling auditing, including permissions and retention policies.
- [Search the audit log](audit-search): Start searching for user and admin activities now that auditing is turned on.
- [Manage mailbox auditing](audit-mailboxes): Verify and customize which mailbox actions are audited in your organization.
