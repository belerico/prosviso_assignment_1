# Studenti

* Luca Brena, matricola: 808216
* Federico Belotti, matricola: 808708

# Tecnologie utilizzate

* Containerization: Docker
* Provisioning: Docker Compose / Kubernetes
* CI: Gitlab CI
* CD: Jenkins

# Struttura progetto

Abbiamo creato tre container Docker, contenenti:

* Nginx: reserve-proxy, load-balancer e fornitore di contenuti statici (html, css, js, ...)
* uWSGI + Flask: uWSGI web server che ospita una semplice applicazione Flask
* Redis: database key-value

