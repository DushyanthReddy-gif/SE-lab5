\# Reflection – Static Code Analysis



\## 1. What did you learn from using Pylint, Bandit and Flake8?



The three tools helped identify different categories of problems in the Python program. Pylint focused mainly on code quality, naming conventions, documentation and possible programming issues. Flake8 identified formatting and style violations. Bandit focused on security-related problems such as insecure cryptographic practices, hardcoded secrets and unsafe template rendering.



Using all three tools together provided a more complete view of the quality and security of the code.



\## 2. Which tool was most useful and why?



Bandit was particularly useful because it identified security issues that may not be obvious during normal testing. For example, it detected the use of AES ECB mode, a hardcoded webhook secret, insecure random generation and unsafe Mako template usage.



Pylint was also useful because the initial score was only 4.43/10, which showed that there were several code-quality and maintainability issues.



\## 3. What was the impact of fixing the issues?



The code became cleaner, more consistent and more secure. The final Flake8 report contained no issues, while the final Bandit report reported no security issues. The Pylint score improved from 4.43/10 to 10.00/10.



The fixes also improved practices such as naming, documentation, exception handling, input escaping and cryptographic implementation.



\## 4. What security issues did you identify?



The main security issues identified by Bandit included deprecated cryptographic library usage, a hardcoded webhook secret, insecure random generation, use of `assert` for validation, unsafe Mako template rendering and insecure AES ECB mode.



These were addressed by using safer cryptographic APIs, environment-based secrets, the `secrets` module, explicit validation, HTML escaping and AES-CBC with a random IV.



\## 5. What would you do in a real software project?



In a real project, I would integrate Pylint, Flake8 and Bandit into the development workflow or CI/CD pipeline so that issues are detected automatically before code is merged.



I would also configure appropriate severity thresholds and maintain coding and security standards across the project rather than checking the code only before submission.

