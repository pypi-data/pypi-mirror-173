# 2022_assignment1_users_db


## Quick start

Questa applicazione gesisce un database di utenti, raccogliendo informazioni come nome, email, password, genere, età ecc...
In particolare è composta da due moduli
- ```package/database.py``` che gestisce la creazione e l'accesso e le modifiche al database
- ```package/functions.py``` che gestisce l'output delle query 

Le librerie utilizzate sono già all'interno del pacchetto python e non è necessario installarle
- sqlite3
- os

## Pipeline

```
stages:
  - build
  - verify
  - testing
  - package
  - upload
```

**Build**: al momento non servono dipendenze particolari per il funzionamento del software, usa sqlite3 già integrata in Python;

**Verify**: usa ```prospector``` e ```bandit``` per analizzare il codice all'interno della cartella ```./package``` (jobs paralleli);
- verifyProspector
- verifyBandit

**Testing**: usa ```pytest``` per effettuare unit e integration tests, valutati separatamente e in parallelo;
- unitTest
- integTest

**Package**: usa ```setup.py``` e ```wheel``` per creare il pacchetto da distribuire;

**Release**: usa ```twine``` per eseguire l'upload del pacchetto appena creato;

**Deploy**: //
