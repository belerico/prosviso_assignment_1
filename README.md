### Studenti

* Luca Brena, matricola: 808216
* Federico Belotti, matricola: 808708

### Descrizione progetto

Il progetto consiste in un'applicazione web in cui, dato uno username, questa mostra quante volte tale username ha visitato la pagina.\n

### Tecnologie utilizzate

* Containerization: Docker
* Provisioning: Docker Compose / Kubernetes
* CI: Gitlab CI
* CD: Jenkins

### Struttura progetto

Abbiamo creato tre container Docker, contenenti:

* Nginx: reserve-proxy, load-balancer e fornitore di contenuti statici (html, css, js, ...)
* uWSGI + Flask: uWSGI web server che ospita una semplice applicazione Flask
* Redis: database key-value

Le richieste del client vengono prese in carico da Nginx che si occupa di reindirizzarle o al web server uWSGI o, se è stato richiesto un contenuto statico, lo fornisce esso stesso.

### Note

Allo stato attuale il provisioning è gestito da `docker-compose`. Per diversificare le tecnologie stiamo sviluppando una versione complementare che utilizza Kubernetes.
