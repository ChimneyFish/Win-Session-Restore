#define MyAppName "winfreezeFrame"
#define MyAppVersion "1.2"
#define MyAppPublisher "LACD, LLC"
#define MyAppURL "https://www.lacd.com/"
#define MyAppExeName "winfreezeFrame"

[Setup]
AppId={{C12426D7-EFFD-40F7-A7A7-0FCDAA31B43F}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\winfreezeFrame
UninstallDisplayIcon={app}\{#MyAppExeName}
DisableProgramGroupPage=yes
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=C:\Users\hotty\OneDrive\Desktop\winfreezeframe
OutputBaseFilename=winfreezeFrame
SetupIconFile=C:\Users\hotty\Win-Session-Restore\icons\icon.ico
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop Icon"; GroupDescription: "Additional Icons"; Flags: unchecked
Name: "addstartup"; Description: "Start winfreezeFrame at boot"; GroupDescription: "Startup Options"; Flags: unchecked

[Files]
Source: "C:\Users\hotty\Win-Session-Restore\dist\winfreezeFrame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hotty\Win-Session-Restore\icons\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hotty\Win-Session-Restore\restore_button_image.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hotty\Win-Session-Restore\msedge-restore.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\hotty\Win-Session-Restore\change-settings.ps1"; DestDir: "{tmp}"; Flags: ignoreversion

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "winfreezeFrame"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: addstartup

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon


[Run]
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{tmp}\change-settings.ps1"""; Flags: runhidden
Filename: "{app}\{#MyAppExeName}"; Description: "Launch winfreezeFrame"; Flags: nowait postinstall skipifsilent