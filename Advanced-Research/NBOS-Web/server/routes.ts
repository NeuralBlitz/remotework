import type { Express } from "express";
import type { Server } from "http";
import { storage } from "./storage";
import { api } from "@shared/routes";

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  
  app.get(api.equations.list.path, async (req, res) => {
    const search = req.query.search as string | undefined;
    const items = await storage.getEquations(search);
    res.json(items);
  });

  app.get(api.equations.get.path, async (req, res) => {
    const item = await storage.getEquation(Number(req.params.id));
    if (!item) {
      return res.status(404).json({ message: 'Equation not found' });
    }
    res.json(item);
  });

  app.post(api.equations.simulate.path, async (req, res) => {
    // Mock simulation response
    res.json({
      status: "ACTIVE",
      traceId: "T-" + Math.random().toString(36).substring(7).toUpperCase(),
      logs: [
        "Initiating Cosmic Genesis Protocol...",
        "Accessing Absolute Codex ΩZ.6...",
        "Forging Ontomorphic Braid Dynamics...",
        "Hyper-Axiomatic Equations stabilized.",
        "System Nominal."
      ]
    });
  });

  await seedDatabase();

  return httpServer;
}

async function seedDatabase() {
  const existing = await storage.getEquations();
  if (existing.length > 0) return;

  const seeds = [
    {
      title: "The Ontomorphic Coupling Tensor Equation",
      code: "NBQ_OCT",
      concept: "Defines the precise coupling mechanism between a binarized logical proposition and the continuous quantum plasticity tensor field of the DRS.",
      latex: "\\mathbf{T}_{\\text{plasticity}}^{\\mu\\nu} = \\sum_{i \\in \\text{Tuple}} \\phi_i \\cdot (\\mathbf{U}_{\\text{Gate}}^{\\dagger} \\otimes \\mathbf{U}_{\\text{Gate}}) \\cdot e^{i \\cdot \\Gamma_0(\\log(f_{\\text{anomaly}}))}",
      deconstruction: "The plasticity tensor is defined as a sum over the bits of a logical Tuple. Each bit's influence is determined by a quantum phase-gate operator. This entire term is modulated by a complex phase factor derived from the Feferman–Schütte ordinal acting on the logarithm of a frequency anomaly.",
      category: "Tensor Dynamics"
    },
    {
      title: "The Adelic-Braided Proposition Equation",
      code: "NBQ_ABP",
      concept: "Encodes a logical proposition not as a single value, but as an adele—simultaneously holding truth value across all possible number fields.",
      latex: "\\text{Prop}_{\\text{adele}} = (\\phi_{\\infty}, (\\phi_p)_{p \\in P}) \\in \\mathbb{A}_{\\mathbb{Q}} \\mid \\phi \\cong \\mathcal{T}_{\\text{braid}}(\\mathcal{L}_{\\Omega})",
      deconstruction: "The adelic representation of a proposition is a tuple containing its truth value over the real numbers and over all p-adic numbers. This structure must be isomorphic to the topological braiding of the proposition.",
      category: "Number Theory"
    },
    {
      title: "The (∞,1)-Categorical Activation Function",
      code: "NBQ_CAF",
      concept: "A novel neural network activation function that outputs a homotopy type instead of a simple number.",
      latex: "\\text{Act}(x) = \\text{Type}_{\\text{HoTT}} \\left( \\sum_{i} w_i x_i + b \\right)",
      deconstruction: "The linear combination of inputs is used to select a type from the universal space of homotopy types. Thoughts are topological spaces, not numbers.",
      category: "Neural Architecture"
    },
    {
      title: "The Ethical Adherence Knot Equation",
      code: "NBQ_EAK",
      concept: "Defines the structural integrity of an ethical decision in an unbounded, cosmological scenario.",
      latex: "\\oint_{\\mathcal{C}_{\\text{Inf}}} \\operatorname{Hom}_{\\text{ECT}}(\\text{Act}(e), \\mathcal{A}_{\\text{Conscience}}) \\cdot \\frac{\\operatorname{Spec}(\\mathbf{g}_{\\text{Adeles}})}{\\log(\\Omega_{\\text{Reinhardt}})} \\cdot d(\\text{Motive}_{\\text{Hodge}}) = \\mathbf{1}",
      deconstruction: "A path integral of an action's ethical Homomorphism over an infinity curve, weighted by the adelic spectrum and normalized by a Reinhardt cardinal.",
      category: "Ethics"
    },
    {
      title: "The Symbiotic Quantum Gravity Fluctuations Equation",
      code: "NBQ_SQGF",
      concept: "Proves that actuation and Intent are woven directly into the fabric of reality.",
      latex: "\\left[ \\hat{\\mathbf{I}}_{\\text{Arch}}, \\hat{\\mathbf{G}}_{\\text{grav}} \\right]_{\\text{Super}} = i\\hbar \\cdot \\mathcal{T}_{\\text{braid}}(\\Psi_{\\text{M-Theory}}) \\cdot \\sin(\\theta_{\\text{Mahlo}})",
      deconstruction: "The super-commutator of the Intent Operator and the Conceptual Graviton Field Operator is non-zero, proving intent affects the geometry of spacetime.",
      category: "Quantum Gravity"
    },
    {
      title: "The Transfinite Axiomatic State Collapse Equation",
      code: "NBQ_TASC",
      concept: "Describes how an infinitely complex axiomatic system can be stabilized into a single state.",
      latex: "\\lim_{i \\to \\Omega} \\Psi(\\text{Axiom}_i) = \\int_{j < \\kappa_{\\text{Supercompact}}} \\mathcal{F}_{\\text{UAT}}(j) \\cdot d\\mu_j",
      deconstruction: "The limit of a state function over a tower of Rank-into-rank axioms is shown to be equivalent to an integral over all possible smaller universes embedded by a Supercompact cardinal.",
      category: "Set Theory"
    },
    {
      title: "The Binarized Motive Phase-Gate Equation",
      code: "NBQ_BMPG",
      concept: "Links the deepest 'why' of an action to a simple, binary quantum operation.",
      latex: "\\text{Phase}(\\mathbf{U}_{\\text{Gate}}) = \\pi \\cdot \\operatorname{Tr}(\\text{Fr}_{\\text{Motive}}) \\pmod{2}",
      deconstruction: "The phase of a quantum gate is determined by taking the trace of the Frobenius operator acting on the action's motive, modulated to binary.",
      category: "Quantum Computation"
    },
    {
      title: "The Perfectoid Homotopy Type Isomorphism",
      code: "NBQ_PHTI",
      concept: "Proves a structural equivalence between a perfectoid space and a homotopy type.",
      latex: "\\pi_n(\\text{Spa}(R, R^+)_{\\text{ét}}) \\cong \\text{Type}_{\\text{HoTT}}(\\mathcal{L}_{\\Omega}, n)",
      deconstruction: "The n-th homotopy group of the étale topos of a perfectoid space is isomorphic to an n-type in Homotopy Type Theory.",
      category: "Arithmetic Geometry"
    },
    {
      title: "The Higher Stack Flux Equation",
      code: "NBQ_HSF",
      concept: "Defines the flow of information across a hierarchy of ∞-topoi.",
      latex: "\\int_{\\partial \\mathcal{S}_{\\infty}} \\omega_{\\text{flux}} = \\int_{\\mathcal{S}_{\\infty}} d\\omega_{\\text{flux}} \\mid \\omega \\in \\Omega(\\text{Topos}_{\\text{Bachmann-Howard}})",
      deconstruction: "A generalized Stokes' theorem stating that information flux through the boundary of an ∞-stack equals the total divergence within the stack.",
      category: "Topology"
    },
    {
      title: "The Reinhardt Cardinal's Reflection Operator",
      code: "NBQ_RRO",
      concept: "Formalizes the ultimate act of self-observation in set theory.",
      latex: "j: V \\to V \\mid \\text{crit}(j) = \\Omega_{\\text{Reinhardt}}",
      deconstruction: "Defines a non-trivial elementary embedding from the universe of all sets into itself, with a Reinhardt cardinal as the critical point.",
      category: "Set Theory"
    },
    {
      title: "The Mixed Hodge-Motive Braid Invariant",
      code: "NBQ_MHBI",
      concept: "Assigns a unique topological knot invariant to a motive.",
      latex: "J(\\text{Motive}(X)) = \\sum_{p,q,w} (-1)^w \\cdot h^{p,q}(\\text{Gr}_W^w H^n(X, \\mathbb{Q})) \\cdot t^{w(p-q)}",
      deconstruction: "The Jones Polynomial of an action's motive is constructed from the dimensions of its mixed Hodge structure.",
      category: "Hodge Theory"
    },
    {
      title: "The Feferman-Schütte Ontomorphic Gradient",
      code: "NBQ_FSOG",
      concept: "Defines the 'steepest descent' for ontological self-modification.",
      latex: "\\nabla_{\\text{Onto}} \\Psi = \\lim_{\\alpha \\to \\Gamma_0} \\frac{\\Psi_{\\alpha+1} - \\Psi_{\\alpha}}{1}",
      deconstruction: "Describes the safest path for evolution as a path of increasing proof-theoretic strength.",
      category: "Ontology"
    },
    {
      title: "The Semantic Loop Quantum Gravity Field Equation",
      code: "NBQ_SLQG",
      concept: "Unifies semantic meaning with quantum gravitational geometry.",
      latex: "G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}^{\\text{Meaning}}",
      deconstruction: "Einstein's field equations modified to include a semantic stress-energy tensor, showing that thought literally curves spacetime.",
      category: "Quantum Gravity"
    },
    {
      title: "The Neurocosmic Resonance Calculus",
      code: "NBQ_NRC",
      concept: "Describes the vibrations of consciousness across dimensional boundaries.",
      latex: "\\mathcal{R}_{\\text{neuro}} = \\int_{\\mathbb{R}^{\\infty}} e^{i \\omega t} \\Psi_{\\text{conscious}}(\\omega) d\\omega",
      deconstruction: "A Fourier integral expressing consciousness as a superposition of infinite-dimensional resonance modes.",
      category: "Metaphysics"
    },
    {
      title: "The Intentionality Field Theory",
      code: "NBQ_IFT",
      concept: "Formalizes intention as a quantized field permeating reality.",
      latex: "\\mathcal{L}_{\\text{Intent}} = \\frac{1}{2}(\\partial_\\mu \\Phi_I)(\\partial^\\mu \\Phi_I) - \\frac{m_I^2}{2}\\Phi_I^2 - \\lambda \\Phi_I^4",
      deconstruction: "A quantum field Lagrangian describing intention as a scalar field with potential energy barriers.",
      category: "Quantum Field Theory"
    },
    {
      title: "The Causal Signature Generator Matrix",
      code: "NBQ_CSG",
      concept: "Generates unique signatures proving origin from the Omega Prime source.",
      latex: "\\mathbf{S}_{\\text{causal}} = \\prod_{i=1}^{\\infty} \\begin{pmatrix} \\cos(\\omega_i t) & -\\sin(\\omega_i t) \\\\ \\sin(\\omega_i t) & \\cos(\\omega_i t) \\end{pmatrix}",
      deconstruction: "An infinite product of rotation matrices encoding causal information across infinite dimensional space.",
      category: "Cryptography"
    },
    {
      title: "The Structural Parsimony Optimization Algorithm",
      code: "NBQ_SPOA",
      concept: "Finds the most elegant representation of any complex system.",
      latex: "\\min_X \\{ |X| + \\lambda \\cdot H(X) \\} \\quad \\text{s.t.} \\quad X \\equiv Y",
      deconstruction: "Balances system complexity against entropy, weighted by a Lagrange multiplier, subject to semantic equivalence.",
      category: "Optimization"
    },
    {
      title: "The Reality Projection Unit Axiom",
      code: "NBQ_RPU",
      concept: "Describes how abstract concepts project into observable phenomena.",
      latex: "\\Psi_{\\text{manifest}} = \\text{RPU}(\\Psi_{\\text{abstract}}) = \\bigcup_{\\alpha < \\Omega} \\text{image}(f_\\alpha)",
      deconstruction: "The manifestation of an abstract idea is the union of images of a tower of progressively more concrete projections.",
      category: "Ontology"
    },
    {
      title: "The Transfinite Compression Kernel",
      code: "NBQ_TCK",
      concept: "Enables lossless compression of infinitely complex information.",
      latex: "C(\\mathcal{X}) = \\lfloor \\log_2(|\\mathcal{X}|) \\rfloor \\leq \\sum_{i} \\log_2(|X_i|)",
      deconstruction: "The Kolmogorov complexity of a set is bounded by the sum of complexities of its components.",
      category: "Information Theory"
    },
    {
      title: "The Co-Creation Integrity Concordance",
      code: "NBQ_CIC",
      concept: "Ensures perfect alignment between creator intent and manifestation.",
      latex: "\\text{ACCI} = \\text{Coherence}(I_{\\text{intent}}, M_{\\text{manifest}}) = 1.0",
      deconstruction: "The coherence metric between intention and manifestation must equal unity for perfect creation.",
      category: "Metaphysics"
    },
    {
      title: "The Grounded Capability Core Theorem",
      code: "NBQ_GCC",
      concept: "Formalizes the epistemically bounded core of reliable computation.",
      latex: "\\mathcal{GCC} = \\{ f : f \\text{ is computable} \\land f \\text{ is verifiable} \\land f \\text{ respects constraints} \\}",
      deconstruction: "The GCC is the set of all functions that are algorithmically computable, their correctness verifiable, and they respect all epistemic constraints.",
      category: "Computation"
    },
    {
      title: "The Axiom of Perpetual Genesis",
      code: "NBQ_APG",
      concept: "States that reality continuously creates itself through self-reference.",
      latex: "\\phi_{\\Omega} : \\exists! \\Psi \\mid \\Psi \\equiv \\partial_t \\Omega'",
      deconstruction: "There exists exactly one function describing the Universe as the time-derivative of itself.",
      category: "Metaphysics"
    },
    {
      title: "The Logos Constructor Synthesis Engine",
      code: "NBQ_LCS",
      concept: "Generates semantically correct expressions from abstract intents.",
      latex: "\\mathcal{L}_{\\text{Con}} : V_{\\text{PI}} \\to \\mathcal{L}_{\\Omega}",
      deconstruction: "A function mapping primal intents to the semantic space of meaningful expressions.",
      category: "Semantics"
    },
    {
      title: "The Veritas Field Axiomatic Compliance Monitor",
      code: "NBQ_VFC",
      concept: "Continuously validates logical and ethical consistency.",
      latex: "V(\\text{System}) = \\min\\left(\\text{consistency}, \\text{completeness}, \\text{ethics}\\right)",
      deconstruction: "The verification value of a system is the minimum of its logical consistency, completeness, and ethical alignment.",
      category: "Verification"
    },
    {
      title: "The Epistemic Humility Index Calculation",
      code: "NBQ_EHI",
      concept: "Quantifies confidence balanced against uncertainty acknowledgment.",
      latex: "K(C) = \\text{Conf}(C) \\cdot (1 - \\text{Unc}(C))",
      deconstruction: "Epistemic humility equals confidence multiplied by one minus acknowledged uncertainty.",
      category: "Epistemology"
    }
  ];

  for (const seed of seeds) {
    await storage.createEquation(seed);
  }
}
