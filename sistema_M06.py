"""
M06 · ¿Rotamos a este jugador?  —  Pista: Reglas
Sistema de reglas si-entonces. Predice SÍ = "el jugador sufre una lesión
muscular en los 14 días siguientes" (=> recomendar rotarlo).

Uso:
  - En vivo, con un caso nuevo:   python sistema_M06.py 200 3.1 6.5
  - Medición sobre la ficha:      python sistema_M06.py   (lee datos/M06.csv)
"""
import csv
import sys

# Umbrales elegidos SOLO con los casos 1-14 (entrenamiento)
MIN_MINUTOS = 90      # minutos jugados en los últimos 7 días
MIN_DISTANCIA = 2.7   # km a alta intensidad en la semana
MAX_SUENO = 8.0       # horas de sueño promedio por noche (debe ser MENOR)


def predecir(minutos, distancia, sueno):
    """Devuelve 1 (SÍ, rotar) o 0 (NO). Las tres reglas se evalúan en orden."""
    carga_alta = minutos >= MIN_MINUTOS                    # R1
    esfuerzo_alto = distancia >= MIN_DISTANCIA             # R2
    recuperacion_baja = sueno < MAX_SUENO                  # R3
    return 1 if (carga_alta and esfuerzo_alto and recuperacion_baja) else 0  # R4


def matriz(filas):
    vp = fn = fp = vn = 0
    for f in filas:
        pred, real = f["pred"], f["real"]
        if pred == 1 and real == 1: vp += 1
        elif pred == 0 and real == 1: fn += 1
        elif pred == 1 and real == 0: fp += 1
        else: vn += 1
    return vp, fn, fp, vn


def pct(num, den):
    return "indefinida" if den == 0 else f"{100 * num / den:.1f} %"


def medir(ruta="datos/M06.csv"):
    with open(ruta, encoding="utf-8-sig") as fh:
        lector = csv.reader(fh)
        next(lector)
        datos = []
        for caso, conj, m, d, s, r in lector:
            m, d, s, r = float(m), float(d), float(s), int(r)
            datos.append({"caso": int(caso), "conj": conj, "pred": predecir(m, d, s),
                          "real": r, "vals": (m, d, s)})

    for conj in ("entrenamiento", "prueba"):
        filas = [x for x in datos if x["conj"] == conj]
        print(f"\n== {conj.upper()} ==")
        for x in filas:
            m, d, s = x["vals"]
            print(f"Caso {x['caso']:>2}: min={m:>5.0f} dist={d:.1f} sueño={s:.1f} -> "
                  f"pred={'SÍ' if x['pred'] else 'NO'} real={'SÍ' if x['real'] else 'NO'}")
        vp, fn, fp, vn = matriz(filas)
        n = len(filas)
        print(f"VP={vp} FN={fn} FP={fp} VN={vn}  (total {n})")
        print(f"Exactitud     {pct(vp + vn, n)}")
        print(f"Precisión     {pct(vp, vp + fp)}")
        print(f"Sensibilidad  {pct(vp, vp + fn)}")
        print(f"Especificidad {pct(vn, vn + fp)}")
        negativos = vn + fp
        print(f"Línea base 'siempre NO': {pct(negativos, n)}")


if __name__ == "__main__":
    if len(sys.argv) == 4:
        m, d, s = map(float, sys.argv[1:])
        print("SÍ: rotar al jugador" if predecir(m, d, s) else "NO: puede jugar")
    else:
        medir(sys.argv[1] if len(sys.argv) == 2 else "datos/M06.csv")
