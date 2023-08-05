import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, AsyncIterable, Awaitable, Callable, Dict

from dateutil.parser import isoparse
from kilroy_server_py_utils import Configurable, Parameter, classproperty

from cilroy.models import SerializableState
from cilroy.scoring import ScoreScheduler
from cilroy.utils import next_time, seconds_until, utcmidnight


class State(SerializableState):
    base: datetime = utcmidnight()
    interval: timedelta = timedelta(days=1)


class IntervalScoreScheduler(ScoreScheduler, Configurable[State]):
    class BaseParameter(Parameter[State, str]):
        async def _get(self, state: State) -> str:
            return state.base.isoformat().replace("+00:00", "Z")

        async def _set(
            self, state: State, value: str
        ) -> Callable[[], Awaitable]:
            original_value = state.base

            async def undo():
                state.base = original_value

            state.base = isoparse(value)
            return undo

        @classproperty
        def schema(cls) -> Dict[str, Any]:
            return {
                "type": "string",
                "format": "date-time",
                "title": cls.pretty_name,
                "default": utcmidnight().isoformat().replace("+00:00", "Z"),
            }

    class IntervalParameter(Parameter[State, float]):
        async def _get(self, state: State) -> float:
            return state.interval.total_seconds()

        async def _set(
            self, state: State, value: float
        ) -> Callable[[], Awaitable]:
            original_value = state.interval

            async def undo():
                state.interval = original_value

            state.interval = timedelta(seconds=value)
            return undo

        @classproperty
        def schema(cls) -> Dict[str, Any]:
            return {
                "type": "number",
                "minimum": 0,
                "title": cls.pretty_name,
                "default": timedelta(days=1).total_seconds(),
            }

    @classmethod
    async def _save_state(cls, state: State, directory: Path) -> None:
        with open(directory / "state.json", "w") as f:
            f.write(state.json())

    async def _load_saved_state(self, directory: Path) -> State:
        with open(directory / "state.json", "r") as f:
            return State.parse_raw(f.read())

    async def wait(self) -> AsyncIterable[None]:
        while True:
            async with self.state.read_lock() as state:
                score_time = next_time(state.base, state.interval)

            await asyncio.sleep(seconds_until(score_time))
            yield
