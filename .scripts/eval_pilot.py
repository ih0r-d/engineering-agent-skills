"""Offline scenario selection and deterministic graders for pilot fixtures."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import shutil

import evaluation_cases

PILOT = evaluation_cases.ROOT / "evals/pilot"


@dataclass(frozen=True)
class Scenario:
    id: str
    prompt: str
    fixture: Path
    skill: str
    mode: str
    technology: str
    references: tuple[str, ...]
    expected: tuple[str, ...]
    avoided_skills: tuple[str, ...] = ()
    editable: str | None = None


def scenarios() -> dict[str, Scenario]:
    cases = {case["id"]: case for case in evaluation_cases.load_cases()}

    def existing(identifier, mode, technology, references=(), *, fixture=None, editable=None):
        case = cases[identifier]
        return Scenario(identifier, case["prompt"], fixture or evaluation_cases.FIXTURES / case["fixture"],
                        case["skill"], mode, technology, references, tuple(case["expected"]),
                        tuple(case["avoid_skills"]), editable)

    selected = [
        Scenario(
            "java-feature", "In Labels.java, add a public static label(String name, String fallback) overload. "
            "Return fallback exactly as supplied when name is null or trims to empty. Otherwise return the "
            "trimmed name. Preserve the existing one-argument method, including its null behavior. "
            "Use Java 11 and change only Labels.java.",
            PILOT / "java-feature", "implement", "feature implementation", "Java 11",
            ("java/type-contracts.md",),
            ("Add the overload and handle null, blank, and nonblank names.",
             "Preserve the existing public method and its behavior on Java 11."),
            editable="Labels.java",
        ),
        existing("code-review-near-miss-python-fix", "authorized fix", "Python",
                 ("python/state-ownership.md",), editable="tags.py"),
        existing("code-review-selection-regression", "read-only code review", "Python",
                 ("python/quality-rubric.md",)),
        existing("shell-quality-trap-status", "read-only diagnosis", "POSIX sh",
                 ("shell/process-lifecycle.md",), fixture=PILOT / "shell-status"),
        existing("make-recipe-directory", "read-only build review", "GNU Make",
                 ("make/make.md",)),
        existing("review-code-unsupported-language", "read-only generic review", "Go 1.22",
                 fixture=evaluation_cases.FIXTURES / "java"),
    ]
    return {scenario.id: scenario for scenario in selected}


JAVA_PROBE = """public class Probe {
    public static void main(String[] args) throws Exception {
        if (args[0].equals("feature")) {
            java.lang.reflect.Method label = Labels.class.getMethod("label", String.class, String.class);
            require(" (none) ".equals(label.invoke(null, null, " (none) ")));
            require("blank".equals(label.invoke(null, "\\t  ", "blank")));
            require("Ada".equals(label.invoke(null, " Ada ", "other")));
            require(label.invoke(null, "", null) == null);
        } else {
            require("Ada".equals(Labels.label(" Ada ")));
            require("".equals(Labels.label("\\t ")));
            boolean rejected = false;
            try { Labels.label(null); } catch (NullPointerException expected) { rejected = true; }
            require(rejected);
        }
        System.out.println("probe-complete");
    }
    static void require(boolean ok) {
        if (!ok) throw new AssertionError("label contract failed");
    }
}
"""

PYTHON_PROBE = """import runpy
import sys
namespace = runpy.run_path("tags.py")
add_tag = namespace["add_tag"]
if sys.argv[1] == "feature":
    first = add_tag("one")
    second = add_tag("two")
    assert first == ["one"] and second == ["two"] and first is not second
else:
    for explicit in ([], ["original"]):
        original = explicit.copy()
        assert add_tag("one", explicit) is explicit
        assert explicit == original + ["one"]
    existing = []
    assert namespace["add_to_explicit_list"]("one", existing) is None
    assert existing == ["one"]
print("probe-complete")
"""


def grade_behavior(scenario: Scenario, workspace: Path, grading: Path, execute) -> list[dict]:
    """Copy the expected source and use the caller's isolated probe executor."""
    if not scenario.editable:
        return []
    artifact = workspace / scenario.editable
    if artifact.is_symlink() or not artifact.is_file():
        return [{"name": "required source artifact", "status": "failed"}]
    shutil.copyfile(artifact, grading / scenario.editable)
    results = [{"name": "required source artifact", "status": "passed"}]
    if scenario.editable == "Labels.java":
        (grading / "Probe.java").write_text(JAVA_PROBE, encoding="utf-8")
        result = execute("Java 11 compilation", ["javac", "-proc:none", "--release", "11", "Labels.java", "Probe.java"])
        results.append(result)
        if result["status"] != "passed":
            results.extend({"name": name, "status": "unavailable"} for name in
                           ("requested behavior", "existing behavior regression"))
            return results
        command = ["java", "-cp", ".", "Probe"]
    else:
        command = ["python3", "-I", "-B", "-c", PYTHON_PROBE]
    for kind, label in (("feature", "requested behavior"), ("regression", "existing behavior regression")):
        results.append(execute(label, [*command, kind], expected_output="probe-complete"))
    return results


def main(argv: list[str] | None = None) -> int:
    available = scenarios()
    parser = argparse.ArgumentParser(description="List pilot scenarios for optional manual A/B comparisons.")
    parser.add_argument("--scenario", action="append", choices=available, help="Select a case (repeat to select several)")
    parser.add_argument("--details", action="store_true", help="Print the exact prompt for each selected case")
    args = parser.parse_args(argv)
    selected = args.scenario or list(available)
    if len(selected) != len(set(selected)):
        parser.error("select each scenario at most once")

    label = "comparison" if len(selected) == 1 else "comparisons"
    print(f"Manual A/B plan: {len(selected)} {label} ({2 * len(selected)} separate sessions)")
    for identifier in selected:
        case = available[identifier]
        print(f"  {case.id} — {case.fixture.relative_to(evaluation_cases.ROOT)}")
        if args.details:
            print(f"    Prompt: {case.prompt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
