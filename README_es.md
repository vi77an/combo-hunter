<div align="center">

```
⠀⠀⠀⠀⠀⠀⠀⠠⡧⠀⠀⠄⠀⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡄⠀⠀⠀⢺⠂⠀⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧
⠤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣿⠇⠀⢿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⠶⠶
⠀⠀⠘⢿⣿⣿⣟⠛⠛⠛⠛
⠀⠀⠁⠀⠈⠛⣿⣿⣦     ✧ combo hunter | a filter tool ✧
⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿            coded by t.me/vi77an
```

**combo hunter** · herramienta de filtrado y limpieza de combo lists

![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey?style=flat-square)

</div>

**🌐 Traducciones:** [Portugués](README.md) · [Inglés](README_en.md)

---

## acerca de

**combo hunter** es un script Python de línea de comandos para filtrar y formatear grandes archivos de combo lists (`.txt`). Soporta búsqueda por dominio, correo electrónico, usuario o URL, con una barra de progreso en tiempo real y procesamiento paralelo automático para archivos grandes.

---

## estructura de carpetas

```
proyecto/
├── combo_hunter.py       ← script principal
├── combos/               ← coloca aquí tus archivos .txt para búsqueda
├── limpar/               ← coloca aquí los archivos .txt para formatear
└── resultados/
    ├── dominios/         ← resultados de búsquedas por dominio
    ├── emails/           ← resultados de búsquedas por correo
    ├── usuarios/         ← resultados de búsquedas por usuario
    ├── urls/             ← resultados de búsquedas por URL
    └── limpos/           ← archivos formateados por el modo limpiar
```

> Las carpetas se crean automáticamente al iniciar el script.

---

## requisitos

- Python 3.8 o superior
- sin dependencias externas — solo biblioteca estándar

```bash
python --version   # debe retornar 3.8+
```

---

## uso

```bash
python combo_hunter.py
```

El script abre un menú interactivo con dos modos:

### modo 1 — buscar

Filtra líneas de un archivo `.txt` por un término de búsqueda. Cuatro tipos disponibles:

| tipo | descripción | ejemplo de coincidencia |
|------|-------------|------------------------|
| **dominio** | campo de dominio/sitio antes del login | `netflix.com:user:pass` |
| **correo** | dirección de correo completa en la línea | `user@gmail.com:pass` |
| **usuario** | campo de login/usuario | `juan123:contraseña` |
| **url** | cualquier ocurrencia del término en la línea | `https://netflix.com/...` |

Los resultados se guardan en `resultados/<tipo>/<término>@<cantidad>_<fecha>.csv`.

### modo 2 — limpiar

Reformatea archivos en el patrón `url:login:contraseña`. Tres opciones de salida:

| opción | entrada | salida |
|--------|---------|--------|
| `1` | `https://site.com:user:pass` | `user:pass` |
| `2` | cualquiera | mantiene líneas con URL, preserva las demás |
| `3` | cualquiera | mantiene el original sin cambios |

---

## formatos soportados

El script reconoce automáticamente los siguientes formatos de línea:

```
https://site.com:login:contraseña      ← url:login:contraseña
http://site.com:login:contraseña       ← url:login:contraseña (http)
login:contraseña                       ← log:pass
login@dominio.com:contraseña           ← email:pass
```

---

## rendimiento

El script adapta su estrategia de búsqueda según el tamaño del archivo:

- **archivos pequeños** (< 200.000 líneas): búsqueda lineal con barra de progreso
- **archivos grandes** (≥ 200.000 líneas): búsqueda paralela usando todos los núcleos disponibles (`multiprocessing.Pool`)

En ambos casos la barra de progreso se actualiza en tiempo real mostrando coincidencias encontradas, porcentaje y tiempo transcurrido.

---

## salida

Los archivos de resultado se guardan en formato `.csv` con el siguiente patrón de nombre:

```
<término>@<cantidad>_<YYYYMMDD_HHMMSS>.csv
```

Ejemplo: `netflix@1523_20240315_142301.csv`

La primera línea de cada archivo contiene un comentario de créditos. Las demás contienen las entradas encontradas, una por línea.

---

## créditos

desarrollado con 🩷 por [vilanele](https://t.me/vi77an)
