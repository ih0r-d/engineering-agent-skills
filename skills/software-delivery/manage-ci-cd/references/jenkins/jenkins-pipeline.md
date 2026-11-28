# Jenkins Pipeline review

Load when a `Jenkinsfile`, shared library, or Jenkins controller/agent behavior is in scope. Confirm installed Pipeline plugins, controller policy, agent images, and credential providers; available steps and syntax depend on that environment.

- Identify Declarative versus Scripted Pipeline and trace stages, `when`, agents, parameters, environment, options, and post conditions. A stage-level agent changes where its steps execute; inspect workspace and tool availability at each agent boundary.
- Review `post` conditions for cleanup, report publication, and notification behavior. Cleanup must not hide the original build failure or publish an artifact after a failed gate.
- Inspect `stash`/`unstash`, archived artifacts, and external artifact storage. Verify artifact identity and retention across agents; a workspace file is not automatically available on another agent.
- Bind credentials only around the steps that need them. Avoid printing bound environment values, interpolating secrets into Groovy strings or command arguments, and exposing credentials to jobs that execute untrusted branches.
- Treat parameters and SCM content as untrusted. Review shared libraries and script approvals because they can execute with controller or agent privileges beyond a single stage.
- Check retry and timeout placement: retrying a whole stage can repeat side effects, while retrying a pure test step may be safe. Preserve failure propagation and distinguish unstable results from successful quality gates according to project policy.
- Validate the Jenkinsfile with the repository's configured linter or a disposable controller when available. Local parsing cannot prove plugin availability, credential binding, agent labels, or hosted authorization.

Sources: [Jenkins Pipeline syntax](https://www.jenkins.io/doc/book/pipeline/syntax/), [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/), [Credentials binding](https://www.jenkins.io/doc/pipeline/steps/credentials-binding/)
