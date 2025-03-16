# Readme

## Struktura aplikacji
- folder `src` zawiera kod źródłowy
- `redis`
  - folder dla plików związanych z redisem
  - `redis` trzyma wyniki zadań
  - jest też brokerem i backendem dla `celery`
- `backend`
  - folder dla plików związanych z logiką wykonania zadania
  - w celu zapewnienia skalowalności i konfiguracji pracy na wątkach wybrałem aplikację `celery`
  - plik `celery.py` zawiera zdefiniowana apkę `Celery`
  - pliki `struct.py` oraz `result.py` zawierają klasy z logiką endpointów
  - ilość wątków można zmienić w pliku `src/backend/Dockerfile`, w linii `CMD`, parametr `--autoscale`
- `api`
  - folder dla plików związanych z interfejsem api
  - zdefiniwoane są dwa endpointy wg specyfikacji z maila
  - api jest wystawiane na port 1111 (mozna zmienić w `docker-compose.yaml` i `src/api/Dockerfile`)
  - swagger jest dostępny pod urlem `/docs`
- `common`
  - pliki przydante w różnych miesjcach
- `resources`
  - pliki konfiguracyjne oraz prompty
  

## Logika strukturyzacji adresu
- wykorzystany jest pakiet `langchain` oraz dostawca llm `openai`
- do transformacji stringu w słownik z podanymi kluczami wykorzystałem klasę `PydanticOutputParser`
- w dalszych pracach można by było obsłużyć przypadek, gdy dostaje się tekst nie związany z danymi adresowymi


## Quick Start (Docker, Ubuntu)
- uruchomić kontenery za pomocą `docker-compose`
```commandline
docker compose build && docker compose up
```
- aby załadowac wprwoadzone zmiany
```commandline
docker compose down
docker compose build && docker compose up
```
