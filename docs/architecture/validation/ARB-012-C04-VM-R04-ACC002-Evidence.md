# ARB-012-C04 — VM-R04 / ACC-002 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R04 |
| Work item | C04-W06 |
| Control | VM-R04 / ACC-002 / ENV-004 |
| Host | `dsg-arb012-c04-val` |
| Hyper-V VM | `DSG-ARB012-C04-VALIDATION` |
| Date | 2026-08-22 |
| Result | **PASS** |
| Runtime effect | Validation VM account only; no observatory runtime effect |

## Evidence

A dedicated non-production validation account for Leonardo Di Egidio was created on the isolated validation VM.

Verified account state:

```text
username: dsgleonardo
uid: 1002
gid: 1002
full name: Leonardo Di Egidio
home: /home/dsgleonardo
shell: /bin/bash
groups: dsgleonardo, users
sudo: denied
```

Command evidence:

```text
id dsgleonardo
uid=1002(dsgleonardo) gid=1002(dsgleonardo) groups=1002(dsgleonardo),100(users)

getent passwd dsgleonardo
dsgleonardo:x:1002:1002:Leonardo Di Egidio,,,:/home/dsgleonardo:/bin/bash

sudo -l -U dsgleonardo
User dsgleonardo is not allowed to run sudo on dsg-arb012-c04-val.
```

A distinct authenticated session was then demonstrated:

```text
su - dsgleonardo
whoami -> dsgleonardo
id -> uid=1002(dsgleonardo) gid=1002(dsgleonardo) groups=1002(dsgleonardo),100(users)
pwd -> /home/dsgleonardo
```

No password, MFA material or other secret was committed as evidence.

## ENV-004 disposition

ACC-001 (`dsgmassimo`) and ACC-002 (`dsgleonardo`) now exist as separate non-production accounts with distinct UIDs, home directories and authenticated sessions. Neither validation account has sudo privileges.

**VM-R04 / ACC-002: PASS.**

**ENV-004 — two distinct authenticated validation accounts: PASS.**