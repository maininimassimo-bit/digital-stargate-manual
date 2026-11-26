# BKL-046 · Rendiconto v81 e supplemento alla conoscenza v1.171

L'incremento aggiunge sei riscontri verificati ai tre assi NOISE_FLUX. Ogni copia coincide con il rapporto al commit GitHub e con il membro dell'archivio sorgente su H:. La replica conserva la v80 e tutti i suoi criteri e stati.

- **NOISE_FLUX/1 e /2.** Le coppie dei calibratori reali ASI2600MC descrivono differenze fra flat e bias alla stessa durata nominale. Una sola durata illuminata lascia aperta la qualificazione del guadagno e della risposta alla dose. Nei flat, un piano stimato su blocchi complementari riduce da 69 a 8 su 504 i casi con varianza della somma oltre 1,2 volte la stima diagonale. La correzione scalare lascia invariato questo conteggio.
- **NOISE_FLUX/3.** Con un kernel bilineare offline e una fase di mezzo pixel su entrambi gli assi, la varianza misurata nei dark è 2,28 volte la diagonale empirica. La previsione con propagazione completa riduce l'errore mediano dal 56% al 5%. Il fascicolo congela 17 ingressi e 85 risultati di controllo. Controllo PJSR simulato e verificatore post-uscita restano collaudi offline. L'istanza DynamicAlignment, la catena del supervisore, le revisioni e l'ammissione restano da completare prima della prova nativa.

I 4.920 requisiti e i 14.521 criteri conservano la copertura registrata. Restano aperte sette famiglie scientifiche, 25 assi e 19 criteri Owner. Il supplemento non modifica la v1.171 di base. La consegna integrale richiede ancora la decisione sul perimetro di distribuzione e la verifica di ricostruzione indipendente.
