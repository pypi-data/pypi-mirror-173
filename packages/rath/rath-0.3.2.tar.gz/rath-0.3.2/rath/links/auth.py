from typing import AsyncIterator, Awaitable, Callable, Optional

from pydantic import Field
from rath.links.base import ContinuationLink
from rath.operation import GraphQLResult, Operation
from rath.links.errors import AuthenticationError


async def fake_loader():
    raise Exception("No Token loader specified")


class AuthTokenLink(ContinuationLink):

    token_loader: Callable[[], Awaitable[str]]
    token_refresher: Optional[Callable[[], Awaitable[str]]]

    maximum_refresh_attempts: int = 3
    load_token_on_connect: bool = True
    load_token_on_enter: bool = True

    _token: str = None

    async def aconnect(self):
        if self.load_token_on_connect:
            await self.token_loader()

    async def aexecute(
        self, operation: Operation, retry=0, **kwargs
    ) -> AsyncIterator[GraphQLResult]:

        operation.context.headers[
            "Authorization"
        ] = f"Bearer {await self.token_loader()}"
        try:

            async for result in self.next.aexecute(operation, **kwargs):
                yield result

        except AuthenticationError as e:
            retry = retry + 1
            operation.context.headers[
                "Authorization"
            ] = f"Bearer {await self.token_refresher()}"
            if retry > self.maximum_refresh_attempts:
                raise AuthenticationError("Maximum refresh attempts reached") from e

            async for result in self.aexecute(operation, retry=retry + 1, **kwargs):
                yield result

    class Config:
        underscore_attrs_are_private = True
        arbitary_types_allowed = True
