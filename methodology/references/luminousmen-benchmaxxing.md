# Summary: "Benchmaxxing" (luminousmen)

Source: https://luminousmen.substack.com/p/benchmaxxing
Author: luminousmen (Substack essay, 2026)
Read status: read from text pasted by the repo owner. The page itself could not be fetched from the environment that wrote this file.

This is a summary in my own words, not a copy. Read the original for the full argument. All specifics about third parties are the author's reports and have not been checked here.

## Thesis

A benchmark number can be real, reproducible and honestly disclosed, and still measure something other than what the reader assumes. The author calls the genre "benchmaxxing" (the essay also uses the older word "benchmarketing"). The mechanism is always the same: pick the operation your change helps most, measure it in isolation, put that number in the title, and leave the system-level number deep in the text.

The topic is database and data infrastructure benchmarks. It is not about AI model benchmarks.

## The cases

| Case | What the author says | The mechanism |
|---|---|---|
| Databricks "Reyden" (June keynote) | Claimed up to 16x better than existing real-time serving stacks, with a live demo where a competitor crashed. No hardware, cluster size, cache state or config was disclosed. A ClickHouse engineer could not reproduce the crash from the only named detail (TPC-H, SF1, Q6). A Snowflake engineer reconfigured the comparison and reported 12.5 s vs 13.2 s at 100 GB and 28.2 s vs 71 s at 1 TB. | Undisclosed environment. A benchmark nobody can rerun is a claim taken on faith. |
| WarpStream "40x" | The 40x is create plus write plus close in isolation (80 to 100 ms down to 2 to 3 ms). The production cluster figure in the same post is 2 to 3 times faster than regional GCS. The faster storage tier costs over 10x more per GiB. | Isolated operation in the title, system-level number in the text. |
| Spotify RAP | O(1) describes the lookup, not the read. Per the post, it reads the whole page containing the row (potentially 4 MB to get 100 bytes). Much of the design is about arranging data at write time so that O(1) pays off. | A true property that hides a cost. |
| ClickBench cold runs | Repeats a QuestDB critique: the harness clears the page cache and restarts a self-hosted database between cold runs, but cannot restart a managed service, so its three "cold" runs hit the same live server. The cold ranking then reflects who the harness can restart, not architecture. | The experiment's own conditions favor one side. |

## Other points

- **Benchmarketing is old.** The author cites a piece tracing hidden hardware, unrealistic scenarios, hidden costs and test-specific tuning back to Oracle and Sybase in the early 1980s.
- **The DeWitt clause.** Many licenses restrict publishing independent benchmarks without vendor approval. The author quotes SQL Server's license and says Oracle's has a similar term. The consequence: vendor benchmarks can be the most accessible, and sometimes the only legally publishable ones.
- **Honest and useless.** The author's point is that disclosure does not make a number useful. A figure that is true for the headline scenario can fit none of the readers' systems.
- **Real cost of a headline.** People size clusters and justify migrations from a multiplier measured on a very different configuration (for example 32 cores per node versus the 4 they actually run). Almost nobody publishes the null result ("it came out to 8%, which does not pay for a migration"), because nobody is promoted for it.
- **The author's rule.** When you see a multiplier in a title, find the configuration. It is in the text, never in the title.

## What this means for this repo

This section is my reading, not the author's.

1. **Report system-level and isolated numbers together.** The headline must be the end-to-end figure, and an isolated-operation number is secondary and labeled as such. This fits the per-stage timing (read, process, write) planned in the framing study.
2. **Name the scenario and publish the configuration** so a reader can rerun it. The checklist already requires this (step 7, [checklist.md](../checklist.md)). The Reyden case is the failure it prevents.
3. **Cold runs need a fairness check.** Report a cold-cache result only when the harness can reset the engine and the cache the same way for every system. Otherwise report hot runs only and say so. This matters when comparing embedded engines (easy to restart) with managed or long-running services.
4. **Test at the size the reader runs.** The framing study proposes one large single node (about 32 vCPU). The "4 cores versus 32" point suggests also reporting a small node, or stating that results do not transfer to small deployments.
5. **Publish null results.** Repo rule 5 ("if a result is not distinguishable from noise, say so") already covers this.
6. **Check engine licenses before publishing** comparisons. The DeWitt clause is mostly a commercial-database issue, and the licenses of the engines in this repo's studies have not been checked.

See also [statistics.md](../statistics.md) for why a single fastest run is not a result.

## To verify before citing

- The Databricks, Snowflake, WarpStream and Spotify claims, against the primary posts.
- The ClickBench cold-run skew, against the QuestDB original (listed in [../references.md](../references.md)).
- The DeWitt clause quotations and license terms, against the current license texts.
