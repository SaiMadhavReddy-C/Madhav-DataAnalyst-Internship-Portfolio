# Task 4 — Statistical Validation

## Business hypothesis
**H0:** Mean transaction sales are equal for Female and Male transactions.
**H1:** Mean transaction sales differ between Female and Male transactions.

## Test
Welch's independent two-sample t-test, two-sided, α = 0.05.

## Results
- Female mean transaction sales: 136,883.21
- Male mean transaction sales: 141,807.34
- Mean difference (Female − Male): -4,924.13
- t-statistic: -0.6826
- p-value: 0.495011
- 95% CI for mean difference: [-19,079.85, 9,231.58]

## Interpretation
Fail to reject H0 at the 5% significance level. The result does not provide sufficient statistical evidence that average transaction sales differ by gender in this supplied dataset.

This is an association test, not a causal claim.
