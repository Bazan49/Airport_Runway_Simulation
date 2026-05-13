Simulación basada en eventos discretos de un aeropuerto con múltiples pistas de aterrizaje. Esta implementación modela el comportamiento de las llegadas de aeronaves, la asignación de runways y la ocupación secuencial del servicio, con el fin de analizar la utilización y el tiempo ocioso de las pistas durante un horizonte temporal definido.

## Idea general

- Se simula un sistema de colas con múltiples servidores idénticos (pistas de aterrizaje).
- Las aeronaves llegan siguiendo un proceso de llegadas aleatorias con tiempos exponenciales.
- Cada aeronave ocupa una pista por un tiempo de servicio compuesto, que incluye:
  - Reabastecimiento de combustible
  - Aterrizaje y despegue
  - Carga/descarga opcional
  - Reparación opcional por avería
- El objetivo es estimar estadísticas de inactividad de las pistas.

## Archivos principales

- `src/parallel_servers_simulation.py`
  - Implementa la simulación del sistema de colas paralelo.
  - Gestiona eventos de llegada y salida, la cola FIFO y el estado de cada servidor.

- `src/rv_generators.py`
  - Contiene generadores de variables aleatorias.
  - Incluye distribución exponencial y distribución normal por Box-Müller.

- `src/solution.py`
  - Define el modelo específico de aeropuerto y ejecuta la simulación.
  - Configura el número de pistas, el horizonte semanal y repeticiones para alcanzar precisión.
  - Muestra resultados de tiempo ocioso promedio y error estándar por pista.

## Requisitos

- Python 3.x 

## Uso

1. Clonar el repositorio:

```bash
git clone https://github.com/Bazan49/Airport_Runway_Simulation.git
cd Airport_Runway_Simulation
```

2. Ejecutar la simulación:

```bash
python src/solution.py
```

La salida muestra el número de réplicas necesarias, la media de arribos semanales y los tiempos de inactividad de cada pista.

## Informe

El informe completo del proyecto, con la descripción del problema, el modelo desarrollado y el análisis estadístico de los resultados, está disponible en simulation_report.pdf.

## Acerca de

Proyecto desarrollado para la asignatura **Simulación**, Universidad de La Habana.
