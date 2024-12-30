from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core import Game

from src.core.util.debug.debugger import Debug
from src.core.util.debug.logger import Log
from src.core.util.timer import LoopTimer
from src.core.util import ref_proxy
from .snapshot import Snapshot
from typing import Optional
from .frame import Frame

class Replayer:
    _start_time = 0.0 # The time the replayer was started
    _time = 0.0 # Amount of time spent in the replay scene

    def __init__(self, game: Game) -> None:
        self.game = ref_proxy(game)
        self.frames: dict[int, Frame] = {}
        self.newest_frame = 0

        self.snapshot_timer = LoopTimer(5)
        self.snapshot_timer.force_end()

    @Debug.requires_debug()
    def record(self) -> None:
        snapshot = None
        if self.snapshot_timer.done:
            snapshot = Snapshot(self, self.game.timestamp)
        self.frames[self.game.timestamp] = Frame(self, snapshot, self.game.timestamp)
        self.newest_frame = self.game.timestamp

    def replay(self) -> None:
        self.game.replaying = True
        self.game.new_scene("Replay", self.game.timestamp)

    def get_frame(self, timestamp: int) -> Frame:
        return self.frames[timestamp]

    def get_snapshot(self, timestamp: int) -> Optional[Snapshot]:
        return self.frames[timestamp].snapshot

    def __getstate__(self) -> dict:
        # Do not include the replayer in any pickle
        return {}
