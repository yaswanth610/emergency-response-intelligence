
# 🚨 Emergency Response Intelligence System

A simulation-driven emergency response decision system that intelligently assigns ambulances and hospitals using road travel time, emergency severity, and hospital capacity.

The project evaluates multiple dispatch strategies against a global optimization approach and measures their performance across hundreds of simulated emergency scenarios.

---

## 🎯 Problem Statement

Emergency response systems must make fast decisions under uncertainty:

- Which ambulance should respond?
- Which route should it take?
- How should critical emergencies be prioritized?
- Which hospital can receive the patient?
- How can multiple emergencies be handled simultaneously?

A simple "nearest ambulance" strategy does not necessarily produce the best overall response.

This project builds a decision-support system that models these decisions and evaluates different strategies using simulated emergency scenarios.

---

## 🧠 Core Idea

The system models a simulated city containing:

- 🚑 Ambulances
- 🏥 Hospitals
- 🚨 Emergency incidents

When an emergency occurs, the system:

1. Detects the emergency severity.
2. Finds available ambulances.
3. Calculates road-based travel routes.
4. Estimates ambulance arrival time.
5. Ranks possible ambulance assignments.
6. Selects a suitable hospital.
7. Considers hospital bed and ICU availability.
8. Supports simultaneous emergency optimization.
9. Evaluates the resulting strategy against baseline approaches.

### High-Level Architecture

```text
                    SIMULATED CITY
                         │
          ┌──────────────┼──────────────┐
          │              │              │
       🚑 Ambulances   🚨 Emergencies   🏥 Hospitals
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                DISPATCH ENGINE
                         │
                         ↓
                 OSRM ROAD ROUTING
                         │
                         ↓
                ETA / DISTANCE ENGINE
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
       AMBULANCE SELECTION    HOSPITAL SELECTION
              │                     │
              └──────────┬──────────┘
                         ↓
                OPTIMIZATION ENGINE
                         │
                         ↓
                 PERFORMANCE EVALUATION
                         │
                         ↓
                  BENCHMARK RESULTS
```
