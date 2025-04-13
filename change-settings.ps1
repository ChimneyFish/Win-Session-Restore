# Enable "Restore Previous Session" for Firefox
Function Enable-FirefoxRestoreSession {
    try {
        # Get the Firefox profile directory
        $FirefoxProfilePath = "$env:APPDATA\Mozilla\Firefox\Profiles"
        $Profiles = Get-ChildItem -Path $FirefoxProfilePath -Directory
        if ($Profiles.Count -eq 0) {
            Write-Host "Firefox profile not found. Skipping..."
            return
        }

        foreach ($Profile in $Profiles) {
            $PrefsFile = "$Profile\prefs.js"
            if (Test-Path $PrefsFile) {
                # Check if the preference already exists
                $Content = Get-Content -Path $PrefsFile
                if (-Not ($Content -match 'user_pref("browser.startup.restoreTabs", true);')) {
                    # Add preference to restore previous session
                    Add-Content -Path $PrefsFile -Value 'user_pref("browser.startup.restoreTabs", true);'
                    Write-Host "Enabled 'Restore Previous Session' for Firefox profile: $Profile"
                } else {
                    Write-Host "'Restore Previous Session' already enabled for Firefox profile: $Profile"
                }
            }
        }
    } catch {
        Write-Host "Error enabling Firefox restore session: $_"
    }
}

# Enable "Continue Where You Left Off" for Chrome
Function Enable-ChromeRestoreSession {
    try {
        # Set Chrome registry key to enable "Continue where you left off"
        $ChromeRestoreKey = "HKCU:\Software\Google\Chrome\PreferenceMACs\Default\"
        New-ItemProperty -Path $ChromeRestoreKey -Name "session.restore_on_startup" -Value 1 -PropertyType DWORD -Force
        Write-Host "Enabled 'Continue Where You Left Off' for Chrome"
    } catch {
        Write-Host "Error enabling Chrome restore session: $_"
    }
}

# Main Function
Function Enable-RestoreSessions {
    Enable-FirefoxRestoreSession
    Enable-ChromeRestoreSession
}

# Call the main function
Enable-RestoreSessions