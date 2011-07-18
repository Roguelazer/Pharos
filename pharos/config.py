# Parse a YAML configuration file
from __future__ import with_statement

import yaml

import pharos

class ConfigParseError(StandardError):
    pass

def load(filename):
    page_tag = ""
    metric_watcher_sets = []
    with open(filename) as f:
        doc = yaml.safe_load(f.read())
        page_tag = doc.get("page_tag", "")
        for watcher in doc.get("metric_watcher_sets", []):
            name = watcher["name"]
            watches_doc = watcher["watches"]
            watches = []
            for watch in watches_doc:
                if watch["type"] == "command":
                    watches.append(pharos.CommandMetricWatcher(name=watch["name"], command=watch["command"]))
                elif watch["type"] == "get":
                    watches.append(pharos.PageGETMetricWatcher(name=watch["name"], url=watch["url"], thresholds=watch["thresholds"]))
                else:
                    raise ConfigParseError("Expected type to be one of 'command', 'get' in watch set %s" % name)
            metric_watcher_sets.append(pharos.WatcherSet(name, watches))
    return (page_tag, metric_watcher_sets)
