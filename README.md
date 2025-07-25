# Kolina – Din Linux Assistent 🇩🇰🐧

Kolina er en letvægts, privatlivsvenlig Linux-assistent bygget med Python og GTK3. Den er udviklet til at hjælpe kommunale ansatte og nye brugere under overgangen fra Windows til Linux. Kolina anvender Mistral AI som samtalemodel og slår pakker op i Ubuntu's officielle repositories.

---

## 🚀 Installation

Appen er stadig under aktiv udvikling og pakkes manuelt. Den kan køres direkte fra kildekoden:

```bash
git clone https://github.com/eigilurfetop/kolina.git
cd kolina
python3 main.py
```

**Kræver:** `python3`, `python3-gi`, `GTK3`, `requests`

---

## 🔑 Sæt din Mistral API-nøgle op

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

Hvis du bruger en `.desktop`-fil til at starte appen, kan du også skrive:

```bash
export MISTRAL_API_KEY=indsæt-din-nøgle-her
```

i din startkommando.

---

## 📆 Ubuntu Pakkeopslag

Kolina opdager automatisk, hvis du skriver spørgsmål om pakkeinstallation, og bruger Launchpad's API til at vise officielle beskrivelser og kommandoer.

---

## 🔐 Privatliv og Datasikkerhed

* Ingen data bliver gemt, logget eller indsamlet
* Bruger Mistral AI som samtalemotor
* Afviser at hjælpe med irrelevante eller usikre forespørgsler
* Henviser til IT-afdelingen ved tvivl

---

## 📜 Licens

MIT License
