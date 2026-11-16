# Live response command examples

Learn about common commands used in live response and see examples on how they're typically used.

Depending on the role you have, you can run basic or advanced live response commands. For more information on basic and advanced commands, see [Investigate entities on devices using live response](live-response).

## `analyze`

```
# Analyze the file malware.txt
analyze file c:\Users\user\Desktop\malware.txt
```

```
# Analyze the process by PID
analyze process 1234
```

## `connections`

```
# List active connections in json format using parameter name
connections -output json
```

```
# List active connections in json format without parameter name
connections json
```

## `dir`

```
# List files and sub-folders in the current folder (by default it will show relative paths [-relative_path])
dir
```

```
# List files and sub-folders in the current folder, with their full path
dir -full_path
```

```
# List files and sub-folders in a specific folder
dir C:\Users\user\Desktop\
```

```
# List files and subfolders in the current folder in json format
dir -output json
```

## `fileinfo`

```
# Display information about a file
fileinfo C:\Windows\notepad.exe
```

## `findfile`

```
# Find file by name
findfile test.txt
```

## `get`

```
# Download a file from a machine
get c:\Users\user\Desktop\work.txt
```

```
# Download a file from a machine, automatically run prerequisite commands
get c:\Users\user\Desktop\work.txt -auto
```

Note

The following file types *can't* be downloaded using this command from within Live Response:

- [Reparse point files](/en-us/windows-hardware/drivers/ifs/reparse-points)
- [Sparse files](/en-us/windows-server/administration/windows-commands/fsutil-sparse)
- Empty files
- Virtual files, or files that aren't fully present locally

[PowerShell](/en-us/powershell/scripting/overview) supports these file types.

Use PowerShell as an alternative, if you have problems using this command from within Live Response.

## `library`

```
# List files in the library
library
```

```
# Delete a file from the library
library delete script.ps1
```

## `processes`

```
# Show all processes
processes
```

```
# Get process by pid
processes 123
```

```
# Get process by pid with argument name
processes -pid 123
```

```
# Get process by name
processes -name notepad.exe
```

## `putfile`

```
# Upload file from library
putfile get-process-by-name.ps1
```

```
# Upload file from library, overwrite file if it exists
putfile get-process-by-name.ps1 -overwrite
```

```
# Upload file from library, keep it on the machine after a restart
putfile get-process-by-name.ps1 -keep
```

## `registry`

```
# Show information about the values in a registry key
registry HKEY_CURRENT_USER\Console
```

```
# Show information about a specific registry value (the double backslash \\ indicates a registry value versus key)
registry HKEY_CURRENT_USER\Console\\ScreenBufferSize
```

## `remediate`

```
# Remediate file in specific path
remediate file c:\Users\user\Desktop\malware.exe
```

```
# Remediate process with specific PID
remediate process 7960
```

```
# See list of all remediated entities
remediate list
```

Note

Currently, `HKEY_USERS` reg hive isn't supported for `remediate`. This is a known issue, and we're looking into it.

## `run`

```
# Run PowerShell script from the library without arguments
run script.ps1
```

```
# Run PowerShell script from the library with arguments
run get-process-by-name.ps1 -parameters "-processName Registry"
```

Note

For long running commands such as '**run**' or '**getfile**', you might want to use the '**&**' symbol at the end of the command to perform that action in the background.
If you use the '**g**' symbol, you can continue investigating the machine and return to the background command when done using '**fg**' [basic command](live-response#basic-commands).

When passing parameters to a live response script, don't include the following forbidden characters: **';'**, **'&'**, **'|'**, **'!'**, and **'$'**.

## `scheduledtask`

```
# Get all scheduled tasks
scheduledtasks
```

```
# Get specific scheduled task by location and name
scheduledtasks Microsoft\Windows\Subscription\LicenseAcquisition
```

```
# Get specific scheduled task by location and name with spacing
scheduledtasks "Microsoft\Configuration Manager\Configuration Manager Health Evaluation"
```

## `undo`

```
# Restore remediated registry
undo registry HKEY_CURRENT_USER\Console\ScreenBufferSize
```

```
# Restore remediated scheduledtask
undo scheduledtask Microsoft\Windows\Subscription\LicenseAcquisition
```

```
# Restore remediated file
undo file c:\Users\user\Desktop\malware.exe
```
