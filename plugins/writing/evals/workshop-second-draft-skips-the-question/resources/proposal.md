# Moving alerts to PageRelay

We should move all production alerts to PageRelay by the end of Q3. The case is about reliability, not just cost. Our current pager drops about one in forty notifications, and the last two Sev-1 incidents started with a missed page.

PageRelay delivers on three channels (push, SMS, and phone call), with automatic escalation (no manual runbook step) after five minutes. The migration is not a rewrite, it's a configuration change. Each team moves its own routes, which keeps the risk small (and keeps ownership clear).

The ask is simple: approve the Q3 date and name one owner per team. This isn't about adding process, it's about removing a failure we already know about.
