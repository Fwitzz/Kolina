# Kolina – Linux assistenten til kommuner og offentlige institutioner

Kolina er en letvægts, privatlivsvenlig Linux-assistent bygget med Python og GTK3. Den er udviklet til at hjælpe kommunale ansatte og nye brugere under overgangen fra Windows til Linux. Kolina anvender Mistral AI som samtalemodel og slår pakker op i Ubuntu's officielle repositories.

Hvis du gerne vil have appen som en applikation i app launcheren, skal du selv compile den med rigtige API keys og alt det vigtige.

## Indhold
- [Installation](#installation)
- [Sæt din Mistral API-nøgle op](#sæt-din-mistral-api-nøgle-op)
- [Ubuntu Pakkeopslag](#ubuntu-pakkeopslag)
- [Privatliv og Datasikkerhed](#privatliv-og-datasikkerhed)
- [Licens](#licens)

---

## Installation

Appen er ikke færdigudviklet, og distribueres manuelt. Den kan køres direkte fra kildekoden:

```bash
git clone https://github.com/fwitzz/kolina.git
cd kolina
python3 main.py
```

**Kræver:** `python3`, `python3-gi`, `GTK3`, `requests`

---

## Sæt din Mistral API-nøgle op

Før Kolina kan fungere, skal du bruge en Mistral API-nøgle fra [mistral.ai](https://mistral.ai).

### Trin 1: Opret `.env` fil

Opret en `.env` fil i projektets rodmappe med følgende indhold:

```
MISTRAL_API_KEY=indsæt-din-nøgle-her
```

### Trin 2: Sæt nøglen når du starter appen

Hvis du starter Kolina manuelt, kan du eksportere nøglen sådan her:

```bash
export $(grep -v '^#' .env | xargs)
python3 main.py
```

Denne kommando: 

```bash
python3 main.py
```

burde køre appen, men for at køre den fra app-launcheren, skal du køre denne fra Root-directory (~/kolina):

```bash
kolina
```

Hvis du bruger en `.desktop`-fil til at starte appen, kan du også skrive:

```bash
export MISTRAL_API_KEY=indsæt-din-nøgle-her
```

i din startkommando.

Du kan også sætte den til din PATH, for nemmere tilgang.

Du skal desuden ændre filen kolina som sidder i:

```bash
usr/local/bin/kolina
```

Du skal indsætte din egen API-Nøgle i linjen der starter med "export", og fjerne linjen der starter med "echo".

```bash

#!/bin/bash
cd /usr/share/kolina || exit 1

# TEMP: hardcode key so it always works when launched from icon
echo "Please set MISTRAL_API_KEY in your environment."
# Or change this key to your own.
export MISTRAL_API_KEY="Insert your key here."


exec python3 main.py
```

Med disse ændringer, burde appen køre.

---

## Ubuntu Pakkeopslag

Kolina opdager automatisk, hvis du skriver spørgsmål om pakkeinstallation, og bruger Launchpad's API til at vise officielle beskrivelser og kommandoer.

---

## Privatliv og Datasikkerhed

* Ingen data bliver gemt, logget eller indsamlet
* Bruger Mistral AI som samtalemotor
* Afviser at hjælpe med irrelevante eller usikre forespørgsler
* Henviser til IT-afdelingen ved tvivl

---

## Licens

MIT License
