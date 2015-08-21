[Setup]
AppName=Bokken
AppVersion=1.8
DefaultDirName={pf}\Bokken
DefaultGroupName=Bokken
OutputDir=bokken-installer-win-output\
OutputBaseFilename=bokken-win32-setup
Compression=lzma2
SolidCompression=yes
LicenseFile=bokken-installer-win\license.txt
;UninstallDisplayIcon={app}\uninstall.ico
WizardImageFile=bokken-installer-win-logo-v2.bmp
WizardSmallImageFile=bokken-installer-win-minilogo.bmp

[Files]
;NOTE: the MSI files are called AfterInstall NOT BeforeInstall due the fact we need the files in TMP before we can call MSIEXEC for them
;NOTE2: the MSI files are REMOVED after installation to keep it all nice and clean, the "deleteafterinstall" flag is responsible for that
Source: "python-2.7.10.msi"; DestDir: "{tmp}"; AfterInstall: PreInstall01; Flags: deleteafterinstall
Source: "pygtk-all-in-one-2.24.2.win32-py2.7.msi"; DestDir: "{tmp}"; AfterInstall: PreInstall02; Flags: deleteafterinstall
Source: "bokken-installer-win\bokken\*.*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "bokken-installer-win\Readme.txt"; DestDir: "{app}"; Flags: isreadme
Source: "bokken-installer-win\site-packages\*.*"; DestDir: "C:\Python27\Lib\site-packages"; Flags: recursesubdirs

[Run]
;NOTE: depreciated MSIEXEC deployment, left here for future purposes
;Filename: "msiexec.exe"; Parameters: "/i ""{tmp}\python-2.7.10.msi"""
;Filename: "msiexec.exe"; Parameters: "/i ""{tmp}\pygtk-all-in-one-2.24.2.win32-py2.7.msi"""
Filename: "{app}\bokken.bat"; WorkingDir: "{app}"; Description: "Launch application"; Flags: postinstall nowait skipifsilent unchecked

[Registry]
;NOTE: A reboot is required in order to set these new environmental changes, the path is currently set in the bokken.bat file so it works immediately.
;Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}\graphviz-2.38\bin"; Check: NeedsAddPath('{app}\graphviz-2.38\bin')
;Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}\radare2-w32-0.9.9\bin"; Check: NeedsAddPath('{app}\radare2-w32-0.9.9\bin')

[Icons]
;Programs folder
Name: "{group}\Bokken"; IconFilename: "{app}\bokken.ico"; Filename: "{app}\bokken.bat"; WorkingDir: "{app}" 
Name: "{group}\ReadMe"; Filename: "{app}\README.txt"; WorkingDir: "{app}"
Name: "{group}\Changelog"; Filename: "{app}\CHANGELOG.txt"; WorkingDir: "{app}"
Name: "{group}\License"; Filename: "{app}\LICENSE.txt"; WorkingDir: "{app}"
Name: "{group}\Uninstall Bokken"; Filename: "{uninstallexe}"
;Desktop shortcut
Name: "{commondesktop}\Bokken"; IconFilename: "{app}\bokken.ico"; Filename: "{app}\bokken.bat"; WorkingDir: "{app}"

[Code]
// Pre-Installation procedures go here, simple message box for instructions or information about upcoming procedures of the installer
procedure PreInstall01();

var
  MsgResult: Integer;
  ErrorCode: Integer;

begin
  MsgResult := SuppressibleMsgBox('Bokken requires Python 2.7 to be installed. Install now?', mbConfirmation, MB_YESNO, IDYES);
  if MsgResult = IDYES then
  begin
  ShellExec('', 'msiexec', ExpandConstant('/I "{tmp}\python-2.7.10.msi"'), '', SW_SHOWNORMAL, ewWaitUntilTerminated, ErrorCode);
  end
  else
  if MsgResult = IDNO then
  begin
  end
end;


procedure PreInstall02();

var
  MsgResult: Integer;
  ErrorCode: Integer;

begin
  MsgResult := SuppressibleMsgBox('Bokken requires PyGTK to be installed. Install now?', mbConfirmation, MB_YESNO, IDYES);
  if MsgResult = IDYES then
  begin
  ShellExec('', 'msiexec', ExpandConstant('/I "{tmp}\pygtk-all-in-one-2.24.2.win32-py2.7.msi" INSTALLLEVEL=2'), '', SW_SHOWNORMAL, ewWaitUntilTerminated, ErrorCode);
  end
  else
  if MsgResult = IDNO then
  begin
  end
end;

function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  // look for the path with leading and trailing semicolon
  // Pos() returns 0 if not found
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') = 0;
end;
