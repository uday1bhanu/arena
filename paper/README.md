# Arena ACM Research Paper

This directory contains the complete ACM-format research paper for the Arena benchmarking framework.

## Files

### ⭐ Enhanced Version (RECOMMENDED)
- **`arena_acm_paper_enhanced.tex`** - ⭐ **Enhanced LaTeX source with professional diagrams and charts**
- **`arena_acm_paper_enhanced.pdf`** - ⭐ **11-page PDF with TikZ diagrams and pgfplots visualization**

### Original Version
- **`arena_acm_paper.tex`** - Original LaTeX source (basic formatting)
- **`arena_acm_paper.pdf`** - 8-page PDF (ASCII diagrams)

### Supporting Documents
- **`ENHANCEMENTS_SUMMARY.md`** - ⭐ **Complete comparison: Original vs. Enhanced**
- **`SUPPLEMENTARY_MATERIALS.md`** - Detailed supplementary materials
- **`PAPER_SUMMARY.md`** - Executive summary for stakeholders
- **`README.md`** - This file
- **`view_papers.sh`** - Script to open both PDFs for comparison

## Paper Information

**Title**: Arena: A Comprehensive Benchmarking Framework for Evaluating LLM-Based Agent Systems on AWS Bedrock

**Authors**:
- Roberto Milev (Navan) - rmilev@navan.com
- Uday Bhanu Prasad Kanagala (Navan) - ukanagala@navan.com

**Location**: Palo Alto, CA, USA

**Conference**: [Conference Name] 2026

## Abstract

Large Language Model (LLM)-based agent systems are increasingly deployed in production environments, yet there exists no standardized methodology for comparing agent frameworks across diverse real-world scenarios. We present **Arena**, a comprehensive benchmarking framework that evaluates four production-ready agent frameworks on AWS Bedrock using Claude Sonnet 4.5. Through 204 benchmark runs across 7 iterations, including novel parallel execution methodology, we evaluate frameworks on 7 key metrics. Our findings reveal that framework rankings completely reverse between simple and complex scenarios, with Claude SDK emerging as the definitive winner (88.58% correctness, 100% consistency, 0% variance).

## Key Contributions

1. **Reproducible Methodology**: Achieves 0-2% variance across iterations
2. **Parallel Execution Validation**: Demonstrates sequential testing introduces 20%+ position bias
3. **Context Management Insight**: Empirically shows context management outweighs speed for complex scenarios
4. **Production Recommendations**: Claude SDK validated as optimal choice (88.58%, 100% consistency, 0% variance)

## Compiling the Paper

### Requirements

- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- ACM LaTeX template (included in `acmart` class)

### Compilation Commands

```bash
# Standard compilation
pdflatex arena_acm_paper.tex
bibtex arena_acm_paper
pdflatex arena_acm_paper.tex
pdflatex arena_acm_paper.tex

# Using latexmk (recommended)
latexmk -pdf arena_acm_paper.tex

# Clean auxiliary files
latexmk -c
```

### Output

The compiled PDF will be `arena_acm_paper.pdf`

### Online Compilation

If you don't have a local LaTeX installation, you can use:
- **Overleaf**: Upload `arena_acm_paper.tex` to https://www.overleaf.com
- **ShareLaTeX**: Similar cloud-based LaTeX editor

## Paper Structure

1. **Abstract** - Summary of work and key findings
2. **Introduction** - Motivation, problem statement, contributions
3. **Background and Related Work** - Prior work in agent benchmarking
4. **Arena Framework Design** - Architecture, scenarios, metrics, frameworks
5. **Experimental Setup** - Infrastructure, methodology, evaluation criteria
6. **Results** - Sequential and parallel benchmark results with tables
7. **Discussion** - Implications, position bias analysis, limitations
8. **Related Work** - Comparison with existing benchmarking efforts
9. **Conclusions and Future Work** - Summary and research directions
10. **References** - 17 cited works

## Tables and Figures

The paper includes 8 tables:

1. **Table 1**: Sequential Benchmark - Simple Scenarios (T1-T3)
2. **Table 2**: Sequential Benchmark - Complex Scenario (T4)
3. **Table 3**: Parallel Benchmark Results (2 Iterations, 96 Runs)
4. **Table 4**: Average Correctness by Scenario (Parallel)
5. **Table 5**: Latency Comparison - Sequential vs. Parallel
6. **Table 6**: Cost Efficiency Analysis
7. **Table 7**: Framework Scalability (Simple → Complex)
8. **Figure 1**: Architecture diagram (ASCII art, should be replaced with proper figure)

## Supplementary Materials

The **SUPPLEMENTARY_MATERIALS.md** file contains:

- Complete test scenario descriptions with expected behaviors
- Detailed results tables (all iterations)
- Framework implementation details with code snippets
- Statistical analysis (confidence intervals, power analysis, ICC)
- Reproducibility package (hardware specs, software dependencies, validation checklist)

## Citation

If you use Arena in your research, please cite:

```bibtex
@inproceedings{milev2026arena,
  title={Arena: A Comprehensive Benchmarking Framework for Evaluating LLM-Based Agent Systems on AWS Bedrock},
  author={Milev, Roberto and Kanagala, Uday Bhanu Prasad},
  booktitle={Conference Proceedings},
  year={2026},
  organization={ACM}
}
```

## License

[TBD - Add appropriate license for academic publication]

## Data Availability

All benchmark results, analysis scripts, and framework implementations are available in the parent directory (`../`):

- Raw results: `../parallel_benchmarks/`
- Framework code: `../arena/frameworks/`
- Test scenarios: `../arena/scenarios.py`
- Evaluation logic: `../arena/evaluator.py`

## Submission Status

- [ ] Draft complete
- [ ] Internal review
- [ ] Camera-ready version
- [ ] Submitted to conference
- [ ] Accepted
- [ ] Published

## Contact

For questions about the paper or benchmark:

**Roberto Milev**: rmilev@navan.com
**Uday Bhanu Prasad Kanagala**: ukanagala@navan.com

**Organization**: Navan, Palo Alto, CA, USA

---

**Version**: 1.0
**Last Updated**: March 13, 2026
**Status**: Draft Ready for Submission
