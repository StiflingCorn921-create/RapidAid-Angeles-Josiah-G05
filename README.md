# RapidAid: Database-Driven Emergency First Aid Guidance and Incident Response System

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x%20%2F%206.x-green.svg)](https://www.djangoproject.com/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20Supabase-336791.svg)](https://www.postgresql.org/)

---

## Project Overview
**RapidAid** is a database-driven emergency response and readiness web platform developed to bridge the critical gap between medical emergencies and professional help. When critical emergencies strike, bystanders often freeze or apply improper techniques due to panic and a lack of structured guidance. RapidAid delivers dynamic, rule-based first-aid protocols (CPR, choking, seizures, bleeding) and equipment tracking (AED locator) powered by a relational backend.

Built on **Django** and **PostgreSQL (Supabase)**, the platform manages structured emergency workflows through dynamic relational tables for categories, protocol steps, incident audit logs, and AED hardware registries. It supports full CRUD operations, strict data integrity constraints (composite ordering, validation checks), and multi-table analytical reporting on emergency response times, incident types, and bystander protocol completion rates.

---

## Problem Statement
During acute medical emergencies, the initial minutes are critical to victim survival. Untrained or panicked bystanders frequently hesitate, freeze, or administer incorrect aid—such as improper CPR compression rates or harmful positioning during seizures—often exacerbating injuries before Emergency Medical Services (EMS) arrive.

Furthermore, existing reference materials are static and lack structured tracking, preventing emergency coordinators from analyzing incident frequency, common response errors, and life-saving equipment availability. There is an urgent need for a database-backed system that delivers structured, standardized first-aid instructions in real time while recording, tracking, and analyzing emergency response actions and community equipment readiness.

---

## Objectives

### General Objective
To design and develop a secure, relational database-driven web platform using Python, Django, and PostgreSQL that provides real-time, guided emergency first-aid protocols, manages emergency device registries, logs response actions, and generates multi-table incident analytics to improve emergency care outcomes.

### Specific Objectives
1. **Relational Database Design**: Design and implement a relational database schema comprising at least 7 interconnected tables with primary keys, foreign keys, unique constraints, and check constraints to manage emergency categories, protocols, sequential action steps, incident logs, and AED registries.
2. **Full Protocol & Device CRUD**: Implement full CRUD functionality allowing administrators to configure, update, and archive medical guidance protocols and AED locations, while enabling users to search, filter, and retrieve emergency guidance based on symptoms and urgency levels.
3. **Dynamic Incident Logging Engine**: Develop a dynamic incident logging engine that records bystander response actions, timestamps, and step completions in real time to ensure reliable emergency data tracking.
4. **Analytical Reporting Modules**: Build analytical reporting modules that query across multiple tables to generate summaries on emergency response durations, protocol completion rates, and regional emergency incident frequencies.

---

## Target Users & Stakeholders

| Role | Description |
| :--- | :--- |
| **Everyday Bystanders / General Public** | Untrained or minimally trained individuals who need real-time, guided first-aid steps during critical emergencies (e.g., CPR, choking, seizures, severe bleeding). |
| **Certified First Responders / Health Officers** | Users who log incident response details, locate life-saving equipment (AEDs), and document field actions. |
| **System Administrators / Medical Coordinators** | Personnel who manage, update, and audit first-aid protocol data, sequential steps, category classifications, and emergency equipment registries. |

---

## Scope & Limitations

### Scope
- **User Management & Role-Based Access Control (RBAC)**: Implements registration, profile management, and role-based permissions distinguishing between Bystanders, Certified First Responders, and System Administrators.
- **Protocol & Step Administration (CRUD)**: Administrative modules to create, view, edit, categorize, and sequence standardized first-aid protocols along with their ordered action steps.
- **Rule-Based Emergency Guidance Engine**: Interactive decision-support workflow for bystanders to filter symptoms, identify emergency scenarios, and follow time-tracked, step-by-step instructions in real time.
- **Incident Reporting & Step Audit Trail**: Enables users and responders to log emergency incidents, track physical location details, and record time-stamped actions taken across each protocol step.
- **Equipped Facility & AED Station Locator**: Searchable directory and map reference of verified institutions (campuses, transit terminals, malls, clinics) tracking internal equipment placement (e.g., floor, lobby, security desk), contact information, and operating hours.
- **Practice Drills & Simulation Module**: Allows users to conduct offline-capable training drills outside of real emergencies, capturing response times and scoring accuracy.
- **Multi-Table Relational Reporting**: Generates summary and analytical reports querying across incidents, protocols, and facility resources to evaluate response durations, protocol completion rates, and emergency category trends.

### Limitations
- **Rule-Based Guidance Only**: Operates strictly on deterministic relational decision rules and established references (Red Cross and WHO) rather than dynamic AI or machine-learning diagnostic models.
- **No Municipal Dispatch Integration**: Emergency contact features supply directory details and local call triggers without direct API or telecommunication links to municipal 911 or hospital computer-aided dispatch networks.
- **Simulated Hardware and Facility Data**: Equipment availability and institutional facility listings are managed using simulated database records rather than live IoT sensor telemetry.
- **Simulated Testing Environment**: Platform verification is restricted to simulated usability scenarios and drill evaluations, excluding deployment during live, clinical medical emergencies.
- **Single-Language Interface**: The initial release is limited strictly to an English-language user interface and dataset.

---

## Technology Stack
- **Backend**: Python 3.12+, Django (MVT architecture)
- **Database**: PostgreSQL / Supabase
- **Frontend**: HTML5, Django Templates, Bootstrap 5 CDN
- **Version Control**: Git & GitHub
