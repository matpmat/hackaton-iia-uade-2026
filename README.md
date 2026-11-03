# M06 · ¿Rotamos a este jugador?

**Integrantes:** Matias Pellegrini (grupo de un integrante)
**IA declarada:** Claude
**Pista:** Reglas
**Publicación en LinkedIn:** <link>

---

## 1. Formulación y PEAS

**La pregunta.** Para cada jugador en una semana, ¿va a sufrir una lesión muscular en los 14 días siguientes? **SÍ** significa: el sistema anticipa la lesión y recomienda al cuerpo técnico **rotarlo** (que descanse en la próxima fecha). NO significa: puede jugar.

| PEAS | Su sistema |
|---|---|
| Medida de rendimiento | Sensibilidad (de los jugadores que se lesionaron, cuántos detectó), con la precisión y la especificidad como control de cuántos titulares se rotan sin necesidad. Medido sobre casos que el sistema no vio (prueba). |
| Entorno | El plantel de un club de Primera, semana a semana, antes de cada fecha: la carga de partidos y entrenamientos de cada jugador y su descanso. |
| Actuadores | Emitir una recomendación por jugador (SÍ = rotar / NO = puede jugar) al cuerpo técnico y al preparador físico, que toman la decisión final. |
| Sensores | Tres datos de la semana previa, todos registrados antes de decidir: minutos jugados en los últimos 7 días, distancia a alta intensidad (GPS, km en la semana) y sueño promedio (h por noche). |

**Objetivo y métrica.** El **objetivo** real es tener a los jugadores disponibles: perder la menor cantidad de semanas de jugador por lesión sin dejar al equipo sin titulares de más. La **métrica** con la que lo medimos es la **sensibilidad**, controlada con precisión y especificidad. **No son lo mismo:** la sensibilidad se puede llevar al 100 % rotando a todo el plantel todas las semanas, cosa que cumple la métrica y traiciona el objetivo (el equipo juega sin titulares). Por eso nunca la miramos sola: siempre junto con la precisión y la especificidad. Tampoco usamos la exactitud como métrica principal, porque con tan pocas lesiones un sistema que dice siempre NO ya saca una exactitud alta (sección 5).

## 2. El sistema

**Cómo decide.** Cuatro reglas si‑entonces, evaluadas en orden:

- **R1:** SI minutos jugados (últimos 7 días) ≥ 90 ENTONCES `carga_alta`
- **R2:** SI distancia a alta intensidad (km en la semana) ≥ 2,7 ENTONCES `esfuerzo_alto`
- **R3:** SI sueño promedio < 8,0 h ENTONCES `recuperacion_baja`
- **R4:** SI `carga_alta` Y `esfuerzo_alto` Y `recuperacion_baja` ENTONCES **SÍ: rotar**. En cualquier otro caso, **NO**.

La idea futbolera detrás: un jugador se lesiona cuando **acumula mucha carga, con mucho esfuerzo de alta intensidad y sin recuperarse bien**. Si falta cualquiera de las tres, el riesgo baja.

**Variables que usa y por qué.** Usa las tres variables de la ficha, y las tres se conocen **antes** de decidir (son datos de la semana que ya pasó), así que el sistema no usa información del futuro.
- **Minutos:** solos no alcanzan. El caso 9 jugó 339 minutos y no se lesionó (su esfuerzo de alta intensidad fue bajo).
- **Distancia a alta intensidad:** sola tampoco. Los casos 3, 10 y 11 corrieron más de 3,4 km y no se lesionaron, porque casi no jugaron.
- **Sueño:** separa un caso que de otro modo sería falsa alarma. El caso 12 tiene carga y esfuerzo altos (230 min, 3,4 km) pero duerme 8,9 h, y no se lesionó.

**Cómo se eligieron los umbrales (solo con los casos 1–14).** Para cada variable pusimos el corte en el punto medio entre los casos de entrenamiento que había que separar, para dejar margen y no quedar pegados a un caso puntual:
- Minutos: el lesionado con menos minutos tiene 155 y los no lesionados con esfuerzo alto y poco sueño tienen como mucho 30 → corte en **90**.
- Distancia: los lesionados tienen 3,4 km o más; los no lesionados con muchos minutos y poco sueño, como mucho 2,1 → corte en **2,7** (punto medio ≈ 2,75).
- Sueño: los lesionados duermen como mucho 7,1 h; el caso 12, 8,9 h → corte en **8,0**.

Los casos 15–20 no se miraron para construir el sistema; solo para medirlo.

**Cómo se corre en vivo.** Con un caso nuevo, a mano y en tres preguntas:
1. ¿Jugó 90 minutos o más en los últimos 7 días?
2. ¿Corrió 2,7 km o más a alta intensidad en la semana?
3. ¿Durmió menos de 8 horas por noche en promedio?

Si las tres son SÍ → **SÍ, rotar**. Si alguna es NO → **NO, puede jugar**.
También está en `sistema_M06.py`: `python sistema_M06.py <minutos> <distancia> <sueño>` (por ejemplo `python sistema_M06.py 200 3.1 6.5`), y sin argumentos recalcula las matrices de abajo desde `datos/M06.csv`.

**Dos casos de ejemplo.**

| Caso inventado | Valores | Salida del sistema |
|---|---|---|
| A | 200 min · 3,1 km · 6,5 h | SÍ (las tres condiciones se cumplen) |
| B | 250 min · 3,5 km · 8,4 h | NO (mucha carga, pero duerme 8 h o más) |

## 3. Medición

**Entrenamiento (casos 1–14)**

| | Predice SÍ | Predice NO |
|---|---|---|
| **Real SÍ** | VP = 2 | FN = 0 |
| **Real NO** | FP = 0 | VN = 12 |

Control: 2 + 0 + 0 + 12 = 14. Lesionados reales: casos 1 y 2 (VP + FN = 2).

**Prueba (casos 15–20)**

| | Predice SÍ | Predice NO |
|---|---|---|
| **Real SÍ** | VP = 1 | FN = 0 |
| **Real NO** | FP = 1 | VN = 4 |

Control: 1 + 0 + 1 + 4 = 6. Lesionado real: caso 20 (detectado). Falsa alarma: caso 18 (122 min · 3,8 km · 5,7 h).

| Métrica | Entrenamiento | Prueba |
|---|---|---|
| Exactitud | (2 + 12) / 14 = 100 % | (1 + 4) / 6 = 83,3 % |
| Precisión | 2 / (2 + 0) = 100 % | 1 / (1 + 1) = 50 % |
| Sensibilidad | 2 / (2 + 0) = 100 % | 1 / (1 + 0) = 100 % |
| Especificidad | 12 / (12 + 0) = 100 % | 4 / (4 + 1) = 80 % |

**Entrenamiento contra prueba.** Sí hay diferencia: en entrenamiento acierta todo y en prueba aparece una falsa alarma (caso 18), así que la precisión cae de 100 % a 50 % y la especificidad a 80 %. Es una señal de **sobreajuste leve**: con solo 2 lesionados en entrenamiento, cualquier regla razonable los separa perfecto, y el 100 % de entrenamiento dice poco. Lo que sí **generaliza** es lo que más importa: la sensibilidad se mantiene en 100 % (detecta al único lesionado de prueba). Igual hay que leerlo con cuidado: la sensibilidad de prueba está calculada sobre **un solo caso positivo**, así que con un lesionado distinto podría haber dado 0 %. Con 20 casos no se puede afirmar que el sistema funciona; solo que no falla en estos.

El caso 18 es la falsa alarma más entendible: corrió muchísimo a alta intensidad (3,8 km) y durmió poco; tiene el perfil de riesgo aunque no se lesionó.

## 4. El error más caro

<¿Es peor el falso positivo o el falso negativo en su problema? ¿Por qué, según la ficha? ¿Qué cambiaron en el sistema para cometer menos ese error?>

## 5. ¿Comparado contra qué?

**Línea base trivial.** <Qué resultado saca un sistema que responde siempre lo mismo, y cómo se compara el suyo.>

| Checklist (Clase 6) | Respuesta |
|---|---|
| ¿Qué datos? | <> |
| ¿Qué métrica? | <> |
| ¿Comparado contra qué? | <> |
| ¿Quién lo midió? | <> |

## 6. Riesgo: el camino completo

<Datos → modelo → decisión → consecuencia aplicado a su caso. Al menos un riesgo concreto.>

## 7. Bitácora

**Uso de la IA**

| # | Qué le pedimos | Qué aceptamos | Qué rechazamos y por qué |
|---|---|---|---|
| 1 | <> | <> | <> |

**Corridas contra el evaluador**

| Corrida | Nota | Agujero que encontró | Qué cambiamos |
|---|---|---|---|
| 1 | <> | <> | <> |
