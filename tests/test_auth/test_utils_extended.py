"""Extended tests for app.auth.utils – cover decode error path."""

from datetime import timedelta

import pytest
from jose import JWTError

from app.auth.utils import create_access_token, decode_access_token


class TestDecodeAccessToken:
    def test_invalid_token_raises(self) -> None:
        with pytest.raises(JWTError):
            decode_access_token("not.a.valid.token")

    def test_expired_token_raises(self) -> None:
        token = create_access_token(subject="u1", expires_delta=timedelta(seconds=-1))
        with pytest.raises(JWTError):
            decode_access_token(token)
