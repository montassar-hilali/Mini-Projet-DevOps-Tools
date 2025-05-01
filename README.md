Système de réservation de salle de réunion
=======
L'application web est développée avec le framework Python Flask et la base de données SQLite3. Son système de connexion est simple, la réservation s'effectuant par authentification. Un compte administrateur est créé par défaut, avec le nom d'utilisateur : admin et le mot de passe : admin. L'administrateur peut gérer directement l'équipe et les utilisateurs.

## Prérequis
1. Python 3.6, [Anaconda](https://anaconda.org/anaconda/python) recommandé
2. Installer SQLite3 depuis [Ici](http://www.sqlite.org/download.html)
3. Navigateur SQLite recommandé [Disponible](http://sqlitebrowser.org/)

## Configuration
1. Installer Flask et les paquets
```
$ pip install flask
$ pip install flask-wtf
$ pip install flask-sqlalchemy
$ pip install flask-migrate
$ pip install flask-login
```
2. Définir le projet
```
$ export FLASK_APP=lab2.py
```

3. Initialiser la base de données
```
$ flask db init
```

## Migration des données
1. Exécuter la commande de migration depuis le répertoire du projet pour créer Tables
```
$ flask db upgrade
```
2. Remplir la base de données avec des données factices (si elles n'ont pas été renseignées après la migration)
```
$ python populate.py
```

# Exécution
1. Exécuter l'application Flask depuis le répertoire du projet, en localhost
```
$ flask run
```
2. Ouvrir l'application dans un navigateur : [localhost](http://127.0.0.1:5000/)
"# Mini-Projet-DevOps-Tools"