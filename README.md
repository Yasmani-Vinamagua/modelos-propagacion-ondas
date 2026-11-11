
# 📡 MODELTEC

### Calculadora de modelos de propagación de ondas de radio

Aplicación de escritorio desarrollada en **Python** para calcular
y analizar las pérdidas de propagación de señales inalámbricas
mediante seis modelos matemáticos.

Diseñada para estudiantes, docentes e ingenieros de
telecomunicaciones.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f6feb)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🖥️ Vista previa

![Interfaz de MODELTEC](screen.png)

## ✨ Características

- 📡 **6 modelos de propagación** para el análisis de señales.
- 🧮 **Cálculo inverso:** despeja frecuencia, distancia,
  altura de antenas y otras variables compatibles.
- 📊 **Resultados en tiempo real:** cálculos con unidades.
- ✅ **Validación de parámetros:** rangos y errores claros.
- 🎨 **Interfaz moderna:** diseño Liquid Glass.
- 🖥️ **Aplicación de escritorio:** desarrollada con Python.

## 📶 Modelos disponibles

| Modelo | Aplicación principal |
|---|---|
| Okumura-Hata | Propagación en entornos urbanos y suburbanos |
| COST-231 Hata | Redes celulares en bandas superiores |
| Walfisch-Ikegami | Análisis de pérdidas por componentes |
| COST-231 Walfisch-Ikegami LOS | Propagación con línea de vista |
| Egli | Estimación empírica de pérdidas |
| Log-Normal | Atenuación según distancia y variabilidad |

## 🚀 Inicio rápido

```bash
git clone https://github.com/Yasmani-Vinamagua/modelos-propagacion-ondas.git

cd modelos-propagacion-ondas

pip install -r requirements.txt

python "modulos python/main.py"
```

> Requiere Python 3.10 o superior y Tkinter.
