#!/usr/local/autopkg/python
#
# Copyright 2020 James Capen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import json

from autopkglib import Processor, ProcessorError, URLGetter

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/

__all__ = ["SlackerCurl"]

class SlackerCurl(URLGetter):
    description = (
        "Posts to Slack via webhook based on output of a MunkiImporter. "
        "Slack alternative to the post processor provided by Andy Semak (@asemak) "
        "that was a Teams alternative to the requests module based "
        "Slack post processor by Ben Reilly (@notverypc)"
        "Based on Graham Pugh's slacker.py - "
        "https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py"  # noqa
        "and "
        "@thehill idea on macadmin slack - "
        "https://macadmins.slack.com/archives/CBF6D0B97/p1542379199001400 "
        "Takes elements from "
        "https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784"
        "and "
        "https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py")  # noqa

    input_variables = {
        "munki_info": {
            "required": False,
            "description": "Munki info dictionary to use to display info.",
        },
        "munki_repo_changed": {
            "required": False,
            "description": "Whether or not item was imported.",
        },
        "webhook_url": {
            "required": False,
            "description": "Slack webhook.",
        }
    }
    output_variables = {
    }

    description = __doc__

    def main(self):
        was_imported = self.env.get("munki_repo_changed")
        munkiInfo = self.env.get("munki_info")
        webhook_url = self.env.get("webhook_url")
        slack_channel = self.env.get("slack_channel")

        # Slack Custom Settings
        ICONEMOJI = ":ghost:"
        AUTOPKGICON = "https://avatars0.githubusercontent.com/u/5170557?s=200&v=4"
        USERNAME = "AutoPkg"

        if was_imported:
            name = self.env.get("munki_importer_summary_result")["data"]["name"]
            version = self.env.get("munki_importer_summary_result")["data"]["version"]
            pkg_path = self.env.get("munki_importer_summary_result")["data"]["pkg_repo_path"]
            pkginfo_path = self.env.get("munki_importer_summary_result")["data"]["pkginfo_path"]
            catalog = self.env.get("munki_importer_summary_result")["data"]["catalogs"]
            if name:
                slack_text = "*New item added to repo:*\nTitle: *%s*\nVersion: *%s*\nCatalog: *%s*\nPkg Path: *%s*\nPkginfo Path: *%s*" % (name, version, catalog, pkg_path, pkginfo_path)
                slack_data = {'text': slack_text, 'channel': slack_channel, 'icon_url': AUTOPKGICON, 'username': USERNAME}
                json_data = json.dumps(slack_data)

            # Build the headers
            headers = {
              "Content-Type": "application/json"
            }
            print ("Headers are:", headers)

            # Build the required curl switches
            curl_opts = [
                # "--request", "POST",
                "--data", json_data,
                "{}".format(self.env.get("webhook_url"))
            ]

            print ("Curl options are:", curl_opts)

            # Initialize the curl_cmd, add the curl options, and execute the curl  # noqa
            try:
                curl_cmd = self.prepare_curl_cmd()
                self.add_curl_headers(curl_cmd, headers)
                curl_cmd.extend(curl_opts)
                print ("Curl command is:", curl_cmd)
                response = self.download_with_curl(curl_cmd)

            except:
                raise ProcessorError("Failed to complete the post")  # noqa

if __name__ == "__main__":
    processor = SlackerCurl()
    processor.execute_shell()
