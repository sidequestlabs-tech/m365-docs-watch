# Identify who modified mailbox rules

This guide explains how to investigate changes to mailbox rules in Exchange Online, including how to view a mailbox's current inbox and forwarding rules and how to search the Microsoft Purview audit log to identify who created, modified, or deleted those rules.

Use these methods to investigate:

- Changes to email forwarding rules
- Rules that cause emails to not appear in expected folders
- Unauthorized rule modifications

## Before you begin

To investigate mailbox rule modifications, you need:

- The *Audit Logs*â¯role assigned in Microsoft Purview
- To connect to Exchange Online PowerShell by using [Connect-ExchangeOnline](/en-us/powershell/module/exchangepowershell/connect-exchangeonline)

## How to identify mailbox rule modifications

Use Get-InboxRule to check current mailbox rules and Search-UnifiedAuditLog to find mailbox rule modifications.

### Check current mailbox rules

The Get-InboxRule output shows:

- **Current rule configuration**: Rule configuration
- **Rule actions**:â¯Move, delete, or forward
- **Rule status**: Enabled or disabled

To see what rules currently exist in a mailbox, run the following command:

```
Get-InboxRule -Mailbox <mailbox> | FL Name,Description,DeleteMessage,MoveToFolder,Enabled
```

### Search for rule modification audit records

The Search-UnifiedAuditLog command looks for:

- **New-InboxRule**: New rules created
- **Set-InboxRule**: Existing rules modified
- **Remove-InboxRule**: Rules deleted

To find out who created, modified, or deleted mailbox rules, run the following command:

```
Search-UnifiedAuditLog -StartDate 01/06/2020 -EndDate 01/20/2020 -UserIds <user1,user2> -Operations New-InboxRule,Set-InboxRule,Remove-InboxRule -ResultSize 1000
```

## What to do when searches return no results

If your audit searches don't find rule modification records:

1. **Expand the date range**â¯to capture older changes:

```
Search-UnifiedAuditLog -StartDate 01/01/2020 -EndDate 03/31/2020 -UserIds <user1,user2> -Operations New-InboxRule,Set-InboxRule,Remove-InboxRule -ResultSize 1000
```

1. **Enable auditing**â¯for future rule changes:

```
Set-Mailbox <mailbox> -AuditEnabled $true -AuditOwner @{Add="Create","Update"}
```

## Quick reference

### Key operations for rule investigation

The following table lists the mailbox rule operations that appear in audit results.

| Operation | Description |
| --- | --- |
| New-InboxRule | New mailbox rule created. |
| Remove-InboxRule | Mailbox rule deleted. |
| Set-InboxRule | Existing mailbox rule modified. |

### Essential commands

The following commands are the primary tools for investigating mailbox rule changes.

| Command | Purpose |
| --- | --- |
| `Get-InboxRule -Mailbox <mailbox>` | Check current rule configuration. |
| `Search-UnifiedAuditLog -Operations New-InboxRule,Set-InboxRule,Remove-InboxRule` | Find who made rule changes. |

## Next steps

- [Use MailItemsAccessed to investigate compromised accounts](audit-log-investigate-accounts): Determine whether unauthorized rule changes indicate a compromised account.
- [Identify who deleted an email message or why an email is missing](audit-log-identify-email-messages): Investigate whether modified rules caused email deletions or missing messages.
- [Export, configure, and view audit log records](audit-log-export-records): Export your rule modification findings for compliance documentation.
