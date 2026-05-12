# Proof techniques and reading list for `emergent_systems.tex` §5.1

A reading list for the proof attempts on the conjectures (C1-C3) and open
problems (OP1-OP3) in [`docs/emergent_systems.tex`](emergent_systems.tex)
§5.1. Status of each item lives in [`RESULTS.md`](../RESULTS.md); per-result
proof papers go under [`docs/papers/`](papers/).

The document is organised in two parts:

1. **Cross-cutting techniques** — the five mathematical pillars that appear
   across multiple items. Read these once and reuse.
2. **Per-item reading lists** — for each of C1, C2, C3, OP1, OP2, OP3,
   the specific proof techniques to study, canonical textbook references,
   and the most directly applicable example proofs already in the literature.

Each per-item section follows the same A/B/C/D structure (techniques /
textbooks / example proofs / proof-pattern sketch where applicable) so
that the same headings can be filled in for any new conjecture added
later.

---

## Part 1 — Cross-cutting techniques

These five pillars each support at least two items below; studying them
once pays off across multiple proof attempts.

### Pillar 1: Order theory and closure operators

Used by **C1** (the conjecture is *about* closure operators) and **C2**
(composition of closure operators). The core objects: posets, complete
lattices, Moore families, closure operators c: 2^X -> 2^X (extensive,
monotone, idempotent), Galois connections / FCA, Knaster-Tarski.

Pillar reference: Davey & Priestley, *Introduction to Lattices and Order*
(2002, 2nd ed.), Chs. 2 and 7. Free supplement: the Stanford Encyclopedia
of Philosophy entry on Formal Concept Analysis.

### Pillar 2: Category theory, operads, and compositional systems

Used by **C2** (functorial / monadic composition of closure operators)
and **OP3** (operadic universality of multiplex topologies). Core
machinery: symmetric monoidal categories, operads (especially the operad
of wiring diagrams of Vagner, Spivak & Lerman 2015), decorated and
structured cospans (Fong; Baez & Courser), algebras over operads, and
universality / finite-presentation theorems for operads (Yau 2018).

Pillar reference: Fong & Spivak, *Seven Sketches in Compositionality*
(2019, free at arXiv:1803.05316), then either Yau's *Operads of Wiring
Diagrams* (Springer LNM 2192) or Markl-Shnider-Stasheff for the deeper
operadic machinery.

### Pillar 3: Information theory and divergences

Used by **C3** (the conjecture is *about* divergences) and **OP1**
(effective information is a KL functional of a perturbed forward
distribution against a uniform intervention). Core machinery:
f-divergences (Csiszar), Bregman divergences (Amari information
geometry), integral probability metrics (Sriperumbudur et al. on the
IPM/f-divergence dichotomy), variational representations
(Donsker-Varadhan, Fenchel duality, MINE), and optimal transport for
the Wasserstein side.

Pillar reference: Polyanskiy & Wu, *Information Theory: From Coding to
Learning* (Cambridge 2025; free draft online), then Nielsen's elementary
information-geometry primer (Entropy 2020) for the Bregman side and
Peyre & Cuturi for OT.

### Pillar 4: Stochastic processes and dynamical systems

Used by **OP2** (FEP rests on Langevin SDEs at NESS with Helmholtz
decomposition) and **OP1** (lumpability of Markov chains under
coarse-graining). Core machinery: finite Markov chains and lumpability
(Kemeny-Snell strong/weak lumpability), Fokker-Planck and Langevin
equations, Helmholtz decompositions of stationary flow into solenoidal
+ dissipative parts, non-equilibrium steady-state probability flow.

Pillar reference: Pavliotis, *Stochastic Processes and Applications*
(Springer TAM 60, 2014) for the continuous-time side; Kemeny & Snell,
*Finite Markov Chains* (1976) Ch. 6 for the discrete side.

### Pillar 5: Causal emergence and coarse-graining

Used by **OP1** directly, and indirectly by **C1/C2** (viability filters
projected through a coarse-graining). Core machinery: Hoel-style
effective information and causal emergence
(Hoel-Albantakis-Tononi 2013, Hoel 2017, Klein-Hoel 2020,
Comolatti-Hoel 2022), Partial Information Decomposition (Williams-Beer
2010) and integrated information decomposition Phi-ID (Mediano et al.
2021/2025), and CA / ECA coarse-graining (Israeli-Goldenfeld 2004/2006).

Pillar reference: Hoel-Albantakis-Tononi (2013, PNAS) is the source
paper; Comolatti & Hoel (2022, arXiv:2202.01854) is the unifying view
across measures.

### Pillar 6: Categorical decomposition theorems (added 2026-05-11)

Used by **N1** (the new top-level necessity conjecture introduced
by the 2026-05-11 framing pivot; see
[`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) §3.2) and indirectly by
**CAT1**. The core question is whether a constructive
decomposition functor
$\mathrm{Decomp}: \mathrm{Alg}(\mathcal{O}_W) \to \mathbf{Sys}^{4\text{-slot}}$
exists with proven essential surjectivity onto $O$-observable
behaviour. The machinery is the same operadic / structured-cospan
apparatus used by C2 and OP3, but applied to the bigger question
of decomposition rather than to compositional preservation.

Core machinery: essential surjectivity of functors (Riehl,
*Category Theory in Context*, Ch. 1); the Yoneda embedding and
density theorems; classifying topoi for operads; the algebraic-
geometry analogy of $\mathrm{Spec}$ functors for $\mathcal{O}_W$-
algebras; lax / pseudonatural transformations as the typing for
"essentially surjective on observable behaviour."

Pillar reference: Riehl, *Category Theory in Context* (Dover 2017)
for the basic categorical apparatus, then Yau, *Operads of Wiring
Diagrams* (Springer LNM 2192, 2018) for the operadic specialisation,
then Baez & Pollard (2017) *A Compositional Framework for Reaction
Networks* (arXiv:1704.02051) as the closest existing instance of a
decomposition-functor proof in a substrate-adjacent context.

This pillar reuses substantial machinery from Pillar 2 (operads
and compositional systems). The new content is specifically about
*decomposing* arbitrary $\mathcal{O}_W$-algebras into the
four-slot form, which is a question the existing pillar does not
cover directly. Expect proofs to combine Yau's finite-presentation
results with a constructive case analysis on operadic generators.

---

## Part 2 — Per-item reading lists

### S1: Sufficiency

**Statement.** There exists a 4-tuple system + observer pair
$(\mathcal{S}, O)$ with vitality profile $(k, \boldsymbol{\sigma})$
satisfying $k \geq 1$, hence is in $\mathbf{LifeCat}$.

**Status.** UNPROVEN as of 2026-05-11. Subsumed in practice by `L1`
(see below) once that lands.

#### A. Proof techniques to study

- **Exhibit-and-verify.** S1 is an existence claim. The standard
  proof technique is to exhibit a concrete witness and verify the
  membership predicate's three conditions ($\mathrm{CE} > 0$,
  entity persistence, level $k \geq 1$ with discriminative
  capacity).
- **Reduction to known causal-emergence results.** If the
  candidate system is a finite Markov chain with a known
  coarse-graining at which $\mathrm{CE} > 0$ (Klein-Hoel; Hoel-
  Levin), the emergence condition is already covered; only entity
  persistence and level-$k$ structure remain.

#### B. Canonical references

Reuse the OP1 reading list — `L1` is a concrete sufficiency
witness, so its references serve `S1` as well.

#### C. Lowest-hanging fruit

Game of Life under Markov-blanket viability per OP1 §D below. A
positive L1 is automatically a positive S1.

---

### N1: Necessity

**Statement.** For every life-producing pair $(\mathcal{S}', O)$
with $\mathcal{S}'$ presentable as an $\mathcal{O}_W$-algebra,
there exists a 4-tuple system $\mathcal{S}$ and a slot-preserving
morphism $\mathcal{S} \to \mathcal{S}'$ that is essentially
surjective on $O$-observable behaviour.

**Status.** UNPROVEN as of 2026-05-11. The hardest of the
top-level conjectures.

#### A. Proof techniques to study

- **Yau's finite-presentation theorem for $\mathcal{O}_W$.** 8
  generators and 28 relations for the directed case. Reduces N1
  to a finite case analysis: verify Decomp respects each
  generator's action.
- **Decorated and structured cospans** (Baez & Courser 2020).
  The natural setting for stating "decomposition functor with a
  decoration that tracks $O$-observable behaviour."
- **Essential surjectivity in 1-categories** (Riehl Ch. 1). The
  weak form of equivalence the framework needs is essential
  surjectivity on objects modulo behavioural equivalence.

#### B. Canonical references

- Riehl, *Category Theory in Context*, Dover 2017.
- Yau, *Operads of Wiring Diagrams*, Springer LNM 2192, 2018.
- Vagner, Spivak & Lerman (2015), arXiv:1408.1598.
- Baez & Pollard (2017), arXiv:1704.02051.

#### C. Example proofs to imitate

- **Baez & Pollard 2017** — every open reaction network maps via
  a black-box functor to an open dynamical system. The blueprint
  for "every $\mathcal{O}_W$-algebra maps via $\mathrm{Decomp}$
  to a 4-slot system." The proof pattern transplants almost
  directly; only the codomain (4-slot systems vs. open dynamical
  systems) changes.
- **Fong 2016** (Oxford PhD thesis) — worked universal-property
  proofs for circuits, signal-flow graphs, Markov processes via
  decorated cospans. The decoration machinery is the right home
  for the $O$-observable-behaviour decoration N1 needs.

#### D. Dependencies

N1's proof needs the Decomp functor *as a constructive object*.
That construction itself is non-trivial and is the bulk of the
work; coordinate with OP3 (which shares the operadic-universality
machinery) and with C1 (which makes Decomp canonical on the
viability side).

---

### CAT1: Characterisation

**Statement.** $\mathbf{LifeCat} \simeq \mathrm{image}(\mathrm{Decomp})$,
with vitality-profile equivalence preserved across the
correspondence.

**Status.** UNPROVEN as of 2026-05-11. Depends on S1 and N1.

#### A. Proof techniques to study

CAT1 is essentially S1 + N1 + a coherence theorem. The new content
is the coherence — verifying that vitality profiles match across
the equivalence. The techniques are:

- **Coherence in symmetric monoidal categories** (Mac Lane Ch. 7,
  *Categories for the Working Mathematician*).
- **2-categorical coherence** if vitality-profile equivalence
  must be tracked as a 2-morphism.

#### B. Canonical references

- Mac Lane, *Categories for the Working Mathematician*, 2nd ed.
  Springer 1998.

#### C. Dependencies

CAT1 should be the *last* of the top-level conjectures attempted.
Once S1 and N1 land, CAT1 is largely bookkeeping; before they
land, CAT1 is meaningless.

---

### LE: Level Emergence

**Statement.** A system $\mathcal{S}$ at vitality profile depth
$k$ undergoes a level transition to depth $k + 1$ over a time
window iff its level-$k$ entities satisfy four conditions over
that window: persistence, aggregation, group variation, group
selection.

**Status.** UNPROVEN as of 2026-05-11. Independent of S1/N1/CAT1
— can be pursued in parallel.

#### A. Proof techniques to study

- **Maynard Smith & Szathmáry 1995** (*The Major Transitions in
  Evolution*) — the empirical / biological precedent. Eight
  transitions, each conforming to the four conditions LE states
  formally.
- **Buss 1987** (*The Evolution of Individuality*) — the
  conflict-mediation story for how level transitions stabilise.
- **Stuart Kauffman** on autocatalytic sets — formal version of
  the aggregation condition for the chemistry → cells case.
- **Niche-construction theory** (Odling-Smee et al. 2003) —
  formalisation of how level-$k$ entities reshape the substrate
  for level-$k+1$ search.
- **Population genetics of multilevel selection** (Hamilton; Price
  equation; Wilson and Sober 1998) — for the group-variation and
  group-selection conditions specifically.

#### B. Canonical references

- Maynard Smith, J. & Szathmáry, E. (1995). *The Major Transitions
  in Evolution*. Oxford University Press.
- Buss, L. W. (1987). *The Evolution of Individuality*. Princeton
  University Press.
- Okasha, S. (2006). *Evolution and the Levels of Selection*.
  Oxford University Press. (Philosophical synthesis.)
- West, S. A., Fisher, R. M., Gardner, A., & Kiers, E. T. (2015).
  "Major evolutionary transitions in individuality."
  *PNAS* 112(33): 10112–10119.

#### C. Example proofs

- **Buss 1987** — Chapter 4's analysis of multicellularity as
  conflict-mediation between cell-level and organism-level
  selection is the template for the group-selection sub-lemma.
- **Hordijk-Steel-Kauffman RAF theory** — establishes the
  aggregation condition for the chemistry-to-cells transition,
  formally. The closest existing formal proof of one of LE's
  four conditions in a substrate.

#### D. Dependencies

LE's four sub-lemmas (persistence, aggregation, group variation,
group selection) are independently provable for specific
transitions. A proof of LE in full generality requires either a
substrate-agnostic statement of each sub-lemma or a case analysis
across the substrate types $\mathcal{O}_W$-algebras support.

---

### C1: Closure-operator unification of viability

**Statement.** Each of Markov-blanket viability, autopoietic closure,
RAF set viability, and Minimal Criterion Coevolution corresponds to a
closure operator on a partial order of supporting sets.

#### A. Proof techniques to study

- **Closure operators on posets / Moore families.** The central
  abstraction. Re-cast each formalism as "supporting set is a fixed
  point of some c."
- **Galois connections and Formal Concept Analysis (FCA).** When the
  closure factors as f* . f_* for an adjunction between two posets
  (objects/attributes, reactants/reactions, internal-states/blanket-
  states), the closure operator drops out for free. This is the right
  template if you want *one* constructive recipe that produces all four
  operators.
- **Knaster-Tarski fixed-point theorem.** RAF's maxRAF, autopoietic
  process-network closure, and FEP's operational closure all want a
  greatest fixed point of a monotone operator on a complete lattice.
  Knaster-Tarski gives the one-line existence proof; the polynomial-
  time RAF algorithm is Kleene-iteration to that gfp.
- **Cryptomorphism (matroid-style).** Matroid theory cryptomorphically
  proves five axiomatisations (independence / bases / circuits / rank /
  closure) define the same structure. The exact move you want for C1.
- **Tarski consequence operators.** Cn(A) on formulas is the
  prototypical closure operator built from a one-step generating
  relation. Beer's GoL preimage step and Hordijk-Steel's
  "food + reactions" step are the same shape; Tarski's framework gives
  the abstract theorem to instantiate.

#### B. Canonical textbook references

- Davey & Priestley, *Introduction to Lattices and Order* (2nd ed.,
  Cambridge 2002), Chs. 2 and 7.
  <https://www.cambridge.org/core/books/introduction-to-lattices-and-order/946458CB6638AF86D85BA00F5787F4F4>
- Ganter & Wille, *Formal Concept Analysis: Mathematical Foundations*
  (Springer 1999).
  <https://philpapers.org/rec/GANFCA-2>

#### C. Example proofs / prior closure-theoretic readings

- **Dittrich & Speroni di Fenizio (2007),** "Chemical Organisation
  Theory," *Bull. Math. Biol.* 69(4):1199-1231. The most directly
  useful prior art: a chemical organisation is literally a fixed point
  of a closure operator on the species lattice. Subsumes RAF and is
  structurally identical to Beer-style autopoietic closure.
  <https://link.springer.com/article/10.1007/s11538-006-9130-8>
- **Hordijk, Steel & Dittrich (2018),** "Autocatalytic sets and
  chemical organizations," *New J. Phys.* 20:015011. Half of the C1
  RAF clause is already done here.
  <https://iopscience.iop.org/article/10.1088/1367-2630/aa9fcd>
- **Hordijk & Steel (2023),** "A Concise and Formal Definition of RAF
  Sets and the RAF Algorithm," arXiv:2303.01809. Cleanest modern
  statement of RAF detection as iterated closure under a monotone
  operator. <https://arxiv.org/abs/2303.01809>
- **Beer (2015),** "Characterizing Autopoiesis in the Game of Life,"
  *Artificial Life* 21(1):1-19. The autopoietic clause: Beer's
  reaction-set lattice with preimage-closure is essentially a closure
  operator, just needs to be made explicit.
  <https://direct.mit.edu/artl/article/21/1/1/2792/>
- **Friston, Da Costa, Sajid, Heins et al. (2022),** "Sparse coupling
  and Markov blankets," arXiv:2205.10190. Most current statement of
  when sparse coupling yields a Markov blanket — closest existing
  approach to a closure-operator reading of FEP.
  <https://arxiv.org/abs/2205.10190>

#### D. Gap

No published closure-theoretic reading of MCC / minimal-criterion
novelty search exists. The MCC clause is therefore the *novel* part of
the C1 proof; the other three clauses are largely a matter of citing-
and-aligning existing work.

---

### C2: Hierarchical viability composition

**Statement.** Under the entity composition rule (E3), each viability
formalism in C1 lifts so that F*-validity at the composite level
implies F-validity of each component.

**Known partial counterexample.** Union of two RAFs is not in general an
RAF unless joint catalyses are present. So strict union-composition
fails; the conjecture requires a more careful composition rule.

#### A. Proof techniques to study

- **Functoriality of closure operators between posets.** Dikranjan &
  Tholen's *Categorical Closure Operators* (1995/2013) is the formal
  arena in which C1 + C2 should be stated.
- **Operad of wiring diagrams.** Vagner, Spivak & Lerman 2015 — the
  canonical compositional framework for open dynamical systems.
- **Decorated and structured cospans.** Fong 2015/2016 and Baez &
  Courser 2020. Decoration functors are the natural slot for "viability
  witness," and the double-categorical structured-cospan framework
  exposes both "compose at boundary" and "nest into larger system" —
  exactly what hierarchical composition needs.
- **Compositional invariants.** Compositional game theory (Ghani et al.
  2018) shows how a non-trivial validity notion (Nash equilibrium /
  best response) lifts functorially along a SMC composition. The proof
  pattern transplants directly: "viability predicate is a lax morphism
  of operad-algebras."

#### B. Canonical textbook references

- Adámek, Herrlich, Strecker, *Abstract and Concrete Categories: The
  Joy of Cats* (TAC Reprints vol. 17, free PDF).
  <http://www.tac.mta.ca/tac/reprints/articles/17/tr17.pdf>
- Yau, *Operads of Wiring Diagrams* (Springer LNM 2192, 2018) —
  textbook treatment complementing Vagner-Spivak-Lerman, with the
  load-bearing finite-presentation theorems.
  <https://link.springer.com/book/10.1007/978-3-319-95001-3>

#### C. Example proofs of compositional preservation

- **Palacios, Razi, Parr, Kirchhoff, Friston (2020),** "On Markov
  blankets and hierarchical self-organisation," *J. Theor. Biol.*
  486:110089. **The template proof.** Proves Markov-blanket structure
  is closed under nesting: a partition of a system's microstates into
  MBs induces an MB at the macroscale, recursively. Essentially C2 for
  the Markov-blanket formalism.
  <https://www.sciencedirect.com/science/article/pii/S0022519319304588>
- **Hordijk & Steel (2015),** "Autocatalytic sets and boundaries," *J.
  Systems Chemistry* 6:1. Characterises when the union of two RAFs is
  again an RAF, in terms of joint catalyses — the place to extract a
  corrected RAF entity-composition rule.
  <https://link.springer.com/article/10.1186/s13322-014-0006-2>
- **Vagner, Spivak & Lerman (2015),** "Algebras of Open Dynamical
  Systems on the Operad of Wiring Diagrams," *TAC* 30. The blueprint
  for any operadic composition theorem in this space.
  <https://arxiv.org/abs/1408.1598>
- **Baez & Courser (2020),** "Structured Cospans," *TAC* 35:1771-1822.
  Successor framework to Fong 2015; better suited for hierarchical
  (nested) composition.
  <https://arxiv.org/abs/1911.04630>
- **Beer (2020),** "An Investigation into the Origin of Autopoiesis,"
  *Artificial Life* 26(1):5-22, and companion "Bittorio Revisited."
  No categorical theorem, but handles structural coupling between an
  autopoietic individual and its environment — the simplest non-
  trivial composite. Useful as the autopoietic-closure test case.
- **Ghani, Hedges, Winschel, Zahn (2018),** "Compositional Game
  Theory," LICS / arXiv:1603.04641. Worked example of a validity
  predicate lifting compositionally; proof pattern transplants
  directly. <https://arxiv.org/abs/1603.04641>

**Suggested reading order:** Palacios et al. 2020 (concrete MB
template) -> Hordijk-Steel RAF papers (concrete obstructions + lattice
fix) -> Dikranjan-Tholen / Joy of Cats (formal closure-operator
category) -> Vagner-Spivak-Lerman / Baez-Courser (operad / cospan
composition machinery) -> Ghani-Hedges (analogue proof in a different
domain to imitate stylistically).

---

### C3: Observer-relative novelty as divergence-functional

**Statement.** All three observer families (density-distance,
FM-embedding, information-theoretic) are instances of a single
schema O[mu] = D(mu || mu_ref) for a context-dependent reference.

#### A. Proof techniques to study

- **f-divergences and IPMs.** Sriperumbudur et al. (2012)'s structural
  result on when an IPM coincides with an f-divergence — the lemma
  needed to argue Wasserstein-novelty and KL-novelty are siblings in
  a larger family but not identical.
- **Unification of binary-experiment quantities.** Reid & Williamson
  (2011) unify f-divergences, Bregman divergences, surrogate regret,
  proper scoring rules, and ROC curves via integral / variational
  representations — a working template for C3.
- **Variational representations.** Donsker-Varadhan, Fenchel duality,
  f-GAN (Nowozin et al. 2016), MINE (Belghazi et al. 2018). The
  bridge from "neural-net-scored novelty" (FM-embedding observers) to
  KL divergence in a learned feature space.
- **Transfer entropy as KL.** Schreiber (2000) — the category-3
  reduction (information-theoretic observer = KL) in one paragraph.
- **Effective information as KL.** Hoel-Albantakis-Tononi (2013):
  EI = uniform-intervention-averaged KL.

#### B. Canonical textbook references

- Polyanskiy & Wu, *Information Theory: From Coding to Learning*
  (Cambridge 2025; free draft).
  <http://www.stat.yale.edu/~yw562/ln.html>
- Nielsen, "An Elementary Introduction to Information Geometry,"
  Entropy 22(10):1100 (2020). Self-contained primer on Bregman / dually
  flat geometry. <https://www.mdpi.com/1099-4300/22/10/1100>
- Peyré & Cuturi, *Computational Optimal Transport* (Found. & Trends
  in ML 11(5-6), 2019). <https://arxiv.org/abs/1803.00567>

#### C. Example proofs that several scoring functionals reduce to one divergence

- **Sriperumbudur et al. (2012),** "On integral probability metrics,
  φ-divergences and binary classification," arXiv:0901.2698.
- **Reid & Williamson (2011),** "Information, Divergence and Risk for
  Binary Experiments," JMLR 12:731-817. arXiv:0901.0356.
- **Nowozin, Cseke, Tomioka (2016),** "f-GAN," NeurIPS / arXiv:1606.00709.
- **Belghazi et al. (2018),** "MINE: Mutual Information Neural
  Estimation," arXiv:1801.04062.
- **Schreiber (2000),** "Measuring Information Transfer," PRL 85:461 /
  arXiv:nlin/0001042.
- **Comolatti & Hoel (2022),** "Causal emergence is widespread across
  measures of causation," arXiv:2202.01854. Direct precedent for the
  kind of unification C3 claims.
- **Buckley, Kim, McGregor, Seth (2017),** "The free energy principle
  for action and perception: a mathematical review," arXiv:1705.09156.
  Walks through every FEP quantity as a KL.
- **Gretton et al. (2012),** "A Kernel Two-Sample Test," JMLR 13:723-
  773. MMD as an IPM with closed-form RKHS embedding — the natural
  model for "FM-embedding distance as an IPM in a learned feature
  space."
- **Lehman & Stanley (2011),** "Abandoning Objectives: Evolution
  Through the Search for Novelty Alone," *Evol. Comp.* 19(2):189-223.
  The reference behavioural-novelty / archive-distance functional —
  anchor for category 1.
- **Kumar et al. (2024),** "Automating the Search for Artificial Life
  with Foundation Models" (ASAL), arXiv:2412.17799. Category-2
  reference.
- **Faldor et al. (2024),** "OMNI-EPIC," arXiv:2405.15568. Companion
  category-2 reference; stress-tests whether C3's schema covers
  "interestingness" as an FM-evaluated functional.

Bonus: **Agrawal & Horel (2020),** "Optimal Bounds between
f-Divergences and Integral Probability Metrics," PMLR 119. Two-way
bounds — useful if C3 ends up restated as "equivalent up to monotone
reparametrisation" rather than literal equality.

---

### OP1: Causal emergence of scaffolded systems

**Statement.** Find substrate-viability pairs (X, F) for which one can
prove sup_Pi CE(M(S), Pi) > 0 for the scaffolded system S, where CE is
Hoel-style causal emergence.

#### A. Proof techniques to study

- **EI as channel capacity.** Hoel 2017 recasts EI as channel
  capacity; this framing is the cleanest target for variational / sup
  arguments over partitions Pi.
- **Determinism-degeneracy decomposition.** EI = determinism -
  degeneracy is the practical handle for explicit proofs (Hoel-
  Albantakis-Tononi 2013).
- **Causal-primitive robustness.** Comolatti-Hoel 2022 shows CE > 0
  is robust across ~a dozen causal measures, meaning a proof can pick
  the easiest primitive to bound.
- **Markov chain lumpability.** Kemeny-Snell strong/weak lumpability
  (`U V P V = P V`) gives a constructive coarse-graining whose
  macro-chain is exactly Markov — the easiest place to compute
  EI(M_Pi).
- **Phi-ID atoms.** Mediano et al. 2021/2025 Phi-ID decomposes mutual
  information into synergy / redundancy atoms; the synergy atom is
  what is "really" emergent. **A Phi-ID-based proof avoids the
  partition-supremum entirely.**

#### B. Canonical textbook references

- Cover & Thomas, *Elements of Information Theory* (2nd ed., Wiley
  2006). MI / channel-capacity machinery.
- Pearl, *Causality: Models, Reasoning, and Inference* (2nd ed.,
  Cambridge 2009). do-calculus and the intervention distribution H_max.
- Kemeny & Snell, *Finite Markov Chains* (Springer 1976), Ch. 6.

#### C. Example proofs / worked cases / critiques

- **Hoel-Albantakis-Tononi (2013),** "Quantifying causal emergence
  shows that macro can beat micro," PNAS 110(49):19790-19795. Original
  EI paper with first worked examples (4-node Markov chain) proving
  CE > 0. <https://www.pnas.org/doi/10.1073/pnas.1314922110>
- **Hoel (2017),** "When the Map Is Better Than the Territory,"
  Entropy 19(5):188. EI as channel capacity. arXiv:1612.09592.
- **Klein & Hoel (2020),** "The emergence of informative higher scales
  in complex networks," *Complexity* 2020:8932526. Proves CE > 0 on
  preferential-attachment, ER, and modular random graphs by
  constructing macronode partitions via spectral clustering — a
  constructive existence-proof template. arXiv:1907.03902.
- **Griebenow, Klein & Hoel (2019),** "Finding the right scale of a
  network through spectral clustering," arXiv:1908.07565. Refines
  Klein-Hoel with an explicit polynomial-time algorithm — exactly the
  "lift via existing lumpable partition" pattern.
- **Hoel & Levin (2020),** "Emergence of informative higher scales in
  biological systems," *Comm. Integr. Biol.* 13(1):108-118. CE > 0 for
  gene-regulatory and protein-interaction networks; the published
  analogue closest to a viability-filtered Markov chain.
- **Comolatti & Hoel (2022),** "Causal emergence is widespread across
  measures of causation," arXiv:2202.01854.
- **Hoel (2025),** "Causal Emergence 2.0," arXiv:2503.13395. New
  axiomatic formulation; may simplify the proof obligation by
  replacing sup_Pi with a scale-apportionment.
- **Pfante, Bertschinger, Olbrich, Ay & Jost (2014),** "Comparison
  between different methods of level identification," *Advances in
  Complex Systems* 17(2):1450007. Surveys lumpability, observational
  commutativity, and information-closure for projected Markov chains.
- **Mediano et al. (2021/2025),** "Towards an extended taxonomy of
  information dynamics via Phi-ID," PNAS 2025 / arXiv:2109.13186.
- **Williams & Beer (2010),** "Nonnegative Decomposition of
  Multivariate Information," arXiv:1004.2515. PID foundation.
- **Israeli & Goldenfeld (2006),** "Coarse-graining of cellular
  automata," *Phys. Rev. E* 73:026203. Local coarse-grainings for ECAs
  including Class III/IV. arXiv:nlin/0508033.
- **Dewhurst (2021),** "Causal emergence from effective information:
  Neither causal nor emergent?," *Thought* 10(3):158-168.
  Philosophical critique — read defensively so the proof states clearly
  what it does and does not establish.
- **Eberhardt & Lee (2022),** "Causal Emergence: When Distortions in a
  Map Obscure the Territory," *Philosophies* 7(2):30. Technical
  critique pointing out EI's sensitivity to state-space cardinality.

#### D. Lowest-hanging fruit

The cleanest candidate is **Game of Life under a Markov-blanket
viability filter on bounded-support configurations**:

- Micro dynamics is deterministic and finite, so EI = log(|reachable
  states|) - degeneracy is finite-arithmetic.
- Israeli-Goldenfeld already exhibit a deterministic block-coarse-
  graining for several ECAs and sketch one for GoL ("blinkers" /
  oscillator equivalence classes); promoting this from "exhibited" to
  "CE > 0" requires only bounding preimage multiplicity — a
  combinatorial argument.
- An MB-viability filter on still-life + period-2 configurations gives
  a finite, strongly connected, lumpable induced chain; strong
  lumpability immediately yields a well-defined macro EI, then compare
  to micro EI by counting.
- The Klein-Hoel network result and the Griebenow et al. spectral
  algorithm are proofs of concept that constructive partition
  exhibition can be promoted to existence proofs.

Flow-Lenia and POET candidates are higher-risk — continuous state
spaces and the substrate isn't obviously Markov without discretisation.
Save them for after a GoL / Diff-Logic-CA proof lands. The Phi-ID
route is an alternative pathway worth a parallel attempt — it sidesteps
sup_Pi entirely by working with a fixed synergy atom.

---

### OP2: FEP-as-lens scope

**Statement.** Characterise precisely the substrate-dynamics pairs
(X, Phi) for which the Free Energy Principle is informative as a
parameterisation of viability and observer slots.

#### A. Proof techniques to study

- **Langevin SDEs at NESS with Helmholtz decomposition.** Friston
  2019 — the construction whose scope OP2 bounds: decompose stationary
  flow into solenoidal (Q) + dissipative (Gamma) components, partition
  state into a "particular" (eta, s, a, mu) Markov-blanket structure.
- **Approximate / weak Markov blankets.** Sakthivadivel 2022 — uses
  large-N adiabatic asymptotics to prove weak Markov blankets are
  generic in high dimensions even when strict ones are not.
- **Bayesian mechanics on the synchronisation manifold.** Da Costa,
  Friston, Heins, Pavliotis 2021 — information-geometric formalisation
  where the internal-state manifold encodes posterior beliefs about
  external states. The formal apparatus for "FEP is informative."
- **Critique-driven scope characterisation.** Aguilera et al. 2022 —
  show codimension of FEP-admitting parameter slice in linear weakly-
  coupled SDEs.

#### B. Canonical textbook and review references

- Pavliotis, *Stochastic Processes and Applications* (Springer TAM 60,
  2014). Reference textbook for the SDE / Fokker-Planck / NESS
  machinery (Pavliotis is now a Friston co-author).
- Parr, Pezzulo & Friston, *Active Inference: The Free Energy Principle
  in Mind, Brain, and Behavior* (MIT Press 2022, open access).
- Buckley, Kim, McGregor & Seth (2017), "The free energy principle for
  action and perception: a mathematical review," J. Math. Psych. /
  arXiv:1705.09156. The clearest pre-particular-physics tutorial.
- Friston, Da Costa, Sajid, Heins, Ueltzhöffer, Pavliotis, Parr (2023),
  "The free energy principle made simpler but not too simple," Physics
  Reports / arXiv:2201.06387. Wellcome group's cleanest current
  statement.

#### C. Example proofs / scope-characterisation papers

- **Aguilera, Millidge, Tschantz, Buckley (2022),** "How particular is
  the physics of the free energy principle?" *Physics of Life Reviews*
  40:24-50 / arXiv:2105.11203. **The model for an OP2 proof.** In
  weakly-coupled linear stochastic systems, Markov-blanket + solenoidal-
  flow restrictions hold only on a measure-zero parameter slice.
- **Biehl, Pollock & Kanai (2021),** "A technical critique of some
  parts of the FEP," *Entropy* 23(3):293 / arXiv:2001.06408. Three
  concrete technical failures: inequivalent MB definitions, unstated
  EoM-rewriting assumptions, an incorrect free-energy lemma.
- **Heins & Da Costa (2022),** "Sparse coupling and Markov blankets,"
  arXiv:2205.10190. Wellcome-side reply: explicit conditions on
  Gaussian-NESS systems under which sparse coupling does/doesn't imply
  Markov-blanket structure. Most direct "iff"-style scope result
  currently in the literature.
- **Sakthivadivel (2022),** "Weak Markov blankets in high-dimensional,
  sparsely-coupled random dynamical systems," arXiv:2207.07620.
- **Da Costa, Friston, Heins, Pavliotis (2021),** "Bayesian mechanics
  for stationary processes," arXiv:2106.13830.
- **Bruineberg, Dołęga, Dewhurst, Baltieri (2022),** "The Emperor's
  New Markov Blankets," BBS 45. Distinguishes instrumental from
  ontological readings of FEP — directly relevant to deciding what
  "informative" means in OP2.
- **Kirchhoff, Parr, Palacios, Friston, Kiverstein (2018),** "The
  Markov blankets of life," *J. R. Soc. Interface* 15:20170792. The
  strong-claim target.
- **Andrews (2021),** "The math is not the territory: navigating the
  free energy principle," *Biology & Philosophy* 36:30.

#### D. Applicable proof pattern

Following Aguilera et al. 2022:

1. **Restrict to a tractable class** — weakly-coupled linear / Gaussian-
   NESS SDEs `dx = (Q - Gamma) grad log p(x) dt + sigma dW`, where Q
   (solenoidal) and Gamma (dissipative) carry the FEP content.
2. **Translate FEP requirements into matrix conditions** — "MB exists"
   becomes a block-zero condition on the NESS precision Pi; "non-trivial
   variational bound" becomes a condition that the synchronisation map
   mu -> E[eta | b] is non-constant.
3. **Compute the codimension** — show the simultaneous block-zero +
   solenoidal constraints cut out a low-dimensional / measure-zero
   submanifold (Aguilera) OR that a relaxation (weak blanket, large-N
   adiabatic limit) recovers a positive-measure regime (Sakthivadivel;
   Heins-Da Costa).
4. **State the iff.** Candidate target: "(X, Phi) admits an informative
   FEP parameterisation iff (i) sparse-causal-coupling-admits-MB regime
   (Heins/Da Costa conditions on NESS precision), (ii) non-degenerate
   synchronisation manifold (Da Costa Bayesian-mechanics non-triviality),
   (iii) tractability / identifiability of the generative model implicit
   in p(b, mu)."

Generic non-linear out-of-equilibrium systems fail (i); high-D sparse
systems satisfy a weakened (i).

---

### OP3: Interaction-topology expressiveness (operadic universality)

**Statement.** Is the multiplex-with-diamond_rho formalism universal —
every "natural" multi-coupling-regime ALife system expressible as a
multiplex with countably many layers? A categorical formulation would
express this in terms of the operad of wiring diagrams.

#### A. Proof techniques to study

- **Operad of wiring diagrams.** Vagner, Spivak & Lerman 2015 — the
  canonical reference, with W-algebras for general and linear ODEs.
- **Continuous-time / network composition.** Lerman & Spivak 2016.
- **Sheaf semantics for time-indexed systems.** Schultz & Spivak 2019
  — machinery for measurable t-indexing of T_t.
- **Decorated and structured cospans.** Fong 2015; Baez & Courser
  2020. Decorations are the natural slot for layer-weights / coupling
  rules rho; structured cospans handle non-symmetric rho.
- **Finite-presentation of operads.** Yau 2018 — proves O(W) has 8
  generators and 28 relations; the undirected variant has 6 and 17.
  This is the actual proof template "every element factors through
  generators."

#### B. Canonical textbook references

- Yau, *Operads of Wiring Diagrams* (Springer LNM 2192, 2018).
- Markl, Shnider & Stasheff, *Operads in Algebra, Topology and Physics*
  (AMS, 2002). Symmetric / coloured operads, free operads, algebras,
  freeness theorems.
- Leinster, *Higher Operads, Higher Categories* (CUP, 2004). Needed
  if the layer index ell is treated as a colour. arXiv:math/0305049.
- Fong & Spivak, *Seven Sketches in Compositionality* (CUP, 2019).
  Ch. 6 (props) and Ch. 7 (toposes / dynamical systems).
  arXiv:1803.05316.

#### C. Example universality / completeness proofs

- **Vagner, Spivak & Lerman (2015),** "Algebras of Open Dynamical
  Systems on the Operad of Wiring Diagrams," *TAC* 30:1793-1822 /
  arXiv:1408.1598. The blueprint.
- **Baez & Pollard (2017),** "A Compositional Framework for Reaction
  Networks," *Rev. Math. Phys.* 29(9) / arXiv:1704.02051. Functorial
  universality: every open reaction network maps via a black-box
  functor to an open dynamical system. Direct template for "every
  multi-coupling-regime ALife system factors through the multiplex
  operad."
- **Fong (2016),** "The Algebra of Open and Interconnected Systems"
  (Oxford PhD thesis). Worked universal-property proofs for circuits,
  signal-flow graphs, Markov processes via decorated cospans.
  <https://math.ucr.edu/home/baez/thesis_fong.pdf>
- **Baez & Courser (2020),** "Structured Cospans," arXiv:1911.04630.
- **Ghani, Hedges, Winschel, Zahn (2018),** "Compositional Game
  Theory," LICS / arXiv:1603.04641. Open games as morphisms in an SMC
  with lenses for state-passing — same shape as rho-coupling between
  layers.
- **Hedges (2017),** "Coherence for lenses and open games,"
  arXiv:1704.02230. Coherence = universality-flavoured result that
  every composition of opens is equivalent to a canonical normal form.
- **Boccaletti et al. (2014),** "The Structure and Dynamics of
  Multilayer Networks," *Physics Reports* 544:1-122 / arXiv:1407.0742.
  Sets the multiplex vocabulary that OP3 must subsume.

**Gap.** I did not find an existing operadic universality theorem for
the Boccaletti-style multiplex framework itself — this appears to be
the gap OP3 fills.

#### D. Applicable proof pattern

A two-stage Vagner-Spivak-Lerman / Yau-style proof:

**Stage 1 — Define the operad explicitly.** A coloured symmetric operad
`W_multi` whose colours are pairs `(X, M+(X))` (substrate state space
paired with population space, one colour per layer-type); operations of
arity `(c_1, ..., c_n) -> c_0` are weighted hyperedge wiring diagrams
with a layer label ell and a coupling rule rho; composition is
concatenation of wiring diagrams modulo associativity of rho, identity
edges, and layer permutation.

The candidate W-algebra `A: W_multi -> Set` sends each colour to the
set of variation kernels `V: X x Theta -> P(X)` and each operation to
the V_T construction implemented in `system.py`'s
`build_population_variation_multiplex`.

**Stage 2 — Factor any "natural" multi-coupling-regime system through
W_multi's generators.** Candidate generators:

- identity wiring (trivial topology)
- single hyperedge of fixed arity k in a single layer with weight w
- layer-mixture operation `sum alpha_ell`
- rho-fusion operation

Stage-2 lemma: every measurable family `T_t` of weighted hypergraphs
admits a (possibly countable) decomposition into these generators, and
V_T agrees with the induced A-action.

**Candidate counterexamples / scope conditions to fix up front.**

- *Uncountable layer index.* O(W) is finitary, so only countable
  layer multiplexes are in the image — state the conjecture for
  countably-many layers explicitly.
- *Non-measurable coupling rules.* rho must be measurable in state for
  V_T to land in P(X); a measurability hypothesis on rho is the
  analogue of Vagner-Spivak-Lerman §3's smoothness hypothesis.
- *Non-symmetric rho.* If rho is non-commutative (master-slave
  coupling), the operad must be non-symmetric (a plain multicategory,
  Leinster Ch. 2).
- *Higher-order coupling* (coupling depending on coupling state). May
  require nesting `W_multi`-algebras inside themselves — Schultz-
  Spivak sheaf semantics handles this; plain operads don't.
- *Stateful topology* (T_t depends on past behaviour). Factor through
  Schultz-Spivak's sheaf-of-streams construction before applying the
  wiring-diagram operad.

**Target statement.** "The `W_multi`-algebra of population variation
kernels is the free A-algebra on the single-layer kernel V^(ell);
equivalently, every measurable countable-layer multi-coupling-regime
variation V_T is uniquely the image under A of a wiring diagram in
O(W_multi)." Yau's finite-presentation theorem then reduces verifying
universality to checking ~6-8 generators and ~17-28 relations on V_T.

**Repo files this proof would touch:**
[`system.py`](../src/emergent_systems/system.py)
(`build_population_variation_multiplex` is the operation A sends
wiring-operations to), [`topology.py`](../src/emergent_systems/topology.py)
(the `InteractionTopology` Protocol is the object-level data the
operad's colours and operations must cover),
[`variation.py`](../src/emergent_systems/variation.py)
(the codomain Protocol the W-algebra A targets).

---

## Cross-item dependencies

- **C2 depends on C1.** C2 is "closure operators compose under E3," so
  C1's identification of each viability formalism with a closure
  operator must land first. (Or both can be done together if the
  proofs are short.)
- **OP1 is independent of C1-C3.** Causal emergence rests on EI, not
  on the viability / observer machinery. But a successful OP1 result
  on a specific (X, F) gives a concrete worked example for C2-C3.
- **OP3 shares machinery with C2.** Both use the operad of wiring
  diagrams / structured cospans. Studying Vagner-Spivak-Lerman, Fong,
  and Baez-Courser pays off for both.
- **C3 shares machinery with OP1.** Both involve KL / f-divergence
  reductions of putatively different functionals. Comolatti-Hoel 2022
  is a load-bearing citation for both.

A reasonable order of attack:

1. C1 — most mature literature, clear gap (MCC), proof template
   already in Dittrich-Speroni-Fenizio + Hordijk-Steel.
2. C3 — directly within established literature; the unification is
   plausibly just a Reid-Williamson-style theorem stitched together
   with Comolatti-Hoel.
3. OP1 on Game of Life + MB-viability — the lowest-hanging concrete
   existence proof. Promotes Israeli-Goldenfeld's exhibited coarse-
   graining to a published CE > 0 statement.
4. C2 (assuming C1) — builds on the operadic / cospan machinery; the
   Palacios et al. proof is the imitation template.
5. OP3 — needs the full Vagner-Spivak-Lerman / Yau machinery; share
   the prep with C2.
6. OP2 — the hardest because it requires committing to what
   "informative" means; following Aguilera et al. is the most
   principled route but the proof itself is technically heavy.

## Updating this document

When a result paper lands, link it from the relevant per-item section
and update [`RESULTS.md`](../RESULTS.md) per its instructions. When the
literature in any pillar changes substantially, edit the cross-cutting
section in Part 1 rather than duplicating across items.
