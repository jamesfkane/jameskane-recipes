#!/bin/sh
string_type=%VERSION_STRING_TYPE%
string_type2=%VERSION_STRING_TYPE2%
version_string_complete="None"
if [ -f "/Applications/%JSS_INVENTORY_NAME%/Contents/Info.plist" ]; then
    version_string=$(defaults read "/Applications/%JSS_INVENTORY_NAME%/Contents/Info.plist" $string_type)
    version_string2=$(defaults read "/Applications/%JSS_INVENTORY_NAME%/Contents/Info.plist" $string_type2)
    version_string_complete="${version_string}.${version_string2}"
fi
echo "<result>$version_string_complete</result>"
exit 0