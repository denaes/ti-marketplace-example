---
name: workflow-guide-me-to-experiment-design-and-measurement
description: >
  Design experiments, instrumentation spec, dashboard requirements, and analyze results. Uses
  measure-experiment-design, measure-instrumentation-spec, measure-dashboard-requirements,
  measure-experiment-results, ab-test-analysis.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Experiment design and measurement

Design experiments (A/B or other), define instrumentation and dashboard requirements, and analyze experiment results. Use when validating a hypothesis, shipping an experiment, or interpreting test data.

## When to Use

- You need to **design an experiment** (hypothesis, variants, success metrics, sample size)
- You need **instrumentation specs** (events, properties) for engineering or analytics
- You need **dashboard requirements** for monitoring the experiment or feature
- You have **experiment results** and need analysis (significance, recommendation)

## Prerequisites

- Input: hypothesis or feature to test; or raw experiment data/results
- Skills: `skills/product/data-analytics/measure-experiment-design/SKILL.md`, `skills/product/data-analytics/measure-instrumentation-spec/SKILL.md`, `skills/product/data-analytics/measure-dashboard-requirements/SKILL.md`, `skills/product/data-analytics/measure-experiment-results/SKILL.md`, `skills/product/data-analytics/ab-test-analysis/SKILL.md`

## Step 1: Clarify goal and inputs

1. **Confirm with the user:** Design only, instrumentation only, dashboard only, or analyze results?
2. **Design path:** Do they have a hypothesis (from discovery or define-hypothesis)? What is the success metric and minimum detectable effect?
3. **Analysis path:** Do they have result data (counts, conversion, segments)? Format (table, CSV, summary)?

## Step 2: Experiment design (if applicable)

1. Read **measure-experiment-design** and its references (EXAMPLE, TEMPLATE).
2. Produce: hypothesis, variants, primary metric, guardrail metrics, sample size / duration, success criteria (e.g. significance level, decision rule).
3. Output as a short doc (markdown or table) the user can share with eng/analytics.

## Step 3: Instrumentation and dashboard (if applicable)

1. **Instrumentation** — Read **measure-instrumentation-spec**. List events, properties, and context needed for the experiment (or feature). Align with existing taxonomy if the user has one.
2. **Dashboard** — Read **measure-dashboard-requirements**. List required charts, filters, segments, and refresh cadence. Output as a short spec for eng or BI.

## Step 4: Analyze results (if applicable)

1. Read **measure-experiment-results** and **ab-test-analysis**.
2. If the user provided raw data, run through the analysis: sample size check, significance, confidence intervals, segment breakdown if relevant.
3. Produce a recommendation: ship winner, extend test, or stop, with short rationale.

## Step 5: Output and next steps

1. Write outputs to files (e.g. `workspace/_notes/YYYY-MM-DD_experiment-design.md`, `YYYY-MM-DD_instrumentation-spec.md`, `YYYY-MM-DD_experiment-results.md`).
2. Tell the user how to hand off to engineering (instrumentation, dashboard) or stakeholders (results).

## References

- Conventions: `standards/conventions.md`
- Define hypothesis: `skills/product/discovery/define-hypothesis/SKILL.md`
