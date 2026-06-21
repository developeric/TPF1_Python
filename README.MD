# 🏠 Valuador Inmobiliario — Cotizador Inteligente de Propiedades

Aplicación web de *Machine Learning* que predice el precio de mercado de una propiedad a partir de sus características (área, habitaciones, ubicación, etc.). El modelo fue entrenado con **regresión lineal** y alcanza un coeficiente de determinación (R²) del **96%**.

El proyecto combina un **backend en FastAPI** que sirve el modelo entrenado y un **frontend en HTML + Tailwind CSS** que consume la API en tiempo real.

---

## 📋 Tabla de contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Requisitos previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Ejecución](#-ejecución)
- [Uso de la API](#-uso-de-la-api)
- [Solución de problemas](#-solución-de-problemas)
- [Créditos](#-créditos)

---

## ✨ Características

- 🔮 **Predicción en tiempo real** del precio de una propiedad.
- 🧠 Modelo de **regresión lineal** pre-entrenado (R² ≈ 0.96) cargado desde archivos `.pkl`.
- 🚀 **API REST** construida con FastAPI, con validación automática de datos vía Pydantic.
- 🎨 **Frontend responsivo** con Tailwind CSS, servido por el mismo backend.
- 🌐 **CORS habilitado** para permitir el consumo desde cualquier origen durante el desarrollo.
- 📄 **Documentación interactiva** automática (Swagger UI) en `/docs`.

---

## 🏗 Arquitectura

```
┌──────────────────┐      POST /predecir       ┌──────────────────────┐
│   index.html     │  ───────────────────────► │     FastAPI (main)   │
│  (Frontend JS)   │                            │                      │
│                  │  ◄─────────────────────── │  ┌────────────────┐  │
└──────────────────┘     { precio_estimado }    │  │ modelo_casas   │  │
                                                 │  │     .pkl       │  │
                                                 │  └────────────────┘  │
                                                 │  ┌────────────────┐  │
                                                 │  │ columnas_modelo│  │
                                                 │  │     .pkl       │  │
                                                 │  └────────────────┘  │
                                                 └──────────────────────┘
```

**Flujo:**
1. El usuario completa el formulario en `index.html`.
2. El frontend envía un `POST /predecir` con los datos en formato JSON.
3. FastAPI valida los datos con el modelo `CasaInput` (Pydantic).
4. Los datos se transforman a un `DataFrame`, se aplican variables *dummy* (`get_dummies`) y se reindexan según las columnas del entrenamiento.
5. El modelo predice el precio y devuelve el resultado.

---

## 🛠 Tecnologías

| Componente   | Tecnología                                  |
|--------------|---------------------------------------------|
| Backend      | Python 3.14 · FastAPI · Uvicorn             |
| ML / Datos   | scikit-learn · pandas · numpy · joblib      |
| Validación   | Pydantic                                    |
| Frontend     | HTML · Tailwind CSS (CDN) · JavaScript (Fetch API) |
| Gestor de paquetes | uv                                    |

---

## 📁 Estructura del proyecto

```
TPF1_Python/
├── main.py                      # Aplicación FastAPI (endpoints y lógica de predicción)
├── index.html                   # Frontend (formulario + consumo de la API)
├── requirements.txt             # Dependencias del proyecto
├── models/
│   ├── modelo_casas.pkl         # Modelo de regresión lineal entrenado
│   └── columnas_modelo.pkl      # Columnas usadas en el entrenamiento (para alinear el input)
├── .gitignore
└── README.MD
```

> **Nota:** Los archivos `main.ipynb` y `dataset.csv` (notebook de entrenamiento y dataset) están excluidos del repositorio vía `.gitignore`. El servidor solo necesita los `.pkl` para funcionar.

---

## ✅ Requisitos previos

- **Python 3.14** (o compatible con las versiones de `requirements.txt`).
- **[uv](https://docs.astral.sh/uv/)** como gestor de paquetes.

### Instalar `uv` (Windows / PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Luego reiniciá la terminal o agregá `uv` al PATH de la sesión actual:

```powershell
$env:Path = "C:\Users\<TU_USUARIO>\.local\bin;$env:Path"
```

---

## 📦 Instalación

Desde la carpeta del proyecto, instalá las dependencias:

```powershell
uv pip install -r requirements.txt
```

Esto instala todo en el entorno virtual `.venv`.

---

## ▶ Ejecución

**1. Activá el entorno virtual:**

```powershell
.\.venv\Scripts\Activate.ps1
```

> Si tu `.venv` está en la carpeta padre, ajustá la ruta:
> `..\.venv\Scripts\Activate.ps1`

**2. Levantá el servidor:**

```powershell
uvicorn main:app --reload
```

**3. Abrí la aplicación en el navegador:**

- 🌐 Aplicación: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📚 Documentación interactiva (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

> 💡 **Alternativa sin activar el venv:** `uv run uvicorn main:app --reload`

---

## 🔌 Uso de la API

### `GET /`
Devuelve la página principal (`index.html`).

### `POST /predecir`
Recibe las características de una propiedad y devuelve el precio estimado.

**Cuerpo de la petición (JSON):**

```json
{
  "Area_SqFt": 1800,
  "Rooms": 3,
  "Build_Year": 2018,
  "Location": "Jaipur",
  "Street_Type": "Main Road",
  "Furnishing": "Semi-Furnished",
  "Property_Type": "Villa",
  "Has_Pool": "Yes"
}
```

**Campos:**

| Campo           | Tipo    | Descripción                  | Valores posibles |
|-----------------|---------|------------------------------|------------------|
| `Area_SqFt`     | float   | Área en pies cuadrados       | numérico         |
| `Rooms`         | float   | Cantidad de habitaciones     | numérico         |
| `Build_Year`    | int     | Año de construcción          | numérico         |
| `Location`      | str     | Ciudad                       | Jaipur, Gurugram, Indore, Kanpur, Lucknow, Noida, Prayagraj |
| `Street_Type`   | str     | Tipo de calle                | Main Road, Gated Society, Highway Facing, Residential Lane |
| `Furnishing`    | str     | Nivel de amueblado           | Semi-Furnished, Unfurnished, Furnished |
| `Property_Type` | str     | Tipo de propiedad            | Villa, Duplex, Independent House |
| `Has_Pool`      | str     | ¿Tiene pileta?               | Yes, No          |

**Respuesta (JSON):**

```json
{
  "mensaje": "Predicción exitosa",
  "precio_estimado": 4520000.75
}
```

**Ejemplo con `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/predecir" \
  -H "Content-Type: application/json" \
  -d "{\"Area_SqFt\":1800,\"Rooms\":3,\"Build_Year\":2018,\"Location\":\"Jaipur\",\"Street_Type\":\"Main Road\",\"Furnishing\":\"Semi-Furnished\",\"Property_Type\":\"Villa\",\"Has_Pool\":\"Yes\"}"
```

---

## 🩺 Solución de problemas

| Problema | Causa | Solución |
|----------|-------|----------|
| `uv : El término 'uv' no se reconoce...` | `uv` no está en el PATH | Reiniciá la terminal o ejecutá `$env:Path = "C:\Users\<USUARIO>\.local\bin;$env:Path"` |
| `uvicorn : El término 'uvicorn' no se reconoce...` | El entorno virtual no está activado | Activá el venv con `.\.venv\Scripts\Activate.ps1` o usá `uv run uvicorn main:app --reload` |
| El frontend muestra "Error" / alerta de conexión | El servidor FastAPI no está corriendo | Asegurate de que `uvicorn` esté activo antes de usar el formulario |
| `No se pudo ejecutar Activate.ps1` | Política de ejecución de PowerShell | Ejecutá `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |

---

## 🙌 Créditos

Trabajo Práctico Final — Programación en Python.

> **Aclaración:** Se usó Google Gemini y trabajos previamente realizados para flexibilizar el desarrollo y el deployment del proyecto. El **frontend** está hecho íntegramente con IA.
