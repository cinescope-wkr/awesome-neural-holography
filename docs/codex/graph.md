# Codex Graph

This project is already more than a paper list. It is a structured codex of papers, method
families, display constraints, labs, software, and subtopics that point to one another. A graph
view should expose those relationships, not replace the readable survey.

## Design Goals

1. Keep the codex as the canonical long-form view.
2. Make graph views derived, typed, filterable, and local-first.
3. Model scientific relationships explicitly instead of treating every link as the same.
4. Let users move between papers, methods, labs, systems, and software without losing context.
5. Avoid the "hairball graph" problem by favoring constrained views over one giant force cloud.

## Core Entities

The graph should be built from a small set of typed nodes that match how this repository is
already organized.

| Entity | Purpose | Example fields |
| --- | --- | --- |
| `paper` | Individual publications and talks | `title`, `year`, `venue`, `authors`, `summary`, `links` |
| `method_family` | Algorithm families and taxonomic buckets | `label`, `summary`, `parent_family` |
| `system_topic` | Display-side constraints or subtopics | `label`, `summary`, `scope` |
| `lab` | Academic or industry groups | `name`, `kind`, `institution`, `homepage` |
| `software` | Reusable codebases and frameworks | `name`, `repo`, `stack`, `scope` |
| `concept` | Cross-cutting ideas such as `ASM`, `CITL`, `phase-only SLM`, `etendue` | `label`, `kind`, `summary` |

That set is enough to start. `researcher`, `dataset`, or `hardware_platform` can be added later if
the codex grows in those directions.

## Metadata Schema

The key is to add structure without forcing the whole project into one-file-per-paper immediately.
For this repository, the cleanest path is:

1. Keep [`README.md`](../readme.md) as the canonical survey text.
2. Add machine-readable sidecar metadata for entries we want in the graph first.
3. Generate a single graph artifact for the docs site.

A paper entry could look like this:

```yaml
id: liang-2021-tensor-holography
type: paper
title: Towards real-time photorealistic 3D holography with deep neural networks
year: 2021
venue: Nature
authors:
  - Liang Shi
  - Wojciech Matusik
labs:
  - mit-cdfg
method_families:
  - learned-hologram-synthesis
system_topics:
  - near-eye-display
concepts:
  - asm
  - phase-only-slm
  - real-time-cgh
links:
  paper: https://cdfg.mit.edu/publications/tensor-holography
summary: Directly predicts holograms with a learned model under an idealized propagation assumption.
```

A method-family entry could look like this:

```yaml
id: learned-hologram-synthesis
type: method_family
label: Learned Hologram Synthesis
parent_family: cgh-algorithms
summary: Neural networks directly predict holograms or intermediate complex fields.
representative_entries:
  - liang-2021-tensor-holography
  - eybposh-2020-deepcgh
```

## Typed Relations

This is where the codex becomes meaningfully better than a generic backlink graph. Relations should
have names that reflect scientific structure.

| Relation | Source -> Target | Meaning |
| --- | --- | --- |
| `belongs_to_family` | `paper -> method_family` | A paper sits inside a method taxonomy |
| `targets_topic` | `paper/software -> system_topic` | A work addresses a system bottleneck or display concern |
| `uses_concept` | `paper/software -> concept` | A work depends on a concept, assumption, or hardware abstraction |
| `from_lab` | `paper -> lab` | A work is tied to a research group |
| `released_as` | `paper -> software` | A paper has a public codebase or framework |
| `extends` | `paper -> paper` | A later work builds on a prior work |
| `compares_with` | `paper -> paper` | A work is a meaningful comparison target |
| `influences` | `paper/method_family -> paper/method_family` | A higher-level intellectual lineage link |
| `supports` | `software -> method_family/system_topic` | A tool is relevant to a family of methods or systems |

The important constraint is that we should not use one vague `related_to` edge when a more precise
edge exists. Typed edges are what make filtering, styling, and local exploration useful.

## Recommended Views

The graph should be multi-view, not singular.

### Local Graph

The default view for any entry page. Show:

- the current node
- its direct typed neighbors
- one-hop expansions on demand

This is the most useful everyday graph because it stays interpretable.

### Method Graph

A family-centered view that answers:

- which papers belong to a method family
- which concepts they assume
- which display topics they target

This is the right graph for `Traditional Heuristic Methods`, `Iterative Methods`, `Learned
Propagation Model Methods`, and `Learned Hologram Synthesis Methods`.

### System Graph

A display-side view connecting:

- bottlenecks such as speckle, etendue, HOEs, compression, or higher-order diffraction
- papers that address them
- labs and software that repeatedly appear around them

This is where the repository becomes more than a pure algorithm survey.

### Community Graph

A community-centered view connecting:

- labs
- seminal papers
- software artifacts
- topic clusters

This is especially good for newcomers trying to understand where different research threads come
from.

## UX Guardrails

If we borrow from Obsidian, we should borrow its discipline, not just its aesthetics.

1. Search-first, graph-second. Users should arrive through a page, query, or filter.
2. Local neighborhoods by default. Do not open with the entire repository graph.
3. Typed color and shape encoding. Papers, labs, software, and concepts should not look identical.
4. Edge filtering. Users should be able to hide `compares_with` edges and keep `belongs_to_family`
   or `from_lab`.
5. Stable layouts. Node positions should not completely reshuffle on every interaction.
6. Progressive disclosure. Expand neighbors intentionally instead of showing everything at once.

## Rendering Strategy

The browser layer should stay lightweight even if the codex grows.

- Use Canvas or WebGL, not SVG, for dense graph views.
- Run force simulation or layout updates off the main thread when possible.
- Precompute initial positions or cluster anchors during the docs build.
- Keep the number of visible nodes capped in default views.
- Favor filtered subgraphs over full-repository global layouts.

For this repository, a pragmatic stack would be:

- a build step that emits `graph.json`
- a client page that loads the graph artifact
- a force-directed local view with typed filters and search

## Progressive Adoption Path

This should be introduced in layers rather than as a large rewrite.

### Phase 1: Structured Metadata

- add sidecar metadata for papers, labs, software, and topics
- validate IDs and typed edges
- keep README and docs as they are

### Phase 2: Derived Graph Artifact

- generate `graph.json` from metadata
- derive node labels, colors, and initial layout groups
- surface missing or broken references during build

### Phase 3: Graph Views in Docs

- add a dedicated graph page
- add local graph panels to selected section pages
- let users filter by entity type, year, topic, and relation type

### Phase 4: Codex-native Authoring

- gradually move important entities from plain lists into structured entries
- preserve the readable survey while improving machine-readable structure
- let the graph, section pages, and future dashboards all share the same data layer

## What This Enables

If this is done well, the project can support several powerful workflows:

- tracing the lineage from classical CGH to learned synthesis methods
- jumping from a system bottleneck like speckle to the papers, labs, and tools around it
- finding which labs repeatedly drive a given technical thread
- building dashboards such as "all CITL papers" or "all works targeting near-eye displays"
- making the codex readable in prose while still explorable as a knowledge network

In short, the graph should not be an ornamental visualization layer. It should be a typed,
searchable, filterable projection of the same codex that the survey already expresses in prose.
