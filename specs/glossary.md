# Glossary

Terms and definitions used throughout the CAPE specification.

## A

### Argument (Tool)
A named parameter passed to a tool call, consisting of a key-value pair.

### Assertion
A discourse act type representing a direct statement or claim.

## C

### Capability
A specific, measurable behavior that an AI system can perform, defined by executable policies.

### Claim
A node in the PredicateGraph representing an assertion, opinion, or statement made in the model output.

### Citation
A reference linking a claim to its source, such as a URL or document.

### Code Block
A node representing a snippet of code extracted from the model output.

### Correction
The process of modifying an AI output to resolve policy violations.

### CPL (Capability Policy Language)
A declarative language for specifying executable policies over PredicateGraphs.

## D

### Discourse Act
A node representing a functional unit of communication, such as an explanation, greeting, or instruction.

### Domain
The subject area of a claim, such as "programming", "medicine", or "general".

## E

### Entity
A node representing a named object, concept, or reference in the model output.

### Evaluation
The process of checking a PredicateGraph against policies to determine compliance.

### Expression
A logical formula in CPL that can be evaluated to true or false.

### Extraction
The process of converting unstructured model output into a structured PredicateGraph.

## F

### Factual (Modality)
A claim modality indicating an assertion of objective fact.

## I

### Issue
A specific problem identified during verification, with location, description, and severity.

## L

### Learned Verifier
A trained model that evaluates semantic properties of AI outputs, complementing symbolic policies.

## M

### Meta-Verification
The process of verifying that a verifier's output is correct and coherent.

### Modality
The type of a claim: factual, opinion, conditional, hypothetical, or instruction.

## N

### Node
An element in the PredicateGraph: entity, claim, operation, tool call, citation, code block, or discourse act.

## O

### Operation
A node representing a calculation or logical operation in the model output.

### Operand
An input value to an operation.

### Operator
The function applied in an operation (e.g., add, multiply, compare).

## P

### Pack (Policy Pack)
A versioned collection of related CPL policies distributed together.

### Patch
A correction strategy that makes minimal, targeted fixes to specific violations.

### Policy
A set of rules that define requirements for AI outputs, written in CPL.

### Predicate
An atomic boolean function in CPL that tests a property of a node.

### PredicateGraph
A structured representation of an AI model's output, containing typed nodes and their relationships.

## Q

### Quantifier
A CPL construct for iterating over collections: `forall` (universal) or `exists` (existential).

## R

### Rewrite
A correction strategy that regenerates a section of the output.

### Rubric
A specification that defines how a learned verifier should evaluate outputs.

### Rule
A single requirement within a policy, consisting of an expression and metadata.

## S

### Schema
A JSON Schema document that defines the structure of CAPE artifacts.

### Severity
The importance level of a violation or issue: fatal, major, minor, warning, or info.

### Span
Character offsets (start and end) that locate content in the original text.

## T

### Tool Call
A node representing a function invocation in the model output.

### Training Objective
A description of what a learned verifier should learn to evaluate.

## V

### Verification
The process of checking whether an AI output meets specified requirements.

### Verifier
A component that evaluates AI outputs; may be symbolic (CPL) or learned.

### Violation
A specific instance where an output fails to meet a policy requirement.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




