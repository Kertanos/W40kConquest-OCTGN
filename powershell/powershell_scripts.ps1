$wh_source = $octgn_wh_source + "\af04f855-58c4-4db3-a191-45fe33381679"
$wh_definitionxml = $wh_source + "\definition.xml"
$wh_o8build = $o8build_location + "\o8build.exe"

$coc_version = "version"

function whbuild
{
    $loc = Get-Location
    Set-Location $wh_source
    
	[xml]$def = (Get-Content $wh_definitionxml) 
    
    $version_number = [version]($def.game.version)
       
    $prev_version = "{0}.{1}.{2}.{3}" -f $version_number.Major, $version_number.Minor, $version_number.Build, $version_number.Revision
    $new_version = "{0}.{1}.{2}.{3}" -f $version_number.Major, $version_number.Minor, $version_number.Build, ($version_number.Revision + 1)
    
    echo ("Changing version number from {0} to {1}" -f $prev_version, $new_version)

    $def.game.version = $new_version
    $def.Save($wh_definitionxml)
    
    get-childitem $wh_source -include *.pyc -recurse | foreach ($_) {remove-item $_.fullname}
    
    & $wh_o8build -i -d=($wh_source)
    
    Set-Location $loc
}

function whb
{
    whbuild
}
