# BKL-046 · Ripristino logico v571 dai contenitori v600

La capsula storica v571/v1.146 è stata ricostruita localmente. Lo staging v600 fornisce 28 membri attraverso 16 contenitori, integrati da quattro membri di controllo dalla capsula storica. Fra i 28 membri c’è il file integrale di conoscenza da 1.153.824.341 byte con SHA-256 `7b11789d0616b54cb002c506f0bd2c4e4cfb123a0569f8c409a09da67b2e567e`.

Il verificatore storico accetta la capsula ricostruita. Coincidono i byte dei singoli oggetti e dei file di verifica, secondo le impronte congelate. La codifica ZIP del contenitore ricostruito ha una propria impronta. La capsula storica originale resta conservata con la sua impronta.

Il complemento locale è uno ZIP da 56.856 byte con dichiarazione della capsula, inventario del publisher originale, job e ricevuta indipendente. La prova di ripristino dalla copia su H: prende questi quattro membri dal complemento e ricostruisce tutti gli altri dai contenitori già preparati. Il publisher non parte durante la prova.

La pubblicazione GitHub della capsula e dei contenitori resta aperta. Per una rilettura integrale da GitHub il trasferimento dovrà comprendere anche il complemento o la capsula storica integrale, nella destinazione e nel perimetro autorizzati. Questo controllo attesta la recuperabilità dei byte e mantiene a zero le chiusure scientifiche.
