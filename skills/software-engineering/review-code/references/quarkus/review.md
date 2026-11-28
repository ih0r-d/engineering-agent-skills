# Quarkus review criteria

- Confirm the Quarkus platform and relevant extension versions. Trace changed REST code through the actual event-loop or worker dispatch and check whether blocking work can delay other requests.
- Check bean discovery, qualifiers and scope for the changed injection path. Verify configuration and deployment profiles where a build-time decision could differ from runtime configuration.
- Check the failing or proposed behavior through the configured Quarkus entrypoint. A successful local development run leaves production profile and native-mode behavior unverified.
