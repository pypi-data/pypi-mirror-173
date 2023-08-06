__all__ = ('Button', 'ButtonStyle', 'Form', 'Option', 'Row', 'Select', 'TextInput', 'TextInputStyle')

from ...discord.component import (
    ButtonStyle, create_button as Button, create_row as Row, create_string_select as Select,
    StringSelectOption as Option, create_text_input as TextInput, InteractionForm as Form, TextInputStyle
)
from ...discord.core import APPLICATION_ID_TO_CLIENT
from ...discord.exceptions import DiscordException, ERROR_CODES


async def acknowledge_component_interaction(interaction_event):
    """
    Acknowledges the given `interaction_event`. If error occurs, calls `client.events.error`.
    
    This function is a coroutine.
    
    Parameter
    ---------
    interaction_event : ``InteractionEvent``
        The component interaction event to acknowledge.
    """
    try:
        client = APPLICATION_ID_TO_CLIENT[interaction_event.application_id]
    except KeyError:
        return
        
    try:
        await client.interaction_component_acknowledge(interaction_event)
    except GeneratorExit:
        raise
    
    except BaseException as err:
        if isinstance(err, ConnectionError):
            # No Internet connection
            return
        
        if isinstance(err, DiscordException) and (err.code == ERROR_CODES.unknown_interaction):
            # We timed out, bad connection.
            return
        
        await client.events.error(client, f'acknowledge_component_interaction', err)
