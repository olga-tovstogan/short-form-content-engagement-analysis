# Beyond Views: What Makes Users Stop Scrolling?

**A product analytics portfolio project for short-form video.** This analysis uses 30,000 synthetic viewing events to distinguish meaningful interest from passive watch time and translate behavior into ranking and experimentation recommendations.

> **Disclosure:** This project is independent and uses entirely synthetic data. It is not affiliated with TikTok and makes no claim about TikTok's internal systems or users.

## Executive takeaway

Raw watch seconds are an incomplete measure of content quality because they are mechanically influenced by video length. In this simulated dataset, **Music** generated the highest normalized watch ratio (54.1%), while **Music** produced the strongest session-continuation rate (49.4%). Completion, explicit positive actions, quick swipes, and negative feedback should therefore be evaluated together rather than collapsed into a single attention metric.

## Product questions

1. Which categories hold attention after controlling for video length?
2. Which behavioral signals are most associated with continued viewing?
3. Where does video length begin to reduce completion?
4. How should a product team test a multi-signal ranking approach?

## Recommendations

1. **Use a multi-signal quality score.** Combine normalized watch time and completion with higher-intent actions such as shares and follows; subtract quick swipes and negative feedback.
2. **Calibrate by content length and category.** Compare videos with structurally similar content rather than rewarding long duration mechanically.
3. **Separate exploration from exploitation.** Preserve category diversity while increasing personalization after reliable preference signals accumulate.
4. **Run an online experiment before launch.** Test the new score against the current ranking logic, using meaningful-view rate and session continuation as primary metrics, with negative feedback and category diversity as guardrails.

## Proposed A/B test

- **Control:** ranking based primarily on predicted watch time.
- **Treatment:** ranking using normalized viewing, completion, shares, follows, rewatches, quick swipes, and negative feedback.
- **Primary metrics:** meaningful-view rate and session-continuation rate.
- **Guardrails:** negative-feedback rate, creator/category concentration, and extreme session-length growth.
- **Decision rule:** ship only if primary metrics improve without a statistically or practically meaningful guardrail deterioration.

## Repository map

```text
data/          Synthetic event data, aggregates, and dictionary
images/        Analysis charts
notebooks/     Reproducible Python walkthrough
src/           Standalone Python analysis
sql/           PostgreSQL-compatible analysis queries
presentation/  Recruiter-facing project brief
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analysis.py
jupyter notebook notebooks/user_engagement_analysis.ipynb
```

The repository includes the generated synthetic dataset so the notebook can be run immediately.

## Methods and limitations

The analysis uses descriptive aggregation, correlations, and an interpretable logistic-regression diagnostic. Associations are not causal. Synthetic outcomes were intentionally generated with realistic dependencies, so estimated relationships demonstrate workflow—not real platform performance. A production decision would require randomized experimentation and checks for novelty, seasonality, network effects, content safety, and creator fairness.
