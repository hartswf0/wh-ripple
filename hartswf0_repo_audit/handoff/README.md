# hartswf0 Creator Trail Handoff

## Purpose

This bundle summarizes the authored GitHub trail for Watson Hartsoe / Loom Mason across the local `hartswf0` repo audit.

It is meant to help fill out repo genome patches, year-in-review cards, creator-trail analysis, and project lineage notes.

## Authorship Filter

Included author identities:

- Loom Mason <user@example.com>
- Watson Hartsoe <watson.hartsoe@gmail.com>

The point is to avoid imported, forked, or vendor history dominating the analysis.

## Main Files

### mine_repo_heat.tsv

Repo-level authored touch counts.

Use this to identify the repos that received the most repeated human return.

Columns:

- touches
- repo

### mine_edit_heat.tsv

File-level authored touch counts.

Use this to identify files repeatedly modified by the creator.

Columns:

- touches
- repo
- path

### mine_hot_organs.tsv

Combined pressure-point score.

Use this as the primary "hot organs" file. It combines edit heat and code body size.

Columns:

- score
- touches
- lines
- bytes
- repo
- path

Interpretation:

- high touches = repeated return
- high lines = thick code body
- high score = file is both substantial and repeatedly worked

### mine_code_mass.tsv

Largest authored code files touched by the included identities.

Use this to identify thick executable surfaces.

Columns:

- lines
- bytes
- repo
- path

### mine_debug_authors_seen.tsv

Debug file showing author identities found during the audit.

Use this to confirm authorship filtering.

## Initial Reading

The creator trail clusters around these major organs:

1. MOTO / VOLHOLLA
   - music, album, song, mandalla, and publishing-interface surfaces

2. TRACTOR-DCE-GYO / WAG
   - object-world construction, courage/grace tools, brickfilm/editor experiments

3. RIPPLE / ABC-FLIX / ICARO
   - browser motion instruments, frame buses, ripple/tunnel/harness systems

4. CORE-AGE / COURAGE
   - symbolic genome, sequence genome, courage-trail, pattern glossary

5. SENSE-RITUAL / ISLAND-ECOLOGY
   - ritual interface, garden/stone surfaces, ecological narrative bridges

## Recommended Next Use

For each repo patch, fill:

- timeline_genome
- artifact_genome
- program_theory_capsule
- creator_trail_genome
- lineage_genome

Use `mine_repo_heat.tsv` to decide which repos deserve deeper patches first.

Use `mine_hot_organs.tsv` to decide which files deserve direct inspection.

## Warning

Do not treat largest file as most important.

A large file may be generated or one-off.
A repeatedly touched file may be a true creator-trail pressure point.
The strongest signal is: authored + recent + repeatedly touched + substantial.

