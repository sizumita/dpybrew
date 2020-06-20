import discord
import asyncio


default_reactions = [
    '\U00002b05',
    '\U000027a1',
]


class Paginator:
    def __init__(self, client, max_page, reactions=None, timeout=60):
        self.client = client
        self.timeout = timeout
        self.max_page = max_page-1  # 0始まり
        self.embed = None
        self.message = None
        self.author = None
        self.channel = None
        self.page = 0
        self.reactions = reactions or default_reactions
        self.is_exit = False

    def exit(self):
        self.is_exit = True

    async def change_page(self, page):
        if asyncio.iscoroutinefunction(self.get_embed):
            embed = await self.get_embed(page)
        else:
            embed = self.get_embed(page)
        self.page = page
        await self.message.edit(embed=embed)

    async def forward(self):
        if self.page == self.max_page:
            return False
        return await self.change_page(self.page+1)

    async def backward(self):
        if self.page == 0:
            return False
        return await self.change_page(self.page-1)

    async def push_reaction(self, page, reaction):
        """
        Inherit this function.
        """
        emoji = str(reaction.emoji)
        if emoji == '\U00002b05':
            return await self.backward()
        if emoji == '\U000027a1':
            return await self.forward()

    def get_embed(self, page):
        """
        Inherit this function.
        This reaction is awaitable.
        """
        embed = discord.Embed()
        return embed

    def check(self, reaction, user):
        if reaction.message.id != self.message.id:
            return False
        if str(reaction.emoji) not in self.reactions:
            return False
        if user.id != self.author.id:
            return False
        return True

    async def remove_user_reaction(self, reaction, user):
        try:
            await self.message.remove_reaction(reaction, user)
        except Exception:  # TODO: ここを直す
            pass

    async def add_reactions(self):
        for emoji in self.reactions:
            await self.message.add_reaction(emoji)

    async def wait_reaction(self):
        try:
            reaction, user = await self.client.wait_for('reaction_add', check=self.check, timeout=self.timeout)
        except asyncio.TimeoutError:
            self.exit()
            return
        await self.remove_user_reaction(reaction, user)
        await self.push_reaction(self.page, reaction)

    async def loop(self):
        while not self.client.is_closed():
            await self.wait_reaction()
            if self.is_exit:
                return

    async def start_by_context(self, context):
        await self.start(context.channel.id)

    async def start(self, message, is_task=False):
        self.channel = self.client.get_channel(message.channel.id)
        self.author = message.author
        if self.channel is None:
            return False
        if asyncio.iscoroutinefunction(self.get_embed):
            embed = await self.get_embed(0)
        else:
            embed = self.get_embed(0)
        self.message = await self.channel.send(embed=embed)
        await self.add_reactions()
        if is_task:
            self.client.loop.create_task(self.loop())
            return
        await self.loop()



