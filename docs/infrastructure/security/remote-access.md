# Remote Access

## Access path

Remote access should follow this controlled path:

```text
Authorized Operator
       ↓
Authenticated VPN
       ↓
Observatory LAN
       ↓
Approved Management Service
```

## Rules

- prohibit direct exposure of device administration interfaces where avoidable;
- use strong credentials and multi-factor authentication where supported;
- review active VPN accounts periodically;
- disable obsolete access paths;
- log administrative actions;
- test emergency local access procedures.
