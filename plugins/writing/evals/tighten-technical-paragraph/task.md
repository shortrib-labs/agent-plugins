Tighten this paragraph from our design doc before I send it out. Save it to `paragraph.md`.

---

We essentially re-architected the ingest path so that Kafka consumers now commit offsets only after the idempotent upsert into the Postgres 15 write-ahead-logged table has been fully acknowledged, which significantly reduces the possibility of duplicate rows during rebalances. In practice, this really brought p99 end-to-end latency down from 840 ms to 210 ms at a sustained 12,000 events per second, and it effectively eliminated the consumer lag spikes we were previously seeing, which had peaked at 1.8 million messages. Quite importantly, the partition count remains fixed at 48, so horizontal scaling is still bounded by that number.
