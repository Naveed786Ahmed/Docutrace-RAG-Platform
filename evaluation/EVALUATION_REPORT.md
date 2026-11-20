# DocuTrace: RAG Evaluation Report

**Project:** DocuTrace, Evidence-Grounded Enterprise Knowledge Assistant  
**Evaluation Status:** Initial benchmark and acceptance testing completed  
**Knowledge Base:** 26 enterprise PDF documents, 239 pages  
**Evaluation Dataset:** 200 questions

## 1. Evaluation Objective

Evaluate DocuTrace's ability to retrieve relevant enterprise documentation, generate evidence-grounded answers, provide traceable citations, and decline questions unsupported by the knowledge base.

The evaluation combines document-level retrieval benchmarking, parameter experimentation, failure analysis, and end-to-end acceptance testing.

## 2. Evaluation Dataset

| Question Category | Count |
|---|---:|
| Single-hop | 180 |
| Multi-hop | 12 |
| Negative / Unanswerable | 8 |
| **Total** | **200** |

Dataset validation confirmed 200 unique question identifiers with zero validation errors and zero warnings.

## 3. Retrieval Benchmark

Retrieval was evaluated against 192 answerable questions.

**Metric:** Document Hit@4

A question passes when all expected source documents appear among the four retrieved chunks.

| Retrieval Configuration | Successful | Document Hit@4 |
|---|---:|---:|
| Dense similarity search, k=4 | 170/192 | 88.54% |
| MMR, k=4, fetch_k=20 | 175/192 | 91.15% |
| MMR, k=4, fetch_k=40 | 171/192 | 89.06% |

**Best experimental configuration:** MMR with `k=4`, `fetch_k=20`, and `lambda_mult=0.5`.

This improved document-level retrieval coverage by **2.61 percentage points** over the similarity-search baseline.

These figures measure expected-document retrieval, not answer accuracy or factual correctness.

The optimized MMR configuration was evaluated experimentally. Its production adoption and performance must be verified separately.

## 4. Retrieval Failure Analysis

The baseline similarity-search configuration failed to retrieve all expected documents within the top four chunks for 22 questions.

Increasing diagnostic retrieval depth to ten chunks recovered expected-document coverage for 15 of these questions. Seven remained unresolved.

The analysis identified several recurring patterns:

- Multiple chunks from the same document occupied retrieval positions.
- Multi-document questions sometimes retrieved only one required source.
- Some expected documents appeared below the top-four cutoff.
- Greater retrieval depth did not consistently improve document coverage.

These findings informed subsequent MMR parameter experiments.

## 5. End-to-End Acceptance Testing

A representative 20-question subset was evaluated through the RAG answer-generation pipeline.

| Category | Tested | Findings |
|---|---:|---|
| Single-hop | 8 | Seven substantially complete answers; one omitted a relevant policy exception |
| Multi-hop | 4 | Three substantially correct answers; one materially incorrect |
| Negative | 8 | All eight returned the expected refusal with no citations |

All 20 test executions completed.

### Identified Issues

**Q001: Incomplete policy answer**

The generated response correctly identified the 90-day probationary period but omitted the possible 30-day extension at manager discretion.

**MH003: Incorrect multi-hop answer**

The response failed to identify the Launchpad onboarding program and did not accurately provide the expected device-security requirements.

The expected Employee Handbook appeared at rank five in the similarity-search diagnosis, outside the pipeline's top-four retrieval window.

**MH004: Incomplete expected-source coverage**

The response included the principal severity, response-leadership, and notification-timing facts but did not cite the expected Privacy Policy document.

Document-level citation matching failed, although the cited Incident Response document may contain overlapping supporting information.

## 6. Citation and Grounding Limitations

Automated citation matching checks whether expected document identifiers appear in the response citations.

It does not independently establish that:

- The cited page contains the supporting passage.
- Every generated claim is supported by the cited evidence.
- The answer includes all required facts.
- The model has avoided unsupported inferences.

Page-level citation verification and full factual grading were not completed across the entire 200-question dataset.

## 7. Negative Question Handling

All eight negative acceptance-test questions returned the standardized response:

"I cannot find this information in the company documents."

No citations were returned for these questions.

This demonstrates correct fallback behavior for the tested cases, not a universal guarantee against hallucinations.

## 8. Engineering Conclusions

The evaluation established a reproducible retrieval baseline, compared alternative retrieval configurations, and identified concrete limitations in multi-document retrieval and answer completeness.

The best experimental Document Hit@4 was **91.15%**, compared with the **88.54%** baseline.

The end-to-end acceptance test demonstrated successful handling of the eight negative questions while exposing areas requiring further reliability improvements.

## 9. Known Limitations and Next Steps

- Verify the retrieval strategy used in the deployed pipeline against the benchmarked configuration.
- Improve multi-document evidence coverage where required.
- Address incomplete and incorrect answers identified during acceptance testing.
- Validate citation support at the PDF page level.
- Implement authentication, structured logging, error handling, and secure configuration.
- Validate deployment behavior and persistent vector storage.
- Perform additional testing with a larger document collection.

## 10. Evaluation Scope

The evaluation used a fictional enterprise knowledge base comprising 26 PDF documents and 239 pages.

Results should not be interpreted as performance guarantees for arbitrary enterprise documents or larger production deployments.

**Conclusion:** Initial evaluation completed with documented findings and known limitations. Production readiness remains subject to security, reliability, deployment, and further acceptance testing.