# M06 · ¿Rotamos a este jugador?

**Integrantes:** Matias Pellegrini (grupo de un integrante)
**IA declarada:** Claude
**Pista:** Reglas
**Publicación en LinkedIn:** https://lnkd.in/p/d56rFA5a

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
- Minutos: el lesionado con menos minutos tiene 155 y los no lesionados con esfuerzo alto y poco sueño tienen como mucho 30 → punto medio 92,5, redondeado hacia abajo a **90**.
- Distancia: los lesionados tienen 3,4 km o más; los no lesionados con muchos minutos y poco sueño, como mucho 2,1 → punto medio 2,75, redondeado hacia abajo a **2,7**.
- Sueño: los lesionados duermen como mucho 7,1 h; el caso 12, 8,9 h → punto medio exacto **8,0**.

Cuando el punto medio no es un número redondo, siempre redondeamos **hacia el lado que detecta más lesiones** (minutos y distancia hacia abajo), por el criterio del error más caro (sección 4).

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

Según la ficha, el **falso negativo es el más caro**: no rotar a quien se lesiona hace perder al jugador **tres o cuatro semanas**, mientras que el falso positivo (rotar a quien no se iba a lesionar) cuesta **un partido** sin ese titular. Un FN cuesta varias veces lo que un FP.

**Qué cambiamos por eso.** En el umbral de minutos, cualquier corte entre 31 y 155 separaba perfecto el entrenamiento. La opción obvia era poner el corte justo debajo del lesionado (150), pero queda pegado al caso 2 (155): un jugador con el mismo perfil y 145 minutos no sería detectado. Por eso cambiamos a un método con margen, el **punto medio** entre los casos a separar (92,5 minutos), y lo redondeamos **hacia abajo** a 90, no hacia arriba, para inclinar el sistema a **detectar más lesiones aunque dé más falsas alarmas**, que es el error barato. 90 no se aparta del método: es el punto medio redondeado con el mismo criterio de costo. Lo mismo hicimos con la distancia (2,75 → 2,7).

Esa decisión tiene un costo visible: en prueba produjo una falsa alarma (caso 18, con 122 minutos). Con 150 minutos la prueba habría salido perfecta, pero **no podemos elegir el umbral mirando la prueba**: eso sería usar los casos 15–20 para construir el sistema y la medición dejaría de valer. Aceptamos esa falsa alarma como el precio de no dejar pasar lesiones.

**¿Cuánto cuestan las falsas alarmas en una temporada?** En los 17 casos sin lesión de la ficha, el sistema dio 1 falsa alarma (≈ 6 %); solo en prueba, 1 de 5 (20 %). Tomando ese rango, por cada 100 semanas de jugadores sanos el sistema rotaría por error entre 6 y 20 veces, y cada error cuesta un partido sin ese titular. Como ejemplo hipotético, 11 titulares durante 30 fechas son 330 semanas‑jugador: entre unas 20 y 65 rotaciones innecesarias. Parece mucho, pero la cuenta que importa es la otra: una lesión no detectada cuesta 3 o 4 partidos, así que **evitar una sola lesión compensa 3 o 4 rotaciones de más**. Con la precisión de prueba (50 %), por cada lesión evitada hay una rotación innecesaria: el sistema sale ganando. Igual, con 20 casos este número es muy incierto, y el SÍ debería tomarse como alerta para el preparador físico, no como rotación automática.

## 5. ¿Comparado contra qué?

**Línea base trivial.** Un sistema que dice **siempre NO** (nunca rota a nadie):
- Entrenamiento: 12 / 14 = **85,7 %** de exactitud, sensibilidad **0 %**.
- Prueba: 5 / 6 = **83,3 %** de exactitud, sensibilidad **0 %**.

En prueba **nuestra exactitud (83,3 %) es igual a la de la línea base**. Por eso la exactitud no sirve para decir si el sistema es bueno: la "neurona tonta" que no mira ningún dato saca lo mismo. La diferencia está en lo que importa: la línea base **no detecta ninguna lesión** (sensibilidad 0 %), y nuestro sistema detecta la única que hubo (100 %), a cambio de una falsa alarma. El otro extremo, **siempre SÍ**, tiene sensibilidad 100 % pero precisión 1 / 6 = 16,7 % y especificidad 0 %: rota al plantel entero. Nuestro sistema logra la misma sensibilidad con 50 % de precisión y 80 % de especificidad.

| Checklist (Clase 6) | Respuesta |
|---|---|
| ¿Qué datos? | Los 20 casos inventados de la ficha M06 (14 de entrenamiento, 6 de prueba). Solo 3 lesionados en total. No son datos reales de un plantel. |
| ¿Qué métrica? | Sensibilidad como principal, con precisión y especificidad como control. La exactitud se informa pero no se usa para decidir. |
| ¿Comparado contra qué? | Contra la línea base "siempre NO" (misma exactitud en prueba, 0 % de sensibilidad) y contra "siempre SÍ" (misma sensibilidad, mucha peor precisión). |
| ¿Quién lo midió? | El propio grupo, sobre los datos de la ficha, a mano y verificado con `sistema_M06.py`. No hubo una medición independiente ni con datos nuevos. |

## 6. Riesgo: el camino completo

**Datos → modelo → decisión → consecuencia.**

- **Datos:** 20 casos inventados con solo 3 lesiones, y el sueño es un dato que en la práctica **reporta el propio jugador**.
- **Modelo:** tres umbrales aprendidos de apenas 2 lesionados de entrenamiento.
- **Decisión:** el cuerpo técnico rota (o no) a un jugador según la recomendación.
- **Consecuencia:** el jugador se pierde (o juega) la fecha.

**Riesgo concreto.** Como la regla exige dormir menos de 8 horas, un jugador que quiere jugar puede **declarar que duerme más** y el sistema nunca lo va a marcar, aunque tenga carga y esfuerzo altísimos: el dato autorreportado se puede manipular justo para evitar la decisión que el sistema toma. Si eso pasa, el FN aparece en el peor caso: el jugador más cargado sigue jugando y se lesiona tres o cuatro semanas. Mitigación: tratar el SÍ como alerta para el preparador físico (no como decisión automática), contrastar el sueño con un dato medido (pulsera o control del club) y revisar al jugador con carga y esfuerzo altos aunque duerma bien.

Además, la regla tiene un punto ciego por construcción: un jugador que se lesiona **con poca carga** (por ejemplo, volviendo de una lesión anterior) nunca va a ser marcado, porque esa situación no aparece en los datos.

## 7. Bitácora

**Uso de la IA**

| # | Qué le pedimos | Qué aceptamos | Qué rechazamos y por qué |
|---|---|---|---|
| 1 | Identificar cuál era nuestra ficha entre las problemáticas de la comisión. | La lista de fichas de fútbol de la comisión mañana con su dominio e IA declarada. | La idea de "DT Virtual" como nuestro dominio: la IA aclaró que ese nombre lo había propuesto ella en conversaciones anteriores y que no aparece en ninguna ficha. Trabajamos sobre M06. |
| 2 | Proponer el sistema para M06 y elegir la pista. | Reglas si‑entonces con tres condiciones encadenadas, porque se pueden correr a mano en la mesa y explicar sin IA. | Usar solo minutos y distancia: el caso 12 (mucha carga, pero duerme 8,9 h) quedaba como falsa alarma. Agregamos el sueño. |
| 3 | Elegir los umbrales. | Puntos medios calculados solo con los casos 1–14. | El corte de 150 minutos, aunque daba la prueba perfecta: queda pegado al caso 2 y elegirlo por la prueba sería usar los datos de prueba para construir. Elegimos 90 para priorizar la sensibilidad. |
| 4 | Calcular las matrices y las métricas. | Las cuentas, después de verificarlas a mano caso por caso y con el script. | La exactitud como métrica principal: en prueba es igual a la de la línea base "siempre NO". |
| 5 | Cambiar la IA declarada en el README a Claude. | Poner Claude, que es la IA con la que hicimos todo el trabajo del hackatón. | Nada, pero la IA nos advirtió que la ficha M06 figura con ChatGPT como IA declarada. Lo dejamos registrado acá para explicar la diferencia. |
| 6 | Ayudarnos a encontrar nuestra ficha, porque no teníamos anotado el código de grupo que se proyectó al inicio. | Trabajar sobre M06, la ficha cuyo dominio (fútbol, cuerpo técnico) era el más parecido al que veníamos trabajando con la IA. | Dar por segura la elección: la IA advirtió que M06 figura con otra IA declarada, y el evaluador marcó que integrantes e IA no coinciden con la ficha. Lo consultamos con el docente: la diferencia se debe a que la ficha figura con ChatGPT y trabajamos con Claude, y nos confirmó que no hay problema en cambiarlo. |

**Corridas contra el evaluador**

| Corrida | Nota | Agujero que encontró | Qué cambiamos |
|---|---|---|---|
| 1 | 9,5 | ¿Por qué 90 minutos y no el punto medio, si ese era el método? | Aclaramos que 90 es el punto medio (92,5) redondeado hacia abajo por el error más caro, y lo dejamos explícito para los tres umbrales. Agregamos el costo de las falsas alarmas por temporada y registramos en la bitácora cómo llegamos a la ficha M06 y a la IA declarada. |
