from dataclasses import dataclass
from typing import List


from origin.models.auth import InternalToken
from origin.tokens import TokenEncoder
from origin.serialize import Serializable
import uuid
from datetime import datetime, timezone, timedelta

from origin.api import (
    Endpoint, Context,
)

token_encoder = TokenEncoder(
    schema=InternalToken,
    secret='123',
)


token = InternalToken(
    issued=datetime.now(tz=timezone.utc),
    expires=datetime.now(timezone.utc) + timedelta(hours=24),
    actor='foo',
    subject='bar',
    scope=['meteringpoints.read'],
)

opaque_token = token_encoder.encode(token)


@dataclass
class FakeMeteringPoint(Serializable):
    """Class to store the parameters for the metering point."""

    gsrn: str


class FakeGetMeteringPointList(Endpoint):
    """Look up many Measurements, optionally filtered and ordered."""

    @dataclass
    class Response:
        """TODO."""

        meteringpoints: List[FakeMeteringPoint]

    def handle_request(
            self,
    ) -> Response:
        """Handle HTTP request."""

        fake_meteringpoint_list = [
            FakeMeteringPoint(gsrn=str(uuid.uuid1())[:18]),
            FakeMeteringPoint(gsrn=str(uuid.uuid1())[:18]),
            FakeMeteringPoint(gsrn=str(uuid.uuid1())[:18]),
        ]

        return self.Response(
            meteringpoints=fake_meteringpoint_list,
        )


class FakeToken(Endpoint):
    """Look up many Measurements, optionally filtered and ordered."""

    @dataclass
    class Request:
        """TODO."""

        token: str

    def handle_request(
            self,
    ) -> Request:
        """Handle HTTP request."""

        return self.Request(
            token=opaque_token,
        )
