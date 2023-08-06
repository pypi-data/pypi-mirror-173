# Qotto Auth Client

The python package `qotto-auth-client` is a client for the API `qotto-auth` which will soon be open sourced.

It allows to manage a scoped permission and authentication system.

More information coming soon...

## Quickstart

The `QottoAuthApi` class allows to interact with a `qotto-auth` GraphQL server.

```python
from qottoauth import (
    QottoAuthService,
    QottoAuthApi,
    QottoAuthGrapheneApi,
    QottoAuthTestApi,
)

# Create a QottoAuthApi instance
api: QottoAuthApi
if TEST:
    # for offline testing
    api = QottoAuthTestApi()
else:
    # qotto-auth server running
    api = QottoAuthGrapheneApi(
        url=QOTTO_AUTH_URL,
    )

# Create a QottoAuthService instance
service = QottoAuthService(
    api=api,
)

# Register this application
service.register_application(
    application_name=APPLICATION_NAME,
    application_description=APPLICATION_DESCRIPTION,
)

# ...
```

You can extend the `QottoAuthService` class to add your own business logic.

In the current version (1.0.1), `QottoAuthTestApi` does not provide all queries and mutations, so you might need to
extend the class if you need to test beahviour depending on these queries and mutations.