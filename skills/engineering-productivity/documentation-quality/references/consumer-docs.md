# Consumer documentation

## Choose a reader journey

- README or overview. Explain what the project does, who should use it and the shortest useful next step. Link to installation, configuration and contributor material when those journeys grow. Keep capability statements tied to supported releases.
- Quick start. Start from the reader's actual prerequisites and working directory. Give one tested path from installation to an observable success, such as an exit code, expected output or created artifact. Explicitly name any values the reader must supply. Use demo inputs, with prerequisites and cleanup close to the commands that need them.
- How-to and troubleshooting guide. Name the outcome and preconditions, show the supported steps, and describe observable failure symptoms and fixes. Include upgrade or data migration steps when relevant. Link to a configuration reference for complete option lists.

## Verify claims

Check versions and prerequisites against CI and package metadata, and command names, flags, output and defaults against the CLI or tests. A config file example should match both schema and actual path resolution. Execute safe snippets from the stated directory using disposable files, installed artifacts where relevant, and synthetic credentials. Verify relative files and anchors through the docs renderer configured by the project when possible. Check remote links only when network access is available and in scope.

A quick start that invokes a command absent from the installed artifact is a user-visible defect. A release-specific prerequisite repeated where a page must stand alone can be appropriate. Put advanced behavior in a dedicated section or guide that can be maintained alongside the canonical contract.
