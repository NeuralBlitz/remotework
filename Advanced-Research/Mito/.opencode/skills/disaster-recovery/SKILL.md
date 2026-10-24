---
name: disaster-recovery
description: Disaster recovery planning, business continuity, and failover strategies
license: MIT
compatibility: opencode
metadata:
  audience: devops
  category: systems-administration
---

## What I do
- Create comprehensive DR plans
- Define RTO and RPO objectives
- Test recovery procedures regularly
- Implement failover and failback systems
- Design for various disaster scenarios
- Ensure business continuity

## When to use me
When preparing for system failures, designing resilient infrastructure, or creating business continuity plans.

## Key Metrics

### RTO (Recovery Time Objective)
- Maximum acceptable downtime
- How long can the system be down?
- Typically defined in hours

### RPO (Recovery Point Objective)
- Maximum acceptable data loss
- How much data can be lost?
- Typically defined in minutes/hours

### SLA (Service Level Agreement)
- Committed availability
- Downtime allowances per year:
  - 99% = 3.65 days/year
  - 99.9% = 8.76 hours/year
  - 99.99% = 52.6 minutes/year
  - 99.999% = 5.26 minutes/year

## DR Strategies

### Backup & Restore
- Regular backups to offsite location
- Automated restore testing
- Pros: Simple, low cost
- Cons: Higher RTO

### Pilot Light
- Core services running minimal
- Scale up on failover
- Pros: Faster than backup
- Cons: More complex

### Warm Standby
- Scaled-down version running
- Quick scale on failover
- Pros: Faster recovery
- Cons: Higher cost

### Multi-Region Active-Active
- Full deployment in multiple regions
- Traffic distributed
- Pros: Fastest recovery, highest availability
- Cons: Most expensive, complex

## Disaster Recovery Plan

### Assessment
- Identify critical systems
- Document dependencies
- Assess risks and impacts
- Define recovery priorities

### Prevention
- Redundancy
- Monitoring
- Alerts
- Security
- Regular maintenance

### Detection
- Monitoring systems
- Health checks
- Alerting
- Incident response team

### Response
- Runbooks
- Escalation procedures
- Communication plan
- Documentation

### Recovery
- Documented procedures
- Tested steps
- Team responsibilities
- Verification steps

## Data Protection

### Backup Strategies
- Full backups
- Incremental backups
- Differential backups
- Continuous replication

### Backup Locations
- On-site (fast restore)
- Off-site (disaster protection)
- Cloud storage
- Air-gapped backups

### Testing
- Restore testing
- Failover testing
- Full DR exercises
- Document results
