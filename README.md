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

**Cómo decide.** <Neurona: pesos y sesgo. Reglas: la lista de reglas si‑entonces. Agente: la regla con la que elige la acción.>

**Variables que usa y por qué.** <Cuáles usa, cuáles descarta y por qué.>

**Cómo se corre en vivo.** <Pasos concretos para resolver un caso nuevo: link al Colab, a la planilla o la cuenta a mano.>

**Dos casos de ejemplo.**

| Caso inventado | Valores | Salida del sistema |
|---|---|---|
| A | <…> | <SÍ/NO> |
| B | <…> | <SÍ/NO> |

## 3. Medición

**Entrenamiento (casos 1–14)**

| | Predice SÍ | Predice NO |
|---|---|---|
| **Real SÍ** | VP = <> | FN = <> |
| **Real NO** | FP = <> | VN = <> |

**Prueba (casos 15–20)**

| | Predice SÍ | Predice NO |
|---|---|---|
| **Real SÍ** | VP = <> | FN = <> |
| **Real NO** | FP = <> | VN = <> |

| Métrica | Entrenamiento | Prueba |
|---|---|---|
| Exactitud | <> | <> |
| Precisión | <> | <> |
| Sensibilidad | <> | <> |
| Especificidad | <> | <> |

**Entrenamiento contra prueba.** <¿Hay diferencia? ¿Por qué? ¿Sobreajuste o generalización?>

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
