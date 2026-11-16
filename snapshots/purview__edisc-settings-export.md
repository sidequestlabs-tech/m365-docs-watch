# Configure export settings in eDiscovery

Note

This setting isn't available in DoD cloud organizations.

Export settings let you manage download links for all exports in eDiscovery. When exporting large eDiscovery results, network interruptions and browser limitations might affect the download experience. Whether you enable the **Enable export download via pre-authorized link** option depends on your environment, security requirements, network bandwidth, and the tools you plan to use.

Note

For export download best practices, see [Best practices for downloading export packages](edisc-search-export).

Use a pre-authorized link when downloading large export packages or when your network connection might be limited. Large exports take longer to download, which naturally increases the chances of a network interruption during the process. Pre-authorized links are designed for this scenario. By using a pre-authorized link, the download can resume when interrupted. Using a pre-authorized link works with tools that support parallel or chunked downloads, such as third-party download accelerators or browser extensions. When you initiate the download, the pre-authorized download link is generated. The link acts like an access token, so tools can download data without repeated sign-ins.

These links grant direct access to your export. If shared, anyone with the link can access the data. To reduce risk, set the shortest possible expiration time based on the size of your export. You can configure export package download link availability for the following durations:

- 1 hour
- 6 hours
- 12 hours
- 24 hours (default)
- 48 hours
- 72 hours
- 168 hours

Disable pre-authorized link for high bandwidth environments. The standard signed-in download method without pre-authorized links is ideal when you have an ExpressRoute connection with high bandwidth to Microsoft. The standard signed-in download method doesn't generate a pre-authorized token, reducing the risk of link misuse. Each session requires sign-in. If the download is interrupted, you need to re-authenticate and restart. Browser resume behavior varies and isn't guaranteed.

## Enable preauthorized export download links

Important

Don't share export download links with anyone. Treat these links as secrets.

Changing this setting to turn preauthorized links on or off only applies to future export downloads. It doesn't affect existing links. For example, if you enable preauthorized links with a one-day expiration, any links you created before you disable the setting remain valid until they expire. Turning off the pre-authorized export download link setting doesn't retroactively change the behavior of existing links.

To enable preauthorized export download links for your organization:

1. Go to the [Microsoft Purview portal](https://purview.microsoft.com) and sign in with the credentials for a user account assigned eDiscovery *Administrator* permissions.
2. Select the **eDiscovery** solution card, then go to **Settings** > **eDiscovery** > **Export**.
3. Select the toggle for **Enable export download via pre-authorized link**.
4. Select a duration in **Export Link Settings**.
5. Select **Save**.
