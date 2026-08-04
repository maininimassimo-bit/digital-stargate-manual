# Enterprise Search Center

<div class="dsg-search-center" data-dsg-search-center>
  <section class="dsg-search-center__panel" aria-labelledby="dsg-search-title">
    <div>
      <p class="dsg-kicker">Enterprise Federated Search</p>
      <h2 id="dsg-search-title">Ricerca unificata della piattaforma</h2>
      <p>Cerca contemporaneamente nella documentazione versionata e nel catalogo delle sessioni scientifiche. La ricerca nativa di Material resta disponibile per la consultazione rapida del portale.</p>
    </div>

    <label>
      <span class="visually-hidden">Testo da cercare</span>
      <input class="dsg-search-center__query" type="search" data-search-query placeholder="Cerca target, sessione, architettura, procedura o componente…" autocomplete="off">
    </label>

    <div class="dsg-search-center__filters" aria-label="Filtri di ricerca">
      <label>Tipo
        <select data-search-type>
          <option value="">Tutti i tipi</option>
        </select>
      </label>
      <label>Anno
        <select data-search-year>
          <option value="">Tutti gli anni</option>
        </select>
      </label>
      <label>Target
        <select data-search-target>
          <option value="">Tutti i target</option>
        </select>
      </label>
      <label>Qualità
        <select data-search-quality>
          <option value="">Tutti gli stati</option>
        </select>
      </label>
    </div>

    <div class="dsg-search-center__toolbar">
      <div>
        <p data-search-status>Caricamento degli indici federati…</p>
        <p data-search-stats></p>
      </div>
      <button class="dsg-search-center__reset" type="button" data-search-reset>Reimposta filtri</button>
    </div>
  </section>

  <section class="dsg-search-center__results" data-search-results aria-live="polite">
    <div class="dsg-search-center__empty">Preparazione del Search Center…</div>
  </section>
</div>

## Ambito della ricerca

Il Search Center usa due sorgenti governate:

- l'indice generato dal plugin Search di MkDocs per la documentazione;
- lo Scientific Data Engine per le sessioni scientifiche.

I dataset JSON restano proiezioni e lo Scientific Data Engine rimane l'unico access layer condiviso per i dati scientifici.