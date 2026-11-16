# Search for eDiscovery activities in the audit log

The audit log records eDiscovery activities that you perform in Microsoft Purview portal or in PowerShell. Events are logged when administrators, eDiscovery managers, or any user assigned [eDiscovery permissions](edisc-permissions) perform the following tasks:

- Creating and managing [eDiscovery cases](edisc-cases-manage).
- Creating and editing [eDiscovery searches](edisc-search-query) in cases.
- Performing search actions, such as generating statistics, sample, and exporting from search.
- Creating, editing, and removing [eDiscovery holds](edisc-hold-create) from cases.
- Creating [eDiscovery review sets](edisc-review-set-manage) and performing review activities in cases.

For more information about searching the audit log, the permissions that are required, and exporting search results, see [Search the audit log](audit-search).

## How to search for and view eDiscovery activities

Perform the following steps to search for and view eDiscovery activities in the audit log.

1. Go to the [Microsoft Purview portal](https://purview.microsoft.com) and sign in with the credentials for a user account assigned eDiscovery permissions.
2. Select the **Audit** solution card.
3. On the **Search** page, complete the following steps:

   1. In the **Activities - friendly names** drop-down list, under **eDiscovery activities**, select one or more eDiscovery activities to search for. For a complete list of all eDiscovery activities, see [Audit log activities](audit-log-activities#ediscovery-activities).

   Note

   The **Activities - friendly names** drop-down list also includes a group of activities named **eDiscovery cmdlet activities** that returns records from the cmdlet audit log.

   1. Select a date and time range to display eDiscovery events that occurred within that period.
   2. In the **Users** box, select one or more users to display search results for. Leave this box blank to return entries for all users.
   3. Select **Search** to run the search using your search criteria.

After the search results are displayed, you can select **Filter results** to filter or sort the resulting activity records. To view details about an activity, select the activity record in the list of search results. A **Details** flyout page is displayed that contains the detailed properties from the event record.

To display additional details, select **More information**. You can export the audit log search results to a .csv file, and then use the Excel Power Query feature to format and filter these records. For more information, see [Export, configure, and view audit log records](audit-log-export-records).

A client **IP Address** field is available for all activities performed in eDiscovery. If the **IP Address** column is blank for an activity, the activity was performed in the legacy eDiscovery experience. All eDiscovery activities performed in eDiscovery include an IP address in the **IP Address** column.

## Audit activities logged for eDiscovery

For a complete listing of all eDiscovery detailed properties and activities included in the audit log, see [Audit log activities](audit-log-activities#ediscovery-activities).
