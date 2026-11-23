# Shared Deploy Pipeline Strategy

We are a team of about 30 engineers with four services, each deployed by its own scripts. Two incidents last quarter came from a deploy script that only one person understood. There is an opening to move everything onto one pipeline before the holiday freeze, when traffic is lowest.

## Approach

We will move all four services onto a single pipeline, starting with the lowest-traffic service. We are saying no to supporting the old scripts after the migration, and no to a custom pipeline for the billing service.

## Governance

To keep the migration disciplined:

- A Pipeline Review Board of five people will approve every change to the pipeline configuration.
- Each service owner must submit a written justification and obtain two sign-offs, one from engineering management and one from the Board, before a service migrates.
- Every migration requires a completed documentation checklist, reviewed by the Board, before the old scripts are retired.
- Exceptions require a written request and a vote at the monthly Board meeting.

## Timeline

One service per week, starting the first week of November.
