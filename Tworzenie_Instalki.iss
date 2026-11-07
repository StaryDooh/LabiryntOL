; ===========================================================================
;  LabiryntOL - skrypt instalatora Inno Setup 6
;
;  Przed kompilacją instalatora uruchom kompiluj.bat (PyInstaller),
;  aby powstał katalog dist\LabiryntOL.
;
;  Numer wersji jest odczytywany automatycznie z pliku LabiryntOL.exe
;  (pochodzi z Wersja.txt), więc tutaj nie trzeba go zmieniać.
;
;  Wynik: GitHub\Setup_LabiryntOL_<wersja>.exe
; ===========================================================================

#define AppName      "LabiryntOL"
#define AppExeName   "LabiryntOL.exe"
#define AppPublisher "Aleksander Markowski, Krzysztof Markowski"
#define DistDir      AddBackslash(SourcePath) + "dist\LabiryntOL"
#define AppExePath   DistDir + "\" + AppExeName

#if !FileExists(AppExePath)
  #error "Brak pliku dist\LabiryntOL\LabiryntOL.exe - najpierw uruchom kompiluj.bat"
#endif

#define AppVersion   GetVersionNumbersString(AppExePath)

[Setup]
; AppId jednoznacznie identyfikuje aplikację - NIE zmieniaj go w kolejnych wersjach
AppId={{B6BD9AA9-91C3-428E-B4EA-24EDFA180231}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppCopyright=© 2026 {#AppPublisher}
VersionInfoVersion={#AppVersion}
VersionInfoDescription=Instalator gry {#AppName}
VersionInfoProductName={#AppName}

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=GitHub\LICENCJA.txt

; Plik wyjściowy
OutputDir=GitHub
OutputBaseFilename=Setup_{#AppName}_{#AppVersion}

SetupIconFile=GitHub\ikona.ico
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName} {#AppVersion}

Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern

; Domyślnie instalacja dla wszystkich (Program Files),
; można wybrać instalację tylko dla bieżącego użytkownika
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog commandline

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Zamknij uruchomioną grę przed aktualizacją
CloseApplications=yes

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Licencja"; Filename: "{app}\LICENCJA.txt"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; usuwa pozostałości po grze (np. pliki __pycache__), jeśli powstaną
Type: filesandordirs; Name: "{app}"
