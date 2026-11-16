# Identify who deleted an email message or why an email is missing

Use this article to investigate missing email messages in Exchange Online and identify who deleted them. It guides administrators through using the Microsoft Purview audit log and Exchange Online PowerShell to locate deletion events, analyze mailbox configurations, check retention and migration activity, and determine whether mailbox rules or shared-mailbox access caused the loss.

Use these methods to investigate:

- Emails deleted by users or administrators
- Missing emails after migration or sync issues
- Emails removed by mailbox rules or retention policies
- Deleted emails from shared mailboxes
- Emails not appearing in expected folders

## Before you begin

To investigate deleted emails and missing messages, you need:

- The *Audit Logs*â¯role assigned in Microsoft Purview
- To connect to Exchange Online PowerShell by using [Connect-ExchangeOnline](/en-us/powershell/module/exchangepowershell/connect-exchangeonline)

## How to identify deleted emails

Use the following methods to investigate missing emails and identify deletion activities. Choose the method based on the type of deletion you're investigating.

### Search for deleted emails by operation type

Use this method to search for the following operations:

- **SoftDelete**: Items moved to Deleted Items folder.
- **HardDelete**: Items permanently removed from mailbox.
- **MoveToDeletedItems**: Items moved to Deleted Items folder by user action.

To search for audit records of email deletions by using specific deletion operations, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations SoftDelete,HardDelete,MoveToDeletedItems -ResultSize 1000
```

Replaceâ¯`<user1,user2>`â¯with user email addresses. Specify multiple users by separating user names with commas.

### Search for shared mailbox deletions

To investigate deletions from shared mailboxes, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -FreeText <sharedmailbox@domain.com> -Operations SoftDelete,HardDelete,MoveToDeletedItems -ResultSize 1000
```

Note

Shared mailbox auditing might not be enabled by default. If this search returns no results, seeâ¯Shared mailbox auditing not configuredâ¯to enable auditing.

### Search for missing emails by using keywords

This method helps identify deletion records for emails with specific subjects or content.

To search for audit records related to specific missing emails, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -FreeText "<email subject or keyword>" -Operations SoftDelete,HardDelete,MoveToDeletedItems -ResultSize 1000
```

### Search for comprehensive email activities

This broader search includes moves and updates that might explain missing emails.

To search for all activities that affect email visibility, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations SoftDelete,HardDelete,MoveToDeletedItems,Move,Update,Create -ResultSize 1000
```

## Understanding search results

Getting no results from audit searches can provide important insights about what didn't cause the missing emails:

- **Deletion operations not found**: Rules out user-initiated deletions during the timeframe.
- **No retention policy actions**: Indicates automated policies didn't delete the emails.
- **No migration activities**: Shows migration processes didn't remove the emails.
- **No administrator actions**: Confirms admins didn't perform bulk operations.

Note

Document which searches return no results. This information helps narrow down the root cause by eliminating potential causes.

## Missing search results

If your audit log searches don't find deletion records for missing emails, try the following steps.

### Missing emails with no deletion audit records

Use the following steps to investigate when emails are missing but no deletion audit records are found.

1. Check if auditing was enabled when the deletion occurred.

   ```
   Get-Mailbox <mailbox> | Select AuditEnabled,AuditOwner,AuditDelegate,WhenCreated
   ```
2. Enable comprehensive auditing for future monitoring.

   ```
   Set-Mailbox <mailbox> -AuditEnabled $true -AuditOwner @{Add="SoftDelete","HardDelete","MoveToDeletedItems","Move","Create","Update"}
   ```
3. Search for retention policy actions that might remove emails.

   ```
   Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations TaggedAsRecord,ApplyRetentionTag -ResultSize 1000
   ```

   If this command returns no results, it indicates that retention policies didn't automatically delete emails during the specified timeframe. This information helps you rule out automated policy-based deletions as the cause of missing emails.

### Shared mailbox auditing not configured

Use the following steps to enable auditing for shared mailboxes when deletion records aren't found.

1. Check the current auditing configuration for the shared mailbox.

   ```
   Get-Mailbox <sharedmailbox> | Select AuditEnabled,AuditOwner,AuditDelegate,AuditAdmin
   ```
2. Enable comprehensive auditing for the shared mailbox.

   ```
   Set-Mailbox <sharedmailbox> -AuditEnabled $true -AuditOwner @{Add="SoftDelete","HardDelete","MoveToDeletedItems"} -AuditDelegate @{Add="SoftDelete","HardDelete","MoveToDeletedItems","SendAs","Move"}
   ```
3. Search for activities by users with shared mailbox access.

   ```
   Get-MailboxPermission <sharedmailbox> | Where {$_.User -ne "NT AUTHORITY\SELF"} | ForEach {
       Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds $_.User -Operations SoftDelete,HardDelete -ResultSize 100 }
   ```

### Migration-related email loss investigation

The following steps show how to investigate emails lost during migration processes.

1. Search for migration-related activities during the migration timeframe.

   ```
   Search-UnifiedAuditLog -StartDate <migration_start_date> -EndDate <migration_end_date> -UserIds <user1,user2> -FreeText "<migration subject or keyword>" -ResultSize 1000
   ```

## Advanced investigation procedures

The following procedures show how to perform detailed analysis when standard searches don't reveal the cause of missing emails.

### Analyze mailbox rules that might delete emails

If you suspect that mailbox rules are causing emails to be deleted or moved to unexpected folders, use the following dedicated mailbox rule investigation procedures.

Tip

For comprehensive mailbox rule investigation, seeâ¯[Identify who modified mailbox rules](audit-log-identify-mailbox-rules) for detailed guidance on identifying who created, modified, or deleted mailbox rules that might affect email delivery.

### Investigate retention and compliance policies

To check if compliance policies are causing email deletion, run the following commands:

1. Check retention policies applied to the mailbox.

   ```
   Get-Mailbox <mailbox> | Select RetentionPolicy,LitigationHoldEnabled,RetainDeletedItemsFor
   ```
2. Search for compliance-related deletions.

   ```
   Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations ComplianceSettingChanged,RetentionPolicyApplied -ResultSize 1000
   ```

### Check for administrator actions

To check if administrators performed actions that affected emails, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations Remove-MailboxFolderPermission,Set-Mailbox,New-MailboxExportRequest,New-MailboxImportRequest -ResultSize 1000
```

## Quick reference

### Key operations for investigating deletions

The following table lists the key audit operations to use when investigating deleted or missing emails.

| Operation | Description | Use Case |
| --- | --- | --- |
| ApplyRetentionTag | Retention policy applied to items | Automated policy actions |
| HardDelete | Items permanently removed from mailbox | Permanent deletions, second-level investigation |
| Move | Items moved between folders | Investigate folder changes |
| MoveToDeletedItems | Items moved to Deleted Items by user action | User-initiated moves to deleted items |
| SoftDelete | Items moved to Deleted Items folder | User deletions, first-level investigation |
| TaggedAsRecord | Items marked for retention | Compliance-related actions |

### Search parameters for investigating deletions

The following table describes the main `Search-UnifiedAuditLog` parameters used in these investigations.

| Parameter | Description | Example |
| --- | --- | --- |
| -FreeText | Search for specific email identifiers | `<email subject or unique identifier>` |
| -Operations | Filter by deletion activity types | SoftDelete,HardDelete,MoveToDeletedItems |
| -ResultSize | Number of results to return | 1,000 (standard), 5,000 (comprehensive) |
| -StartDate/-EndDate | Define investigation timeframe | Based on when emails went missing |
| -UserIds | Filter by who performed the action | `<user1@domain.com,user2@domain.com>` |

## Next steps

- [Use MailItemsAccessed to investigate compromised accounts](audit-log-investigate-accounts): Investigate whether deletions are part of a broader account compromise.
- [Identify who modified mailbox rules](audit-log-identify-mailbox-rules): Check whether mailbox rules are auto-deleting or forwarding messages.
- [Export, configure, and view audit log records](audit-log-export-records): Export your investigation results for reporting or evidence preservation.
