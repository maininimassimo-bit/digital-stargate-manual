# BKL-046 · Sensibilità dell'orientazione PSF M8/M20 alla larghezza e alle ali

Il confronto rigenera il rapporto di base e mantiene invariati stelle, pixel CFA, centri proiettati, maschere e metà di esposizione. Estende la griglia della larghezza geometrica al 70–130% oppure il parametro Moffat beta ai valori 1,8, 2,5, 3,5 e 5. Anche il modello circolare dispone delle stesse alternative. Ogni forma è scelta su sette pose e verificata sulle altre sette con le soglie già fissate.

| Griglia di modelli | Angoli ripetibili in rosso | Angoli ripetibili in blu | Stelle confrontabili fra bande |
| --- | ---: | ---: | ---: |
| Base | 6 | 0 | 0 |
| Larghezze estese | 6 | 1 | 0 |
| Ali estese | 7 | 0 | 0 |
| Larghezze e ali estese | 8 | 2 | 1 |

Le sei stelle rosse di base ricompaiono in tutte le varianti con angoli che concordano entro 15 gradi. L'unica stella confrontabile fra bande nella griglia più ampia è 12-1-1, con 150 gradi in rosso e 52,5 in blu. La differenza assiale di 82,5 gradi riguarda un solo caso. Non stabilisce un effetto cromatico fisico. L'orientazione resta sensibile al dominio dei modelli, al supporto CFA in ciascuna banda e ai riferimenti astrometrici condivisi.

Il programma riceve protocollo, kit delle pose disgiunte, ZIP dei mosaici, ricevuta delle larghezze, dipendenze e nuova directory per i rapporti. La base viene confrontata byte per byte. Il kit H/K conserva tutte le decisioni per stella e metà di esposizione. [Studio di base](../bkl046-m8-m20-psf-disjoint-exposures-v1/README.md)