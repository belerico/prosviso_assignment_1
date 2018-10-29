### Studenti

* Luca Brena, matricola: 808216
* Federico Belotti, matricola: 808708

### Descrizione progetto

Il progetto consiste in un'applicazione web in cui, dato uno username, questa mostra quante volte tale username ha visitato la pagina. Vengono inoltre messe a disposizione delle semplici API per operare con i dati.

### Tecnologie utilizzate

* Containerization: Docker
* Provisioning: Docker Compose / Kubernetes
* CI/CD: Gitlab CI

### Struttura progetto

Abbiamo creato quattro container Docker, contenenti:

* Nginx: reserve-proxy, load-balancer e fornitore di contenuti statici (html, css, js, ...)
* uWSGI + Flask: uWSGI web server che ospita una semplice applicazione Flask
* uWSGI + Flask API: web server che ospita una semplice API per operare con i dati
* Redis: database key-value

L'architettura è la seguente:

* Nginx <--> uWSGI + Flask <--> Flask API <--> Redis

Le richieste del client vengono prese in carico da Nginx che si occupa di reindirizzarle al web server uWSGI o all'API o, se è stato richiesto un contenuto statico, lo fornisce esso stesso.

### Note

Allo stato attuale il provisioning è gestito da `docker-compose`. Per diversificare le tecnologie stiamo sviluppando una versione complementare che utilizza Kubernetes.
