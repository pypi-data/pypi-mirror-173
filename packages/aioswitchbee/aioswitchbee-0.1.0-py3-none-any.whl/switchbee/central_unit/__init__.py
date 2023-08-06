from __future__ import annotations
from dataclasses import dataclass

import socket
import json
import asyncio
from asyncio import get_running_loop, BaseTransport
from socket import AF_INET

from logging import getLogger
from types import TracebackType
from typing import Any, Callable, Optional, Type


logger = getLogger(__name__)


PORT = 8872


@dataclass
class CentralUnit:
    """Central Unit data class."""

    version: str
    name: str
    mac: str
    port: int
    switches: int
    ip_address: str


class UdpClientProtocol:
    def __init__(self, on_datagram: Callable[[CentralUnit], Any]):
        self.message = "FIND"
        self.transport = None
        self._on_datagram = on_datagram

    def connection_made(self, transport: BaseTransport):
        self.transport = transport
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast()

    def datagram_received(self, data, addr):
        logger.debug("Received:", data.decode())
        if data:
            json_data = json.loads(data.decode())
            json_data["internalIp"] = addr[0]
            self._on_datagram(
                CentralUnit(
                    json_data["CUVersion"],
                    json_data["name"],
                    json_data["mac"],
                    json_data["port"],
                    json_data["switches"],
                    addr[0],
                )
            )

    def error_received(self, exc):
        logger.error("Error received:", exc)

    def broadcast(self):
        logger.debug("sending:", self.message)
        self.transport.sendto(self.message.encode(), ("255.255.255.255", PORT))

    def connection_lost(self, exc: Optional[Exception]):
        if exc:
            logger.critical(f"udp bridge lost its connection {exc}")
        else:
            logger.info("udp connection stopped")


class CUFinder:
    def __init__(
        self,
        on_device: Callable[[CentralUnit], Any],
    ) -> None:
        self._on_device = on_device
        self._central_units: dict[str, Any] = {}
        self._transport = None
        self._is_running = False

    async def __aenter__(self) -> "CUFinder":
        """Enter CUFinder asynchronous context manager."""
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the CUFinder asynchronous context manager."""
        await self.stop()

    async def start(self) -> None:
        """Create an asynchronous listener and start the bridge."""

        logger.info("starting the udp bridge on port %s", PORT)

        transport, protocol = await get_running_loop().create_datagram_endpoint(
            lambda: UdpClientProtocol(self._on_device),
            family=AF_INET,
        )
        self._transport = transport
        logger.debug("udp bridge on port %s started", PORT)

        self._is_running = True

    async def stop(self) -> None:
        """Stop the asynchronous bridge."""

        if self._transport and not self._transport.is_closing():
            logger.info("stopping the udp bridge on port %s", PORT)
            self._transport.close()
        else:
            logger.info("udp bridge on port %s not started", PORT)

        self._is_running = False


def on_device_found_callback(device: CentralUnit) -> None:
    """Use as a callback printing found devices."""
    print(device)


async def discover():
    async with CUFinder(on_device_found_callback):
        await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(discover())
