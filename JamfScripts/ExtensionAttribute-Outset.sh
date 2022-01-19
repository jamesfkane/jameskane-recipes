#!/bin/bash
OutsetVersion=""
if [ -f "/usr/local/outset/outset" ]; then
	OutsetVersion=$(/usr/local/outset/outset --version)
fi

echo "<result>$OutsetVersion</result>"

exit 0
