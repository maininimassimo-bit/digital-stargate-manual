# BKL-046 — Controllo ePSF tra visite sulla posa da 30 secondi

Il metodo ePSF fissato su GO-11880 è stato applicato a `jbbf01i3q` di GO-11887, lasciando invariati soglie, maschere e ricetta affine. Il P90 sulle tessere di verifica è 0,0657 pixel con 55 stelle per la coppia 1 → 2 e 0,0651 con 67 stelle per quella 2 → 1. Entrambe rispettano il limite di 0,100 pixel.

La proiezione su coppie con geometria qualificata porta un solo centro, il 208, a superare il filtro preliminare di segnale e DQ. Il massimo intero dista 3,459 pixel dal centro previsto, a fronte di un limite di 3,5. La retroproiezione del massimo cade nel componente saturo sorgente, con 0,352 pixel dal centro del pixel più vicino. Questo verifica la coerenza spaziale con la scia. Il controllo del picco non consente un centroide valido e resta da distinguere il nucleo da eventuali sorgenti vicine. La fotometria resta aperta.
