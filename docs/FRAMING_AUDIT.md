# Framing audit and proposed pivot

## Purpose

The current docs --- the scaffolding paper [`emergent_systems.tex`](emergent_systems.tex)
and the proof-strategy notes in
[`proof_techniques.md`](proof_techniques.md) --- consistently
position the five-slot decomposition as a **descriptive vocabulary** that
**reads existing artificial-life systems** in a common language. The
project-instructions claim ("all artificial life, and subsequently all
general life, arises from a very abstract system structure") is a
**substantively stronger thesis** than what the docs currently argue.

(A previously-existing textbook draft under `docs/textbook/`
articulated the same descriptive stance through preface, ch01–ch09,
and a math primer; that draft was **deleted on 2026-05-11** as part
of this pivot. The framework's downstream work moves to focused
result papers under [`docs/papers/`](papers/) per the existing
papers template.)

This memo:

1. Documents where the weaker framing lives, with `file:line` citations
   so the eventual rewrite has a checklist.
2. Proposes the structural change needed to support the stronger thesis
   --- specifically, taking the observer out of the system tuple and
   recasting it as an external measurement functor.
3. Lays out a staged proof obligation: sufficiency first, then necessity,
   converging on a characterization theorem.
4. Names the new conjecture/axiom set and shows how the existing
   `C1`–`C3` / `OP1`–`OP3` slot into it as lemmas.
5. Itemises the ripple effects across paper, code, and
   `RESULTS.md`.

The memo deliberately stops short of editing any of the source docs;
that pass should happen after this framing is signed off.

---

## Part 1 — Current state diagnosis

The current docs are internally coherent about what the framework
**is** and **is not**. Five passages establish the stance most
explicitly:

### 1.1 The paper

- [`emergent_systems.tex:99`](emergent_systems.tex) (abstract):
  *"The result is a methodology for specifying, comparing, and
  implementing emergent-system models without assuming a single
  substrate, fitness landscape, or observer."*  — A methodology
  framing, not a characterization theorem.
- [`emergent_systems.tex:116`](emergent_systems.tex):
  *"... many of them can be described in terms of five recurring
  roles ..."* — "Many," not "all"; "can be described," not "must
  decompose as."
- [`emergent_systems.tex:121`](emergent_systems.tex):
  *"The proposed framework is intentionally non-prescriptive."*
- [`emergent_systems.tex:124–125`](emergent_systems.tex):
  *"Its purpose is therefore comparative and constructive:
  comparative because it provides a common vocabulary for existing
  traditions ..."* — Existing traditions; not all possible systems.
- [`emergent_systems.tex:1495–1500`](emergent_systems.tex) (Scope and
  Commitments): *"The scaffold stays neutral on ... the metaphysical
  status of agency ... and — critically — the relationship between
  causal emergence and the rest of the framework (left as OP1)."*

### 1.2 The observer-in-tuple problem

The five-tuple
$\mathcal{S}=(\mathbf{X},V,F,T,O)$ in
[`emergent_systems.tex:270–298`](emergent_systems.tex) places the
observer $O$ **inside the system**. The paper hedges this in
prose ([`emergent_systems.tex:745–748`](emergent_systems.tex)):
*"the observer is not another hidden force in the default simulator
loop. It is the measurement apparatus,"* but the typing still has
$O$ as a component of $\mathcal{S}$, not a morphism out of
$\mathcal{S}$. That commits the framework to an internalist reading
of observation, which is incompatible with an "independent observer"
thesis.

### 1.3 Where biology already half-lives

The bridge to **organic** life in the scaffolding paper exists
only briefly: `emergent_systems.tex` mentions biology twice (lines
426, 936) and both times only as a worked example of substrate
composition. The framework's claim to substrate-agnosticism is not
yet cashed out for organic substrates anywhere in the current
documentation.

*Note*: a textbook draft under `docs/textbook/` also articulated
the descriptive-vocabulary stance through preface, ch01–ch09, and
a math primer. That draft was **deleted on 2026-05-11** as part of
this framing pivot; the framework's downstream work moves to a
series of focused result papers under [`docs/papers/`](papers/)
instead. See `CHANGELOG.md` for the deletion record.

### 1.4 The conjecture set is narrowly scoped

Conjectures `C1`–`C3` and open problems `OP1`–`OP3` (paper
[§5.1](emergent_systems.tex), tracked in
[`RESULTS.md`](../RESULTS.md)) all live **within** the descriptive
framework rather than making a claim **about** it:

| ID  | Scope                                                                  | Universal? |
|-----|------------------------------------------------------------------------|------------|
| C1  | Four existing viability formalisms share a closure-operator structure  | No         |
| C2  | Those four lift to hierarchical viability                              | No         |
| C3  | Three existing observer families are divergence functionals            | No         |
| OP1 | Some scaffolded systems exhibit Hoel causal emergence                  | Existence  |
| OP2 | The FEP applies on some substrate–dynamics pairs                       | Scope      |
| OP3 | Multiplex topology is universal among "natural" multi-coupling systems | Universal, but only for topologies |

None of `C1`–`C3` / `OP1`–`OP3` claims that
*every* emergent + open-ended + novel system **must** decompose as
$(\mathbf{X},V,F,T,O)$. That is the missing conjecture.

### 1.5 Summary of the gap

| Axis                       | Current docs                                                 | Project-instructions thesis                                            |
|----------------------------|--------------------------------------------------------------|------------------------------------------------------------------------|
| Status of the 5-slot model | Descriptive vocabulary for existing ALife systems            | Characterization of the category of emergent / open-ended / novel systems |
| Observer                   | Slot $O$ inside $\mathcal{S}=(\mathbf{X},V,F,T,O)$           | External measurement functor on $\mathcal{S}$                          |
| Scope                      | "Existing traditions," "engineered systems"                  | All life, artificial and organic                                       |
| Proof obligations          | Local unifications (`C1`–`C3`) and existence claims (`OP1`)  | Sufficiency, necessity, eventually iff                                 |
| Stance on agency           | "Stays neutral on ... the metaphysical status of agency"     | Agency is what an independent observer ascribes to viable trajectories |

---

## Part 2 — Target framing

### 2.1 The redefinition

Drop the observer from the system tuple. A **substrate-agnostic
emergent system** is now a 4-tuple

$$
\mathcal{S} \;=\; (\mathbf{X},\,V,\,F,\,T),
$$

iterating on the joint state space
$Z = X \times \mathcal{M}_+(X)$ exactly as before, but with **no
observer slot inside $\mathcal{S}$**. The composite tick rule

$$
\widetilde{S}_F \circ \widetilde{V}_T \circ \widetilde{\Phi}
$$

is unchanged. What changes is what we say about $O$.

### 2.2 The independent observer

An **observer** is a morphism

$$
O \;:\; \mathbf{Sys} \longrightarrow \mathbf{Obs},
$$

from the category $\mathbf{Sys}$ of substrate-agnostic emergent
systems (objects: 4-tuples
$(\mathbf{X},V,F,T)$; morphisms: appropriate slot-preserving
maps) to a category $\mathbf{Obs}$ of *observation records* (objects:
measurable spaces of observation traces; morphisms: measurable
maps). Concretely, $O$ sends a system $\mathcal{S}$ to its
trajectory-functor

$$
O(\mathcal{S}) \;:\; \mathbb{N} \;\longrightarrow\; Y,
\qquad t \;\longmapsto\; O_t\big((x_s,\mu_s)_{s\le t}\big),
$$

with the same windowed-or-stateful flexibility we already have
([`emergent_systems.tex:716–743`](emergent_systems.tex)).

Independence is now a property of the morphism, not a property of
the system: $O$ is **independent** of $\mathcal{S}$ if it factors
through the trajectory functor of $\mathcal{S}$ rather than through
any of the slots $V, F, T$. Equivalently, $O$ does not appear in the
right-hand side of the iteration rule. Novelty-search-style observer
feedback (which couples back into $V$ via archive state) is recovered
as a **second** observer $O'$ whose output is post-composed onto
$V$'s parameter space — the slot machinery of
[`emergent_systems.tex:783–795`](emergent_systems.tex) already handles
this without putting $O$ back inside $\mathcal{S}$.

### 2.3 What "life" becomes

With the observer external, **life** is no longer a property of the
system in isolation; it is a property of the system–observer pair,
reported as a **vitality profile** $(k, \boldsymbol{\sigma})$ that
captures both the depth of the system's search hierarchy and the
self-referential character of the search at each level.

A pair $(\mathcal{S}, O)$ is **in $\mathbf{LifeCat}$** iff:

1. **Emergence** in the Hoel sense:
   $\sup_\Pi \mathrm{CE}(M(\mathcal{S}),\Pi) > 0$
   (Definition CE, [`emergent_systems.tex:840–851`](emergent_systems.tex)).
2. **Entity persistence.** There is an entity $e = (S, \pi)$
   (Def. of Entity, paper §3.2) whose support remains non-empty
   across a window centred at $t$, with positive $F$-weight.
3. **Search-active at level $k \geq 1$.** The vitality profile
   $(k, \boldsymbol{\sigma})$, defined below, has $k \geq 1$.

The vitality profile is the structured measurement that replaces the
binary "is alive" predicate. It has two components.

#### Search-hierarchy depth $k$: recursive definition

The level structure is defined **recursively**, with no a-priori
labelling of levels by human categories (substrate / entity /
population / meta). Those labels become emergent descriptions of
what the recursion produces in particular systems; they are not
axioms of the framework.

**Base case (level 0).** $\Phi$ explores the substrate state space
$X$. The *level-0 entities* are the persistent patterns produced
by $\Phi$ alone: $(S, \pi)$ pairs satisfying the information-
closure condition E1 of paper §3.2, with variation given by
identity (they persist by $\Phi$, not by any separate $V$ acting
on them).

**Recursive case (level $n \geq 1$).** The system reaches level $n$
iff:

1. **Lower-level search continues.** The system reaches level
   $n - 1$.
2. **Search acts on level-$(n-1)$ entities.** There exists a
   $(V_n, F_n)$ pair acting on the level-$(n-1)$ entities such
   that $V_n$ proposes variants of those entities, $F_n$ filters
   the variants, and the iteration retains *discriminative
   capacity at level $n$*: a strictly-fitter candidate at level
   $n$ would be amplified by the level-$n$ iteration.

The **level-$n$ entities** are the persistent patterns at level
$n$ — $(S, \pi)$ pairs satisfying E1 under the
$(V_n, F_n)$-induced dynamic.

The recursion bottoms out at level 0 and ascends through the
system's hierarchical structure. The depth $k$ of the recursion
for a given system is the deepest level at which the recursive
case fires.

**Worked instances** of the recursion (illustrative; not part of
the structural definition):

- *Hurricane.* Level 0: $\Phi$ = atmospheric dynamics; level-0
  entity = the hurricane itself, a persistent attractor of $\Phi$.
  Level 1: no $(V_1, F_1)$ acts on hurricane-as-entity; no
  variation operator proposes new hurricane variants and no filter
  selects among them. Level 1 not reached. $k = 0$.
- *Tierra arms race.* Level 0: $\Phi$ = VM instruction cycles.
  Level 1: $(V_1, F_1)$ = bit-flip mutation + reaper, acting on
  programs (level-0 entities). Level 2: $(V_2, F_2)$ acting on
  lineages (level-1 entities), with new ecological roles emerging
  and going extinct. $k = 2$.
- *Cultural evolution.* Level 0: $\Phi$ = humans speaking. Level
  1: $(V_1, F_1)$ on linguistic items. Level 2: $(V_2, F_2)$ on
  languages (level-1 entities). Level 3: $(V_3, F_3)$ on
  variation mechanisms (level-2 entities). $k = 3$.

**Why the recursive definition is the right shape.** Under Q1's
resolution — $\mathbf{Sys}$ is the SMC of $\mathcal{O}_W$-algebras
in $\mathbf{Stoch}$ — level $n$ corresponds to **arity-$n$
compositions in the operad**, with the level-$n$ entities produced
by the operad's $n$-th composition iterate. The level count is not
an additional axiom; it falls out of the ambient category. The
substrate-agnosticism of the framework now extends to the level
structure itself: the framework refers only to "level-$(n-1)$
entities" without committing to whether those are atoms, cells,
populations, languages, or anything else. The substrate / entity /
population / meta labels are emergent descriptions of what the
recursion happens to produce in particular substrates.

**Where human choice still enters.** The recursive level structure
is structural, but entity-detection at each step still depends on
the scale projection $\pi$, which is a modeler choice (paper §3.2
already commits to this). Different reasonable $\pi$ choices
typically give the same level count $k$ but may disagree on which
entities exist at each level. The framework isolates human
dependence to the choice of $\pi$, not the level structure.

The same observer-dependence applies to **horizontal composition**.
Whether two physically-coupled subsystems are read as a single
entity, as a horizontal composition $\boxtimes_\kappa$ of two
entities, or as a vertical composition of finer-grained entities,
depends on $\pi$. Consider the lichen: the same physical situation
admits at least three coherent framework descriptions:

- *Description A — single composite entity.* Pick $\pi_A$ that
  projects the whole lichen to one $(S, \pi)$ pair at level 1.
  The lichen is a single level-1 entity; the alga and fungus are
  unresolved internal structure.
- *Description B — horizontal composition.* Pick $\pi_B$ that
  separately resolves alga and fungus as level-1 entities. The
  lichen is $\mathcal{S}_{\text{alga}} \boxtimes_\kappa \mathcal{S}_{\text{fungus}}$,
  with $\kappa$ encoding the metabolic coupling.
- *Description C — finer-grained vertical composition.* Pick
  $\pi_C$ that resolves down to individual cells. Each cell is
  level 1; the alga and fungus are level-2 vertical composites
  of their cells; the lichen is a horizontal $\boxtimes_\kappa$
  composition at level 2.

All three descriptions are coherent. They produce different
vitality profiles for the same physical situation. The framework's
claim is that the categorical description is always relative to a
chosen $\pi$, and that there is no observer-independent fact about
which description is "really" right. What constrains $\pi$ is the
information-closure condition E1 (paper §3.2) — a valid $\pi$ is
one under which the projected dynamics is approximately
self-predicting from its own past, conditional on the outside. E1
is a non-trivial constraint, but it does not single out a unique
$\pi$ for most physical systems.

The framework's discipline is therefore: **when you describe a
system, declare your $\pi$**. Two readers using different $\pi$
choices will produce different vitality profiles for the same
physical situation, and that disagreement is meaningful — it
tells you which structural facts each reader is committing to.
This is the Option-A-foundational commitment from Q1 being honest
with itself: boundaries are choosable subject to E1, with the
local-to-global reading recovered through the Option-C interpretive
lift when a particular $\pi$ has natural locality structure.

#### Formal definitions of non-trivial $V$, non-trivial $F$, and discriminative capacity

The recursive case used "non-trivial $V_n$," "non-trivial $F_n$,"
and "discriminative capacity at level $n$" without making the
terms precise. The following definitions tighten each.

**Non-trivial $V_n$.** A variation operator
$V_n : E_{n-1} \times \Theta \to \mathcal{P}(E_{n-1})$ on the
space of level-$(n-1)$ entities is **non-trivial** iff there
exists $e \in E_{n-1}$ and $\theta \in \Theta$ such that

$$
V_n(e, \theta) \;\neq\; \delta_e,
$$

where $\delta_e$ is the Dirac measure on $e$. Equivalently, the
support of $V_n(e, \theta)$ contains at least one entity other
than $e$ with positive probability.

In plain English: $V_n$ is non-trivial iff there is *some* input
for which the variation operator can produce *some* output that
differs from the input. The identity map (every entity reproduces
itself exactly) is the only trivial case. A stronger condition
worth naming: $V_n$ is **diversifying** iff $V_n(e, \theta)$ has
positive Shannon entropy for some $(e, \theta)$. Most operationally
interesting variation operators are diversifying; the distinction
matters when classifying near-deterministic mutation rates.

**Non-trivial $F_n$.** A viability filter
$F_n : \mathcal{M}_+(E_{n-1}) \to \mathcal{M}_+(E_{n-1})$ on the
space of population measures over level-$(n-1)$ entities is
**non-trivial** iff it is not a scalar multiple of the identity.
Formally, there exist entities $e_1, e_2 \in E_{n-1}$ such that

$$
\frac{F_n(\delta_{e_1})(\{e_1\})}{F_n(\delta_{e_2})(\{e_2\})} \;\neq\; 1.
$$

In plain English: $F_n$ is non-trivial iff it differentially
retains different entities. A filter that simply scales down the
whole population uniformly (e.g., a fixed death rate applied to
everything) is trivial — it changes total mass but not relative
composition. A filter that retains some entities preferentially is
non-trivial — it does the work of selection. This rules out two
degenerate cases: the identity filter (no death) and the uniform
scaling filter (death rate independent of entity).

**Discriminative capacity at level $n$.** A level-$n$ iteration
$(V_n, F_n)$ has **discriminative capacity** at level $n$ iff,
for any candidate entity $e^* \in E_{n-1}$ that is *strictly
fitter* than the current population under $F_n$ — meaning

$$
\frac{F_n(\delta_{e^*})(\{e^*\})}{F_n(\delta_e)(\{e\})} > 1 \quad \text{for all } e \text{ in the current population} ,
$$

the iteration $V_n \circ F_n$ applied to the population augmented
by $\epsilon \delta_{e^*}$ gives $e^*$ a strictly increasing share
of the population mass over time, for all small enough $\epsilon > 0$.

In plain English: a fitter mutant injected into the population
grows in relative frequency. This is the operational condition
that distinguishes a converged-but-still-search-active GA (which
would amplify a strictly fitter mutant) from a frozen-in-time
snapshot (which would not). The condition is observable via a
perturbation experiment: drop a known-fitter mutant into the
simulation, run forward, check that its share grows. This is the
formal version of the `has_discriminative_capacity` helper
specified in
[`vitality_computation.md`](vitality_computation.md) §1.4.

These three definitions cleanly exclude cases the framework needs
to exclude. A hurricane has trivial $V$ at level 1 (no variation
operator proposes new hurricane variants) and trivial $F$ at level
1 (no filter selects among them); the recursion halts at level 0
by the non-triviality conditions, not by hand-waving. A pure
Game-of-Life run has trivial $V$ at level 1 (gliders are not
subject to variation; $V$ is identity); the recursion halts at
level 0 cleanly. The Beer-autopoietic-GoL-with-artificial-mutation
case becomes the interesting borderline: $V$ is now non-trivial,
so the recursion's verdict depends on whether $F$ is also
non-trivial and whether the iteration has discriminative capacity.

The discriminative-capacity condition replaces an earlier "not at
a fixed point" reading; convergence is consistent with life
provided the system retains the capacity to respond to fitter
candidates if any appear.

#### Horizontal composition via $\boxtimes_\kappa$

The recursive definition above describes **vertical composition**:
level-$n$ entities become the substrate for level-$(n+1)$ search,
and the recursion climbs the hierarchy. This is one of two
compositional moves in the framework. The other is **horizontal
composition** via the substrate composition operator
$\boxtimes_\kappa$ (paper §3.3), which combines systems running in
parallel at the same level.

Under Q1's resolution, $\boxtimes_\kappa$ is the **monoidal product
of $\mathbf{Sys}$**. The associativity-up-to-canonical-isomorphism
already proven in paper §3.3 is the SMC structure of the ambient
category. Horizontal composition was therefore always available in
the framework; the recursive level definition needed to be stated
to make it clear that horizontal composition acts **at fixed
level** rather than raising it.

**Formal statement.** Given systems $\mathcal{S}_1$ and
$\mathcal{S}_2$ at vitality profiles $(k_1, \boldsymbol{\sigma}_1)$
and $(k_2, \boldsymbol{\sigma}_2)$ with $k_1 = k_2 = k$, the
horizontal composition $\mathcal{S}_1 \boxtimes_\kappa \mathcal{S}_2$
is a system at level $k$. Its $\sigma$ profile depends on the
coupling structure of $\kappa$ at each shared level $i \leq k$:

- **Trivial $\kappa$** (independent product): $\sigma_i$ for the
  composite is approximately
  $\max(\sigma_i^{(1)}, \sigma_i^{(2)})$. No new self-reference
  is created; the components are simply running side by side.
- **One-way coupling** ($\kappa_{1 \to 2}$ non-trivial,
  $\kappa_{2 \to 1}$ trivial): $\mathcal{S}_2$'s effective $\sigma_i$
  rises by the dependence on $\mathcal{S}_1$ that the coupling
  introduces; $\mathcal{S}_1$'s $\sigma_i$ is unchanged.
- **Mutual coupling**: both directions non-trivial. $\sigma_i$ for
  the composite can be strictly greater than either component's
  $\sigma_i$ in isolation. **This is the case where horizontal
  composition generates self-reference that was not present in
  the components.**

The mutual-coupling case is the operationally interesting one. It
explains the felt difference between isolated systems and
coevolving systems: a host lineage on its own can be $(2, (1, 0))$
under Darwinian selection from a fixed environment, but the same
host lineage horizontally composed with a parasite lineage via
mutual $\kappa$ jumps to $(2, (1, 1))$ — *the host's $\sigma_2$ is
manufactured by the coupling, not present intrinsically*. This is
why coevolutionary ALife systems "feel more alive" than vanilla GAs
even at the same level: their $\sigma$ uplift is real and
measurable.

**Interaction between vertical and horizontal composition.** The
two operations are independent and can be applied in any order:

| Composition                 | Operator                                      | Level effect            |
|-----------------------------|-----------------------------------------------|-------------------------|
| Vertical                    | $(V_{n+1}, F_{n+1})$ acting on level-$n$ entities | Raises level by 1    |
| Horizontal                  | $\boxtimes_\kappa$                            | Preserves level         |
| Horizontal with channel coupling | $\boxtimes_\kappa$ combined with $\diamond_\rho$ | Preserves level; couples variation |
| Vertical applied to a horizontal composite | $\boxtimes_\kappa$ then recursive ascent | Raises after parallel coupling |

The framework's full compositional space is generated by composing
vertical and horizontal moves in any order. Symbolically, every
system in $\mathbf{Sys}$ is built from substrate atoms by some
finite combination of $\boxtimes_\kappa$ (horizontal) and the
recursive level-raising (vertical). Yau's finite-presentation
theorem for $\mathcal{O}_W$ (8 generators, 28 relations) covers
both axes — horizontal composition is the operad's monoidal
structure; vertical composition is the operad's arity-counting.

**Examples across substrates.** A non-exhaustive list of cases
worth keeping in mind when reading the framework:

- *Symbiosis (lichen).* Alga (level 1, $\sigma_1 \approx 1$) plus
  fungus (level 1, $\sigma_1 \approx 1$), horizontally composed
  via mutualistic metabolic coupling. Composite is still level 1
  but is operationally a single entity in many readings.
- *Coevolutionary populations (Tierra arms race).* Host lineage
  and parasite lineage at level 2, horizontally composed via the
  exploit/resist coupling. Composite has $\sigma_2$ manufactured
  by the coupling.
- *Coupled organs.* Heart + lungs in a vertebrate — both at
  level 2 (organ-systems within the multicellular hierarchy),
  composed via the circulatory $\kappa$. The composite remains
  level 2; the coupling is constitutive of both components' viability.
- *Endosymbiosis.* Historically, an ancestral bacterium $\boxtimes$
  an archaeon at level 1, fused so tightly that the composite now
  reads as a single level-1 entity (the eukaryotic cell), with the
  mitochondrion no longer self-sufficient. Long-running horizontal
  composition can fuse two systems into one and operationally drop
  a level.
- *Ecological communities.* Multi-component $\boxtimes_\kappa$
  among many species at level 2, with the coupling structure given
  by the food web and niche-overlap matrices.
- *Bilingual speech communities.* English and Spanish at level 2,
  horizontally composed via shared speakers, code-switching, and
  loanword traffic. Each language's $\sigma_2$ is raised by the
  coupling.
- *Hybrid biological–computational systems.* A bacterium plus a
  foundation-model agent observing and acting on it — horizontal
  composition across substrates. The paper's worked composite
  example (§3.8) is exactly this shape.
- *Holobiont (host + microbiome).* A human host (level $\geq 3$)
  horizontally composed with a gut microbial community (level 2).
  Modern biology increasingly treats them as a single
  horizontally-composed system rather than as host + environment.

The framework's predictive thesis from Q4 includes the prediction
that *all* of these are genuinely alive in the framework's sense,
at vitality profiles determined jointly by their component profiles
and their coupling structure.

#### Self-reference vector $\boldsymbol{\sigma}$

For each level $i \leq k$, $\sigma_i \in [0, 1]$ measures how much
the viability filter $F$ at level $i$ depends on the system's own
dynamical state beyond the current population. Specifically:

$$
\sigma_i = 1 \iff F_i \text{ is a non-trivial function of the }
\text{system's state at level } i.
$$

The flag captures the autopoietic / FEP / co-evolutionary content
of life. A standard GA has $\sigma_1 = 0$ (the fitness function is
externally fixed); a frequency-dependent GA has $\sigma_1 = 1$ (the
effective fitness depends on the population). A bacterium in a
fixed nutrient bath has $\sigma_1 = 1$ at the cell level
(autopoietic) but $\sigma_2 \approx 0$ at the population level
(externally controlled). HeLa cells in lab culture are at
$(2, (1, \approx 0.4))$ — wild at the cell scale, partially
domesticated at the population scale.

#### Worked vitality profiles

The composite predicate gives principled verdicts across the full
range of cases the framework needs to handle:

| System                                      | Profile             | In $\mathbf{LifeCat}$? |
|---------------------------------------------|---------------------|:----------------------:|
| Hurricane                                   | $(0, (0))$          | No (level 0 only)      |
| Chaotic map, no entity                      | $(0, (0))$          | No                     |
| Crystal phase change                        | $(0, (0))$          | No                     |
| Plain GoL glider, no $V$                    | $(0, (0))$          | No                     |
| Standard converged GA                       | $(1, (0))$          | Yes                    |
| Bacteria in fixed nutrient bath             | $(1, (1))$          | Yes                    |
| Frequency-dependent GA                      | $(1, (1))$          | Yes                    |
| Active Tierra arms race                     | $(2, (1, 1))$       | Yes                    |
| Stabilised Tierra                           | $(2, (1, 0))$       | Yes                    |
| HeLa cells in lab culture                   | $(2, (1, \approx 0.4))$ | Yes                |
| Wild bacterial ecosystem                    | $(2, (1, 1))$       | Yes                    |
| Multicellular organism                      | $(3, (1, 1, 1))$    | Yes                    |
| Human language / cultural evolution         | $(3, (1, 1, 1))$ or $(4, (1, 1, 1, 1))$ | Yes |

The horizontal-composition cases — explicit instances of $\boxtimes_\kappa$ — extend the table as follows. Component-profile columns show what each component looks like in isolation; composite-profile columns show how horizontal coupling shifts the result. Asterisks mark $\sigma$ values that are manufactured by the coupling and would not be present in either component on its own.

| Composite system                  | Components                                                          | Coupling $\kappa$                  | Composite profile          |
|-----------------------------------|---------------------------------------------------------------------|------------------------------------|----------------------------|
| Lichen                            | Alga $(1, (1))$ + fungus $(1, (1))$                                 | Mutualistic metabolite exchange    | $(1, (1))$ ; coupling raises effective $\sigma_1$ |
| Tierra host–parasite ecology      | Host lineage $(2, (1, 0))$ + parasite lineage $(2, (1, 0))$         | Mutual exploit/resist              | $(2, (1, 1^*))$            |
| Predator–prey populations         | Predator $(2, (1, 0))$ + prey $(2, (1, 0))$                         | Trophic dependence                 | $(2, (1, 1^*))$            |
| Coupled heart + lungs (organism)  | Heart $(2, (1, 1))$ + lungs $(2, (1, 1))$                           | Circulatory coupling, mutual       | $(2, (1, 1))$ at organism level |
| Endosymbiosis (proto-eukaryote)   | Aerobic bacterium $(1, (1))$ + anaerobic archaeon $(1, (1))$        | Initially partial; eventually fused| $(1, (1))$ (with eventual operational level-drop into one entity) |
| Ecological community              | $n$ species, each $(2, (1, \sigma_2))$                              | Food-web + niche graph             | $(2, (1, \text{coupled}))$ with $\sigma_2$ uplifted by community structure |
| Bilingual speech community        | Language $A$ $(3, (1, 1, 1))$ + language $B$ $(3, (1, 1, 1))$       | Code-switching, loanwords          | $(3, (1, 1, 1))$ with coupling-uplifted $\sigma_2$ and $\sigma_3$ |
| Holobiont (host + microbiome)     | Host $(\geq 3, \ldots)$ + microbiome $(2, (1, 1))$                  | Biochemical + immune signalling    | Composite profile inheriting the deeper host levels with mutual coupling at the gut interface |
| Hybrid LLM-Lenia worked example   | Lenia $(1, (\text{depends}))$ + LLM agent $(1, (1))$                | Cross-substrate observer-feedback  | $(1, (1^*))$ — coupling manufactures $\sigma_1$ on the Lenia side |

Reading the table: for the host–parasite, predator–prey, and hybrid-LLM-Lenia rows, the coupling is what produces $\sigma$ at the shared level. These are exactly the cases that ALife has historically struggled to formalise — "open-ended coevolution" turns out to be horizontal composition with mutual $\kappa$ that manufactures $\sigma$ uplift.

#### Comparing vitality profiles across systems with different measures

A natural question once the profile is defined: when can we say one
system is "more life-like" than another? Two systems will, in
general, have different state spaces, different probability
measures, different variation kernels, different filters. The
vitality profile $(k, \boldsymbol{\sigma})$ is substrate-agnostic
in its *structural* content, but the floating-point values of
$\sigma_i$ depend on the underlying probability measure through
the conditional transfer entropy estimator. So same profile across
two systems does not automatically mean equal life-likeness in any
numerical sense.

The framework handles this with three distinct comparison
operations, each appropriate in different contexts.

**Comparison 1 — structural equivalence in $\mathbf{LifeCat}$.**
Two systems with the same $k$ and componentwise-equal
$\boldsymbol{\sigma}$ (within estimator noise) are
**structurally equivalent** as objects of $\mathbf{LifeCat}$.
They have the same categorical shape — they reach the same depth
of recursive search hierarchy, with the same self-reference at
each level. This is what the framework's substrate-agnostic claim
delivers: a Tierra arms race at $(2, (1, 1))$ and a wild bacterial
ecosystem at $(2, (1, 1))$ are structurally equivalent in
$\mathbf{LifeCat}$, regardless of substrate differences. They are
the same life-form *as categorical objects*.

Structural equivalence is necessary but not sufficient for
operational equivalence. Two structurally-equivalent systems can
still differ in how they behave under any particular observer; the
profile captures the categorical structure, not the dynamical
fine-grain.

**Comparison 2 — partial order on profiles.** A natural partial
order on vitality profiles:

$$
(k_1, \boldsymbol{\sigma}_1) \;\preceq\; (k_2, \boldsymbol{\sigma}_2)
\quad \iff \quad
k_1 \leq k_2 \text{ and } \forall i \leq k_1, \; \sigma_{1, i} \leq \sigma_{2, i} .
$$

System 2 is "at least as life-like" as System 1 in the partial
order iff it dominates in every component — same or deeper search
hierarchy, and same or higher self-reference at every shared level.
Most pairs of systems are incomparable in this partial order, which
is honest about what the framework actually says. A two-level
ecosystem with weak coevolution $(2, (1, 0.3))$ and a one-level
system with strong autopoiesis $(1, (1.0))$ are not ordered by
$\preceq$ — neither dominates the other. The partial order rules
out cheap "more alive than" claims that don't have structural
backing.

**Comparison 3 — observer-mediated quantitative comparison.**
Quantitative comparison across substrates requires a common
observer functor $O$ that both systems can be evaluated against.
Given $\mathcal{S}_1, \mathcal{S}_2$ and an observer $O$ valid for
both, compute $O$'s output trajectories and compare via standard
statistical methods (KL divergence between observer-score
distributions, Wasserstein distance, MMD, or any divergence
satisfying C3'). The comparison result is *quantitative* but
*observer-relative*: the same two systems compared under different
observers can produce different orderings.

The framework's existing observer-functor machinery from Q1's
resolution provides exactly the right structure for this:
$O: \mathbf{Sys} \to \mathbf{Obs}$ is what makes cross-substrate
comparison possible. ASAL's CLIP-embedding observer is the
canonical example — it gives a substrate-independent observation
space in which Lenia, Boids, and any system that can be rendered
into images become quantitatively comparable.

**Reporting discipline.** A framework-conforming research paper
should report three things when comparing two systems:

1. *Structural profile.* The vitality profile $(k, \boldsymbol{\sigma})$
   for each system. This is the substrate-agnostic structural fact.
2. *Partial-order verdict.* Whether the two profiles are
   $\preceq$-comparable, and if so, in which direction. If
   incomparable, say so explicitly.
3. *Observer-mediated comparison.* If a quantitative comparison
   is needed beyond the partial order, name the observer $O$ used
   and report the comparison only relative to $O$.

The discipline forbids the move "system A has higher $\sigma_2$
than system B, therefore A is more alive than B" when A and B have
different state spaces and the $\sigma$ values are not estimator-
normalised. The right reading of two structurally-equivalent
systems is: *they are the same life-form categorically; for
quantitative differentiation, specify an observer*.

**Worked comparison.** Tierra in its arms-race phase and a wild
bacterial ecosystem are both at $(2, (1, 1))$. They are
*structurally equivalent* in $\mathbf{LifeCat}$. They are equal
under the partial order $\preceq$. Whether one is "more alive"
quantitatively requires a common observer — for example, an
information-theoretic observer counting the number of distinct
ecological roles per generation. Under such an $O$, the
biological ecosystem might score higher (more roles per unit time)
or lower (slower turnover) than Tierra; the verdict depends on
$O$. The framework's structural claim (they are the same
life-form) does not resolve the quantitative claim (which is
"more alive"); the two claims are about different things, and the
framework keeps them separate.

This is consistent with how thermodynamics handles its own
substrate-independent quantities. Two systems can be at the same
temperature without being the same thing; comparing them requires
specifying which measurement (heat capacity? entropy production?
specific heat?) you are after. The vitality profile is the
thermodynamic-analog "temperature" of life — the substrate-
agnostic structural measurement — and observer-mediated
comparisons are the substrate-specific further measurements.

#### Where intrinsic vs. observer-relative content lives

Conditions 1 (CE > 0) and 2 (entity persistence) are intrinsic to
the system. The level-$k$ condition is intrinsic. The
$\boldsymbol{\sigma}$ vector is intrinsic. The observer functor
$O$ does not enter the membership predicate; it *ascribes* life
by reporting the vitality profile, but the profile itself is a
property of $\mathcal{S}$. The independent-observer thesis of Q1
is preserved by making the observer the witness, not the source,
of aliveness.

### 2.4 The target category

Let $\mathbf{LifeCat}$ be the category whose objects are
**life-producing pairs** $(\mathcal{S},O)$ satisfying conditions
1–3 on a non-trivial set of initial conditions, and whose morphisms
are slot-preserving maps compatible with $O$. The thesis is that
$\mathbf{LifeCat}$ is **non-empty, faithful, and broad enough** to
contain every example of life we recognise — artificial **and**
organic — and **structured enough** that everything in it factors
through the 4-tuple decomposition.

### 2.5 What the framework predicts

The framework is **predictive, not descriptive**. It does not merely
re-notate biological life in slot vocabulary; it claims that life is
realisable in **any** $\mathcal{O}_W$-presentable substrate that
admits the four slots and satisfies S1's sufficiency conditions
under some independent observer.

This commits the framework to a falsifiable position. The thesis
asserts the existence of forms of life that biological life is one
instance of, including:

- **Programmatic life.** Tierra and Avida are early empirical
  evidence; the framework predicts that with appropriate
  substrate complexity (instruction set, memory model, energy
  accounting), variation (self-modification, recombination),
  viability (self-replication closure under the substrate's reaction
  network), and topology (program-to-program interaction via shared
  state or message passing), programmatic systems produce life in
  the same formal sense as biological cells. The 4-tuple is not a
  metaphor for biology in this case; biology and programs are
  **two specialisations of the same theorem**.
- **Hybrid / coupled life.** A coupled substrate
  $\mathbf{X}_{\mathrm{bio}} \boxtimes_\kappa \mathbf{X}_{\mathrm{LLM}}$
  produces life in $\mathbf{LifeCat}$ whenever both components
  produce viable entities under the coupled dynamics. The framework
  predicts that hybrid biological–computational life-forms
  (engineered organisms with foundation-model-mediated behaviour,
  for example) are not metaphorically alive but are genuine
  instances of the same theorem.
- **Cultural / memetic life.** With substrate
  $\mathbf{X}_{\mathrm{cult}}$ a population of cultural items,
  variation $V_c$ cultural transmission with copying error, viability
  $F$ transmission-success closure, and topology $T$ the social
  graph, sufficiently complex cultural systems satisfy the
  $\mathbf{LifeCat}$ membership conditions. Cultures, on this view,
  can be alive in the same formal sense as cells. (Whether human
  cultures *are* in $\mathbf{LifeCat}$ is an empirical question
  the framework makes precise.)
- **Substrate-novel life.** The framework predicts that life-forms
  with substrates currently outside biological reach — formal
  reaction networks in non-chemical media, hypothetical
  high-dimensional flow fields, swarms of synthetic robotic agents,
  $\mathcal{O}_W$-presentable systems we have not yet built — are
  potentially in $\mathbf{LifeCat}$ if they satisfy S1 under some
  independent observer.

A negative prediction is equally important: many physical systems
with $\mathrm{CE} > 0$ are **not** alive at any level
above $k = 0$, because they lack an entity-level search. The
framework excludes hurricanes, chaotic dynamical systems, plain
cellular automata, and crystal phase changes via the level
condition — they sit at vitality profile $(0, (0))$ and do not
reach level $k = 1$.

The predictive thesis cashes out concretely via vitality profiles.
The framework commits to predicting that:

- **Programmatic systems with active variation and selection**
  reach level 1 with $\sigma_1$ determined by whether their
  selection landscape is externally fixed or co-evolving. Tierra in
  its arms-race phase reaches $(2, (1, 1))$ — the same profile as
  a wild bacterial ecosystem. This is the operational version of
  "programmatic life is the same theorem as biological life."
- **Hybrid biological–computational systems** reach the profile of
  their dominant level, with cross-substrate self-reference
  contributing to higher-level $\sigma$ values.
- **Cultural and linguistic systems** reach $(3, (1, 1, 1))$ or
  deeper, exceeding individual biological organisms in
  search-hierarchy depth. This is a strong substantive prediction
  the framework commits to: human culture is the most structurally
  alive system on Earth in the framework's sense, not because
  cultures matter more than people but because cultural systems
  have more nested levels of self-shaping search.
- **Substrate-novel systems** are alive iff their vitality profile
  reaches $k \geq 1$. The framework gives a substrate-independent
  test that any future system can be evaluated against.

This predictive stance is what distinguishes the framework from
philosophy-of-biology accounts that treat "life" as a cluster
concept. If the thesis is correct, programmatic life, biological
life, and cultural life are not analogous — they are the same
mathematical phenomenon at different vitality profiles, in
different substrates.

### 2.6 How hierarchies emerge: the LE conjecture

The recursive level definition of §2.3 is *static*: given a system,
it determines what level the system has reached. It does not
describe how a system at depth $k$ comes to reach depth $k + 1$.
But the historical and dynamical reality is that biological life
underwent multiple **level transitions** — chemistry begat cells,
cells begat multicellular organisms, organisms begat ecosystems,
hominid lineages begat cultures — and the framework should be
able to describe the mechanism of these transitions, not just the
hierarchy of completed levels.

Biology calls these **major evolutionary transitions**
(Maynard Smith & Szathmáry 1995). Their eight transitions —
replicating molecules → compartments → chromosomes → DNA+protein
→ eukaryotes → sexual populations → multicellular organisms →
societies → linguistic societies — have not been formalised
categorically. The framework can do that, with a structural
characterization that applies in any substrate, not just biology.

#### The mechanism

A level transition from depth $k$ to depth $k + 1$ requires the
system to develop a $(V_{k+1}, F_{k+1})$ pair acting on level-$k$
entities. Where does this pair come from? It cannot be supplied
from outside — the framework treats $V$ and $F$ as intrinsic. It
has to emerge from the dynamics of level-$k$ entities themselves.

Four conditions, drawn from the cases biology recognises, are the
framework's structural characterization of the transition:

1. **Persistence.** Level-$k$ entities exist and persist with
   lifetimes much longer than the substrate's relaxation time.
   There must be something durable to aggregate before
   aggregation can produce a new level.
2. **Aggregation.** A non-trivial coupling structure $\kappa^{(k)}$
   on level-$k$ entities (horizontal composition in the sense of
   §2.4) produces persistent multi-entity patterns. These are the
   *candidate* level-$(k+1)$ entities.
3. **Group variation.** The coupling $\kappa^{(k)}$ varies across
   the population of aggregates — different aggregate types are
   possible and arise with positive frequency. This is the
   precursor to $V_{k+1}$: variation at the new level.
4. **Group selection.** Different aggregate types have measurably
   different persistence rates. This is the precursor to
   $F_{k+1}$: differential filtering at the new level.

When all four conditions are met over a sufficient time window,
the system has undergone a level transition. The level-$(k+1)$
entities are the persistent aggregates; $V_{k+1}$ and $F_{k+1}$
are the implicit variation-and-selection on aggregate types; the
system's vitality profile depth $k$ has increased by 1.

These conditions are themselves graded: each can be partially met.
A system in which the four conditions are partially satisfied is
"on the way to" a level transition without having completed one.
This is the framework's content for the "becoming" intuition —
systems can be intermediate between levels in the sense that the
four LE conditions are partially met, even though $k$ itself
remains integer-valued.

#### Conjecture LE (Level Emergence)

**Conjecture LE.** A system $\mathcal{S}$ at vitality profile
depth $k$ undergoes a level transition to depth $k + 1$ over a
time window $W$ if and only if its level-$k$ entities satisfy
the four conditions above (persistence, aggregation, group
variation, group selection) over $W$.

The "iff" is non-trivial in both directions. *Necessity*
(transition implies the four conditions) says these are the
structural requirements for any level emergence in any substrate.
*Sufficiency* (the four conditions imply transition) says wherever
the conditions are met, a new level *will* emerge given enough
time. The sufficiency direction carries the predictive content:
the framework predicts level emergence wherever the four
conditions hold, in any substrate.

#### Walking through chemistry → cells → organisms → ecosystems

**Chemistry → cells (level 0 → level 1).**

- *Persistence*: autocatalytic chemical reaction networks (RAFs
  in the Hordijk–Steel sense) persist in primordial chemistry as
  level-0 entities — patterns sustained by $\Phi$ alone.
- *Aggregation*: lipid bilayer membranes form spontaneously and
  enclose patches of chemistry. The membrane is $\kappa^{(0)}$,
  the coupling structure that binds together a particular set of
  reactions.
- *Group variation*: different membrane compositions, different
  sets of enclosed reactions, different geometries. Proto-cell
  populations are heterogeneous.
- *Group selection*: proto-cells with internally self-sustaining
  chemistry (RAF closure holds inside the membrane) persist;
  ones whose internal chemistry collapses do not. This is the
  emergent $F_1$.

Result: level-1 entities (cells) emerge as a new categorical type.

**Cells → organisms (level 1 → level 2).**

- *Persistence*: free-living cells reproduce and persist over
  generations.
- *Aggregation*: cells adhere via cell-cell adhesion molecules;
  some form colonies (Volvox), some form true multicellular
  structures. The adhesion-and-signalling network is $\kappa^{(1)}$.
- *Group variation*: different patterns of cell adhesion,
  different multicellular geometries, different division-of-labour
  configurations.
- *Group selection*: some multicellular configurations are
  mechanically and metabolically stable; others fall apart.

Result: level-2 entities (multicellular organisms) emerge.

**Organisms → ecosystems (level 2 → level 3).**

- *Persistence*: free-living organisms persist over generations.
- *Aggregation*: organisms develop trophic relationships,
  mutualisms, competitive interactions, niche construction. The
  coupling $\kappa^{(2)}$ is the food web plus the interaction
  matrix.
- *Group variation*: different community compositions, different
  food-web topologies, different species assemblages.
- *Group selection*: stable communities (cycled nutrients,
  balanced trophic levels, robust feedbacks) persist; collapsed
  ones don't.

Result: level-3 entities (ecosystems) emerge.

The same four-condition mechanism applies to each transition. The
framework reads them uniformly; only the starting-level substrate
differs.

#### What LE adds to the framework

LE joins S1, N1, CAT1 as a top-level conjecture of the framework.
It contributes three distinct pieces of structural content.

**A theory of biogenesis at every level.** The mechanism above
explains not just the origin of life from chemistry but the origin
of multicellularity from unicellular life, the origin of
ecosystems from organism populations, the origin of cultures from
hominid behaviour. The framework's substrate-agnosticism extends
to the transition mechanism itself.

**A precise meaning for "open-ended evolution."** A system is
**open-ended** at time $t$ iff there is positive probability that
it reaches profile depth $k + 1$ at some later time. This is a
structural condition on the system, not a vague "novelty doesn't
stop" handwave. The "open-endedness problem" in ALife becomes the
question of which systems have positive transition probability
over their natural time scales. Tierra in the arms race had it;
Tierra after stabilisation lost it; biology has retained it for
3.5 billion years across multiple transitions.

**A formal frame for evolvability.** A system is more evolvable
than another iff its level-$k$ entities have more spare structure
for the four LE conditions to be met — more potential coupling
configurations, more variable aggregation patterns, more
differential persistence among aggregates. Evolvability becomes
a measurable property of $(\mathcal{S}, t)$ pairs rather than a
vague trait.

#### Cross-substrate level transitions

LE's predictive content extends beyond biology, consistent with
the Q4 stance.

- **Programmatic level transitions.** Tierra during its arms race
  underwent the level-1 → level-2 transition: individual programs
  (level 1) aggregated into ecological roles (level 2), the
  role-structure varied, and some role configurations persisted.
  The exact moment of the transition is empirically dateable from
  the simulation logs.
- **Foundation-model agent ecologies.** Multi-agent LLM systems
  can undergo level transitions when groups of agents start
  exhibiting persistent collective patterns (coalitions, niches,
  trade networks) with their own variation-and-selection. LE
  predicts this will happen wherever the four conditions are met,
  regardless of whether the agents are individually "intelligent."
- **Cultural transitions.** The transition from spoken language
  to written language was a level transition: oral linguistic
  items (level 1) aggregated into texts (level 2 — texts are
  persistent multi-item patterns with their own variation and
  selection). The printing press was another transition. The
  Internet may be enabling a further one.
- **Synthetic biology.** Engineered cells designed to cooperate
  may undergo level transitions where the cooperating-group
  becomes the categorical unit of variation and selection. LE
  predicts when this happens and when it doesn't.

The negative predictions are equally important. A hurricane does
not undergo level transitions because its level-0 entities do not
satisfy conditions 3 and 4 — there is no variation among
hurricane types and no differential persistence among aggregates.
A converged GA does not undergo a transition because its level-1
entities don't aggregate into stable higher-level structures.

---

## Part 3 — Staged proof obligations

The user asked for a characterization theorem to be the eventual
target, with sufficiency and necessity proved first. The natural
staging is:

### 3.1 Stage A — Sufficiency (the easier direction)

**Conjecture S1 (sufficiency).** There exists a non-trivial subclass
$\mathcal{C} \subseteq \mathbf{Sys}$ such that for every
$\mathcal{S} \in \mathcal{C}$, some observer $O$ exists for which
$(\mathcal{S},O) \in \mathbf{LifeCat}$.

This is the version of "five slots are enough to produce life-like
phenomena under some observation." Concretely:

- For $\mathcal{C}$ = {Flow-Lenia substrates with autopoietic-closure
  viability and bounded-radius topology}, exhibit an $O$ (CLIP-novelty
  archive or $\Omega$) under which emergence + open-endedness +
  persistence hold.
- This is essentially `OP1` re-cast as a sufficiency result: a positive
  answer to `OP1` (for any candidate system) is a non-trivial witness
  to `S1`.

**Proof handle**: `OP1` reduction on the Game of Life under
Markov-blanket viability (proof_techniques.md OP1 §D, "lowest-hanging
fruit"), then promote from "$\mathrm{CE} > 0$ exists" to "the full
life triple holds." Sufficiency needs only one $(\mathcal{S}, O)$
witness; `OP1` is precisely a witness machine.

### 3.2 Stage B — Necessity (the harder direction)

**Conjecture N1 (necessity).** Let $\mathcal{O}_W$ denote the operad
of wiring diagrams of Vagner–Spivak–Lerman 2015 (with extensions
to time-indexed systems via Schultz–Spivak 2019). For every
life-producing pair $(\mathcal{S}', O)$ in which $\mathcal{S}'$ is
presentable as a $\mathcal{O}_W$-algebra
$A : \mathcal{O}_W \to \mathbf{Set}$, there exists a
$\mathcal{S} = (\mathbf{X},V,F,T)$ and a slot-preserving morphism
$\mathcal{S} \to \mathcal{S}'$ that is essentially surjective on
$O$-observable behaviour.

Plain English: if a system produces life-like phenomena and is
expressible as a wiring-diagram algebra (CAs, Markov chains, ODEs,
agent-based models, reaction networks, multi-layer coupled systems,
and combinations thereof are all $\mathcal{O}_W$-algebras), then it
canonically decomposes as a 4-slot system without losing the
phenomena.

**Why fix the ambient framework to $\mathcal{O}_W$.**
The operad of wiring diagrams is the strongest known unifier of
open dynamical systems (Vagner–Spivak–Lerman), reaction networks
(Baez–Pollard 2017), continuous-time networks (Lerman–Spivak 2016),
and time-indexed / streamed systems (Schultz–Spivak 2019). It is
finitely presented (Yau 2018: 8 generators / 28 relations for the
directed case; 6 / 17 for the undirected variant), so essential
surjectivity of the decomposition functor reduces to checking a
small finite list of cases. It also already underwrites `OP3'`
(operadic universality of multiplex topologies), so anchoring N1 on
$\mathcal{O}_W$ gives full reuse of the same machinery for both
necessity statements --- they become facets of one decomposition
theorem rather than two parallel research programmes.

What N1 requires:

- A constructive **decomposition functor**
  $\mathrm{Decomp} : \mathrm{Alg}(\mathcal{O}_W) \to \mathbf{Sys}^{4-\text{slot}}$
  with proven essential surjectivity onto $O$-observable behaviour.
- A **finite generator check**: verify that for each of Yau's
  generators (identity wiring, single-arity hyperedge, layer-mixture,
  $\rho$-fusion, and the small number of remaining ones), the
  $\mathrm{Decomp}$ image lands in the four-slot category and the
  $O$-observable behaviour is preserved.
- **Specialisations** that recover known life: instantiate
  $\mathrm{Decomp}$ for a cell (a CRN / RAF presentation), for an
  immune-system trajectory (a finite-state Markov chain
  presentation), and for an ecological food web (a coupled
  multi-substrate presentation). Each specialisation is a
  freestanding $\mathcal{O}_W$-algebra by construction; what N1
  proves is that all three project canonically to the same kind of
  4-slot system.

This is genuinely open. It is the hardest piece, and the one that
makes the framework a **theory** rather than a vocabulary.

### 3.3 Stage C — Characterisation (the iff)

**Conjecture CAT1 (characterisation).** $\mathbf{LifeCat}$ is
equivalent, as a category, to the image of $\mathrm{Decomp}$ inside
$\mathbf{Sys}^{4-\text{slot}} \times \mathbf{Obs}$ (with the
appropriate over-category structure on observers).

This is the user's final statement: every life-producing system is
canonically a 4-slot system observed by an independent observer, and
conversely. CAT1 is essentially S1 + N1 + a coherence theorem; it is
not a separate proof in addition to the first two, but the assertion
that they fit together categorically.

### 3.4 How the existing `C1`–`C3` and `OP1`–`OP3` fit

Each existing conjecture/open problem becomes a **lemma toward S1 or
N1**, not a standalone unification:

| ID  | Original scope                          | Role in the new framing                                                                                  |
|-----|-----------------------------------------|----------------------------------------------------------------------------------------------------------|
| C1  | Closure-operator unification of $F$     | Lemma toward N1: a unified $F$ makes the decomposition functor canonical instead of formalism-by-formalism.   |
| C2  | Hierarchical viability composition      | Required for organic life (cells in tissues in organisms), so it is a sub-lemma of N1 applied to biology. |
| C3  | Observer divergence-functional schema   | Reformulated against the external-observer category: $\mathbf{Obs}$-morphisms are divergence functionals. |
| OP1 | $\sup_\Pi \mathrm{CE} > 0$ exists       | The sufficiency witness for S1 (Stage A).                                                                |
| OP2 | FEP scope                               | Specialisation of N1 to FEP-presentable substrate–dynamics pairs.                                        |
| OP3 | Multiplex universality                  | Specialisation of N1 to interaction-topology morphisms.                                                  |

In particular, **`OP1` becomes the load-bearing first result**: it
graduates from "an open problem" to "the lowest-hanging concrete
existence proof for S1," and a positive answer immediately gives the
sufficiency direction.

---

## Part 4 — Structural changes required

### 4.1 The tuple

Replace
$\mathcal{S} = (\mathbf{X},V,F,T,O)$
with
$\mathcal{S} = (\mathbf{X},V,F,T)$ + an external observer functor
$O : \mathbf{Sys} \to \mathbf{Obs}$.

Affected files at the type level:

- [`emergent_systems.tex`](emergent_systems.tex) §3.1 (the System
  Definition, lines 270–298).
- [`emergent_systems.tex`](emergent_systems.tex) §3.6 (Observer slot,
  lines 716–795). The relevant System Description schema runs lines
  1295–1366 in the same file.
- [`src/emergent_systems/system.py`](../src/emergent_systems/system.py)
  — the `System` dataclass and `run`/`step` signatures will need a
  refactor.
- [`src/emergent_systems/observer.py`](../src/emergent_systems/observer.py)
  — the `Observer` / `StatefulObserver` Protocols stay, but are now
  consumed by an external `observe(system, trajectory)` function
  rather than living inside the system.
- [`src/emergent_systems/spec.py`](../src/emergent_systems/spec.py) —
  `SystemSpec` enumerates 7 structural items including iteration order;
  it gains an 8th item for the observer attached at run time, and the
  observer fields move from "structural" to "attached at observation."

### 4.2 Why this is structurally sound, not just rhetorical

The framework already has the right type for an external observer; it
just types it as an internal slot. The relevant signature
([`emergent_systems.tex:721`](emergent_systems.tex))

$$
O \;:\; Z^w \longrightarrow \mathbb{R}^k
$$

reads $w$ ticks of trajectory and emits a score. Nothing about that
signature requires $O$ to be one of the things the tick rule
composes — and indeed the paper already says the observer
"acts on trajectories rather than on single ticks"
([`emergent_systems.tex:299`](emergent_systems.tex)).

Moving $O$ from "fifth slot of the tuple" to "external functor on
the trajectory" is therefore a **typographical correction of an
inconsistency that already exists** in the docs, not a destruction
of the existing machinery.

### 4.3 What survives

- The four-slot tuple $(\mathbf{X},V,F,T)$ keeps all the composition
  machinery: $\boxtimes_\kappa$, $\diamond_\rho$, the entity
  definition, $V_T$, the hierarchical viability filter $F^\ast$.
- The lifted operators
  $\widetilde{\Phi},\widetilde{V}_T,\widetilde{S}_F$ are unchanged.
- Hoel-style causal emergence (Definition CE) is unchanged.
- All four viability formalisms are unchanged.
- All three observer families (density-distance, FM-embedding,
  information-theoretic) are unchanged --- they are now described
  as families of $\mathbf{Sys}\to\mathbf{Obs}$ functors instead of
  as a slot.

### 4.4 What changes

- The system-description schema
  ([`emergent_systems.tex:1295–1322`](emergent_systems.tex)) splits
  cleanly: structural items 1–7 belong to $(\mathbf{X},V,F,T)$;
  item 6 (observer family + window + state) moves to a new
  *"observation record"* section that ships separately.
- The paper's abstract, introduction, scope-and-commitments, and
  results section all need rewrites. The new sections covering the
  observer-as-functor reading, the vitality-profile predicate, and
  the conjecture set are listed in
  [`FRAMING_PIVOT_TASKS.md`](FRAMING_PIVOT_TASKS.md) Part 1.

---

## Part 5 — The new conjecture set

Replace `C1`–`C3` + `OP1`–`OP3` with the following hierarchy.
Existing items are kept (renamed where appropriate) and slotted as
lemmas underneath the three top-level statements. The conjecture
set is now organised around the vitality-profile predicate of §2.3.

```
S1   Sufficiency: some 4-tuple system + observer has vitality
     profile (k, σ) with k ≥ 1, hence is in LifeCat.
 |
 +-- L1 (= OP1): ∃ scaffolded system with CE > 0.
 +-- Persistence-lemma: F retains a non-empty entity across the window.
 +-- Discriminative-capacity lemma: V_T ∘ F preserves the entity AND
     would amplify a strictly fitter mutant if one appeared.
 +-- σ_1-witness lemma: ∃ system with σ_1 = 1, i.e. F at level 1
     depends on the system's own dynamical state (e.g. frequency-
     dependent or coevolutionary selection).

N1   Necessity: every system + observer pair with vitality profile
     (k, σ), k ≥ 1, decomposes as a 4-tuple system whose 𝒪_W-algebra
     reaches level k with the corresponding σ structure.
 |
 +-- C1' (closure-operator unification of F): makes Decomp canonical
     at each level i ≤ k.
 +-- C2' (hierarchical viability composition): the level-k+1 search
     is constructed from level-k operators; this is exactly C2'
     for each k.
 +-- C3' (observer = Sys→Obs functor in a divergence schema):
     the ascription side of LifeCat membership.
 +-- OP3' (operadic universality of T): topology side of Decomp;
     also underwrites multi-level topology structure.
 +-- OP2' (FEP scope): characterises the (X, Φ) pairs for which
     σ at every level can be FEP-parameterised.

CAT1 Characterisation: LifeCat ≃ image(Decomp), with the vitality-
     profile equivalence preserved — life-producing pairs at profile
     (k, σ) correspond to 4-tuple systems in Decomp's image at
     matching (k, σ).

LE   Level Emergence: a system at depth k undergoes a level
     transition to depth k+1 over a time window iff its level-k
     entities satisfy the four conditions (persistence, aggregation,
     group variation, group selection) over that window.
 |
 +-- Persistence sub-lemma: level-k entities have lifetimes much
     longer than substrate relaxation time.
 +-- Aggregation sub-lemma: kappa^(k) produces persistent multi-
     entity patterns.
 +-- Group-variation sub-lemma: kappa^(k) varies non-trivially
     across the population of aggregates.
 +-- Group-selection sub-lemma: aggregate types have measurably
     different persistence rates.
 +-- Connection to C2': hierarchical viability composition is the
     post-transition state of LE's mechanism.
 +-- Connection to OP3': operadic universality of kappa structure
     provides the substrate-independent statement.
```

`C1'`, `C2'`, `C3'`, `OP1` (= `L1`), `OP2'`, `OP3'` are the
statements we already have, re-pointed at the new framing and
graded by the vitality-profile level. The novel conjectures are
`S1`, `N1`, `CAT1`, `LE`, plus the three new sub-lemmas
(discriminative capacity, $\sigma_1$-witness, hierarchical $\sigma$
structure) and LE's four sub-lemmas. Together they are the
statements the project-instructions thesis requires.

LE differs from S1/N1/CAT1 in that it is *about transitions in
time*, not about static characterizations. The other three
conjectures ask "what is in $\mathbf{LifeCat}$, and what is its
structure?"; LE asks "how do systems move within $\mathbf{LifeCat}$,
and what conditions make movement possible?". LE is the dynamical
companion to the static characterization theorems.

---

## Part 6 — Ripple-effect inventory

The framing change has a known, finite set of edit targets. Listed
here roughly in dependency order:

### 6.1 Paper

| File | Action |
|------|--------|
| `emergent_systems.tex` abstract (lines 84–103) | Replace "methodology" wording with "characterization theorem and its staged proof obligations." |
| `emergent_systems.tex` intro (lines 110–137) | Replace "non-prescriptive ... comparative" stance with the stronger thesis; introduce `S1`/`N1`/`CAT1` upfront. |
| `emergent_systems.tex` §3.1 (lines 270–298) | Redefine $\mathcal{S}=(\mathbf{X},V,F,T)$; move $O$ to a new §3.7 or §4. |
| `emergent_systems.tex` §3.6 (Observer, lines 716–795) | Promote to its own section: "The independent observer functor." |
| `emergent_systems.tex` §3.8 (worked example, lines 1041–1156) | Re-write the Flow-Lenia + LLM example using the 4-tuple + external O. |
| `emergent_systems.tex` §4 (System Description, lines 1295–1366) | Reorganise structural items 1–7; add observation-record schema. |
| `emergent_systems.tex` §5.1 (conjectures, lines 1374–1500) | Replace with the `S1`/`N1`/`CAT1` + restatements of `C1'`–`OP3'`. |
| `emergent_systems.tex` §5.2 (scope, lines 1484–1500) | Rewrite — the framework no longer "stays neutral on agency"; it gives agency a precise operational meaning via the observer functor. |
| `emergent_systems.tex` results section (line 1368) | Currently a stub; populate with the sufficiency witness once `OP1`/`L1` lands. |

### 6.2 Textbook *(deleted)*

The textbook draft under `docs/textbook/` was **deleted on
2026-05-11**. The deletion is recorded in `CHANGELOG.md`.

The current strategy is to develop the framing pivot's implications
as a **series of focused result papers** under
[`docs/papers/`](papers/) using the existing
[`docs/papers/_template/`](papers/_template/) structure. Each
conjecture, worked example, and methodology piece becomes its own
focused paper, none of which compiles into a textbook unless and
until the framework's claims have substantial empirical and formal
support. The catalogue of result papers to be written is in
[`FRAMING_PIVOT_TASKS.md`](FRAMING_PIVOT_TASKS.md) Part 5.

### 6.3 Code

| File | Action |
|------|--------|
| `src/emergent_systems/system.py` | `System` becomes `System4Tuple`; `run(system, observer, ...)` takes the observer as an argument, not an attribute. |
| `src/emergent_systems/observer.py` | Protocols unchanged; usage site moves from inside `run()` to an external `observe()` function. |
| `src/emergent_systems/spec.py` | `SystemSpec` splits into `SystemSpec` (structural, 7 items minus observer) + `ObservationSpec` (observer family, window, state, descriptor space). |
| `tests/test_pipeline.py`, `tests/test_conformance.py` | Update fixtures to construct system and observer separately. |
| `examples/*` | Update stubs to reflect the new constructor signature. |

### 6.4 Notes / trackers

| File | Action |
|------|--------|
| `RESULTS.md` | Add rows for `S1`, `N1`, `CAT1`. Rename `C1` → `C1'` etc. with a note about the framing pivot. Update `Last updated` dates. |
| `docs/IMPLEMENTATION_PLAN.md` | Append a new section at the bottom documenting this framing change as a v2 design pivot. Per CLAUDE.md, "append a note to that file rather than silently diverging." |
| `proof_techniques.md` | The five cross-cutting techniques (Pillars 1–5) are all still relevant; their primary use cases shift slightly. Add a sixth pillar for **categorical decomposition theorems** (Decomp functor essential surjectivity) targeting N1. |
| `CLAUDE.md` | Update the "what this repo is" paragraph and the "load-bearing design decisions" item 1 (which currently asserts that the observer is one of the five slots). |
| `README.md` (project root) | Briefly tag the v2 pivot. |

---

## Part 7 — Open questions before any rewriting begins

Two of the four framing-prior questions are resolved; two remain
open and should be settled before Part 6's edit pass starts.

### Q1 — Ambient category for $\mathbf{Sys}$ *(resolved: SMC of $\mathcal{O}_W$-algebras in $\mathbf{Stoch}$, with an interpretive lift to a sheaf topos)*

**Decision.** $\mathbf{Sys}$ is the symmetric monoidal 1-category
whose objects are $\mathcal{O}_W$-algebras valued in the Markov
category $\mathbf{Stoch}$ (measurable spaces with Markov kernels),
with monoidal product inherited from $\mathcal{O}_W$ and morphisms
the $\mathcal{O}_W$-algebra natural transformations. This is the
minimal extension of what the existing framework already commits to:
$\boxtimes_\kappa$ is symmetric monoidal, $V$ is stochastic,
$F$ is measure-theoretic, and N1's anchor on $\mathcal{O}_W$ now
matches the foundational ambient.

**Why this option and not a topos or a 2-category.** The first
round of theorems (S1, $L_1$, N1) is most tractable in a
1-categorical operadic setting where Yau 2018's finite-presentation
result transfers directly. Adding 2-morphisms or sheaf-theoretic
locality would buy specific features (essential surjectivity as a
first-class concept; locality as a primitive) at the cost of
heavier proof machinery, and neither feature is load-bearing for
the early theorems. Upgrade paths remain open: 2-categorical
(Baez–Pollard-style) is reachable if N1's essential surjectivity
demands first-class treatment; double-categorical
(Baez–Courser-style) is reachable when C2' (hierarchical viability)
becomes the active research target.

**Interpretive lift to Option C.** The Aristotelian / autopoietic /
FEP reading of life as local-pattern-that-glues is preserved as an
**interpretive layer** rather than discarded. Three functorial
bridges from $\mathbf{Sys}$ to a sheaf topos are available, in
order of directness:

1. **Schultz–Spivak 2019.** Their Temporal Type Theory provides a
   functor from $\mathcal{O}_W$-algebras to sheaves on a base site
   of time-windows of observation. This bridge handles the
   time-indexing axis directly and is the published precedent that
   makes the lift citable rather than novel.
2. **Classifying topos of $\mathcal{O}_W$.** Every operad
   $\mathcal{O}$ admits a classifying topos
   $\mathbf{Sh}(\mathcal{O})$ such that
   $\mathcal{O}_W$-algebras in any topos $\mathcal{T}$ correspond to
   geometric morphisms $\mathcal{T} \to \mathbf{Sh}(\mathcal{O})$.
   The category of wiring-diagram algebras is therefore *already a
   topos in disguise*; Option A and Option C are two presentations
   of the same data.
3. **Substrate-induced locality.** When the substrate
   $\mathbf{X}$ has a natural locality structure (lattice geometry,
   particle positions, memory adjacency), that locality pulls back
   through the $\mathcal{O}_W$-algebra to a site $\mathcal{B}$ of
   substrate patches, and the algebra induces an honest sheaf on
   $\mathcal{B}$. This is the practically useful bridge for
   biology-like discussion: a Flow-Lenia algebra becomes a sheaf of
   local field-patches; a cell becomes a sheaf of local
   reaction-network patches; the cell-membrane-as-local-self-
   maintenance reading falls out naturally.

The strategy is therefore: **prove in Option A, interpret in
Option C.** All theorems (S1, N1, CAT1, the restated C1'/C2'/C3'
and OP1-3') are stated and proved in $\mathbf{Sys}$ as defined
above. The companion sheaf-topos view is invoked when the
discussion turns to philosophical commitments (Aristotelian form;
autopoiesis; FEP) or to biology-specific intuitions about
local-to-global self-maintenance. The lift is faithful — the same
underlying algebra appears in both presentations — but each
presentation makes different things crisp: compositional theorems
are clean in A; locality-based interpretations are clean in C.

What gets less crisp in the lifted Option C view is the operadic
composition itself (it becomes implicit in the gluing). This is
acceptable because the proofs do not happen in the lifted view.

### Q2 — Precise definition of "life-producing" *(resolved: vitality profile)*

**Decision.** $\mathbf{LifeCat}$ membership is defined by the
composite predicate of §2.3: $\mathrm{CE} > 0$ + entity persistence
+ search-hierarchy level $k \geq 1$ with discriminative capacity at
each level, with the full vitality profile $(k, \boldsymbol{\sigma})$
reported as an attribute of each member.

The predicate was stress-tested across six representative cases:

- **Hurricane** → $(0, (0))$ — substrate-only dynamics, excluded.
- **Standard converged GA** → $(1, (0))$ — homeostatic Darwinian
  life with externally-fixed objective. Convergence is consistent
  with life via the discriminative-capacity refinement.
- **HeLa cells in lab culture** → $(2, (1, \approx 0.4))$ — wild at
  the cell scale, partially domesticated at the population scale.
  The $\sigma$ vector formally captures "domestication."
- **Active Tierra in arms race** → $(2, (1, 1))$ — programmatic
  life reaching the same vitality profile as wild biology. The
  operational cash-out of the Q4 predictive thesis.
- **Stabilised Tierra** → $(2, (1, 0))$ — alive at level 1, but
  level-2 self-reference has degraded. Open-endedness loss is
  $\sigma_2$ collapse, not death.
- **Human language / cultural evolution** → $(3, (1, 1, 1))$ or
  $(4, (1, 1, 1, 1))$ — the deepest profile observed, exceeding
  individual biology. Cultural systems are *more structurally
  alive* than individual organisms in the framework's metric.

In every case the predicate produced a principled verdict matching
or sensibly extending intuition. The verdicts cleanly distinguished
cases that classical definitions of life muddle.

**Consequences for the framing.**

- The membership predicate is binary at the level of "is the
  system in $\mathbf{LifeCat}$" (yes iff $k \geq 1$), but the
  framework reports the full $(k, \boldsymbol{\sigma})$ as the
  vitality profile of each member. This gives the framework both
  the categorical clarity it needs for theorems (binary
  membership) and the fine-grained discrimination biology
  actually cares about (graded profile).
- Open-endedness is no longer constitutive of life. It is the
  property that $\sigma$ stays non-zero at higher levels over
  time. A system that loses higher $\sigma$ values is still alive
  at its lower levels; it has just become less open-endedly
  creative. This resolves the long-standing ALife puzzle of
  "novelty production stopping" — what stops is not life but
  the higher-level $\sigma$ structure.
- Agency, in the deflationary sense of §8.4, gets sharper
  structural content: it is the value of the highest non-zero
  $\sigma_i$. A system has more agency at higher levels of
  self-reference.

**What remains as downstream technical work.**

- The exact mathematical definition of "$\sigma_i$ depends on the
  system's dynamical state beyond the current population" needs
  to be tightened against the ambient category of Q1 (SMC of
  $\mathcal{O}_W$-algebras in $\mathbf{Stoch}$). The informal
  reading is clear; the formal version requires specifying which
  measurability and dependence conditions the framework demands.
- The discriminative-capacity condition at level $i$ needs a
  precise operational form: probably "there exists a perturbation
  to $V$'s output distribution that the iteration $V_T \circ F$
  would amplify."
- The relationship between vitality-profile composition under
  $\boxtimes_\kappa$ and the existing hierarchical-viability
  formalism $F^*$ needs to be worked out. This is downstream
  of C2'.

These are paper-rewrite-pass-level details, not framing-prior
decisions.

### Q3 — Ambient framework for N1 *(resolved: operadic wiring diagrams)*

**Decision.** N1 is stated in the operad of wiring diagrams
$\mathcal{O}_W$ of Vagner–Spivak–Lerman 2015 (with extensions to
streamed / time-indexed systems via Schultz–Spivak 2019). Every
life-producing $\mathcal{O}_W$-algebra must factor through
$\mathrm{Decomp}$ into the 4-slot category. See §3.2 for the
restated conjecture and §3.4 / Part 5 for how `OP3'` (multiplex
universality) becomes a facet of the same theorem rather than a
parallel result.

**Consequences for the edit pass.**

- The paper rewrite anchors on
  [proof_techniques.md §OP3](proof_techniques.md), Pillar 2
  (category theory / operads / compositional systems), and Yau 2018
  (finite presentation of $\mathcal{O}_W$) rather than maintaining
  a list of "any-formalism" candidates.
- The decomposition functor $\mathrm{Decomp}$ becomes a
  $\mathcal{O}_W$-algebra morphism with checkable generator-by-
  generator obligations.
- N1 and OP3' share machinery; their proofs should be coordinated,
  not pursued in parallel.

### Q4 — Predictive vs. re-descriptive *(resolved: predictive)*

**Decision.** The framework is **predictive**. The thesis claims
that life is realisable in any $\mathcal{O}_W$-presentable substrate
satisfying the S1 sufficiency conditions under some independent
observer; biological life is one such realisation. Specifically,
the framework predicts:

- **Programmatic life** as a genuine instance of the same theorem
  that produces biological life, not as a metaphor.
- **Hybrid biological–computational life** via $\boxtimes_\kappa$
  composition.
- **Cultural / memetic life** under sufficiently rich substrates.
- **Substrate-novel life** in any $\mathcal{O}_W$-presentable system
  meeting the conditions.

It must also predict **negatives**: physical systems with
$\mathrm{CE} > 0$ that are not alive (hurricanes, chaotic maps)
must be cleanly excluded by the conjunction of conditions 1–3.

The full statement and worked predictions live in §2.5. The
predictive stance is now load-bearing: non-engineered domains
(biology, culture, ecology) are no longer "frontiers" but
**predictions of the theory**, and the framework's philosophical
content must commit to the substrate-agnostic position rather than
preserving neutrality. Future result papers under
[`docs/papers/`](papers/) will work these out one by one.

**Status of Q1 and Q2 dependencies.** Q3's resolution constrains
Q1's natural answer; Q4's resolution makes Q2 more urgent because
the membership predicate must do both inclusion (programmatic life
in) and exclusion (hurricanes out). Q1 and Q2 are the remaining
framing-prior decisions before §3.1 of the paper is rewritten.

---

## Part 8 — Philosophical implications of the chosen framing

The choice of ambient category is not metaphysically neutral. The
formal apparatus of Part 2 + the Q1 / Q3 / Q4 resolutions commit
the framework to a specific philosophical position. This section
records that position so future editing of the paper and future
result papers can be coherent with it, and so subsequent decisions
(Q2 in particular) can be made in light of it.

### 8.1 What "system" commits us to

The 4-tuple $\mathcal{S}=(\mathbf{X},V,F,T)$ presented as an
$\mathcal{O}_W$-algebra in $\mathbf{Stoch}$ commits the framework
to a **modernised mechanism with compositionality**. The mechanist
intuition — that a living thing is a kind of machine — is preserved
but is upgraded in two ways. First, the machine is *compositional*:
it is not a single integrated artefact but a recipe for building
bigger machines out of smaller ones, with the operadic structure
making the composition first-class. Second, the machine is
*stochastic*: probability is not a description-of-our-ignorance but
a feature of the components, present in the Markov-category
structure of $\mathbf{Stoch}$.

There is no intrinsic essence of a system separate from its slot
decomposition. Two systems are *the same system* exactly when their
$\mathcal{O}_W$-algebras agree. If two presentations of a system
cannot be told apart by their box-contents and wiring, they are not
"secretly different"; they are literally identical objects of
$\mathbf{Sys}$. This is a strong anti-essentialist commitment that
matches the predictive thesis: substrate is what's inside the
boxes and never appears in the formalism, so substrate-agnosticism
is *enforced* rather than asserted.

### 8.2 What "life" commits us to

In the Option-A formal layer, **a life-form is a particular wiring
of stochastic components that produces emergence + open-endedness +
persistence under some independent observer**. There is no
additional life-essence beyond the slot decomposition and the
observer that witnesses it. Two systems are the same life-form iff
their algebras agree (or, in a later 2-categorical upgrade, iff
they are 2-equivalent).

In the Option-C interpretive layer accessed through the lift,
**a life-form is a pattern of local self-consistency that glues to
a coherent global identity**. The Aristotelian / autopoietic / FEP
readings — life as form, life as self-production, life as
surprise-minimisation — are recoverable as descriptions of the
induced sheaf of substrate patches. The lifts of Schultz–Spivak,
the classifying topos, and substrate-induced locality each make
explicit a different facet of this reading.

These two readings are not in tension. They are two presentations
of the same underlying $\mathcal{O}_W$-algebra. The compositional
reading (A) is what the proofs are about. The local-self-maintenance
reading (C) is what the philosophical discussion is about. Both
can be invoked without contradiction because they are different
forgetful projections of the same data.

### 8.3 Stances the framing rejects

The framing as resolved is not philosophically neutral on every
question. Three positions are explicitly rejected by the choice of
Option A + the C-via-lift strategy:

- **Pure substantialism.** Life is not a kind of stuff. There is
  no élan vital, no carbon chauvinism, no insistence that biology
  is the only substrate for life. The substrate-agnostic typing
  forbids this position structurally — substrate never appears
  outside the box-contents.
- **Eliminative reductionism about levels.** Life is not "really
  just" microphysics with macroscopic redescriptions. Hoel-style
  causal emergence as a $\mathbf{LifeCat}$ membership condition
  makes macroscopic causal structure a non-eliminable part of the
  definition: if the system has $\mathrm{CE} > 0$ at some
  coarse-graining, the macro level is not a redescription.
- **Pure functionalism without composition.** Life is not just
  "anything that does the right kind of input-output mapping."
  The compositional / operadic structure means life-forms have
  internal architecture that matters, not just behavioural
  profiles. Two systems with the same input-output behaviour but
  different $\mathcal{O}_W$-algebras are not the same life-form in
  the strict (Option A) sense; whether they should be in a later
  2-categorical extension is Q1's deferred upgrade question.

### 8.4 The agency question

The previous framing
([`emergent_systems.tex:1497`](emergent_systems.tex)) said the
scaffold "stays neutral on ... the metaphysical status of agency."
The new framing does not stay neutral. Agency in this picture is
**what an independent observer ascribes to a system whose
viable-entity trajectories the observer cannot predict from the
substrate dynamics alone**. Concretely, agency is a property of the
pair $(\mathcal{S}, O)$, not of $\mathcal{S}$: it is the gap
between what $O$ would predict from $\Phi$ alone and what $O$
observes once $V$ and $F$ have acted on $\mathcal{S}$'s viable
entities.

This is a deflationary account of agency that nonetheless gives the
concept formal content. It rejects both "agency is an illusion"
(the gap is real and computable) and "agency requires a special
metaphysical category" (the gap lives entirely in the
observer-functor's prediction residual). Whether biological
organisms are agents on this account is an empirical question the
framework makes precise rather than a metaphysical question it
takes a position on.

### 8.5 What kind of theory this is

The framework is a **mathematical theory of life** in the same
sense that thermodynamics is a mathematical theory of heat:
substrate-agnostic, predictive, and stated as theorems with proof
obligations rather than as a metaphysics. Biological life is one
realisation. Programmatic life is another. Cultural and linguistic
life is another. The theory predicts the existence of further
realisations in substrates we have not yet explored — wherever an
$\mathcal{O}_W$-algebra in $\mathbf{Stoch}$ satisfies the S1
sufficiency conditions under some independent observer, the theory
commits us to calling the result alive at some vitality profile.

This is the position the scaffolding paper's introduction and
abstract should articulate: not "vocabulary, not theory," but **a
mathematical theory of life as the categorical structure of
emergent stochastic systems whose search hierarchies reach level
$k \geq 1$, observed and ascribed life by an independent observer
functor**. Result papers under [`docs/papers/`](papers/) should
treat this as the central thesis from page one.

### 8.6 Life as graded, not binary

The vitality-profile resolution of Q2 commits the framework to a
specific structural picture of life that is neither the binary
"alive vs. not alive" of much of biology nor the cluster-concept
treatment of analytic philosophy. Life on this view is a **graded
phenomenon with categorical membership** — there is a binary
threshold (the system is in $\mathbf{LifeCat}$ iff $k \geq 1$),
but membership comes with a vitality profile $(k, \boldsymbol{\sigma})$
that locates the system on a multidimensional landscape of
life-likeness.

The philosophical commitments this involves:

- **Life is not all-or-nothing above the threshold.** A hurricane
  is not alive (level 0 only). But a converged GA, a homeostatic
  bacterium in a fixed environment, a wild bacterial population,
  a multicellular organism, and a cultural system are all alive
  in different ways measurable by $(k, \boldsymbol{\sigma})$.
  The framework rejects the cluster-concept reading by giving a
  precise predicate; it rejects the binary reading by reporting
  structure inside the predicate.
- **Cultural systems are deeper than individual biological
  organisms.** This is a non-trivial commitment that the
  scaffolding paper and the cultural-life result paper
  (`cultural_life_decomposition/`) must defend. The framework's
  "depth" is structural — number of nested levels of self-shaping
  search — not moral or axiological. Cultures matter because of
  the people who carry
  them, not because of their categorical depth, and the framework
  is explicit about this.
- **Open-endedness is a $\boldsymbol{\sigma}$ property, not a
  $\mathbf{LifeCat}$-membership property.** Systems can be alive
  without being open-endedly creative; they just sit at lower
  $\sigma$ values at the higher levels. This makes the
  "open-endedness problem" of ALife into a precise question
  about $\sigma_2$ (and higher) collapse over time, rather than
  a question about what life is.
- **The framework predicts new categories of life-like systems
  that biology has not named.** Programmatic life at $(1, (1))$
  is real — frequency-dependent GAs are alive in the framework's
  sense. Domesticated systems at $(2, (1, \approx 0))$ form a
  category that includes both HeLa cells and old-style stable
  Tierra runs. The framework's taxonomy may turn out to be
  empirically useful even before the central theorems are
  proved.

This graded picture is recoverable in the Option-C interpretive
layer: the levels of the search hierarchy correspond to nested
sites in the sheaf-topos lift, and the $\sigma_i$ at each level
corresponds to the local-to-global self-consistency at that site.
The Aristotelian / autopoietic / FEP readings remain available;
they now refer not to "life or not life" but to "life at level $i$
with $\sigma_i = 1$."

The recursive level definition of §2.3 makes this even more
explicit. The framework no longer commits to a fixed taxonomy of
levels (substrate / entity / population / meta); it commits to a
recursion in which each level's entities are defined by the
previous level's $(V, F)$-induced dynamics. Under the Q1
resolution, this recursion is exactly the arity-counting of the
operad of wiring diagrams — level $n$ is what the operad produces
by composing $n$ times. The framework's "depth of life" is
therefore not a measured-from-outside property; it is the
intrinsic compositional depth of the system viewed as an
$\mathcal{O}_W$-algebra. This is the strongest possible form of
substrate-agnosticism: even the level structure that distinguishes
biological from cultural systems is a property of the categorical
shape, not of the substrate's chemistry or physics.

### 8.7 The two ways of being made

The framework now commits to two distinct compositional moves —
**vertical** (recursive level-raising) and **horizontal**
($\boxtimes_\kappa$ at fixed level) — and the philosophical content
of this distinction is worth pulling out.

Vertical composition is the **stacking** move: smaller things
become the substrate for the activity of larger things. Cells
become the material out of which tissues are made; tissues become
the material of organs; organs become the material of organisms.
The recursion ascends through scales of organisation, with each
ascent producing genuinely new entities that have their own search
dynamic. Aristotle's hierarchy of nutritive, sensitive, and
rational souls is — in the framework's terms — a vertical
composition: each ensouled kind builds on the kind below.

Horizontal composition is the **alongside** move: things at the
same scale combine to produce something whose existence depends on
the coupling. The lichen is not above the alga and fungus in any
scale-of-organisation sense; it is alongside both of them,
constituted by their mutual coupling. A coevolutionary host-parasite
ecology is not a higher level above the host and parasite
populations; it is the two populations together with the coupling
that joins them. The composite is a real categorical object — an
$\mathcal{O}_W$-algebra in its own right — but it lives at the
same level as its components.

The framework's claim is that life is **assembled by both
operations**. Neither alone produces what we recognise as
life-likeness in its full form. Purely vertical composition without
horizontal coupling would give organisms with no ecological
context, no co-evolving partners, no symbiotic associations —
structurally hollow at every level. Purely horizontal composition
without vertical recursion would give parallel substrates with no
emergent higher-level structure — coevolving particles that never
form cells, communities that never form societies. Real life-forms
exhibit both: a cell is vertically composed of molecular machinery
and horizontally coupled to its environment; an organism is
vertically composed of cells and horizontally coupled to its
symbionts and predators; a culture is vertically composed of
practices and horizontally coupled to neighbouring cultures.

This two-axis picture also clarifies what was contested in earlier
philosophical traditions. The **mechanists** focused on vertical
composition (everything is built from parts at the level below);
they missed the horizontal coupling that constitutes things at
their own level. The **holists** focused on horizontal composition
(everything depends on its environment); they sometimes denied the
real vertical structure that makes nested levels of organisation
non-arbitrary. The **autopoieticists** focused on the case where
vertical and horizontal coupling fuse into a single self-producing
loop — the cell as a structure whose components horizontally
produce each other and vertically constitute the membrane that
bounds the whole. Each frame is articulating one piece of the
two-axis picture. The framework's job is to hold both axes
without choosing.

The operational consequence: when discussing a specific life-form,
the framework asks two separate structural questions. *What is its
vertical depth?* — its $k$. *What are its horizontal couplings at
each level?* — its $\kappa$-structure. A human individual is at
$k \approx 3$ vertically and is horizontally coupled to a
microbiome at the gut level, to a speech community at the cultural
level, to a planetary biosphere at the ecological level. Each of
these couplings is a real compositional fact about the human, and
the human's full categorical description requires naming all of
them.

The framework's Option-C interpretive lift makes this
two-axis structure particularly clean. Sheaves naturally express
both: the vertical structure becomes nested sites at different
scales of locality, the horizontal structure becomes the gluing of
local patches across substrates at a single site. The
Aristotelian / autopoietic / FEP readings of biology all live
inside this lifted view, with vertical and horizontal composition
appearing as the operations they implicitly require but rarely
distinguish.

### 8.8 Biogenesis at every level

With LE added in §2.6, the framework now commits to a third
philosophical position: **biogenesis is a structural mechanism
that applies at every level of organisation, not a one-time event
at the chemistry-to-cell transition**. The same four conditions —
persistence of lower-level entities, aggregation via horizontal
coupling, variation of the coupling, differential selection of
aggregates — that gave rise to cells from chemistry also gave rise
to multicellular organisms from cells, to ecosystems from
organisms, to cultures from hominid behaviour. The mechanism is
substrate-agnostic and recursive.

This positions the framework against three alternative views.

**Against vitalism in any form.** Vitalism claims that life
required a special principle to come into being. LE replaces the
special principle with a structural mechanism that has no
substrate-specific content. Wherever the four conditions are met,
a level transition follows; no special-cause is needed at the
chemistry-to-cell step or any subsequent step.

**Against "origin of life" exceptionalism.** A common reading
treats the origin of life on Earth as a uniquely difficult
problem requiring uniquely improbable circumstances. The framework
treats it as one instance of a recurring mechanism. The chemistry
→ cells transition is structurally identical to the cells →
organisms transition and to the organisms → ecosystems transition.
Each step is "improbable" in the same sense — it requires the four
conditions to align over a sufficient time window — but no step is
metaphysically more difficult than any other.

**Against accidental hierarchies.** A reductionist reading might
treat hierarchical organisation as a contingent accident of
evolutionary history — biology happens to have multiple levels,
but there's no deep reason for this. LE says the levels are not
accidental: they are the necessary structural consequence of the
four conditions being met repeatedly. Any system in any substrate
that satisfies the conditions will develop hierarchical structure;
hierarchy is a structural attractor of compositional dynamics, not
a historical artefact.

The framework's prediction is that level transitions are happening
right now in non-biological substrates. Programmatic ecosystems
(Tierra-style or modern), multi-agent foundation-model systems,
cultural systems in rapid change — all of these are candidates for
ongoing level transitions, and LE gives the structural test for
detecting them. The "origin of life" question becomes the special
case of LE applied to chemistry; the more general question is "at
what level transitions is the universe currently in the middle
of?", and the framework is committed to answering it across
substrates.

---

## Recommendation

**All four framing-prior questions are now resolved.** Adopt the
framing in Parts 2–5 and the philosophical commitments in Part 8.
The paper-edit pass in Part 6 is unblocked.

- **Q1** (ambient category of $\mathbf{Sys}$): SMC of
  $\mathcal{O}_W$-algebras in $\mathbf{Stoch}$, with interpretive
  lift to a sheaf topos via Schultz–Spivak / classifying-topos /
  substrate-induced-locality. *Prove in Option A, interpret in
  Option C.*
- **Q2** ($\mathbf{LifeCat}$ membership predicate): vitality
  profile $(k, \boldsymbol{\sigma})$ with $k \geq 1$ membership
  threshold and the full profile reported as an attribute.
  Discriminative-capacity refinement replaces the earlier "not a
  fixed point" reading. $\sigma$ is vector-valued over the search
  hierarchy. Stress-tested against six representative cases:
  hurricane, converged GA, HeLa, active and stabilised Tierra,
  cultural evolution.
- **Q3** (necessity-side ambient framework): operad of wiring
  diagrams (Vagner–Spivak–Lerman 2015; Yau 2018 for finite
  presentation; Schultz–Spivak 2019 for time-indexing).
- **Q4** (descriptive vs. predictive): predictive. The framework
  predicts programmatic, hybrid, cultural, and substrate-novel
  life as genuine instances at specific vitality profiles, with
  the operational verdict matching biological life at the same
  profile.

Three concrete milestones to prioritise in the order given:

1. **`L1` (= renamed `OP1`) as the first concrete result.** A
   positive `L1` result on Game-of-Life-under-Markov-blanket-
   viability remains the lowest-cost piece of evidence that the
   stronger thesis is tractable. Once it lands, the paper rewrite
   has a concrete sufficiency witness with a known vitality
   profile to anchor on.
2. **Programmatic-life decomposition.** Specialise
   $\mathrm{Decomp}$ to a Tierra-arms-race fragment and exhibit
   the four slots plus the vitality profile $(2, (1, 1))$. The
   cheapest demonstration that programmatic life and wild
   biological life have the same profile by the framework's own
   criteria — making the "same theorem" claim immediately
   auditable.
3. **Cultural-life decomposition.** Specialise $\mathrm{Decomp}$
   to a small slice of linguistic evolution (the Great Vowel
   Shift, or a meme cycle on social media) and exhibit the
   level-3 vitality profile. This is the deepest test the
   framework's predictive thesis is committed to and the one
   most likely to draw productive pushback from outside ALife.

With these three milestones in hand, the paper rewrite in Part 6
can proceed against concrete witness systems at each of the
vitality-profile levels the framework commits to. Each milestone
becomes a focused result paper under
[`docs/papers/`](papers/) per the catalogue in
[`FRAMING_PIVOT_TASKS.md`](FRAMING_PIVOT_TASKS.md) Part 5.
