  ## Product Brief: Daily Performance Summary Bot

### Problem
Marketing analysts spend 2+ hours daily pulling data from 5+ platforms to report performance. The answer varies by person. If that analyst is OOO, the question goes unanswered. This creates delays for clients and internal decisions.

### Primary User
**Internal Marketing Analyst** at Tacheon 
Secondary: Client Account Managers who need quick status before calls

### v1 Solution: Slack Command `/marketing-status`
**What it DOES in v1:**
1. Runs at 9 AM IST daily or on-demand via Slack command
2. Pulls spend, clicks, CPA from GA4, Google Ads, Meta for last 24hrs
3. Flags 2 types of anomalies: spend >2x 7-day avg, CPA shift >30%
4. Posts 1 Slack message: 3 bullets + "Focus: Meta CPA spiked 40%, check creative fatigue"

**What it does NOT do in v1 + Why:**
1. **Auto-pause campaigns** → Too risky without human review. Trust issue
2. **Predictive budget reallocation** → Needs 90 days historical data we don't have yet
3. **New dashboard** → Violates constraint: "team won't change tools". Analysts live in Slack

### Key Constraint: Fit Existing Workflow
Team uses Slack + GA4 + Ads Manager daily. They will NOT adopt new dashboards. Solution must live where they already work. Slack bot = 0 learning curve.

### What Builds Trust in v1
1. **Show your math**: Every anomaly includes "vs 7-day avg" so analyst can verify
2. **One source of truth**: Same logic for everyone, unlike manual pulls
3. **No black box**: Link to raw data in BigQuery for drill-down

### Success Metrics
1. Time saved per analyst per day: Target 1.5 hrs
2. % of teams using it daily after 2 weeks: Target >80%
3. Reduction in "hey, can you pull numbers?" Slack pings: Target -70%

