# M365 DFIR Watch List — Starter Draft (wide net)

Drafted 2026-11-15. Every URL below was checked and returns a live page.
**How to use:** strike through (`~~ ~~`) or delete anything you don't care about. Add notes inline.

Legend: ⭐ = core, I'd keep it no matter what · ◽ = useful, cut if you want less noise

---

## 1. Purview Audit — the unified audit log (UAL) (20)
The single most important log source in M365 investigations. Changes here (retention, licensing, new events, search limits) directly change what you can prove.

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Learn about auditing solutions](https://learn.microsoft.com/en-us/purview/audit-solutions-overview) | States Standard vs Premium differences and **default retention**. This is the page where a 90→180-day change shows up. |
| ⭐ | [Get started with auditing](https://learn.microsoft.com/en-us/purview/audit-get-started) | Licensing and setup requirements. Tells you if auditing was even on for the tenant. |
| ⭐ | [Turn auditing on or off](https://learn.microsoft.com/en-us/purview/audit-log-enable-disable) | How to check whether auditing was disabled. An attacker turning it off is itself evidence. |
| ⭐ | [Search the audit log](https://learn.microsoft.com/en-us/purview/audit-search) | The portal search: limits, how long results are kept, how many rows you can get. |
| ⭐ | [Export, configure, and view audit log records](https://learn.microsoft.com/en-us/purview/audit-log-export-records) | CSV export from the portal and how to unpack the `AuditData` JSON column. This is your "CSV export vs PowerShell" question. |
| ⭐ | [Use a PowerShell script to search the audit log](https://learn.microsoft.com/en-us/purview/audit-log-search-script) | Microsoft's own script for pulling large volumes past the portal limits. |
| ⭐ | [Manage audit log retention policies](https://learn.microsoft.com/en-us/purview/audit-log-retention-policies) | Custom retention (up to 10 years with add-ons). Changes here affect how far back you can look. |
| ⭐ | [Manage mailbox auditing](https://learn.microsoft.com/en-us/purview/audit-mailboxes) | Which mailbox actions are logged by default per license, including MailItemsAccessed. Critical for "did they read the email?" |
| ⭐ | [Audit log activities](https://learn.microsoft.com/en-us/purview/audit-log-activities) | The master list of every operation name. New operations appear here first. |
| ⭐ | [Detailed properties in the audit log](https://learn.microsoft.com/en-us/purview/audit-log-detailed-properties) | What each field in a record means. Needed to interpret any export. |
| ◽ | [Exchange properties in the audit log](https://learn.microsoft.com/en-us/purview/audit-log-exchange-properties) | Exchange-specific fields (LogonType, ClientInfoString, etc.). |
| ⭐ | [Microsoft 365 services that support auditing](https://learn.microsoft.com/en-us/purview/audit-supported-services) | Which workloads log at all. Tells you when a question **can't** be answered from the UAL. |
| ⭐ | [Audit logs for Copilot and AI applications](https://learn.microsoft.com/en-us/purview/audit-copilot) | Copilot prompts and responses, a newer and fast-changing area that's increasingly part of insider cases. |
| ⭐ | [Investigate compromised accounts](https://learn.microsoft.com/en-us/purview/audit-log-investigate-accounts) | Microsoft's guidance on using MailItemsAccessed and other events for account takeover (business email compromise). |
| ◽ | [Investigate deleted or missing emails](https://learn.microsoft.com/en-us/purview/audit-log-identify-email-messages) | Step-by-step for a very common question. |
| ◽ | [Investigate specific email messages](https://learn.microsoft.com/en-us/purview/audit-log-search-email) | Tracing what happened to one message. |
| ⭐ | [Investigate mailbox rule changes](https://learn.microsoft.com/en-us/purview/audit-log-identify-mailbox-rules) | Forwarding and inbox rules, the classic sign of business email compromise. |
| ◽ | [Investigate sharing activities](https://learn.microsoft.com/en-us/purview/audit-log-sharing) | SharePoint/OneDrive external sharing, for data exfiltration questions. |
| ◽ | [Investigate Microsoft Teams events](https://learn.microsoft.com/en-us/purview/audit-teams-audit-log-events) | Which Teams actions are logged. |
| ◽ | [Investigate deleted mailbox items](https://learn.microsoft.com/en-us/purview/audit-log-search-deleted-mailbox-items) | Deletion tracking, for anti-forensics questions. |

## 2. Purview eDiscovery — collecting content (17)
For when you need the actual emails, files and chats rather than logs. The newer unified eDiscovery experience replaced the classic one, so these pages change often.

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Learn about eDiscovery](https://learn.microsoft.com/en-us/purview/edisc) | Overview of the current experience and what's included per license. |
| ⭐ | [Get started with eDiscovery](https://learn.microsoft.com/en-us/purview/edisc-get-started) | Prerequisites and first-time setup. |
| ⭐ | [Assign eDiscovery permissions](https://learn.microsoft.com/en-us/purview/edisc-permissions) | Role groups needed. The first blocker in many engagements. |
| ⭐ | [Create and manage cases](https://learn.microsoft.com/en-us/purview/edisc-cases-manage) | Your "eDiscovery cases section". |
| ⭐ | [Create a search for a case](https://learn.microsoft.com/en-us/purview/edisc-search-query) | Building searches in the current UI. |
| ⭐ | [Use Keyword Query Language (KQL) to create search queries](https://learn.microsoft.com/en-us/purview/edisc-keyword-query-language) | Search syntax. Note: this "KQL" is **Keyword** Query Language, a different language from **Kusto** Query Language. |
| ◽ | [Use the condition builder](https://learn.microsoft.com/en-us/purview/edisc-condition-builder) | The point-and-click alternative to typing queries. |
| ◽ | [Evaluate and refine search results](https://learn.microsoft.com/en-us/purview/edisc-search-results) | Statistics and sampling before export. |
| ⭐ | [Export search results](https://learn.microsoft.com/en-us/purview/edisc-search-export) | Export formats and options. Defensibility depends on doing this right. |
| ◽ | [Configure export settings](https://learn.microsoft.com/en-us/purview/edisc-settings-export) | Tenant-wide export defaults. |
| ◽ | [Manage review sets](https://learn.microsoft.com/en-us/purview/edisc-review-set-manage) | Premium-tier review and processing. |
| ◽ | [Export items from a review set](https://learn.microsoft.com/en-us/purview/edisc-review-set-export) | Export path from review sets, which differs from search export. |
| ⭐ | [Create holds](https://learn.microsoft.com/en-us/purview/edisc-hold-create) | Preserving evidence before it ages out. |
| ◽ | [Identify mailbox hold types](https://learn.microsoft.com/en-us/purview/edisc-hold-types-mailboxes) | Working out which holds already exist on a mailbox. |
| ⭐ | [eDiscovery limits](https://learn.microsoft.com/en-us/purview/edisc-ref-limits) | Hard numbers (search/export sizes, concurrent jobs). Limit changes are notification-worthy. |
| ⭐ | [Partially indexed items in eDiscovery](https://learn.microsoft.com/en-us/purview/edisc-ref-partially-indexed-items) | Content search may **miss**. You need this to explain gaps in a report. |
| ◽ | [Search for eDiscovery activities in the audit log](https://learn.microsoft.com/en-us/purview/edisc-ref-audit-log) | Proving your own collection steps, for chain of custody. |

## 3. Insider Risk & other Purview investigation tools (8)

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Insider Risk Management overview](https://learn.microsoft.com/en-us/purview/insider-risk-management) | What it detects and the licensing. |
| ⭐ | [Insider risk audit log](https://learn.microsoft.com/en-us/purview/insider-risk-management-audit-log) | Who in the tenant viewed or changed insider risk cases. |
| ⭐ | [Insider risk activities](https://learn.microsoft.com/en-us/purview/insider-risk-management-activities) | Reviewing user activity timelines and alerts. |
| ◽ | [Insider risk forensic evidence](https://learn.microsoft.com/en-us/purview/insider-risk-management-forensic-evidence) | Screen-capture evidence on endpoints. Has privacy and legal implications. |
| ◽ | [Insider risk settings](https://learn.microsoft.com/en-us/purview/insider-risk-management-settings) | Settings like anonymization and policy indicators that affect what you'll see. |
| ⭐ | [Data Security Investigations](https://learn.microsoft.com/en-us/purview/data-security-investigations) | Newer AI-assisted investigation product in Purview. Fast-changing. |
| ◽ | [Activity explorer](https://learn.microsoft.com/en-us/purview/data-classification-activity-explorer) | Label and DLP activity history, with its own retention window. |
| ◽ | [Communication compliance](https://learn.microsoft.com/en-us/purview/communication-compliance) | Message policy matches. Sometimes the source of an internal case. |

## 4. PowerShell & API acquisition (14)
Your "PowerShell export to CSV/JSON" path and programmatic collection. Watch for deprecations here: they break scripts.

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Search-UnifiedAuditLog](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/search-unifiedauditlog?view=exchange-ps) | The main cmdlet for UAL pulls. Parameter and limit changes matter. |
| ◽ | [Search-MailboxAuditLog](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/search-mailboxauditlog?view=exchange-ps) | Older mailbox-audit cmdlet, being retired. Watching for its end date. |
| ◽ | [Search-AdminAuditLog](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/search-adminauditlog?view=exchange-ps) | Exchange admin changes. |
| ⭐ | [New-ComplianceSearch](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/new-compliancesearch?view=exchange-ps) | Scripted eDiscovery searches. |
| ⭐ | [New-ComplianceSearchAction](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/new-compliancesearchaction?view=exchange-ps) | Scripted export and purge actions. |
| ⭐ | [Get-MessageTraceV2](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/get-messagetracev2?view=exchange-ps) | Replacement for the older Get-MessageTrace. Message flow evidence. |
| ◽ | [Get-InboxRule](https://learn.microsoft.com/en-us/powershell/module/exchangepowershell/get-inboxrule?view=exchange-ps) | Current-state collection of inbox rules. |
| ⭐ | [Connect to Exchange Online PowerShell](https://learn.microsoft.com/en-us/powershell/exchange/connect-to-exchange-online-powershell?view=exchange-ps) | Authentication changes, like module versions or auth methods being retired, break your workflow. |
| ⭐ | [Connect to Security & Compliance PowerShell](https://learn.microsoft.com/en-us/powershell/exchange/connect-to-scc-powershell?view=exchange-ps) | Same, for the eDiscovery cmdlets. |
| ⭐ | [Graph API: auditLogQuery](https://learn.microsoft.com/en-us/graph/api/resources/security-auditlogquery?view=graph-rest-1.0) | The newer API for UAL searches, returning JSON. Likely the future of bulk audit pulls. |
| ⭐ | [Office 365 Management Activity API reference](https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-reference) | Streaming audit API used by SIEMs and collection tools. |
| ⭐ | [Office 365 Management Activity API schema](https://learn.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema) | The JSON field definitions, including record type numbers. |
| ◽ | [Graph API: list sign-ins](https://learn.microsoft.com/en-us/graph/api/signin-list?view=graph-rest-1.0) | Programmatic Entra sign-in export. |
| ◽ | [Graph API: list directory audits](https://learn.microsoft.com/en-us/graph/api/directoryaudit-list?view=graph-rest-1.0) | Programmatic Entra audit export. |

## 5. Defender XDR — Advanced Hunting (Kusto KQL) (13)

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Advanced hunting overview](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-overview) | Includes the **30-day lookback** for hunting data. A change there matters a lot. |
| ⭐ | [Advanced hunting schema tables](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-schema-tables) | Index of all tables. New tables appear here. |
| ⭐ | [Advanced hunting limits](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-limits) | Row, time and resource limits on queries and exports. |
| ⭐ | [Advanced hunting API](https://learn.microsoft.com/en-us/defender-xdr/api-advanced-hunting) | Exporting query results programmatically. |
| ⭐ | [CloudAppEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-cloudappevents-table) | M365 activity (similar to UAL data) queryable in KQL. |
| ⭐ | [EmailEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-emailevents-table) | Email delivery and threat data. |
| ◽ | [UrlClickEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-urlclickevents-table) | Safe Links clicks: "did the user click the phishing link?" |
| ⭐ | [EntraIdSignInEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-entraidsigninevents-table) | Entra sign-ins in hunting. Newer name for the table below. |
| ◽ | [AADSignInEventsBeta table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-aadsignineventsbeta-table) | Old table name. Watching for its retirement date. |
| ◽ | [IdentityLogonEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-identitylogonevents-table) | Logons seen by Defender for Identity and Defender for Cloud Apps. |
| ◽ | [GraphApiAuditEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-graphapiauditevents-table) | Graph API calls, useful for spotting attacker tooling. |
| ◽ | [OAuthAppInfo table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-oauthappinfo-table) | Malicious app consent investigations. |
| ◽ | [Defender XDR data privacy & retention](https://learn.microsoft.com/en-us/defender-xdr/data-privacy) | Where Defender data is stored and how long it's kept. |

## 6. Entra ID (Azure AD) logs (5)

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Entra data retention](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-reports-data-retention) | Sign-in and audit log retention per license, as short as 7 days on free tiers. **High-priority watch.** |
| ⭐ | [Sign-in logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-ins) | Log types (interactive, non-interactive, service principal) and their fields. |
| ⭐ | [Audit logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-audit-logs) | Directory changes such as MFA resets, role grants and app consents. |
| ⭐ | [Download logs](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-download-logs) | Portal CSV/JSON export limits. |
| ◽ | [Send logs to Azure Monitor](https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-integrate-activity-logs-with-azure-monitor-logs) | How to keep logs longer than default retention. A "next time" recommendation for clients. |

## 7. Microsoft Sentinel / Log Analytics (5)

| | Page | Why it's on the list |
|---|---|---|
| ◽ | [Sentinel data connectors (Microsoft 365 connector)](https://learn.microsoft.com/en-us/azure/sentinel/data-connectors-reference#microsoft-365-formerly-office-365) | What M365 data a client's Sentinel actually holds. |
| ◽ | [OfficeActivity table](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/officeactivity) | Where UAL data lands in Sentinel, often kept longer than Purview's retention. |
| ◽ | [Log Analytics data retention](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-retention-configure) | Interactive vs long-term retention tiers. |
| ◽ | [Sentinel moving to the Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/move-to-defender) | Ongoing portal migration that changes where you click. |
| ◽ | [Connect Sentinel to Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/microsoft-sentinel-onboard) | The unified portal setup. |

## 8. Exchange mail evidence (3)

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Message trace (modern EAC)](https://learn.microsoft.com/en-us/exchange/monitoring/trace-an-email-message/message-trace-modern-eac) | Portal message trace: how far back it goes and what it shows. |
| ⭐ | [Recoverable Items folder](https://learn.microsoft.com/en-us/exchange/security-and-compliance/recoverable-items-folder/recoverable-items-folder) | Where "deleted" mail still lives and for how long. |
| ◽ | [Litigation holds](https://learn.microsoft.com/en-us/exchange/policy-and-compliance/holds/litigation-holds) | Mailbox-level preservation. |

## 9. Change feeds & licensing (watch these for *new* things) (7)
These catch new pages and announcements that aren't on the list yet.

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [What's new in Purview](https://learn.microsoft.com/en-us/purview/whats-new) | Monthly roundup for Audit, eDiscovery and Insider Risk. |
| ⭐ | [What's new in Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/whats-new) | New tables, features and retirements. |
| ⭐ | [What's new in Entra](https://learn.microsoft.com/en-us/entra/fundamentals/whats-new) | Sign-in log and retention changes, deprecations. |
| ◽ | [What's new in Sentinel](https://learn.microsoft.com/en-us/azure/sentinel/whats-new) | Connector and table changes. |
| ⭐ | [Microsoft 365 Roadmap RSS](https://www.microsoft.com/releasecommunications/api/v2/m365/rss) | Announces changes **before** the docs update. Filtered to security and compliance keywords. |
| ⭐ | [M365 security & compliance licensing guidance](https://learn.microsoft.com/en-us/office365/servicedescriptions/microsoft-365-service-descriptions/microsoft-365-tenantlevel-services-licensing-guidance/microsoft-365-security-compliance-licensing-guidance) | Which license unlocks which logs. The answer to "why doesn't this tenant have MailItemsAccessed?" |
| ◽ | [Purview retention overview](https://learn.microsoft.com/en-us/purview/retention) | Content retention and deletion policies that decide whether evidence still exists. |

## 10. Microsoft's own IR playbooks (4)
Microsoft's view of how to investigate common attacks. Good reference for the playbook later; changes are rare.

| | Page | Why it's on the list |
|---|---|---|
| ◽ | [Incident response playbooks (index)](https://learn.microsoft.com/en-us/security/zero-trust/security-operations-incident-response-playbooks) | Entry point. |
| ◽ | [Phishing playbook](https://learn.microsoft.com/en-us/security/zero-trust/security-operations-playbook-phishing) | Lists which logs to pull for phishing / business email compromise. |
| ◽ | [App consent grant playbook](https://learn.microsoft.com/en-us/security/zero-trust/security-operations-playbook-app-consent) | Malicious OAuth app investigations. |
| ◽ | [Password spray playbook](https://learn.microsoft.com/en-us/security/zero-trust/security-operations-playbook-password-spray) | Sign-in log analysis. |

## 11. Endpoint forensics — Defender for Endpoint (20)
Device-level evidence: process, file, network, registry and logon telemetry, plus remote collection from the machine itself.

| | Page | Why it's on the list |
|---|---|---|
| ⭐ | [Defender for Endpoint data storage & retention](https://learn.microsoft.com/en-us/defender-endpoint/data-storage-privacy) | States how long device telemetry is kept (the device timeline window). A retention change here is a top-tier alert. |
| ⭐ | [Investigate devices (device page & timeline)](https://learn.microsoft.com/en-us/defender-endpoint/investigate-machines) | The portal device timeline: how far back it goes and how to export events from it. |
| ⭐ | [Live response](https://learn.microsoft.com/en-us/defender-endpoint/live-response) | Remote shell on a device to collect files, memory-related artifacts and run scripts. Your remote acquisition tool. Permission and command changes matter. |
| ◽ | [Live response command examples](https://learn.microsoft.com/en-us/defender-endpoint/live-response-command-examples) | Exact syntax for `getfile`, `collect`, `run` and others. |
| ⭐ | [Take response actions on a device](https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts) | **Collect investigation package** (logs, autoruns, prefetch, etc.) and isolate a device. Lists what the package contains. |
| ◽ | [Take response actions on a file](https://learn.microsoft.com/en-us/defender-endpoint/respond-file-alerts) | Download or collect a file sample from devices for analysis. |
| ◽ | [API: Collect investigation package](https://learn.microsoft.com/en-us/defender-endpoint/api/collect-investigation-package) | Scripted collection across many devices. |
| ◽ | [API: Run live response](https://learn.microsoft.com/en-us/defender-endpoint/api/run-live-response) | Scripted live response, for automating collection at scale. |
| ◽ | [Automated investigations](https://learn.microsoft.com/en-us/defender-endpoint/automated-investigations) | What Defender did automatically, such as remediating files. Explains changes to the device you might misread as attacker activity. |
| ◽ | [Defender for Endpoint overview](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint) | Plan tiers (P1 vs P2). P1 tenants lack much of the telemetry below. |
| ⭐ | [What's new in Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/whats-new-in-microsoft-defender-endpoint) | Change feed for new telemetry, response actions and retirements. |
| ⭐ | [DeviceProcessEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table) | Process creation with command lines. The backbone of execution evidence. |
| ⭐ | [DeviceEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceevents-table) | Catch-all security events (USB mounts, AV detections, PowerShell commands, etc.). New ActionTypes appear here. |
| ⭐ | [DeviceFileEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicefileevents-table) | File create, modify, rename and delete. Exfiltration staging and malware drops. |
| ⭐ | [DeviceNetworkEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table) | Outbound connections, for C2 and exfiltration questions. |
| ⭐ | [DeviceLogonEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicelogonevents-table) | Local and remote logons (RDP, network), for lateral movement. |
| ⭐ | [DeviceRegistryEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceregistryevents-table) | Registry changes, for persistence. |
| ◽ | [DeviceImageLoadEvents table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceimageloadevents-table) | DLL loads, for side-loading and injection questions. |
| ◽ | [DeviceInfo table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceinfo-table) | Device names, OS versions and onboarding state over time. Needed to map hostnames to device IDs. |
| ◽ | [DeviceFileCertificateInfo table](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicefilecertificateinfo-table) | Signer info, for spotting unsigned or spoofed binaries. |

---
**Total: 116 pages.** ⭐ core: 66 · ◽ optional: 50
Not included on purpose: Intune, Azure resource logs. Say if you want either added.
