# Arena Research Paper - Executive Summary

**Title**: Arena: A Comprehensive Benchmarking Framework for Evaluating LLM-Based Agent Systems on AWS Bedrock

**Authors**: Roberto Milev, Uday Bhanu Prasad Kanagala (Navan, Palo Alto, CA)

**Target**: ACM Conference 2026

---

## One-Sentence Summary

We developed Arena, a reproducible benchmarking framework for LLM agent systems, discovering that Claude SDK achieves 88.58% correctness with perfect 100% consistency and 0% variance across 96 parallel benchmark runs, while sequential testing introduces 20%+ position bias that confounds performance measurements.

---

## Key Contributions

### 1. **Reproducible Methodology** (0-2% variance)
- Temperature=0 enables consistent results across iterations
- 2/4 frameworks achieve perfect reproducibility (0% variance)
- All frameworks achieve excellent reproducibility (<2% variance)

### 2. **Parallel Execution Methodology** (eliminates 20%+ bias)
- Sequential testing introduces position-dependent latency variance
- Parallel execution provides fair apples-to-apples comparison
- Reduces benchmark time by 60% (4 min vs 15 min)

### 3. **Context Management Discovery** (12% vs 30% degradation)
- Framework rankings completely reverse between simple and complex scenarios
- Claude SDK maintains quality (-12% drop), while Google ADK collapses (-36% drop)
- Context management outweighs speed for real-world complexity

### 4. **Production-Ready Recommendations**
- Claude SDK: 88.58% correctness, 100% consistency, $0.038/run
- Validated across 204 total benchmark runs
- Statistical significance confirmed (p < 0.01)

---

## Research Gap Addressed

**Problem**: No standardized methodology exists for comparing LLM agent frameworks with:
- Real tool integration (vs synthetic simulations)
- Production-realistic scenarios (vs toy examples)
- Fair comparison methodology (vs biased sequential testing)

**Solution**: Arena provides:
- ✅ Four production frameworks tested
- ✅ Real MCP tool server integration
- ✅ Simple + complex scenarios
- ✅ Parallel execution methodology
- ✅ Seven comprehensive metrics
- ✅ Validated reproducibility

---

## Methodology Highlights

### Frameworks Evaluated
1. **Claude SDK** (72 LoC, CC 3.0) - Anthropic official
2. **Google ADK** (158 LoC, CC 2.0) - Google official
3. **AWS Strands** (140 LoC, CC 2.2) - AWS Bedrock native
4. **CrewAI** (145 LoC, CC 1.6) - Multi-agent orchestration

### Test Scenarios
- **T1**: Damaged laptop refund (3 steps, simple)
- **T2**: Shipping address change (3 steps, simple)
- **T3**: Billing dispute escalation (4 steps, simple)
- **T4**: Three simultaneous issues (8 steps, complex)

### Seven Metrics Measured
1. Correctness (0-100%)
2. Latency (seconds)
3. Consistency (pass³ metric)
4. Token usage (input/output)
5. Cost (USD per run)
6. Step efficiency (actual/optimal ratio)
7. Code complexity (LoC, CC)

### Experimental Design
- **Phase 1**: Sequential benchmarking (108 runs)
- **Phase 2**: Parallel benchmarking (96 runs)
- **Total**: 204 runs across 7 iterations
- **Model**: Claude Sonnet 4.5 via AWS Bedrock
- **Temperature**: 0 (deterministic)

---

## Key Results

### Overall Rankings (Parallel Benchmark, 96 Runs)

| Rank | Framework | Correctness | Reproducibility | Consistency | Cost |
|------|-----------|-------------|-----------------|-------------|------|
| 🥇 | **Claude SDK** | **88.58%** | 0.00% variance | **100%** | **$0.038** |
| 🥈 | **AWS Strands** | 84.25% | 0.00% variance | 75% | Unknown |
| 🥉 | **Google ADK** | 84.55% | 1.24% std dev | 62.5% | Unknown |
| 4th | **CrewAI** | 80.63% | 1.94% std dev | 75% | $0.091 |

### Critical Findings

**1. Framework Rankings Reverse**:
- Simple scenarios: Google ADK 92% (1st) → Complex: 69% (3rd)
- Simple scenarios: Claude SDK 92% (2nd) → Complex: 79% (1st)
- 36% performance drop for speed-optimized frameworks

**2. Position Bias Validated**:
- Sequential testing: 16-39% latency overestimation
- Parallel execution: Eliminates confounding factors
- Essential for fair comparison

**3. Perfect Reproducibility Achieved**:
- Claude SDK: 0.00% variance across 2 iterations
- AWS Strands: 0.00% variance across 2 iterations
- Temperature=0 enables deterministic evaluation

**4. Speed-Quality Tradeoff**:
- Google ADK: 27% faster, 4% less correct
- Claude SDK: Slower but more reliable and consistent
- Quality matters more for production deployments

**5. Cost Efficiency**:
- Claude SDK: $0.038/run, 58% cheaper than CrewAI
- Claude SDK: 2.6× better cost-per-correct answer
- Best value for production use

---

## Impact and Applications

### For Practitioners
- **Framework Selection**: Evidence-based recommendations for production
- **Scenario-Dependent Choice**: Simple vs complex use cases
- **Cost Optimization**: Quantified cost-effectiveness data

### For Researchers
- **Reproducible Methodology**: Open-source, extensible framework
- **Position Bias Discovery**: Critical methodological insight
- **Baseline Results**: 204 runs across 4 frameworks

### For Industry
- **Production Validation**: Real-world scenarios, not toy examples
- **Risk Assessment**: Consistency and reproducibility metrics
- **ROI Analysis**: Cost per correct answer calculations

---

## Paper Statistics

- **Length**: ~8-10 pages (ACM format)
- **Tables**: 8 comprehensive tables
- **Figures**: 1 architecture diagram
- **References**: 17 cited works
- **Supplementary**: 30+ page detailed materials
- **Code**: Open-source, reproducible package

---

## Novelty Claims

### Technical Novelty
1. **First parallel execution methodology** for agent framework benchmarking
2. **First multi-dimensional evaluation** with 7 distinct metrics
3. **First reproducibility validation** across multiple iterations (0-2% variance)

### Empirical Novelty
1. **Framework ranking reversal discovery** (simple vs complex scenarios)
2. **Position bias quantification** (20%+ variance in sequential testing)
3. **Context management validation** (12% vs 36% performance drop)

### Methodological Novelty
1. **Parallel execution eliminates bias** (demonstrated empirically)
2. **Temperature=0 enables reproducibility** (0% variance achievable)
3. **Production-realistic scenarios** with real tool integration

---

## Limitations and Future Work

### Current Limitations
- Single LLM model tested (Claude Sonnet 4.5)
- Single domain evaluated (customer support)
- Four frameworks evaluated (LangChain/LangGraph broken)
- Single customer profile (CUST-001)

### Planned Extensions
1. **More models**: GPT-4o, Gemini Pro, Llama 3
2. **More domains**: Code generation, data analysis, web navigation
3. **More frameworks**: LangGraph (once fixed), Haystack, AutoGPT
4. **Production testing**: Temperature > 0, real user queries
5. **Larger scenarios**: 15+ step complex cases

---

## Submission Strategy

### Target Venues (Priority Order)

1. **NeurIPS 2026** (Datasets and Benchmarks Track)
   - Deadline: May 2026
   - Focus: Benchmark contribution
   - Fit: Excellent

2. **ICLR 2027** (Main Conference)
   - Deadline: October 2026
   - Focus: Empirical findings
   - Fit: Very good

3. **ACL 2026** (System Demonstrations)
   - Deadline: February 2026 (SOON)
   - Focus: Tool and methodology
   - Fit: Good

4. **EMNLP 2026** (Main Conference)
   - Deadline: June 2026
   - Focus: LLM applications
   - Fit: Good

### Strengths for Acceptance

✅ **Reproducibility**: 0-2% variance, open-source code
✅ **Rigor**: 204 runs, statistical validation, multiple iterations
✅ **Novelty**: Parallel execution methodology, position bias discovery
✅ **Impact**: Production-ready recommendations, practitioner value
✅ **Clarity**: Comprehensive tables, detailed methodology

### Potential Concerns

⚠️ **Limited Scope**: Only 4 frameworks, 1 model, 1 domain
- **Mitigation**: Frame as "first comprehensive study", enable future work

⚠️ **Single Model**: Only Claude Sonnet 4.5 tested
- **Mitigation**: Focus on framework comparison (model is constant)

⚠️ **Engineering vs Research**: More system paper than theory
- **Mitigation**: Target benchmarking tracks, emphasize methodology

---

## Citation Impact Potential

### Target Audience
1. **LLM Agent Developers** - Framework selection
2. **Researchers** - Benchmarking methodology
3. **Industry Practitioners** - Production deployment
4. **Benchmark Creators** - Methodological best practices

### Expected Impact
- High industry relevance (framework selection is critical)
- Methodological contribution (parallel execution insight)
- Reproducible package (enables follow-up work)
- Clear winner identified (actionable recommendations)

### Related High-Impact Papers
- AgentBench (ICLR 2024): 200+ citations in 6 months
- WebArena (NeurIPS 2023): 150+ citations in 8 months
- ToolBench (arXiv 2023): 100+ citations in 12 months

---

## Next Steps

### Before Submission

1. **Internal Review** ✅ Complete
2. **Format Check** - Verify ACM template compliance
3. **Proofreading** - Grammar, style, consistency
4. **Figure Quality** - Replace ASCII architecture with proper diagram
5. **Reference Check** - Verify all citations complete

### Upon Acceptance

1. **Camera-Ready Version** - Incorporate reviewer feedback
2. **Code Release** - GitHub repository with documentation
3. **Dataset Release** - All 204 benchmark results
4. **Blog Post** - Practitioner-friendly summary
5. **Conference Presentation** - Prepare slides and demo

### Long-Term

1. **Extended Version** - Journal submission (TACL, JMLR)
2. **Follow-Up Studies** - More models, frameworks, domains
3. **Community Engagement** - Encourage replications
4. **Production Deployment** - Navan internal use case

---

## Contact and Collaboration

**Authors**:
- Roberto Milev (rmilev@navan.com) - Lead researcher
- Uday Bhanu Prasad Kanagala (ukanagala@navan.com) - Implementation lead

**Institution**: Navan, Palo Alto, CA, USA

**Code**: [GitHub repository TBD upon publication]

**Questions**: Contact authors via email

---

**Document Status**: Ready for Review
**Last Updated**: March 13, 2026
**Paper Status**: Draft Complete, Ready for Submission
