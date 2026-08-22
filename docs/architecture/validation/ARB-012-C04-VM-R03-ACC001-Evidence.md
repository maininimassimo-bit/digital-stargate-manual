# ARB-012-C04 — VM-R03 / ACC-001 Evidence

| Field | Value |
|---|---|
| Evidence ID | E-ARB012-C04-VM-R03 |
| Work item | C04-W06 |
| Control | VM-R03 / ACC-001 / ENV-004 |
| Host | `dsg-arb012-c04-val` |
| Hyper-V VM | `DSG-ARB012-C04-VALIDATION` |
| Date | 2026-08-22 |
| Result | **PASS** |
| Runtime effect | Validation VM account only; no observatory runtime effect |

## Evidence

A dedicated non-production validation account for Massimo Mainini was created on the isolated validation VM.

Verified account state:

```text
username: dsgmassimo
uid: 1001
gid: 1001
full name: Massimo Mainini
home: /home/dsgmassimo
shell: /bin/bash
groups: dsgmassimo, users
sudo: denied
```

Command evidence:

```text
id dsgmassimo
uid=1001(dsgmassimo) gid=1001(dsgmassimo) groups=1001(dsgmassimo),100(users)

getent passwd dsgmassimo
dsgmassimo:x:1001:1001:Massimo Mainini,,,:/home/dsgmassimo:/bin/bash

sudo -l -U dsgmassimo
User dsgmassimo is not allowed to run sudo on dsg-arb012-c04-val.
```

A distinct authenticated session was then demonstrated:

```text
su - dsgmassimo
whoami -> dsgmassimo
id -> uid=1001(dsgmassimo) gid=1001(dsgmassimo) groups=1001(dsgmassimo),100(users)
pwd -> /home/dsgmassimo
exit
whoami -> dsgoperator
```

No password, MFA material or other secret was committed as evidence.

## Disposition

**VM-R03 / ACC-001 / ENV-004: PASS for Massimo account creation and distinct-session evidence.**

ENV-004 remains partially open until ACC-002 for Leonardo Di Egidio is created and independently demonstrated.