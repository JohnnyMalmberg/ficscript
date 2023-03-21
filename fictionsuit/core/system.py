from utils import make_stats_str
import openai
import config
from typing import Sequence
from abc import ABC, abstractmethod
from api_wrap.user_message import UserMessage
from commands.command_group import CommandGroup, command_split
from core.core import chat_message, get_openai_response

class System(ABC):
    '''A system for handling incoming user messages.'''
    @abstractmethod
    async def enqueue_message(self, message: UserMessage):
        '''Called whenever a new user message arrives.'''
        pass

class BasicCommandSystem(System):
    def __init__(
        self, 
        command_groups: Sequence[CommandGroup], 
        stats_ui: bool = True,
        respond_on_unrecognized: bool = False
        ):
        self.command_groups = command_groups
        self.stats_ui = stats_ui
        self.respond_on_unrecognized = respond_on_unrecognized

        all_commands = [command for group in command_groups for command in group.get_all_commands()]

        if len(all_commands) != len(set(all_commands)):
            # TODO: Print out more useful information, like where the name collision actually is.
            print(f'{"!"*20}\n\nWARNING: MULTIPLE COMMANDS WITH OVERLAPPING COMMAND NAMES\n\n{"!"*20}')

    async def enqueue_message(self, message: UserMessage):
        if not message.has_prefix(config.COMMAND_PREFIX):
            return # Not handling non-command messages, for now

        (cmd, args) = command_split(message.content, config.COMMAND_PREFIX)

        if cmd is None:
            return # Nothing but a prefix. Nothing to do.

        for group in self.command_groups:
            if await group.handle(message, cmd, args):
                return

        if cmd == 'help':
            await message.reply(f'Sorry, there\'s no command called "{args}".')
            return

        if self.respond_on_unrecognized:
            await self.direct_chat(message)

    async def direct_chat(self, message: UserMessage):
        messages = chat_message('system', config.SYSTEM_MSG)
        messages += chat_message('user', message.content)
        res = await get_openai_response(messages)
        content = res['choices'][0]['message']['content']
        content = make_stats_str(content, messages, 'chat') if self.stats_ui else content
        await message.reply(content)

