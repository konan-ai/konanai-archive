# Contribution Guidelines

We appreciate your interest in contributing to our project. Corporate contributors play an integral role in enhancing and growing our software, and we greatly value your expertise and perspective. The following document details the procedures and expectations for contributing to our project.

## Code Repository

Our codebase is hosted on GitHub, which also serves as our primary platform for issue tracking, feature requests, and code contributions via pull requests.

## Code Contributions and Pull Requests

The project follows the [GitHub Flow](https://guides.github.com/introduction/flow/index.html) workflow. We kindly request all codebase modifications be submitted through pull requests:

1. Initiate the process by forking the repository and creating a new branch from `master`.
2. If your modifications include code changes that warrant testing, please include appropriate tests.
3. If your changes involve modifications to APIs, please ensure corresponding documentation is updated.
4. Verify that all existing tests in the test suite pass with your modifications.
5. Ensure your code is in compliance with our linting guidelines.
6. Once the above steps have been completed, submit your pull request for review.

## Licensing

Please note that all contributions to this project are accepted under the terms of the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0). If you have any concerns regarding this, please contact the project maintainers.

## Developer Certificate of Origin

It is required that all contributors adhere to the Developer Certificate of Origin (DCO). The DCO is a declaration that you have the legal right to make the contribution under the project's license, and you agree to do so under the terms of the DCO. 

The full text of the DCO is available at [developercertificate.org](https://developercertificate.org/).

To indicate your agreement to the DCO terms, sign-off your commit using the `git commit -s` command. This appends a Signed-off-by line, with the author's name and email, to your commit message.

For example:

```
Signed-off-by: Jane Smith <jane.smith@email.com>
```

The sign-off confirms that the submitted work complies with the DCO requirements.

## Reporting Bugs

Bug tracking is conducted through GitHub's issue tracking feature. Report bugs by [opening a new issue](https://github.com/konan-ai/konanai/issues).

When filing an issue, please provide a concise description of the issue, relevant background information, and if possible, steps to reproduce the issue. Including sample code that demonstrates the problem can greatly facilitate the process.

## Coding Style

Contributions must adhere to the [PEP 8](https://pep8.org/), the official style guide for Python code. 

Please note the following:

* Indentation should consist of 4 spaces.
* Please use a linting tool such as pylint or flake8 to ensure PEP 8 compliance before submitting your pull request.

By making a contribution, you certify that your contribution is under the same [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0) that covers the project.
