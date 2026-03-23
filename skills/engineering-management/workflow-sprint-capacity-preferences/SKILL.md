---
name: workflow-sprint-capacity-preferences
description: Sprint Capacity Preferences
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Sprint Capacity Preferences

Configuration for the `sprint-capacity-plan` workflow. Updated automatically after each run.

---

## Jira Config

| Setting | Value |
|---------|-------|
| Cloud ID | *(populated on first run via `getAccessibleAtlassianResources`)* |
| Project Key | `TI` |
| Board ID | `284` (Combined — scrum board with active sprints) |
| Pod Filter | Learning Value Agent, Learning Platform, Infrastructure, Arch, Pod 1, Pod 2, UX |
| Pod Custom Field | `customfield_10138` (multi-select; values like "Pod 1", "Infrastructure") |
| Story Points Field | `customfield_10037` |
| Sprint Field | `customfield_10020` (array of sprint objects) |

---

## Google Sheets Webhook

| Setting | Value |
|---------|-------|
| Deploy ID | `AKfycbxuxvCiDwT3FaDIsPGN_Vk3DZk3gPK0CIoyAs4n2DSKrNcY2aYJRgG7EqecJD2xEktbcA` |
| Webhook URL | `https://script.google.com/a/macros/thoughtindustries.com/s/AKfycbxuxvCiDwT3FaDIsPGN_Vk3DZk3gPK0CIoyAs4n2DSKrNcY2aYJRgG7EqecJD2xEktbcA/exec` |

Use this URL when configuring Jira Automation rules (Issue Created, Issue Updated, Sprint events).

---

## Sprint Config

| Setting | Value |
|---------|-------|
| Sprint length (days) | 14 |
| Default capacity (SP) | 13 |

---

## Team Roster

Fill in your team. The workflow uses this to compute capacity and match engineers to pods. Capacity is split by role: Fullstack (dev), SRE (infra/ops), DE (data), QA (testing), and UX (design).

| Engineer | Pod(s) | Fullstack SP | SRE SP | DE SP | QA SP | UX SP | Notes |
|----------|--------|-------------|--------|-------|-------|-------|-------|
| *(Example) Alice Smith* | *Pod 1* | *18* | *0* | *0* | *0* | *0* | *Fullstack dev* |
| *(Example) Bob Jones* | *Pod 2, Infrastructure* | *8* | *5* | *0* | *0* | *0* | *Cross-pod; 8 FS to Pod 2, 5 SRE to Infra* |
| *(Example) Carol Lee* | *Pod 1* | *0* | *0* | *0* | *18* | *0* | *QA engineer (cross-cutting)* |
| *(Example) Dave Kim* | *Data Engineering* | *0* | *0* | *13* | *0* | *0* | *Data engineer* |
| *(Example) Eve Park* | *UX* | *0* | *0* | *0* | *0* | *13* | *UX designer* |

**Cross-pod engineers:** List all pods comma-separated. Add a note describing the split. The capacity-planning skill defines how to handle this.

**Capacity type → Pod mapping:**

| Capacity type | Pods it covers | Jira LOE field |
|---|---|---|
| **Fullstack SP** | Pod 1, Pod 2, Architecture, LVA, LP | Est Dev LOE (`customfield_10066`) |
| **SRE SP** | Infrastructure | Story Points on infra issues |
| **DE SP** | Data Engineering | Story Points on DE issues |
| **QA SP** | All pods (cross-cutting) | Est Testing LOE (`customfield_10067`) |
| **UX SP** | UX | Est UX LOE (`customfield_10412`) or SP on UX-tagged issues |

---

## Pod Definitions

| Pod | Capacity type | Description |
|-----|---------------|-------------|
| Pod 1 | Fullstack | Feature development |
| Pod 2 | Fullstack | Feature development |
| Learning Value Agent | Fullstack | LVA feature development |
| Learning Platform | Fullstack | LP feature development |
| Architecture | Fullstack | Platform architecture and design |
| Infrastructure | SRE | DevOps, infra, CI/CD, SRE |
| Data Engineering | DE | Data pipelines, analytics, data platform |
| UX | UX | UX/design work |

---

## Previous Run History

Updated automatically after each run. Used for delta reporting.

| Run Date | Sprints Covered | Total SP | Team Capacity | Utilization % | Over-allocated | Unassigned SP |
|----------|-----------------|----------|---------------|---------------|----------------|---------------|
| *(no runs yet)* | | | | | | |
