class MessageManager:
    reaction_events = dict()
    bot = None

    @classmethod
    def on_startup(cls, bot):
        cls.bot = bot

    @classmethod
    async def send_message(cls, medium, content):
        await medium.send(content)

    @classmethod
    async def edit_message(cls, message, content):
        try:
            if message in cls.bot.cached_messages:
                await message.edit(content=content)
            else:
                channel = await cls.bot.fetch_channel(message.channel.id)
                message = await channel.fetch_message(message.id)
                await message.edit(content=content)
        except Exception as e:
            await cls.bot.on_error(f"EDIT MESSAGE\n message_id: {message.id}\n channel_id: {message.channel.id}", e)

    @classmethod
    async def delete_message(cls, message):
        try:
            if message in cls.bot.cached_messages:
                await message.delete()
            else:
                channel = await cls.bot.fetch_channel(message.channel.id)
                message = await channel.fetch_message(message.id)
                await message.delete()
        except Exception as e:
            await cls.bot.on_error(f"DELETE MESSAGE\n message_id: {message.id}\n channel_id: {message.channel.id}", e)

    @classmethod
    async def add_reaction(cls, message, emoji):
        try:
            if message in cls.bot.cached_messages:
                await message.add_reaction(emoji)
            else:
                channel = await cls.bot.fetch_channel(message.channel.id)
                message = await channel.fetch_message(message.id)
                await message.add_reaction(emoji)
        except Exception as e:
            await cls.bot.on_error(f"ADD REACTION\n message_id: {message.id}\n channel_id: {message.channel.id}", e)

    @classmethod
    async def add_reaction_and_event(cls, message, emoji, user_id, handler, *args):
        cls.reaction_events[(message.id, emoji, user_id)] = (handler, args)
        await cls.add_reaction(message, emoji)

    @classmethod
    async def add_reaction_event(cls, message, emoji, user_id, handler, *args):
        cls.reaction_events[(message.id, emoji, user_id)] = (handler, args)

    @classmethod
    async def remove_reaction_event(cls, message_id, emoji, user_id):
        if (message_id, emoji, user_id) in cls.reaction_events.keys():
            cls.reaction_events.pop((message_id, emoji, user_id))

    @classmethod
    async def remove_reaction(cls, message, emoji, user):
        try:
            if message in cls.bot.cached_messages:
                await message.remove_reaction(emoji, user)
            else:
                channel = await cls.bot.fetch_channel(message.channel.id)
                message = await channel.fetch_message(message.id)
                await message.remove_reaction(emoji, user)
        except Exception as e:
            await cls.bot.on_error(f"REMOVE REACTION\n message_id: {message.id}\n channel_id: {message.channel.id}", e)

    @classmethod
    async def clear_reaction(cls, message, emoji):
        to_remove = []
        for (message_id, emoji_, user_id) in cls.reaction_events.keys():
            if message_id == message.id and emoji_ == emoji:
                to_remove.append((message_id, emoji_, user_id))
        for container in to_remove:
            cls.reaction_events.pop(container)

        try:
            if message in cls.bot.cached_messages:
                await message.clear_reaction(emoji)
            else:
                channel = await cls.bot.fetch_channel(message.channel.id)
                message = await channel.fetch_message(message.id)
                await message.clear_reaction(emoji)
        except Exception as e:
            await cls.bot.on_error(f"CLEAR REACTION\n message_id: {message.id}\n channel_id: {message.channel.id}", e)

    @classmethod
    async def clear_reactions(cls, message):
        to_remove = []
        for (message_id, emoji, user_id) in cls.reaction_events.keys():
            if message_id == message.id:
                to_remove.append((message_id, emoji, user_id))
        for container in to_remove:
            cls.reaction_events.pop(container)

        try:
            if message in cls.bot.cached_messages:
                await message.clear_reactions()
            else:
                channel = await cls.bot.fetch_channel(message.channel.id)
                message = await channel.fetch_message(message.id)
                await message.clear_reactions()
        except Exception as e:
            await cls.bot.on_error(f"CLEAR REACTIONS\n message_id: {message.id}\n channel_id: {message.channel.id}", e)

    @classmethod
    async def on_raw_reaction(cls, payload):
        container = (payload.message_id, payload.emoji.name, payload.user_id)
        if container in cls.reaction_events.keys():
            (handler, args) = cls.reaction_events[container]
            await handler(*args)
