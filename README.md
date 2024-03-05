# ETL Refinement for Data Lakes

Questo repository include il codice per il processo di refinement dei dati già acquisiti dalle precedenti fasi di ingestione ed eventualmente ripuliti dalla fase di cleaning.

Il progetto consente di creare le versioni consolidate di alcune view (in tabelle iceberg), oltre che il ricaricamento delle view stesse:

- src/sql_create/*.sql -> definizione delle tabelle o viste
- src/sql_load/*.sql -> definizione dell'Insert/Merge (iceberg)

NOTA BENE:

I file SQL vengono caricati automaticamente SOLO se hanno l'estensione .sql; quindi per disabilitare un file è sufficiente rinominare l'estensione (o chiaramente rimuovere il file per una rimozione totale).

I file vengono caricati in ordine alfabetico, quindi per mantenere la consequenzialità bisogna far precedere un numero al nome del file.

Vengono deployate due State Machine:

- etl-refinement-{STAGE}-CreateTables
- etl-refinement-{STAGE}-LoadData

dove {STAGE} sarà "prod", "dev", ecc, a seconda dell'ambiente.

La prima `CreateTables` si occuperà di creare le viste e le tabelle sulla base dei codice presenti all'interno dei file SQL.

La seconda `LoadData` può:

- Giornaliera: per inserire la partizione giornaliera.
- Manuale: questa applica gli insert/merge per range di date (a seconda dei parametri forniti)
- Riparatrice: questa legge da una tabella DynamoDB le partizioni che devono essere riprocessate (a causa dell'arrivo di misure su partizioni vecchie) e funziona in modo analogo a quella manuale (con end_date = start_date).

Per avviare la versione manuale di `LoadData` è necessario passare il parametro

```json
{
    "history": "true",
    "start_date": "2023-08-01",
    "end_date": "2023-08-04",
}
```

dove "end_date" è opzionale e se non fornito verrà usato l'end_date definito nel codice ("ieri").

Per alcune tabelle che sono indipendenti dalla data e che sostanzialmente sono una lastversion del dato, non è necessario eseguirle N volte (a seconda del range start-end). Per escluderle da questa procedura ed essere eseguite solo una volta per run è necessario aggiungere "JUST-ONCE" nel nome del file SQL.
Natare che non sono state separate in cartelle diverse (rispetto a quelle che devono essere eseguite N volte) per poter eventualmente preservare l'ordine di esecuzione.


## License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) for more information.

---

This is a project created by [Linkalab](https://linkalab.it).
