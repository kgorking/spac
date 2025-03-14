# Cereal API
Implementation af et API der behandler morgenmadsprodukter.

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

`/api/cereal`: Hent alle morgenmadsprodukter som en liste af dictionaries

`/api/cereal/create`: Opret en ny morgenmad. `name` og `mfr` er påkrævet.

`/api/cereal/update`: Opdater en eksisterende morgenmad.

`/api/cereal/delete/<id>`: Deletes an existing cereal

`/api/cereal/login`: Log in with username and password. A default user 'user' exists with password 'password'

`/api/cereal/logout`: Logs out the user

`/api/image/<id>`: Returns the image of the cereal id

## Filtering
Use url arguments to filter on certain key-value pairs. You can specify multiple filters.

`api/cereal?calories=50` will return all cereals that have 50 calories.

## Sorting
Use the url argument `sort` to sort on a certain key.

`api/cereal?sort=fat` will return all cereals sorted by their fat content.

