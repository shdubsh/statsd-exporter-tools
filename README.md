StatsD Exporter Tools
===
A collection of scripts to help classify metrics for inclusion into Prometheus.

Generate set of metrics
---
```bash
cd whisper/metric_root
ls -R > ~/raw_metrics
python cli.py convert --infile ~/raw_metrics --outfile ~/formatted_metrics --prepend metric_root 
```

Test a rule
---
```bash
python cli.py test --infile ~/formatted_metrics -g 'metric_root.group.*'
```

Validate rules from yaml hash
---
```bash
python cli.py validate --rules rules.yaml --key statsd_exporter_rules --infile ~/formatted_metrics
```

Validate Watcher
---
```bash
while :; do inotifywait -q -e modify rules.yaml; clear; python cli.py validate --rules rules.yaml --key statsd_exporter_rules --infile ~/formatted_metrics; done
``` 
