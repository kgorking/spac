# PDF downloader
Simpelt script til at downloade pdf filer, hvis url addresser hentes fra en Excel fil.

## F�r brug
K�r `pip install -r requirements.txt`, evt. i et virtual environment.

## K�rsel
Brug kommandoen `py dlpdf.py "excel-fil" "output-folder"`, hvor
* `excel-fil` er stien til excel filen der skal tr�kkes links ud af.
* `output-folder` er mappen hvor pdf-filerne gemmes, fx. `./downloads`

Hvis ingen argumenter er angivet, benyttes der standard argumenter, som st�r i .py filen.