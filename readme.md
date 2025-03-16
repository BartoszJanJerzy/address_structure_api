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

## Ograniczenia, wnioski, itd
- aplikacja jest dosyc mocno rozbudowana jak na tak prosta funkcjonalność (redis, celery, fastapi)
  - chciałem mieć pewność, że wszystkie wymagania są spełnione
- domyślnie ustawiłem ilość wątków w `Celery` na min 10 (max 100) tak aby spełnić wymaganie dot. min 10ciu równoczesnych requestów
  - oczywiście maszyna musi obsłuzyć 10 workerów
- logika strukturyzacji adresu jest tutaj dosyć prosta
  - nie zakładałem (a można) żadnego etapu analizy podanego tekstu w inpucie
  - nie zakładałem (a można) obsługi przypadków, gdy podany tekst nie ma informacji adresowych lub ma sporo szumu (np. niepotrzebnych informacji)
  - nie zakładałem (a można) różnicowania języków, w którym podany jest tekst wejściowy
- wybrałem OpenAI oraz model `gpt-4o`, ponieważ na nich najczęściej pracowałem
  - mozna potencjalnie sparametryzować uruchaianie llm i testowac różnych dostawców i modele
- napisałem kilka testów jednostkowych (zrozumiałem że jest to wymagane)
  - oczywiście mozna mocniej otestować aplikację, uzyć większej ilości funkcjonalności pakietu `pytest`
  - uznałem że na cele ćwiczeniowe to co jest wystarczy   
