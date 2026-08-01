-- Export the complete Apple Music library, replacing Bibliotheek.xml.
-- Run with: osascript export_music_library.applescript [destination-folder]

on run argv
	if (count of argv) > 0 then
		set destinationFolder to item 1 of argv
	else
		set destinationFolder to POSIX path of (container of (path to me))
	end if
	if destinationFolder does not end with "/" then set destinationFolder to destinationFolder & "/"
	
	set exportPath to destinationFolder & "Bibliotheek.xml"
	set temporaryPath to destinationFolder & ".Bibliotheek.new.xml"
	set exportFile to POSIX file temporaryPath
	
	tell application "Music"
		activate
		export library playlist 1 as XML to exportFile
	end tell
	do shell script "/usr/bin/plutil -lint " & quoted form of temporaryPath
	do shell script "/bin/mv -f " & quoted form of temporaryPath & " " & quoted form of exportPath
	
	return exportPath
end run
