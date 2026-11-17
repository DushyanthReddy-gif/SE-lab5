\# Static Code Analysis – Issue Table



\## Bandit Issues



| ID | Issue | Severity | Fix Applied |

|---|---|---|---|

| B413 | Deprecated `Crypto.Cipher.AES` usage | High | Replaced deprecated PyCrypto AES usage with `cryptography` AES implementation. |

| B105 | Hardcoded webhook secret | Low | Changed the webhook secret to be loaded from an environment variable. |

| B311 | Use of `random.choice()` for security-sensitive random generation | Low | Replaced `random.choice()` with `secrets.choice()`. |

| B101 | Use of `assert` in application code | Low | Removed the `assert` and replaced it with explicit validation. |

| B702 | Mako templates allow HTML/JS rendering | Medium | Removed Mako template rendering and used explicit HTML escaping with `html.escape()`. |

| B305 | Use of insecure AES ECB mode | Medium | Replaced ECB with AES-CBC using a randomly generated IV. |



\*\*Final Bandit result:\*\* 0 issues identified.



\## Flake8 Issues



| Issue | Description | Fix Applied |

|---|---|---|

| F401 | Unused imports | Removed unused imports. |

| E401 | Multiple imports on one line | Separated imports. |

| E302/E303 | Incorrect blank-line formatting | Corrected blank-line spacing. |

| E501 | Lines exceeding the recommended length | Reformatted long lines. |

| E711 | Comparison with `None` using `==` | Replaced with `is None`. |

| W292 | No newline at end of file | Added a newline at the end of the source file. |



\*\*Final Flake8 result:\*\* 0 issues identified.



\## Pylint Issues



| Issue | Description | Fix Applied |

|---|---|---|

| Missing module docstring | Module did not contain a module-level docstring | Added a module docstring. |

| Missing function docstrings | Functions lacked documentation | Added docstrings to functions. |

| Naming convention issues | CamelCase function/variable names | Renamed identifiers using snake\_case. |

| Unused imports | `os` and `sys` were unused | Removed unused imports. |

| `dict()` / `list()` suggestions | Unnecessary constructor usage | Replaced with appropriate literals. |

| `== None` | Incorrect comparison with `None` | Changed to `is None`. |

| Return in `finally` | Return statement could suppress exceptions | Reworked the control flow. |

| Lost exception | Exception could be unintentionally suppressed | Corrected exception handling. |

| Refund calculation issue | Incorrect refund calculation | Corrected refund logic. |

| Long lines | Lines exceeded recommended length | Reformatted the affected lines. |

| Naming issues | Non-standard identifier naming | Converted identifiers to snake\_case. |



\*\*Initial Pylint score:\*\* 4.43/10  

\*\*Final Pylint score:\*\* 10.00/10



The remaining `I1101` message concerning `lxml.etree` is informational and does not reduce the Pylint score.

