# Search the audit log for specific email messages

Use this article to search the Microsoft Purview audit log for specific email messages that are missing, moved, or need investigation. It shows practical Exchange Online PowerShell searches and investigation steps you can use when standard audit searches don't return the records you expect.

Use these methods to investigate:

- Email migration issues
- Messages moved between folders
- Email access patterns
- Missing email items

## Before you begin

To search audit logs for specific email items, you need:

- The *Audit Logs* role assigned in Microsoft Purview
- To connect to Exchange Online PowerShell by using [Connect-ExchangeOnline](/en-us/powershell/module/exchangepowershell/connect-exchangeonline)

## Search for specific email messages

Use these methods to find audit records for specific email messages. Select the method based on what information you have about the email you're looking for.

### Search by email subject or keywords

Use the FreeText parameter to search for:

- Email subject lines
- Keywords from email content
- Sender names
- Any identifying text from the email

To search for audit records by using email subjects, keywords, or other identifying information, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -FreeText "<subject or keyword>" -ResultSize 1000
```

### Search for moved emails

To search for Move and MoveToDeletedItems operations in a mailbox, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations Move,MoveToDeletedItems -ResultSize 1000
```

Important

The audit feature for move operations isn't enabled by default.

### Search all email activities

To search for all email-related activities in a mailbox, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations Send,Create,Move,SoftDelete,HardDelete,MailItemsAccessed -ResultSize 1000
```

## What to do when searches return no result

If your audit log searches don't find the email records you're looking for, try these investigation steps.

### Missing emails after migration

Use the following steps to investigate missing emails after migration when searches return no results.

1. Check if auditing was enabled before the migration occurred.

```
Get-Mailbox <mailbox> | Select AuditEnabled,WhenCreated
```

1. Expand the search date range to cover a broader timeframe.

```
Search-UnifiedAuditLog -StartDate 01/01/2020 -EndDate 03/31/2020 -ObjectIds <mailbox> -ResultSize 1000
```

### Emails moved but no audit records found

Use the following steps to investigate when users move emails but you can't find audit records.

1. Check if auditing is configured for move operations.

```
Get-Mailbox <mailbox> | Select AuditOwner
```

1. Enable auditing for move operations if it's not configured.

```
Set-Mailbox <mailbox> -AuditOwner @{Add="Move","MoveToDeletedItems","SoftDelete","HardDelete"}
```

1. Search using additional operation types that might capture the activity.

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -ObjectIds <mailbox> -Operations Move,MoveToDeletedItems,Update -ResultSize 1000
```

## Locating specific email messages

The following steps help you investigate when you can't find audit records for specific email messages.

1. Search by subject or keywords

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -FreeText "<subject or keyword>" -ResultSize 1000 | FL
```

1. Search by user

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <sender> -ResultSize 1000 | FL
```

## Advanced investigation procedures

The following procedures help you resolve issues when standard investigation steps don't resolve the issue.

### Enable comprehensive mailbox auditing

To enable all relevant audit actions and ensure future activities are captured, run the following command:

```
Set-Mailbox <mailbox> -AuditEnabled $true -AuditOwner @{Add="Move","MoveToDeletedItems","SoftDelete","HardDelete","Create"} -AuditDelegate @{Add="SendAs","Move"}
```

### Verify organization-wide audit configuration

To ensure that auditing is enabled at the organization level, run the following command:

```
Set-OrganizationConfig -AuditDisabled $false
```

## Quick reference

### Search parameters

Use these key parameters to search audit logs for specific email items:

| Parameter | Description | Example |
| --- | --- | --- |
| -FreeText | Search for specific email identifiers | `<email subject or unique identifier>` |
| -Operations | Filter by deletion activity types | SoftDelete,HardDelete,MoveToDeletedItems |
| -ResultSize | Number of results to return | 1,000 (standard), 5,000 (comprehensive) |
| -StartDate/-EndDate | Define investigation timeframe | Based on when emails went missing |
| -UserIds | Filter by who performed the action | `<user1@domain.com,user2@domain.com>` |

## Next steps

- [Identify who deleted an email message or why an email is missing](audit-log-identify-email-messages): Investigate deletion causes if your search reveals missing or deleted messages.
- [Search the audit log for deleted mailbox items](audit-log-search-deleted-mailbox-items): Narrow your search to deleted items using deletion-specific operations and filters.
- [Export, configure, and view audit log records](audit-log-export-records): Export your email search results for detailed review or reporting.
