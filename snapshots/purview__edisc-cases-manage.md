# Create and manage cases in eDiscovery

After setting up Microsoft Purview eDiscovery and [assigning permissions to eDiscovery managers](edisc-get-started#step-1-assign-permissions) in your organization who manage cases, create and manage a case for escalation activities or investigation requests.

Tip

Get started with Microsoft Security Copilot to explore new ways to work smarter and faster using the power of AI. Learn more about [Microsoft Security Copilot in Microsoft Purview](copilot-in-purview-overview).

## Cases dashboard

The **Cases** dashboard in the Microsoft Purview portal displays all eDiscovery cases in your organization. You can quickly see the cases in your organization, the status of each case, and important information associated with each case.

- **Name**: The name of the case. The case name must be unique in your organization.
- **Case status**: The current status of the case.
- **Case type**: The type of case.
- **Created on**: The date and time in Coordinated Universal Time (UTC) when the case was created.
- **Last modified**: The date and time in Coordinated Universal Time (UTC) when the case was last modified.
- **Last modified by**: The name of the user that last modified the case.
- **Number**: The optional docket number or other custom numeric identifier for the case.
- **Description**: The description of the case entered when the case was created.

Select **Customize columns** to customize the displayed columns and the order of the columns in the **Cases** dashboard. Choose the columns to display or drag and drop columns to reorder.

### Filter cases

To filter cases on the **Cases** dashboard, enter a keyword to filter by case names that contain the keyword or select **Filter** on the command bar. Select one or more of the following filters and select **Apply** to help you organize cases for review on the dashboard.

**Case status** options:

- **Active**: The case is active.
- **Pending delete**: The case likely has a hold in the pending deletion state. Check the hold policy and redistribute to resolve the error. Afterward, cases without any holds should be deleted successfully.
- **Closing**: The case is being closed. This status is seen only for case with active holds. Cases without holds are immediately closed.
- **Closed**: The case is closed without errors and the case can be reopened.
- **Closed with errors**: The case is closed, but there are errors. Errors are most likely associated with holds that weren't released during closing. To resolve, check policies with errors, resolve the errors, and redistribute the policies.

**Case type** options:

- **Premium**: eDiscovery (Premium) cases.
- **Standard**: eDiscovery (Standard) cases.
- **User data search**: Legacy user data search cases.
- **Content search**: Content searches in your organization.

Important

Case type is used only to map cases to the Microsoft Purview compliance portal during the preview of eDiscovery in the Microsoft Purview portal. This mapping helps you find cases in the compliance portal (if needed). All cases created in the Microsoft Purview portal are the *Premium* type, regardless of your license or subscription. Access to premium features isn't governed by the case settings toggle.

To clear **Case** dashboard filters, select **Filter** > **Clear filters** > **Apply**.

### Grouping cases

To group cases on the **Cases** dashboard, select **Group** on the command bar. Select one of the following groupings to help you organize cases for review on the dashboard.

- **None**: Clears grouping for cases.
- **Status**: Groups cases by the status of the case.
- **Last modified by**: Groups cases by the user that last modified the case.
- **Case type**: Groups cases by the case type.

### Download a list of cases

To download a list of all cases displayed in the **Cases** dashboard, select **Download list**. A .csv file is generated that contains the case name and all of the **Cases** dashboard column properties for each case.

## Create a case

Tip

Do you prefer an interactive configuration guide experience? Check out the [Create and configure a case](https://mslearn.cloudguides.com/guides/Create%20and%20configure%20a%20case%20with%20Microsoft%20Purview%20eDiscovery) guide.

Complete the following steps to create a case and configure case properties. The user who creates the case is automatically added as a member. Members of the case can access the case in the Microsoft Purview portal and perform eDiscovery tasks.

1. Go to the [Microsoft Purview portal](https://purview.microsoft.com) and sign in using the credentials for a user account assigned eDiscovery permissions. Members of the *Organization Management* role group can also create eDiscovery cases.
2. Select the **eDiscovery** solution card and then select **Cases** in the left navigation.
3. Select **Create case**.
4. On **Enter details to get started**, complete the following fields:

   - **Case name**: give the case a name (required). The case name must be unique in your organization.
   - **Case description**: Add an optional description to help others understand this case.
5. Select **Create** to create the new case and start your investigation.

## Add data sources to a case

Tip

Want to try premium eDiscovery features? See the [subscription requirements](https://aka.ms/M365EnterprisePlans) for Microsoft 365 Enterprise E5 licensing.

Data sources define the locations that you can quickly include in all case searches and holds. Add data sources to a case with [premium eDiscovery features enabled](edisc-settings-cases) to quickly use data sources across multiple case activities. When you add a data source at the case level, you include all associated resources (mailboxes, sites, and more) for the data source.

SharePoint Embedded container support in eDiscovery (preview) lets you add supported container URLs individually or through bulk import as case data sources.

To discover supported containers relevant to a selected user or filter containers by application, manage the data source in an individual search or hold. Group-owned and app-owned SharePoint Embedded containers aren't currently supported.

For step-by-step guidance on adding data sources to a case, see [Data sources in eDiscovery](edisc-data-sources).

## Summarize a case with Copilot (preview)

When you summarize cases with Copilot, you can quickly access a comprehensive summary of eDiscovery cases. Copilot consolidates case information into a single, easy-to-understand summary. Copilot analyzes content within the case and generates natural language summaries, giving you a clear, actionable overview of key details in real-time. It eliminates the need to navigate through multiple case tabs by consolidating status updates, completed actions, pending tasks, and ongoing jobs into a single, easy-to-read summary. To use Copilot to summarize a case, Security Copilot must be enabled and the user must be assigned the *eDiscovery Administrator* or *eDiscovery Manager* role.

Whenever you view a case, Copilot automatically reviews the case and displays summary information in the Copilot pane. You can also select **Summarize this case** to run Copilot and display or refresh this summary and pane. When Copilot completes the summary, it displays details about the case in the following areas:

- **Case information**: A high level summary information about the case, including information about the case type, when the case was created, when the case was modified, who the last user was that modified the case, and more.
- **Data sources**: A summary of [data sources](edisc-features-components#data-sources) associated with the case.
- **Exports**: A summary of [search](edisc-search-export) and [review set](edisc-review-set-export) exports associated with the case, including details about export items, file sizes, and item counts.
- **Holds**: A summary of [hold policies](edisc-hold-manage) associated with the case, including hold policy, query, and location details.
- **Jobs**: A summary of all the [processes](edisc-process-managers) associated with the case.
- **Review sets**: A summary of the [review sets](edisc-review-set-manage) associated with the case, when they were created, modified, and who edited.
- **Searches**: A summary of [searches](edisc-search-query) associated with the case, including query conditions, sources, options, and settings.
- **Settings**: A summary of the [case settings](edisc-settings-cases), such as OCR, near-duplicate detection, search, document processing, and review set settings.

If the case doesn't have activity for an area, the Copilot summary indicates that the area doesn't have any activities to summarize. For example, if the case doesn't have associated exports, the Copilot summary in **Exports** section confirms that the case doesn't have any exports.

You can also enter customized prompts directly in Copilot to further refine and narrow the scope to specific areas about the case.

To change the data source used for the Copilot summary, select **Microsoft Learn documentation** at the end of the summary. This scopes the Copilot summary to support guidance that can help you learn more about working with cases and can provide step by step guidance or details about eDiscovery features and capabilities.

## Mark a case as a favorite

You can mark an eDiscovery case as a favorite for quicker access to cases you want to prioritize. You can quickly access cases marked as favorites through the **Cases** dashboard. To mark a case as a favorite, select the star icon to the left of a case in the case list on the **Cases** dashboard.

## Limited format cases

Some cases you previously created in the eDiscovery classic experience might have the *Limited format* status applied. If applicable to a case, this tag appears next to the case title when on any of the action tabs within a case (**Searches**, **Hold policies**, etc.). These cases have some limitations from the features and functionality available in cases created in the Microsoft Purview portal and with the new eDiscovery experience. Advanced indexing isn't available for searches, exporting items from a search, and when adding a search results to a review set.

## Manage case settings

Case settings include case information, case license level control, access permissions, and settings that control search and analytics behavior for the case. You can access settings for a specific case by selecting **Case settings** after selecting a case. You can define specific parameters for feature capabilities based on eDiscovery licenses in your organization, which users, role groups, and guests have access and permissions for the case, and which additional locations are included during organization-wide searches for the case.

For more information about case settings, see:

- [Learn about case settings in eDiscovery cases](edisc-settings-cases)
- [Learn about access and permission settings in eDiscovery cases](edisc-settings-access-permissions)
- [Learn about data sources settings in eDiscovery cases](edisc-settings-data-sources)
- [Learn about search and analytics settings in eDiscovery cases](edisc-settings-search-analytics)
- [Learn about review set settings in eDiscovery cases](edisc-settings-review-sets)

## Manage case status

Warning

Closing or deleting a case turns off all holds. Any content that was on hold is released, which might result in data loss.

To close or delete a case, select **Actions** for an individual case and choose **Close case** or **Delete case**.

For more information about managing case actions, see:

- [Closing a case](edisc-settings-cases#close-a-case)
- [Reopening a case](edisc-settings-cases#reopen-a-closed-case)
- [Deleting a case](edisc-settings-cases#delete-a-case)

## Related content

For more information about tracking eDiscovery case activities, see the following resource:

- [Search for eDiscovery activities in the audit log](edisc-ref-audit-log)
