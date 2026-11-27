"""Check the exact ImageAnalysis argv built during staging. No process is launched here."""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path

EXE = 'C:/Program Files/PixInsight/bin/PixInsight.exe'
STARTUP = ('-n', '--no-startup-scripts', '--no-startup-check-updates', '--no-focus-stealing')


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def verify_launch(staged, root, now):
    require(type(now) is datetime and now.tzinfo is not None, 'IA_LAUNCH_CLOCK')
    root = Path(root)
    records = staged['staged']
    by_path = {record['path']:record for record in records}
    require(len(by_path) == len(records), 'IA_LAUNCH_DUPLICATE_PIN')
    entry = (root/'entry.js').as_posix()
    config = (root/'runtime-config.json').as_posix()
    require(',' not in entry and root.name == staged['operation'],
            'IA_LAUNCH_ENTRY_PATH')
    argv = staged['launchArguments']
    require(type(argv) is list and argv == [EXE, *STARTUP, '--run='+entry], 'IA_LAUNCH_ARGUMENTS')
    for path in (entry, config):
        raw = Path(path).read_bytes()
        expected = by_path.get(path)
        require(expected == dict(path=path, byteLength=len(raw), sha256=sha256(raw).hexdigest()),
                'IA_LAUNCH_PIN')
    settings = json.loads(Path(config).read_bytes())
    require(settings['operationRef'] == staged['operation'] and settings['plan']['operationRef'] == root.name,
            'IA_LAUNCH_OPERATION')
    ends = datetime.fromisoformat(settings['deadlineUTC']).astimezone(timezone.utc)
    remaining = ends-now
    require(timedelta(seconds=30) <= remaining <= timedelta(seconds=120), 'IA_LAUNCH_BUDGET')
    return dict(argvCount=len(argv), entrySha256=by_path[entry]['sha256'],
                configSha256=by_path[config]['sha256'], newInstanceRequested=True,
                profileIsolationEstablished=False, automationMode=False,
                nativeAdmission=False, pixInsightStarted=False)