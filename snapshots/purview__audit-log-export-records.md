# Export, configure, and view audit log records

When you search the audit log and download the search results to a comma-separated value (.csv) file, the file contains a column named **AuditData**. This column holds extra information about each event. The data in this column is formatted as a JSON object. This object contains multiple properties that appear as *property:value* pairs separated by commas. You can use the JSON transform feature in the Power Query Editor in Excel to split each property in the JSON object in the **AuditData** column into multiple columns so that each property has its own column. This feature lets you sort and filter on one or more of these properties, which can help you quickly locate the specific auditing data you're looking for.

## Step 1: Export audit log search results

Important

For export processes to work correctly, make sure that your network firewall doesn't block the Azure Front Door domain (azurefd.net).

When you use Audit (Standard), you can export up to **50,000 records** to a .csv file from a single audit search query. For Audit (Premium), the export limit increases to **1,000,000** **records**. If the number of results returned by your audit search query exceeds these limits, the exported .csv file doesn't include all results and might omit some audit logs. To ensure complete data export, consider the following recommendations:

1. **Refine the scope of your search query** by narrowing the date range or applying other filters like UserId, Operation, and more.
2. **Perform multiple searches** with smaller, segmented date ranges to capture all relevant audit logs.

Narrowing the search scope and splitting large date ranges into smaller segments helps ensure comprehensive coverage of audit data within the export limits.

To search the audit log and export the results in a .csv file to your local computer, complete the following steps:

1. Run an [audit log search](audit-search) and revise the search criteria if necessary until you have the desired results.
2. On the search results page, select **Export**.

   ![Screenshot of audit search results page with the Export option highlighted to download all results.](media/audit-export-audit-search-results.png)

   This option exports all the audit records from the audit log search you ran in step 1. It adds the raw data from the audit log to a .csv file. It takes a while to prepare the download file for a large search. Large files result when searching for all activities or using a wide date range.
3. When the export process completes, a message appears at the top of the window that prompts you to open the .csv file and save it to your local computer. You might need to refresh the page to see this message. You can also access the .csv file in the **Downloads** folder.

## Step 2: Format the exported audit log using the Power Query Editor

In this step, you use the JSON transform feature in the Power Query Editor in Excel to split each property in the JSON object in the **AuditData** column into its own column. Then, you filter columns to view records based on the values of specific properties. This process helps you quickly locate the specific auditing data you're looking for.

1. Open a blank workbook in Excel for Microsoft 365, Excel 2019, or Excel 2016.
2. On the **Data** tab, in the **Get & Transform Data** ribbon group, select **From Text/CSV**.

   ![Screenshot of Excel Data tab with the From Text/CSV option selected to import the audit log file.](media/jsontransformopencsvfile.png)
3. Open the .csv file that you downloaded in Step 1.
4. Select **Transform Data** in the window that's displayed.

   ![Screenshot of the import dialog with the Transform Data option selected to open the file in Power Query Editor.](media/jsonopenpowerquery.png)

   The **Query Editor** opens the .csv file. You see four columns: **CreationDate**, **UserIds**, **Operations**, and **AuditData**. The **AuditData** column is a JSON object that contains multiple properties. You need to create a column for each property in the JSON object.
5. Right-click the title in the **AuditData** column, select **Transform**, and then select **JSON**.

   ![Screenshot of Power Query context menu for the AuditData column with Transform and JSON selected.](media/jsontransform.png)
6. Select the expand icon in the upper-right corner of the **AuditData** column.

   ![Screenshot of the Power Query AuditData column with the expand icon highlighted to show JSON properties.](media/jsontransformexpandicon.png)

   You see a partial list of the properties in the JSON objects in the **AuditData** column.
7. Select **Load more** to display all properties in the JSON objects in the **AuditData** column.

   ![Screenshot of the expanded JSON properties list in the AuditData column with the Load more option to display all properties.](media/jsontransformloadjsonproperties.png)

   You can clear the check box next to any property that you don't want to include. Eliminating columns that aren't useful for your investigation is a good way to reduce the amount of data displayed in the audit log.

   Note

   The JSON properties displayed in the previous screenshot (after you select **Load more**) are based on the properties found in the **AuditData** column from the first 1,000 rows in the .csv file. If different JSON properties exist in records after the first 1,000 rows, these properties (and a corresponding column) don't appear when you split the **AuditData** column into multiple columns. To help prevent this issue, consider rerunning the audit log search and narrow the search criteria so that fewer records return. Another workaround is to filter items in the **Operations** column to reduce the number of rows (before you perform step 5) before transforming the JSON object in the **AuditData** column.

   Tip

   To view an attribute within a list such as AuditData.AffectedItems, select the **Expand** icon in the upper right corner of the column you want to pull an attribute from, and then select **Expand to New Row**. From there it's a record and you can select the **Expand** icon in the upper right corner of the column, view the attributes, and select the one you want to view or extract.
8. Do one of the following things to format the title of the columns that you add for each JSON property that you select.

   - Clear the **Use original column name as prefix** check box to use the name of the JSON property as the column names; for example, **RecordType** or **SourceFileName**.
   - Leave the **Use original column name as prefix** check box selected to add the AuditData prefix to the column names; for example, **AuditData.RecordType** or **AuditData.SourceFileName**.
9. Select **OK**.

   You split the **AuditData** column into multiple columns. Each new column corresponds to a property in the AuditData JSON object. Each row in the column contains the value for the property. If the property doesn't contain a value, the *null* value appears. In Excel, cells with null values are empty.
10. On the **Home** tab, select **Close & Load** to close the Power Query Editor and open the transformed .csv file in an Excel workbook.

## Use PowerShell to search and export audit log records

Instead of using the audit log search tool in the Microsoft Purview portal, you can use the [Search-UnifiedAuditLog](/en-us/powershell/module/exchange/search-unifiedauditlog) cmdlet in Exchange Online PowerShell to export the results of an audit log search to a .csv file. Then you can follow the same procedure described in Step 2 to format the audit log using the Power Query editor. One advantage of using the PowerShell cmdlet is that you can search for events from a specific service by using the *RecordType* parameter. The following examples show how to use PowerShell to export audit records to a .csv file so you can use the Power Query editor to transform the JSON object in the **AuditData** column as described in Step 2.

In the following example, run the commands to return all records related to SharePoint sharing operations.

```
$auditlog = Search-UnifiedAuditLog -StartDate 06/01/2019 -EndDate 06/30/2019 -RecordType SharePointSharingOperation
```

```
$auditlog | Select-Object -Property CreationDate,UserIds,RecordType,AuditData | Export-Csv -Path c:\AuditLogs\PowerShellAuditlog.csv -NoTypeInformation
```

The search results are exported to a .csv file named *PowerShellAuditlog* that contains four columns: CreationDate, UserIds, RecordType, AuditData.

You can use the name or enum value for the record type. For a list of record type names and their corresponding enum values, see the *AuditLogRecordType* table in [Office 365 Management Activity API schema](/en-us/office/office-365-management-api/office-365-management-activity-api-schema#enum-auditlogrecordtype---type-edmint32).

You can only include a single value for the *RecordType* parameter. To search for audit records for other record types, run the two previous commands again to specify a different record type and append those results to the original .csv file. For example, run the following two commands to add SharePoint file activities from the same date range to the PowerShellAuditlog.csv file.

```
$auditlog = Search-UnifiedAuditLog -StartDate 06/01/2019 -EndDate 06/30/2019 -RecordType SharePointFileOperation
```

```
$auditlog | Select-Object -Property CreationDate,UserIds,RecordType,AuditData | Export-Csv -Append -Path c:\AuditLogs\PowerShellAuditlog.csv -NoTypeInformation
```

## Tips for exporting and viewing the audit log

Here are some tips and examples of exporting and viewing the audit log before and after you use the JSON transform feature to split the **AuditData** column into multiple columns.

- Filter the **RecordType** column to display only the records from a specific service or functional area. For example, to show events related to SharePoint sharing, select **14** (the enum value for records triggered by SharePoint sharing activities). For a list of the services that correspond to the enum values displayed in the **RecordType** column, see [Detailed properties in the audit log](audit-log-detailed-properties).
- Filter the **Operations** column to display the records for specific activities. For a list of most operations that correspond to a searchable activity in the audit log search tool in the Microsoft Purview portal, see the "Audited activities" section in [Search the audit log](audit-log-activities).

### Run the diagnostic for audit log configuration check

Note

You must be a Microsoft 365 global administrator to run the diagnostic.

To run the diagnostic for audit log configuration check, complete the following steps:

1. Select the diagnostic in the [Microsoft 365 admin center](https://aka.ms/PillarAuditConfigDiag).
2. Enter the User principal name (UPN) or email address of the user missing Audit entries.

Note

If you don't enter user details, the diagnostic performs general audit configuration validation checks.

1. Select **Run Tests**.
2. Review the key findings from the diagnostic to check the user and audit configuration for your organization.

## Next steps

- [Use a PowerShell script to search the audit log](audit-log-search-script): Automate recurring searches and export large result sets using PowerShell.
- [Detailed activity properties in the audit log](audit-log-detailed-properties): Understand the properties in your exported data to interpret results accurately.
- [Search the audit log to investigate common support issues](audit-troubleshooting-scenarios): Use exported data to investigate scenarios like compromised accounts or unauthorized access.
