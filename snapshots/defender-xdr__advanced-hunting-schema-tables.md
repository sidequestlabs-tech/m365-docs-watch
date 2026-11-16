# Understand the advanced hunting schema

Important

Some information in this article relates to a prereleased product which may be substantially modified before it's commercially released. Microsoft makes no warranties, expressed or implied, with respect to the information provided here.

The [advanced hunting](advanced-hunting-overview) schema is made up of multiple tables that provide either event information or information about devices, alerts, identities, and other entity types. To effectively build queries that span multiple tables, you need to understand the tables and the columns in the advanced hunting schema.

Microsoft Sentinel also ingests data from some of these tables through data connectors. For more information, see [Stream data from Microsoft Defender XDR to Microsoft Sentinel in the Azure portal](/en-us/azure/sentinel/connect-microsoft-365-defender).

## Get schema information

While constructing queries, use the built-in schema reference to quickly get the following information about each table in the schema:

- **Tables description**âtype of data contained in the table and the source of that data.
- **Columns**âall the columns in the table.
- **Action types**âpossible values in the `ActionType` column representing the event types supported by the table. This information is provided only for tables that contain event information.
- **Sample query**âexample queries that feature how the table can be utilized.

### Access the schema reference

To quickly access the schema reference, select the **View reference** action next to the table name in the schema representation. You can also select **Schema reference** to search for a table.

[![The Schema Reference page on the Advanced Hunting page in the Microsoft Defender portal](/en-us/defender/media/understand-schema-1.png)](/en-us/defender/media/understand-schema-1.png#lightbox)

## Learn the schema tables

The following reference lists all the tables in the schema. Each table name links to a page describing the column names for that table. Table and column names are also listed in Microsoft Defender as part of the schema representation on the advanced hunting screen.

| Table name | Description |
| --- | --- |
| **[AADSignInEventsBeta](advanced-hunting-aadsignineventsbeta-table)** | Microsoft Entra interactive and non-interactive sign-ins |
| **[AADSpnSignInEventsBeta](advanced-hunting-aadspnsignineventsbeta-table)** | Microsoft Entra service principal and managed identity sign-ins |
| **[AgentsInfo](advanced-hunting-agentsinfo-table)** | Information about AI agents and their properties from various platforms |
| **[AlertEvidence](advanced-hunting-alertevidence-table)** | Files, IP addresses, URLs, users, or devices associated with alerts |
| **[AlertInfo](advanced-hunting-alertinfo-table)** | Alerts from Microsoft Defender for Endpoint, Microsoft Defender for Office 365, Microsoft Defender for Cloud Apps, and Microsoft Defender for Identity, including severity information and threat categorization |
| **[BehaviorEntities](advanced-hunting-behaviorentities-table)** (Preview) | Entities (file, process, device, user, and others) that are involved in a behavior in Microsoft Defender for Cloud Apps (not available for GCC) and User and Entity Behavior Analytics (UEBA) |
| **[BehaviorInfo](advanced-hunting-behaviorinfo-table)** (Preview) | Behaviors from Microsoft Defender for Cloud Apps (not available for GCC) and User and Entity Behavior Analytics (UEBA) |
| **[CallActivityEvents](advanced-hunting-callactivityevents-table)** | Activities performed during Microsoft Teams calls in your organization |
| **[CampaignInfo](advanced-hunting-campaigninfo-table)** (Preview) | Email campaigns identified by Microsoft Defender for Office 365 |
| **[CloudAppEvents](advanced-hunting-cloudappevents-table)** | Events involving accounts and objects in Office 365 and other cloud apps and services |
| **[CloudAuditEvents](advanced-hunting-cloudauditevents-table)** | Cloud audit events for various cloud platforms protected by the organization's Microsoft Defender for Cloud |
| **[CloudDnsEvents](advanced-hunting-clouddnsevents-table)** | DNS activity events from cloud infrastructure environments |
| **[CloudKeyVaultEvents](advanced-hunting-cloudkeyvaultevents-table)** (Preview) | Operations performed against Azure Key Vault resources |
| **[CloudPolicyEnforcementEvents](advanced-hunting-cloudpolicyenforcementevents-table)** (Preview) | Policy enforcement evaluation decisions and metadata of security gating events for various cloud platforms protected by the organization's Microsoft Defender for Cloud |
| **[CloudProcessEvents](advanced-hunting-cloudprocessevents-table)** (Preview) | Cloud process events for various cloud platforms protected by the organization's Microsoft Defender for Containers |
| **[CloudStorageAggregatedEvents](advanced-hunting-cloudstorageaggregatedevents-table)** (Preview) | Cloud storage activity and related events |
| **[DataSecurityBehaviors](advanced-hunting-datasecuritybehaviors-table)** (Preview) | Insights about potentially suspicious user behaviors that violate user-defined or default policies configured in the Microsoft Purview suite of solutions |
| **[DataSecurityEvents](advanced-hunting-datasecurityevents-table)** (Preview) | Information about user activities that violate user-defined or default policies in the Microsoft Purview suite of solutions |
| **[DeviceBaselineComplianceAssessment](advanced-hunting-devicebaselinecomplianceassessment-table)** (Preview) | Baseline compliance assessment snapshot, which indicates the status of various security configurations related to baseline profiles on devices |
| **[DeviceBaselineComplianceAssessmentKB](advanced-hunting-devicebaselinecomplianceassessmentkb-table)** (Preview) | Information about various security configurations used by baseline compliance to assess devices |
| **[DeviceBaselineComplianceProfiles](advanced-hunting-devicebaselinecomplianceprofiles-table)** (Preview) | Baseline profiles used for monitoring device baseline compliance |
| **[DeviceEvents](advanced-hunting-deviceevents-table)** | Multiple event types, including events triggered by security controls such as Microsoft Defender Antivirus and exploit protection |
| **[DeviceFileCertificateInfo](advanced-hunting-devicefilecertificateinfo-table)** | Certificate information of signed files obtained from certificate verification events on endpoints |
| **[DeviceFileEvents](advanced-hunting-devicefileevents-table)** | File creation, modification, and other file system events |
| **[DeviceImageLoadEvents](advanced-hunting-deviceimageloadevents-table)** | DLL loading events |
| **[DeviceInfo](advanced-hunting-deviceinfo-table)** | Machine information, including OS information |
| **[DeviceLogonEvents](advanced-hunting-devicelogonevents-table)** | Sign-ins and other authentication events on devices |
| **[DeviceNetworkEvents](advanced-hunting-devicenetworkevents-table)** | Network connection and related events |
| **[DeviceNetworkInfo](advanced-hunting-devicenetworkinfo-table)** | Network properties of devices, including physical adapters, IP and MAC addresses, as well as connected networks and domains |
| **[DeviceProcessEvents](advanced-hunting-deviceprocessevents-table)** | Process creation and related events |
| **[DeviceRegistryEvents](advanced-hunting-deviceregistryevents-table)** | Creation and modification of registry entries |
| **[DeviceTvmBrowserExtensions](advanced-hunting-devicetvmbrowserextensions-table)** (Preview) | Browser extension installations found on devices from Microsoft Defender Vulnerability Management |
| **[DeviceTvmBrowserExtensionsKB](advanced-hunting-devicetvmbrowserextensionskb-table)** (Preview) | Browser extension details and permission information used in the Microsoft Defender Vulnerability Management browser extensions page |
| **[DeviceTvmCertificateInfo](advanced-hunting-devicetvmcertificateinfo-table)** (Preview) | Certificate information for devices in the organization from Microsoft Defender Vulnerability Management |
| **[DeviceTvmHardwareFirmware](advanced-hunting-devicetvmhardwarefirmware-table)** | Hardware and firmware information of devices as checked by Defender Vulnerability Management |
| **[DeviceTvmInfoGathering](advanced-hunting-devicetvminfogathering-table)** | Defender Vulnerability Management assessment events including configuration and attack surface area states |
| **[DeviceTvmInfoGatheringKB](advanced-hunting-devicetvminfogatheringkb-table)** | Metadata for assessment events collected in the `DeviceTvmInfogathering` table |
| **[DeviceTvmSecureConfigurationAssessment](advanced-hunting-devicetvmsecureconfigurationassessment-table)** | Microsoft Defender Vulnerability Management assessment events, indicating the status of various security configurations on devices |
| **[DeviceTvmSecureConfigurationAssessmentKB](advanced-hunting-devicetvmsecureconfigurationassessmentkb-table)** | Knowledge base of various security configurations used by Microsoft Defender Vulnerability Management to assess devices; includes mappings to various standards and benchmarks |
| **[DeviceTvmSoftwareEvidenceBeta](advanced-hunting-devicetvmsoftwareevidencebeta-table)** | Evidence info about where a specific software was detected on a device |
| **[DeviceTvmSoftwareInventory](advanced-hunting-devicetvmsoftwareinventory-table)** | Inventory of software installed on devices, including their version information and end-of-support status |
| **[DeviceTvmSoftwareVulnerabilities](advanced-hunting-devicetvmsoftwarevulnerabilities-table)** | Software vulnerabilities found on devices and the list of available security updates that address each vulnerability |
| **[DeviceTvmSoftwareVulnerabilitiesKB](advanced-hunting-devicetvmsoftwarevulnerabilitieskb-table)** | Knowledge base of publicly disclosed vulnerabilities, including whether exploit code is publicly available |
| **[DisruptionAndResponseEvents](advanced-hunting-disruptionandresponseevents-table)** (Preview) | [Automatic attack disruption](automatic-attack-disruption) events in Microsoft Defender XDR |
| **[EmailAttachmentInfo](advanced-hunting-emailattachmentinfo-table)** | Information about files attached to emails |
| **[EmailEvents](advanced-hunting-emailevents-table)** | Microsoft 365 email events, including email delivery and blocking events |
| **[EmailPostDeliveryEvents](advanced-hunting-emailpostdeliveryevents-table)** | Security events that occur post-delivery, after Microsoft 365 delivers the emails to the recipient mailbox |
| **[EmailUrlInfo](advanced-hunting-emailurlinfo-table)** | Information about URLs on emails |
| **[EntraIdSignInEvents](advanced-hunting-entraidsigninevents-table)** | Microsoft Entra interactive and non-interactive sign-ins |
| **[EntraIdSpnSignInEvents](advanced-hunting-entraidspnsigninevents-table)** | Microsoft Entra service principal and managed identity sign-ins |
| **[ExposureGraphEdges](advanced-hunting-exposuregraphedges-table)** | Microsoft Security Exposure Management exposure graph edge information provides visibility into relationships between entities and assets in the graph |
| **[ExposureGraphNodes](advanced-hunting-exposuregraphnodes-table)** | Microsoft Security Exposure Management exposure graph node information, about organizational entities and their properties |
| **[FileMaliciousContentInfo](advanced-hunting-filemaliciouscontentinfo-table)** (Preview) | Files that were processed by Microsoft Defender for Office 365 in SharePoint Online, OneDrive, and Microsoft Teams. |
| **[GraphAPIAuditEvents](advanced-hunting-graphapiauditevents-table)** | Microsoft Entra ID API requests made to Microsoft Graph API for resources in the tenant |
| **[IdentityAccountInfo](advanced-hunting-identityaccountinfo-table)** | Account information from various sources, including Microsoft Entra ID. This table also includes information and link to the identity that owns the account. |
| **[IdentityDirectoryEvents](advanced-hunting-identitydirectoryevents-table)** | Events involving an on-premises domain controller running Active Directory (AD). This table covers a range of identity-related events and system events on the domain controller. |
| **[IdentityEvents](advanced-hunting-identityevents-table)** (Preview) | Information about identity events obtained from other cloud identity service providers |
| **[IdentityInfo](advanced-hunting-identityinfo-table)** | Account information from various sources, including Microsoft Entra ID |
| **[IdentityLogonEvents](advanced-hunting-identitylogonevents-table)** | Authentication events on Active Directory and Microsoft online services |
| **[IdentityQueryEvents](advanced-hunting-identityqueryevents-table)** | Queries for Active Directory objects, such as users, groups, devices, and domains |
| **[MessageContents](advanced-hunting-messagecontents-table)** | Microsoft Teams message snippets and related message metadata |
| **[MessageEvents](advanced-hunting-messageevents-table)** | Messages sent and received within your organization at the time of delivery |
| **[MessagePostDeliveryEvents](advanced-hunting-messagepostdeliveryevents-table)** | Security events that occurred after the delivery of a Microsoft Teams message in your organization |
| **[MessageUrlInfo](advanced-hunting-messageurlinfo-table)** | URLs sent through Microsoft Teams messages in your organization |
| **[OAuthAppInfo](advanced-hunting-oauthappinfo-table)** (Preview) | Microsoft 365-connected OAuth applications registered with Microsoft Entra ID and available in the Defender for Cloud Apps app governance capability |
| **[UrlClickEvents](advanced-hunting-urlclickevents-table)** | Safe Links clicks from email messages, Teams, and Office 365 apps |

## Related topics

- [Advanced hunting overview](advanced-hunting-overview)
- [Learn the query language](advanced-hunting-query-language)
- [Work with query results](advanced-hunting-query-results)
- [Use shared queries](advanced-hunting-shared-queries)
- [Hunt across devices, emails, apps, and identities](advanced-hunting-query-emails-devices)
- [Apply query best practices](advanced-hunting-best-practices)

Tip

Do you want to learn more? Engage with the Microsoft Security community in our Tech Community: [Microsoft Defender XDR Tech Community](https://techcommunity.microsoft.com/t5/microsoft-365-defender/bd-p/MicrosoftThreatProtection).
