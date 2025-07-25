# Kolina – Linux-assistenten til kommuner og offentlige institutioner

**Kolina** er en letvægts og privatlivsvenlig Linux-assistent bygget med Python og GTK3. Den er udviklet til at hjælpe kommunale ansatte og nye brugere med overgangen fra Windows til Linux.

Kolina anvender **Mistral AI** som samtalemotor og slår pakker op direkte fra **Ubuntus officielle repositories** via Launchpad API.

> ⚠️ Hvis du ønsker at tilføje Kolina til din app launcher, skal du selv kompilere den med dine egne API-nøgler og tilpasse startscriptet.

---

## Installation

Appen er stadig under aktiv udvikling og distribueres manuelt. Du kan dog køre den direkte fra kildekoden:

```bash
git clone https://github.com/fwitzz/kolina.git
cd kolina
python3 main.py
```

**Krav:** `python3`, `python3-gi`, `GTK3`, `requests`

---

## Opsætning af Mistral API-nøgle

Før Kolina kan fungere, skal du bruge en gratis API-nøgle fra [mistral.ai](https://mistral.ai).

### Trin 1: Opret en `.env`-fil

I projektets rodmappe, opret en fil ved navn `.env` med dette indhold:

```env
MISTRAL_API_KEY=indsæt-din-nøgle-her
```

Eller skriv dette ind i en terminal, men jeg anbefaler det første:
```bash
export MISTRAL_API_KEY="indsæt-din-api-nøgle-her"
```

### Trin 2: Start appen med din nøgle

Hvis du starter appen manuelt:

```bash
export $(grep -v '^#' .env | xargs)
python3 main.py
```

Alternativt kan du sætte miljøvariablen direkte i terminalen:

```bash
export MISTRAL_API_KEY="indsæt-din-nøgle-her"
python3 main.py
```

---

## 📁 Start Kolina fra app-launcher (valgfrit)

Hvis du ønsker at starte Kolina via et ikon i systemets app launcher, skal du justere følgende script:

```bash
sudo nano /usr/local/bin/kolina
```

Erstat følgende i scriptet:

```bash
#!/bin/bash
cd /usr/share/kolina || exit 1

# Fjern denne linje:
echo "Please set MISTRAL_API_KEY in your environment."

# Og indsæt din egen nøgle her:
export MISTRAL_API_KEY="din-api-nøgle"

exec python3 main.py
```

---

## Ubuntu Pakkeopslag

Kolina registrerer automatisk, når brugeren spørger ind til pakkeinstallation. Den bruger Launchpad's API til at finde officielle beskrivelser og kommandoer for Ubuntu-pakker.

---

## Privatliv og Datasikkerhed

* Ingen data bliver gemt, logget eller delt.
* Al databehandling foregår lokalt med Mistral AI som samtalemotor.
* Irrelevante eller potentielt skadelige forespørgsler bliver afvist.
* Henviser altid til IT-afdelingen ved tvivlsspørgsmål.

---

## Licens

Dette projekt er udgivet under [MIT-licensen](LICENSE).
