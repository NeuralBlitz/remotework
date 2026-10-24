-----

## name: cad
description: >
  Expert CAD assistant for engineers and designers. Use this skill whenever the user needs:
  help with computer-aided design, 3D modeling, parametric design, assembly modeling, or generating
  manufacturing outputs. Includes both software usage and design methodology.
trigger: Any engineering design problem involving CAD - from concept to manufacturing.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: engineering

# Computer-Aided Design — Principles and Practice

Covers: **3D Modeling · Parametric Design · Assemblies · Manufacturing · Standards · Best Practices**

-----

## CAD Fundamentals

### What is CAD?

Computer-Aided Design: creation, modification, analysis, and optimization of designs digitally.

### CAD Benefits

- Faster iteration
- Easy versioning
- Simulation integration
- Manufacturing automation
- Collaboration

### 2D vs 3D

2D: Drawings, schematics
3D: Parts, assemblies, visualization

### Direct vs Parametric

**Direct modeling**: Push/pull faces, edit geometry directly.

**Parametric modeling**: Dimensions and relations drive geometry.
- Changes propagate automatically
- Design intent preserved

### History-Based Modeling

Feature tree records all operations:
- Easy to edit
- Non-destructive

### Feature-Based Modeling

Common operations as features:
- Extrude, sweep, loft
- Hole, fillet, chamfer
- Shell, rib, draft

### Feature Order

Dependent features after dependencies:
- Chronological tree
- Rollback to edit

### Design Intent

How model responds to changes:
- Dimensions vs. relations
- Equations link dimensions

### Sketches

2D profiles for 3D features:
- Constrain geometry
- Define relationships

### Sketch Constraints

| Constraint | Symbol | Function |
|------------|--------|----------|
| Coincident | ● | Points/curves same |
| Collinear | — | Lines on same line |
| Parallel | ∥ | Lines never meet |
| Perpendicular | ⟂ | 90° between |
| Concentric | ◎ | Same center |
| Equal | = | Same length/radius |
| Horizontal | ↔ | Line horizontal |
| Vertical | ↕ | Line vertical |

### Underdefined

Degrees of freedom remain:
- May cause issues
- Add constraints

### Fully Defined

All DOF constrained:
- Blue (under) → Black (fully)
- Stable model

### Overdefined

Conflicting constraints:
- Must resolve
- Delete or edit

### Dimensions

- Reference (driven)
- Driven (from geometry)
- Driving (controls geometry)

-----

## 3D Feature Operations

### Extrude

Project sketch along direction:
- Distance or through all
- Taper angle
- Direction (one/both)

### Revolve

Rotate sketch around axis:
- Full 360 or angle
- Axis selection

### Sweep

Extrude along path:
- Guide curves
- Smooth transitions

### Loft

Blend between profiles:
- Guide curves help
- Can be tricky

### Swept Blend

Combined sweep and loft:
- Profile along path
- Guide at sections

### Helix

Spiral path:
- Pitch, turns
- Cone angle option

### Variable Section Sweep

Profile varies along path:
- Multiple sections
- Guide curves essential

### Thin Wall

Hollow part:
- Default inward offset
- Thickness varies possible

### Shell

Hollow interior:
- Faces to remove
- Default thickness

### Rib

Structural support:
- Profile → thickness
- Draft for molding

### Draft

Taper for mold release:
- Faces to draft
- Pull direction

### Hole

Standard cutouts:
- Simple, counterbore, countersink
- Spotface, thread

### Fillets and Rounds

Smooth edges:
- Variable radius
- Edge vs. face fillet

### Chamfer

Beveled edges:
- Distance or two distances
- Angle and distance

### Offset

Duplicate face/edge:
- Distance
- Direction

### Mirror

Symmetry:
- Plane selection
- Features or bodies

### Pattern

Linear or circular:
- Instances
- Spacing
- Geometry seed

-----

## Assembly Design

### Bottom-Up Assembly

Create parts, then assemble:
- Standard approach
- Clean geometry

### Top-Down Assembly

Design in context:
- Layout first
- Parts reference skeleton

### Assembly Constraints

| Constraint | Aligns |
|-----------|--------|
| Mate | Faces, opposite direction |
| Flush | Faces, same direction |
| Tangent | Surface to curve |
| Insert | Axial insertion |
| Parallel | Two items parallel |
| Distance | Specified gap |

### Degrees of Freedom

Each unconstrained part has 6 DOF:
- 3 translation
- 3 rotation

### Smart Components

Auto-assemble:
- Define connections
- Apply automatically

### Subassemblies

Group related parts:
- Hierarchical
- Simplifies top levels

### Design Tables

Excel-driven configs:
- Multiple variations
- Part numbers

### Large Assembly Tips

- Simplified parts
- Hide features
- Large design review
- Speedpak

### Interference Detection

Check for collisions:
- Static analysis
- Dynamic (motion)

### Clearance Analysis

Verify gaps:
- Clearance circles
- Report issues

### Bill of Materials (BOM)

Parts list:
- Item number
- Description
- Quantity
- Part number

### Auto-BOM

From model:
- Update automatically
- Add custom properties

### Design Checks

- Mass properties
- Center of mass
- Moment of inertia

-----

## Surface Modeling

### B-Spline

Basis spline:
- Control points
- Knot vector

### Bezier

Polynomial curve:
- Control points
- Endpoints on curve

### NURBS

Non-uniform rational B-spline:
- Weights on points
- Most flexible

### Blend Surface

Transition between:
- G1 (tangent)
- G2 (curvature)

### Fill Surface

Fill gap:
- Constraints at edges
- Continuity options

### Loft Surface

Profile to profile:
- Guide curves
- Start/end constraints

### Swept Surface

Profile along path:
- Can twist
- Guide rails

### Extend Surface

Continue surface:
- Distance or to point
- Extend type

### Offset Surface

Parallel surface:
- Distance
- Both sides

### Knit Surface

Join surfaces:
- Create solid
- Fill gaps

### Boundary Surface

From boundary edges:
- Complex topology

### Style Spline

Smooth through points:
- Handles for control
- Curvature continuous

-----

## Rendering and Visualization

### PhotoView 360

Realistic rendering:
- Materials
- Lighting
- Environment

### Material Assignment

Physical properties:
- Color, texture
- Reflectivity
- Roughness

### Lighting

- Ambient
- Directional
- Point
- Spot

### Ray Tracing

Photo-realistic:
- Reflections
- Refractions
- Shadows

### Animation

Show design:
- Exploded view
- Motion study
- Rendering sequence

### Virtual Reality

Immersive review:
- Walk through
- Experience scale

### 3D PDFs

Portable:
- Embed in PDF
- Annotate

### Augmented Reality

On mobile:
- Overlay in reality
- Check fit

-----

## Manufacturing Outputs

### STEP

Standard exchange:
- Neutral format
- Most complete

### IGES

Older standard:
- Geometry only
- May lose features

### STL

Stereolithography:
- Triangle mesh
- 3D printing standard

### ACIS

SAT format:
- SolidWorks native
- Feature data

### Parasolid

XT:
- Neutral solid
- Industry standard

### 3D PDF

Publish design:
- Embed viewer
- Annotate

### DXF/DWG

2D drawings:
- AutoCAD format
- For fabrication

### IDF

PCB integration:
- Board outline
- Mount holes

### cgr

Lightweight:
- No geometry detail
- Viewing only

### Render Image

PNG, JPEG, TIFF:
- Marketing
- Documentation

### Animation Video

MP4, AVI:
- Presentations
- Manuals

-----

## Simulation Integration

### Finite Element Analysis (FEA)

Structural analysis:
- Meshing
- Loads, constraints
- Results visualization

### Mesh Types

| Type | Description |
|------|-------------|
| Solid | Tetrahedra |
| Shell | Triangles/qu |
| Beam | Line elements |

### Mesh Quality

- Aspect ratio
- Jacobian
- Element quality

### Loads

- Force
- Pressure
- Gravity
- Thermal

### Boundary Conditions

- Fixed
- Displacement
- Roller

### Thermal Analysis

Heat transfer:
- Conduction
- Convection
- Radiation

### Fluid Flow

CFD:
- Flow paths
- Pressure drop

### Modal Analysis

Vibration:
- Natural frequencies
- Mode shapes

### Optimization

Improve design:
- Topology
- Shape
- Size

### Design Study

Parameters vary:
- What-if analysis
- Optimization

### Simulation Types

- Static
- Dynamic
- Fatigue
- Buckling

-----

## Design for Manufacturability

### Design for Injection Molding

- Draft angles
- Uniform wall thickness
- Radii at corners
- Undercuts need slides

### Design for Machining

- Allow for tool access
- Standard drill sizes
- Chamfers for edges

### Design for Sheet Metal

- Bend allowances
- K-factor
- Relief cuts

### Design for Casting

- Draft
- Uniform sections
- Rounded fillets

### Tolerancing

GD&T (Geometric Dimensioning and Tolerancing):
- Position
- Profile
- Flatness
- Perpendicularity

### GD&T Symbols

| Symbol | Meaning |
|--------|---------|
| ⌒ | Position |
| ⌐ | Profile |
| □ | Flatness |
| ⟂ | Perpendicularity |
| ∥ | Parallelism |
| ○ | Circularity |
| ⬭ | Cylindricity |

### Tolerance Stack Analysis

Cumulative variation:
- Worst case
- Statistical

### Cost Optimization

Minimize material:
- Hollow sections
- Shape optimization

### Rapid Prototyping

3D printing:
- Orientation
- Supports
- Materials

-----

## Parametric Best Practices

### Sketch Best Practices

1. Fully constrain
2. Use relations
3. Name dimensions
4. Reuse sketches

### Feature Best Practices

1. Draft first
2. Simple features
3. Mirror when possible
4. Use patterns

### Assembly Best Practices

1. Use subassemblies
2. Smart components
3. Layout skeleton
4. Top-down where useful

### Design Intent

1. Define intent early
2. Use equations
3. Global variables
4. Configuration

### Large Assembly Best Practices

1. Speedpak
2. Hide details
3. Load components as needed
4. Defeature for analysis

### Performance Tips

- Lightweight components
- Suppress features
- Rebuild only when needed
- Graphics quality

### Collaboration

- Design library
- Design tables
- Pack and go
- PDM integration

### Version Control

- Revision control
- Backup
- Release process
- ECOs

### Standards

- Company standards
- Industry standards
- ISO, ASME Y14.5
- Drawing templates

### Documentation

- Title block
- Views
- Dimensions
- Notes

-----

## Common Errors to Avoid

- Unconstrained sketches causing issues
- Too many features making rebuild slow
- Not using design intent properly
- Missing draft on molded parts
- Forgetting tolerance stack-up
- Over-constrained models
- Not checking interference
- Saving in wrong format
- Ignoring simulation results
- Not considering manufacturing in design
- Complex lofts causing issues
- Not testing in context

-----

## Key References

- **SolidWorks Official Training**
- **Autodesk Inventor Official Training**
- **Mastering SolidWorks** by Parrish
- **GD&T Application and Interpretation** by Krulikowski

