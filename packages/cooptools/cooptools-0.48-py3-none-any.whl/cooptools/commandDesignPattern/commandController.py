from dataclasses import dataclass, field
from cooptools.commandDesignPattern.commandProtocol import CommandProtocol
from cooptools.commandDesignPattern.exceptions import ResolveStateException
from typing import List, Any, Tuple

@dataclass
class CommandController:
    init_state: Any
    command_stack: List[CommandProtocol] = field(default_factory=list)
    cache_interval: int = 100
    _cached_states: List[Tuple[Any, int]] = field(default_factory=list, init=False)
    cursor: int = field(default=-1, init=False)

    def __post_init__(self):
        self._cache_state(self.init_state)

    def _cache_state(self, state):
        self._cached_states.append((state, self.cursor))



    def execute(self, commands: List[CommandProtocol]) -> Any:
        # delete any registered commands after the current cursor
        del self.command_stack[self.cursor + 1:]

        # delete any cached states after the current cursor
        for ii, cache in [(ii, x) for ii, x in enumerate(self._cached_states) if x[1] > self.cursor]:
            del self._cached_states[ii]

        # add new commands
        for command in commands:
            self.command_stack.append(command)
            self.cursor += 1

        # resolve
        latest_state = self.resolve()

        # determine to cache
        if self.cursor - self._cached_states[-1][1] > self.cache_interval:
            self._cache_state(latest_state)

        return latest_state

    def resolve(self, idx: int = None) -> None:
        command = None

        if idx is None:
            idx = self.cursor

        if idx == -1:
            return self.init_state

        try:
            state, cached_idx = next(iter(reversed([(x, cached_idx) for x, cached_idx in self._cached_states if cached_idx < idx])))
            # execute the commands in the stack up to the cursor
            for command in self.command_stack[cached_idx + 1:idx + 1]:
                state = command.execute(state)
            return state
        except Exception as e:
            # raise the exception on the command that failed
            raise ResolveStateException(command=command, inner=e)

    def undo(self):
        # move cursor back in time
        if self.cursor > -1:
            self.cursor -= 1

        return self.resolve()

    def redo(self):
        # move cursor forward in time
        if self.cursor < len(self.command_stack):
            self.cursor += 1

        return self.resolve()

    @property
    def CachedStates(self):
        return self._cached_states

    @property
    def ActiveCommands(self):
        return self.command_stack[:self.cursor + 1]