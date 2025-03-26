<div align="center">

# AcquaLux Backend API

Backend REST API per il sistema di prenotazione imbarcazioni di lusso AcquaLux, sviluppato come project work
universitario.

</div>

<details>
<summary><strong>📚 Contesto Accademico</strong></summary>

|                                      |                                                                                                             |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **Università**                       | Università Telematica Pegaso                                                                                |
| **Corso di Studio**                  | Informatica per le Aziende Digitali (L-31)                                                                  |
| **Settori Scientifico-Disciplinari** | • Informatica (INF/01)<br>• Ingegneria Economico-Gestionale (ING-IND/35)                                    |
| **Tema**                             | 1 - La digitalizzazione dell'impresa                                                                        |
| **Traccia**                          | 1.4 - Sviluppo di una pagina web per un servizio di prenotazione online di un'impresa del settore terziario |
| **CFU**                              | 3                                                                                                           |

</details>

## 📝 Descrizione del Progetto

AcquaLux rappresenta l'implementazione di un sistema di prenotazione online per imbarcazioni di lusso, rispondendo alle
esigenze delle imprese del settore terziario di disporre di sistemi efficienti per la gestione della clientela. Questo
repository contiene la componente backend del sistema, sviluppata seguendo le specifiche del project work che richiedeva
l'utilizzo di Python per la creazione di API che gestiscano le logiche di prenotazione.

Il sistema è stato progettato per essere intuitivo e di facile utilizzo, implementando le best practices di sviluppo
software e garantendo un'esperienza utente ottimale attraverso API REST ben strutturate.

## 🛠️ Tecnologie Principali

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

</div>

## ⚙️ Funzionalità Implementate

<div align="center">

| Funzionalità          | Descrizione                                            |
|-----------------------|--------------------------------------------------------|
| 🔐 **Autenticazione** | Sistema di autenticazione e autorizzazione utenti      |
| 📅 **Prenotazioni**   | Gestione completa del ciclo di vita delle prenotazioni |
| 🚤 **Catalogo**       | Gestione del catalogo delle imbarcazioni disponibili   |
| 📚 **Documentazione** | API documentate attraverso OpenAPI/Swagger             |

</div>

## 📖 Documentazione API

La documentazione completa delle API è accessibile attraverso l'interfaccia Swagger UI, disponibile all'indirizzo
`/docs` dopo l'avvio del server.

## 👨‍💻 Sviluppato da

<div align="center">

**Giuseppe Jari Pappalardo**  
Matricola: 0312300959  
Università Telematica Pegaso  
Corso di Laurea in Informatica per le Aziende Digitali

</div>

## 📄 Licenza

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Questo progetto è distribuito con licenza MIT. Vedere il file `LICENSE` per maggiori dettagli.

</div>

## ⚙️ Configurazione

È necessario avere installato **Python 3.12** o una versione successiva per garantire il corretto funzionamento del
backend.

Prima di avviare il backend, è necessario installare tutte le dipendenze richieste. Nella root folder del progetto,
eseguire il seguente comando:

```bash
pip install -r requirements.txt
```


È necessario definire le variabili d'ambiente per il corretto funzionamento del backend. Si consiglia di creare un file
`environment.sh` o comunque assicurarsi che le seguenti variabili siano disponibili nel contesto di esecuzione:

```shell
export DB_USER={db_user}
export DB_PASSWORD={db_password}
export DB_HOST={host}
export DB_PORT=3306
export DB_NAME=acqualux
export ENVIRONMENT_NAME=dev
export JWT_SECRET_KEY=secret
export JWT_ALGORITHM=HS256
export JWT_ACCESS_TOKEN_EXPIRE_MINUTES=3600
```

Dopo aver inserito le informazioni all'interno del file, eseguire il comando:

```bash
source config/environment.sh
```

## 🚀 Avvio del Backend

Per avviare il backend, assicurarsi che tutte le variabili d'ambiente siano correttamente configurate come descritto
nella sezione sopra. Una volta fatto ciò, utilizzare il seguente comando:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Questo comando avvierà il server FastAPI in modalità di sviluppo, rendendo il backend disponibile all'indirizzo
`http://127.0.0.1:8000`. L'opzione `--reload` consente di applicare automaticamente le modifiche al codice senza la
necessità di riavviare manualmente il server.
