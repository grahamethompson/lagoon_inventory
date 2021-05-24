#!/usr/bin/python

import json


class FilterModule(object):
    def filters(self):
        return {
            'organise_hosts_by_metadata': self.organise_hosts_by_metadata
        }

    @staticmethod
    def organise_hosts_by_metadata(hosts):
        if not isinstance(hosts, list):
            return "Requires list object"
        elif isinstance(hosts, list):
            organised_hosts = {}
            for host in hosts:
                metadata = json.loads(host["metadata"])
                for key, value in metadata.items():
                    metadata = key+"-"+value
                    if metadata in organised_hosts:
                        organised_hosts[metadata].append(host['name'])
                    else:
                        organised_hosts[metadata] = []
                        organised_hosts[metadata].append(host['name'])
            return organised_hosts


if __name__ == "__main__":
    hosts = [
        {
            "name": "sandbox",
            "id": 123,
            "metadata": "{\"govcms-type\": \"paas\", \"govcms-version\": \"8\", \"govcms-scaffold-version\": \"1.1.2\", \"project-status\": \"development\", \"foo\": \"bar\", \"drupal-version\": \"8\"}"
            },
        {
            "name": "sandbox2",
            "id": 1234,
            "metadata": "{\"govcms-type\": \"paas\", \"govcms-version\": \"7\", \"project-status\": \"production\", \"drupal-version\": \"7\"}"
            }
    ]
    f = FilterModule()
    print(f.organise_hosts_by_metadata(hosts))
