# Microsoft services that support auditing

You can search the unified audit log for activities performed in different Microsoft services. The following table lists the Microsoft services, apps, and features that the unified audit log supports.

| Microsoft service or feature | Record types |
| --- | --- |
| Microsoft Entra ID | AzureActiveDirectory, AzureActiveDirectoryAccountLogon, AzureActiveDirectoryStsLogon |
| Azure Information Protection    (For the Microsoft Purview Information Protection client and scanner) | AipDiscover, AipSensitivityLabelAction, AipProtectionAction, AipFileDeleted, AipHeartBeat |
| Communication compliance | ComplianceSupervisionExchange |
| Content explorer | LabelContentExplorer |
| Data connectors | ComplianceConnector |
| Data loss prevention (DLP) | ComplianceDLPSharePoint, ComplianceDLPExchange, DLPEndpoint |
| Dynamics 365 | CRM |
| eDiscovery (Standard + Premium) | Discovery, AeD |
| Encrypted message portal | OMEPortal |
| Exact Data Match | MipExactDataMatch |
| Exchange Online | ExchangeAdmin, ExchangeItem, ExchangeItemAggregated |
| Forms | MicrosoftForms |
| Information barriers | InformationBarrierPolicyApplication |
| Microsoft Defender XDR | AirInvestigation, AirManualInvestigation, AirAdminActionInvestigation, MS365DCustomDetection |
| Microsoft 365 Copilot and Microsoft 365 Copilot Chat | CopilotInteraction |
| Microsoft Defender Experts | DefenderExpertsforXDRAdmin |
| Microsoft Defender for Identity (MDI) | MicrosoftDefenderForIdentityAudit |
| Microsoft Planner | PlannerCopyPlan, PlannerPlan, PlannerPlanList, PlannerRoster, PlannerRosterSensitivityLabel, PlannerTask, PlannerTaskList, PlannerTenantSettings |
| Microsoft Project for the web | ProjectAccessed, ProjectCreated, ProjectDeleted, ProjectTenantSettingsUpdated, ProjectUpdated, RoadmapAccessed,RoadmapCreated, RoadmapDeleted, RoadmapItemAccessed,RoadmapItemCreated,RoadmapItemDeleted, RoadmapItemUpdated, RoadmapTenantSettingsUpdated, RoadmapUpdated, TaskAccessed, TaskCreated,TaskDeleted, TaskUpdated |
| Microsoft Purview Information Protection (MIP) labels | MIPLabel, MipAutoLabelExchangeItem, MipAutoLabelSharePointItem, MipAutoLabelSharePointPolicyLocation |
| Microsoft Teams | MicrosoftTeams |
| Microsoft To Do | MicrosoftToDo, MicrosoftToDoAudit |
| MyAnalytics | MyAnalyticsSettings |
| OneDrive for Business | OneDrive |
| Power Apps | PowerAppsApp, PowerAppsPlan |
| Power Automate | MicrosoftFlow |
| Power BI | PowerBIAudit |
| Quarantine | Quarantine |
| Sensitive information types | DlpSensitiveInformationType |
| Sensitivity labels | MIPLabel, SensitivityLabelAction, SensitivityLabeledFileAction, SensitivityLabelPolicyMatch |
| SharePoint Online | SharePoint, SharePointFileOperation,SharePointSharingOperation, SharePointListOperation, SharePointCommentOperation |
| Stream | MicrosoftStream |
| SystemSync | DataShareCreated, DataShareDeleted, GenerateCopyOfLakeData, DownloadCopyOfLakeData |
| Threat Intelligence | ThreatIntelligence, ThreatIntelligenceUrl, ThreatFinder, ThreatIntelligenceAtpContent |
| Viva Goals | VivaGoals |
| Viva Insights | VivaInsights |
| Viva Engage | Viva Engage |

For more information about the operations that each service audits, see the [Audit log activities](audit-log-activities) article.

The previous table also identifies the record type value to use to search the audit log for activities in the corresponding service by using the **Search-UnifiedAuditLog** cmdlet in Exchange Online PowerShell or by using a PowerShell script. Some services have multiple record types for different types of activities within the same service. For a more complete list of auditing record types, see [Office 365 Management Activity API schema](/en-us/office/office-365-management-api/office-365-management-activity-api-schema#auditlogrecordtype).

For more information about using PowerShell to search the audit log, see:

- [Search-UnifiedAuditLog](/en-us/powershell/module/exchange/search-unifiedauditlog)
- [Use a PowerShell script to search the audit log](audit-log-search-script)
