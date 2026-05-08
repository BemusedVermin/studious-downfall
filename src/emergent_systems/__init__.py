"""Public API surface for `emergent_systems`.

Module organisation maps onto the paper's five slots plus orchestration. The naming
convention is plain English with each identifier carrying a `# paper: <symbol>` sibling
comment so code and the paper can be navigated without translation.

The library does not ship concrete substrates. Implementers supply slots conforming to the
protocols below; the harness composes, validates, and runs them.
"""

from __future__ import annotations

from emergent_systems._types import PRNGKey, TickIndex
from emergent_systems.distribution import Categorical, Distribution, Gaussian, PointMass
from emergent_systems.emergence import (
    causal_emergence,
    coarse_grain_transition_matrix,
    effective_information,
    find_emergent_partition_bruteforce,
    find_emergent_partition_heuristic,
)
from emergent_systems.entity import (
    Entity,
    EntityDetector,
    compose_entities,
    verify_boundedness,
    verify_persistence_estimate,
)
from emergent_systems.observer import JointState, StatefulObserver, WindowedTrajectory
from emergent_systems.perf import PERF_FLAG, PerformanceWarning, flag_bottleneck
from emergent_systems.population import ImplicitInSubstrate, Population, WeightedSamples
from emergent_systems.spec import (
    ComplexityReport,
    ConformanceReport,
    DescriptorReport,
    EntityReport,
    ObserverReport,
    RNGReport,
    SubstrateReport,
    SystemSpec,
    TopologyReport,
    VariationReport,
    ViabilityReport,
)
from emergent_systems.substrate import (
    Coupling,
    Substrate,
    compose_substrates_coupled,
    compose_substrates_independently,
)
from emergent_systems.system import (
    RunResult,
    SlotName,
    System,
    build_population_variation,
    build_population_variation_multiplex,
    run,
    step,
)
from emergent_systems.topology import (
    Hyperedge,
    Hypergraph,
    InteractionTopology,
    MultiplexLayer,
    MultiplexTopology,
)
from emergent_systems.variation import (
    ChannelCoupling,
    IndependentChannelCoupling,
    Variation,
    compose_variation_channels,
)
from emergent_systems.viability import (
    AutopoieticClosureViability,
    MarkovBlanketViability,
    MinimalCriterionViability,
    RAFSetViability,
    ViabilityFilter,
    verify_is_closure_operator,
)

__all__ = [
    # Slots — protocols and concrete types.
    "Substrate",
    "Variation",
    "ViabilityFilter",
    "InteractionTopology",
    "StatefulObserver",
    # Distribution / Population — paper: P(X), M+(X).
    "Distribution",
    "PointMass",
    "Gaussian",
    "Categorical",
    "Population",
    "WeightedSamples",
    "ImplicitInSubstrate",
    # Substrate composition — paper: ⊠, ⊠_κ.
    "Coupling",
    "compose_substrates_independently",
    "compose_substrates_coupled",
    # Variation channel composition — paper: ⋄_ρ.
    "ChannelCoupling",
    "IndependentChannelCoupling",
    "compose_variation_channels",
    # Topology — paper: T_t, multiplex.
    "Hyperedge",
    "Hypergraph",
    "MultiplexLayer",
    "MultiplexTopology",
    # Entity — paper: e = (S, π).
    "Entity",
    "EntityDetector",
    "compose_entities",
    "verify_boundedness",
    "verify_persistence_estimate",
    # Viability — paper: F : M+(X) → M+(X) and the four formalisms.
    "MarkovBlanketViability",
    "AutopoieticClosureViability",
    "RAFSetViability",
    "MinimalCriterionViability",
    "verify_is_closure_operator",
    # Observer — paper: O_s.
    "JointState",
    "WindowedTrajectory",
    # Emergence — paper: EI, CE.
    "effective_information",
    "causal_emergence",
    "coarse_grain_transition_matrix",
    "find_emergent_partition_bruteforce",
    "find_emergent_partition_heuristic",
    # Orchestration.
    "System",
    "SlotName",
    "RunResult",
    "step",
    "run",
    "build_population_variation",
    "build_population_variation_multiplex",
    # Conformance — paper §4.
    "SystemSpec",
    "ConformanceReport",
    "SubstrateReport",
    "EntityReport",
    "VariationReport",
    "ViabilityReport",
    "TopologyReport",
    "ObserverReport",
    "DescriptorReport",
    "RNGReport",
    "ComplexityReport",
    # Performance flagging.
    "PERF_FLAG",
    "PerformanceWarning",
    "flag_bottleneck",
    # Type aliases.
    "PRNGKey",
    "TickIndex",
]
