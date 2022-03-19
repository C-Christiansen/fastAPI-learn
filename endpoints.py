from typing import List, Optional

from origin.api import Endpoint
from dataclasses import dataclass, field


class TestEndpoint(Endpoint):
    """Look up many Measurements, optionally filtered and ordered."""

    @dataclass
    class Response:
        """TODO."""

        success: bool

    async def handle_request(
        self,
        name: str,
    ) -> Response:
        """Handle HTTP request."""

        return TestEndpoint.Response(success=True)
