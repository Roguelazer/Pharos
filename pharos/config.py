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
        app_config = {}
        if "listen_port" in doc:
            app_config["listen_port"] = doc["listen_port"]
        if "listen_host" in doc:
            app_config["listen_host"] = doc["listen_host"]
        port = doc.get("port", 8080)
        host = doc.get("listen_host", "0.0.0.0")
        for watcher in doc.get("metric_watcher_sets", []):
            name = watcher["name"]
            watches_doc = watcher["watches"]
            watches = []
            for watch in watches_doc:
                common_kwargs = {}
                if "interval" in watch:
                    common_kwargs["interval"] = watch["interval"]
                if watch["type"] == "command":
                    watches.append(pharos.CommandMetricWatcher(name=watch["name"], command=watch["command"], **common_kwargs))
                elif watch["type"] == "get":
                    watches.append(pharos.PageGETMetricWatcher(name=watch["name"], url=watch["url"], thresholds=watch["thresholds"], **common_kwargs))
                else:
                    raise ConfigParseError("Expected type to be one of 'command', 'get' in watch set %s" % name)
            metric_watcher_sets.append(pharos.WatcherSet(name, watches))
    return (page_tag, metric_watcher_sets, app_config)
