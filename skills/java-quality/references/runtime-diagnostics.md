# JVM runtime and memory diagnostics

Load for heap growth, long pauses, thread starvation, class-loader retention, or memory errors. First record the exact JDK vendor/version, JVM flags, container limits, workload, and whether the symptom reproduces after restart.

## Memory boundaries

- Distinguish Java heap from native memory. Metaspace stores class metadata; direct buffers, thread stacks, code cache, JNI, and native libraries also consume process memory. A rising process RSS with a stable heap requires native-memory investigation, not only heap tuning.
- A memory leak is reachable retained state that grows beyond the intended lifetime. GC activity alone is not evidence of a leak. Compare retained object paths and dominators across equivalent snapshots.
- Check class-loader ownership in plugin or redeploy environments. Static registries, thread locals, executor threads, and callbacks can retain an application loader after undeploy.
- Diagnose GC before tuning: correlate allocation rate, live set after collection, pause distribution, throughput, and allocation sites. Do not select a collector or heap size from a single pause or generic rule.

## Focused evidence

- `jcmd <pid> VM.version`, `VM.flags`, and `VM.command_line` establish runtime configuration.
- `jcmd <pid> GC.heap_info` and `GC.class_histogram` give snapshots; inspect production impact before requesting expensive operations.
- `jcmd <pid> JFR.start` / `JFR.dump` can capture allocation, lock, and thread evidence when recording options and storage are approved.
- Thread dumps identify blocked, waiting, and runnable stacks. Compare repeated dumps to distinguish a stuck thread from normal waiting.
- Heap dumps can contain secrets and personal data. Obtain authorization, protect the file, limit transfer, and use a disposable analysis environment.
- For native memory, use Native Memory Tracking only when enabled at startup; it cannot account for every native allocation.

Reproduce with the same JDK, flags, container limits, and representative workload. For microbenchmarks use JMH with warmup, forks, and realistic inputs; do not infer application throughput from a hand-timed loop.

Sources: [JDK 21 GC tuning](https://docs.oracle.com/en/java/javase/21/gctuning/), [jcmd reference](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html), [JFR guide](https://docs.oracle.com/en/java/javase/21/jfapi/).
