# Cereal API
Implementation af et API der behandler morgenmadsprodukter.

## Kørsel
Start serveren med kommandoen `py src/app.py`

## Test
Kør `tests/test_all_endpoints.py` for at teste alle endpoints.

## Endpoints
`/api/cereal/<id>`: Hent morgenmad med `id` som et dictionary.
```
http://localhost:81/api/cereal/2

...

{
  "calories": 120,
  "carbo": 8.0,
  "cups": 1.0,
  "fat": 5,
  "fiber": 2.0,
  "id": 2,
  "mfr": "Q",
  "name": "100% Natural Bran",
  "potass": 135,
  "protein": 3,
  "rating": 0.33983679,
  "shelf": 3,
  "sodium": 15,
  "sugars": 8,
  "type": "C",
  "vitamins": 0,
  "weight": 1.0
}
```

`/api/cereal`: Hent alle morgenmadsprodukter som en liste af dictionaries. Kan filtreres og sorteres.

`/api/cereal/create`: Opret en ny morgenmad. `name` og `mfr` er påkrævet.

`/api/cereal/update`: Opdater en eksisterende morgenmad.

`/api/cereal/delete/<id>`: Slet en morgenmad.

`/api/cereal/login`: Log in med navn og kode. En standard bruger 'user' er oprettet med koden 'password'

`/api/cereal/logout`: Log brugeren ud

`/api/image/<id>`: Hent et billede til den angivne morgenmad

### Filter
`api/cereal?calories=50` returnerer alle morgenmadsprodukter der indeholder 50 kalorier.

### Sortering
Brug `sort` argumentet til at sortere på en nøgle.

`api/cereal?sort=fat` returnerer alle morgenmadsprodukter sorteret efter deres fedtindhold.


# Design
Lavet med:
* Flask, til opsætning af http server
* Flask RESTful, til opsætning af endpoints
* Flask Login, til at håndtere autentifikation
* SQLAlchemy, til at håndtere data tiil/fra databasen
