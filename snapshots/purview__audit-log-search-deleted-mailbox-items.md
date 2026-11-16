# Search the audit log for deleted mailbox items

Use this article to investigate whether a user deleted email items from a mailbox in Exchange Online. It provides step-by-step guidance on checking audit settings, verifying permissions, reviewing retention policies, and searching audit logs in Microsoft Purview. By following the procedure in this article, you can determine if deletion activity occurred and confirm whether the audit data is still available.

Before you start, review the [prerequisites](#before-you-begin) to ensure you have the required permissions, information, and access.

## Before you begin

To complete this procedure, you need:

- The email address of the affected mailbox.
- The license type assigned to the affected mailbox.
- The approximate date and time when the operation occurred.

You must also have access to Exchange Online PowerShell and the [Microsoft Purview portal](purview-portal) with your administrator credentials.

## Check mailbox auditing status

Note

Before searching for audit activity, verify that mailbox auditing is enabled for the affected user.

Complete the following steps to confirm that mailbox auditing is enabled:

1. In Exchange Online PowerShell, run the following command to check the organization-level audit configuration:

   ```
   Get-AdminAuditLogConfig | FL UnifiedAudit*
   ```

   Note

   Run this command in Exchange Online PowerShell. In Security & Compliance PowerShell, the `UnifiedAuditLogIngestionEnabled` property always returns `False`, even when auditing is enabled.
2. Check if mailbox audit logs are disabled at the tenant level:

   ```
   Get-OrganizationConfig | FL AuditDisabled
   ```
3. At the mailbox level, `AuditEnabled` always returns `True`, even if auditing is disabled for a specific mailbox. To verify, use:

   ```
   Get-Mailbox -Filter {AuditEnabled -eq "True"}
   ```

If you receive an error that the mailbox can't be found, auditing is disabled for that mailbox. For more information, see [Verify the auditing status for your organization](audit-log-enable-disable#verify-the-auditing-status-for-your-organization).

## Verify administrator permissions

Ensure that you have the required permissions to search or export audit logs:

1. In the Microsoft Purview portal, go to **Settings** > **Roles and scopes** > **Role groups**.
2. Verify that your account is assigned to the **View-Only Audit Logs** or **Audit Logs** role.
3. In the Exchange admin center, use the **Audit Logs** role to enable or disable auditing and access audit cmdlets. Use the **View-Only Audit Logs** role to grant read-only access to audit logs.

For more information, see [Assign permissions to search the audit log](audit-get-started#step-2-assign-permissions-to-search-the-audit-log).

## Check audit log retention policies

Audit log retention policies determine whether older activities are still available:

1. Determine when the activity occurred.
2. By default, audit logs are retained for 180 days.
3. If the affected user doesn't have an Audit (Premium) license and no audit retention policy is configured, audit logs older than 180 days aren't available.

For more information, see [Get-UnifiedAuditLogRetentionPolicy](/en-us/powershell/module/exchangepowershell/get-unifiedauditlogretentionpolicy).

## Search for deletion activity in Microsoft Purview Audit

When searching for audit data, use filters that match the suspected deletion time and the mailbox deletion activity being investigated.

### Option 1: Search by user and activities

Use this option to search for deletion activity by specifying the mailbox user and relevant audit operations.

- **Date and time range (UTC)**: Specify when the deletion occurred. Audit timestamps are always in UTC.
- **Users**: Enter the affected mailbox.
- **Activities â operation names**: Select Move, MoveToDeletedItems, Create, SoftDelete, and HardDelete.
- **Activities â friendly names**: If available, use the friendly names in the dropdown list.

### Option 2: Search by activities and keywords

Use this option when you want to search by audit activity and identify the mailbox with a keyword such as its SMTP address or ExchangeGUID.

- **Date and time range (UTC)**: Specify when the deletion occurred.
- **Activities â operation names**: Select Move, MoveToDeletedItems, Create, SoftDelete, and HardDelete.
- **Keywords**: Enter the primary SMTP address or ExchangeGUID of the mailbox.

### Option 3: Search by message ID prefix

Use this option if you know the message ID prefix and want to narrow the audit search to a specific message.

- **Date and time range (UTC)**: Specify when the deletion occurred.
- **Keywords**: Enter the prefix of the email messageID.

## Next steps

After you complete your audit log search, use these resources to continue your investigation:

- [Identify who deleted an email message or why an email is missing](audit-log-identify-email-messages): Determine the root cause of deletions, including retention policies, rules, and admin actions.
- [Export, configure, and view audit log records](audit-log-export-records): Export your deletion search results for evidence collection or reporting.
- [Use the MailItemsAccessed audit event to investigate compromised accounts](audit-log-investigate-accounts): Check whether email deletions are linked to a compromised account.
