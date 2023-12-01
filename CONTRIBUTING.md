# Contributing to Genie

Thank you for your interest in contributing to Genie! All contributions are welcome no
matter how big or small. This includes (but is not limited to) filing issues,
adding documentation, fixing bugs, creating examples, and implementing features.

## Finding issues to work on

If you're looking to get started,
check out issues and readme
For simple documentation changes or typos, feel free to just open a pull request.

If you're considering larger changes or self motivated features, please contact [contact](mailto:ziinxed@gmail.com)

## Choosing an issue

If you'd like to contribute, please claim an issue by commenting, forking, and
opening a pull request, even if empty. This allows the maintainers to track who
is working on what issue as to not overlap work.

## Issue Guidelines

Please follow these guidelines:

Before coding:

- choose a branch name that describes the issue you're working on
- enable [commit signing](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)

While coding:

- Submit a draft PR asap
- Only change code directly relevant to your PR. Sometimes you might find some code that could really need some refactoring. However, if it's not relevant to your PR, do not touch it. File an issue instead. This allows the reviewer to focus on a single problem at a time.
- If you write comments, do not exceed 80 chars per line. This allows contributors who work with multiple open windows to still read the comments without horizontally scrolling.
- Write adversarial tests. For example, if you're adding a new account type, do not only write tests where the instruction succeeds. Also write tests that test whether the instruction fails, if a check inside the new type is violated.
