import discord

from decouple import config
from discord import app_commands
from discord.ext import commands

server = config('server_id')
role = config('role_id')
TOKEN = config("token_secreto")

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def setup_hook(self) -> None:
        self.add_view(DropdownView1())
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await tree.sync(guild = discord.Object(id=server)) # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Sucesso | bot online entramos como  {self.user}.") 

aclient = client()
tree = app_commands.CommandTree(aclient)

#-----------Inicio do menu 01-----------

class Dropdown1(discord.ui.Select):
    #menu para suporte geral
    def __init__(self):
        options = [
            discord.SelectOption(value="staff",label="Entre para equipe", emoji="👨🏻‍🔧"),
            #discord.SelectOption(value="compras",label="Comprar ou alugar um bot", emoji="🛒"),
            discord.SelectOption(value="duvidas",label="Estou com dúvidas!", emoji="❓"),
            discord.SelectOption(value="projeto",label="Cadastrar projeto", emoji="📝"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "staff":
            await interaction.response.send_message("Nessa seção, você pode tirar suas dúvidas ou entrar em contato com a nossa equipe. \n \n No momento oferecemos suporte para te ajudar em relação ao nosso recrutamento! \n \n Sempre que precisar estaremos todos os dias e em qualquer horário ensinando Clean/Redraw e Edição. Contudo, dependerá também da disponibilidade da equipe e por conta disso o atendimento pode demorar um pouco.",ephemeral=True,view=CreateTicket())
        
        #elif self.values[0] == "compras":
            #await interaction.response.send_message("Deseja Alugar ou comprar seu proprio bot para discord entre no servidor da arteca https://discord.gg/CCmDRYku5s  e ** Solicite um orçamento**",ephemeral=True)
        
        elif self.values[0] == "duvidas":
            await interaction.response.send_message("Está com dúvidas? **abra um ticket no botão abaixo**",ephemeral=True,view=CreateTicket())
        
        elif self.values[0] == "projeto":
            await interaction.response.send_message("Antes de Abrir um ticket para cadastrar o projeto da sua scan, crie uma conta de cliente no site: https://scanart.arteca.fun/ Atenção: em nome Coloque seu nome do discord, em sobre nome coloque seu nome de perfil completo ex: Art | ticket#8595 , em empresa coloque o nome da sua scan após isso **abra um ticket no botão abaixo** e informe os dados cadastrados",ephemeral=True,view=CreateTicket())
        
class DropdownView1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Dropdown1())

@tree.command(guild = discord.Object(id=server), name = 'menu01', description='Envia menu para o canal de atendimento principal')
@commands.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    await interaction.channel.send(embed=embed01,view=DropdownView1())

#-----------inicio da configuração do ticket-----------

class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value=None

    @discord.ui.button(label="Abrir Ticket",style=discord.ButtonStyle.blurple,emoji="📩")
    async def confirm(self,interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True,content=f"Você já tem um atendimento em andamento!")
                    return
        
        if ticket != None:
            await ticket.unarchive()
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080,invitable=False) #Exclusivo para Thread Privada
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})",auto_archive_duration=10080,type=discord.ChannelType.private_thread) 
            await ticket.edit(invitable=False) #Exclusivo para Thread Privada

        await interaction.response.send_message(ephemeral=True,content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"📩  **|** {interaction.user.mention} ticket criado! fale sobre você e com o que quer trabalhar e espere alguem do <@&1049122835383206029> responder!")


#-----------fim da Configuração do client-----------

#-----------Inicio dos embeds-----------

#-----------Embed Atendimento Geral-----------
embed01 = discord.Embed(
    colour= discord.Color.blue(),
    title = "Atendimento - Scanart",
    description = "Está querendo entrar em contato ou fazer parte da equipe selecione a opção e abra um ticket agora mesmo!",

        )
embed01.set_thumbnail(url = "https://media.discordapp.net/attachments/1046534969863962738/1049129766873219112/logo_profile.png?width=413&height=413")
embed01.set_footer(text='Ticket system - desenvolvido por Arteca \n © COPYRIGHT 2022 POWERED BY ARTECA.')    
embed01.set_image(url = "https://media.discordapp.net/attachments/1047382196798902273/1047711914676994098/baner01.png")
#-----------Fim dos embeds-----------


#-----------inicio dos comandos-----------

@tree.command(guild = discord.Object(id=server), name="fecharticket",description='Feche um atendimento atual.')
@commands.has_permissions(manage_guild=True)
async def _fecharticket(interaction: discord.Interaction):
    mod = interaction.guild.get_role(role)
    if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
        await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
        await interaction.channel.edit(archived=True)
    else:
        await interaction.response.send_message("Isso não pode ser feito aqui...")

    

aclient.run(TOKEN)