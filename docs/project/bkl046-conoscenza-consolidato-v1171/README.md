# BKL-046 — Pacchetto intermedio di conoscenza v1.171

Il pacchetto VM conserva la capsula v1.171 con i suoi byte originali, i due addenda sul fondo diffuso e sulla saturazione, e il rendiconto v74. Ogni membro ha dimensione e SHA-256 registrati nel manifesto interno. L'archivio è stato verificato sul volume di lavoro della VM e su H:.

La prova di ripristino ha letto la copia su H:, verificato i membri esterni e decompresso in streaming il file di conoscenza dalla capsula interna. I 3.030.957.683 byte letti restituiscono lo stesso SHA-256 della baseline registrata. Il pacchetto conserva la baseline e i supplementi come membri distinti, accessibili a partire dal manifesto. [Impronte di recupero](riscontro.json)

L'archivio contiene materiali a distribuzione mista. Su GitHub sono pubblicate le impronte e la ricevuta di rilettura. La consegna remota integrale e l'accettazione finale restano aperte.