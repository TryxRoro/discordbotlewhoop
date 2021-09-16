
from os import name
import os
import discord
from discord import guild
from discord import embeds
from discord import client
from discord import user
from discord import reaction
from discord.colour import Color
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import has_any_role
from discord.utils import get, resolve_invite
from discord.embeds import Embed
import random 






bot = commands.Bot(command_prefix = "!", description = "Bot de Tryx")


@bot.event
async def on_ready():
	print("Ready !")


image = [
	"https://www.serieously.com/app/uploads/2020/07/Rouge-%C3%A0-l%C3%A8vres-laser-600x0-c-default.webp",#rouge a lèvre
	"https://www.serieously.com/app/uploads/2020/07/S%C3%A8che-cheveux-600x0-c-default.webp",#Sèche-cheveux
	"https://www.serieously.com/app/uploads/2020/07/bottes-propuls%C3%A9es-600x0-c-default.webp",#bottes-propulsées
	"https://www.serieously.com/app/uploads/2020/07/Compoudrier-600x0-c-default.webp",#compoudrier
	"https://www.serieously.com/app/uploads/2020/07/skateboard-600x0-c-default.webp",#skateboard
	"https://www.serieously.com/app/uploads/2020/07/Mp3-600x0-c-default.webp",#mp3
	"https://www.serieously.com/app/uploads/2020/07/Lunettes-infrarouges-600x0-c-default.webp",#Lunettes-infrarouges
]


@bot.command()	#commande !say
@commands.guild_only()
async def say(ctx, *texte):
	await ctx.message.delete()
	await ctx.send(" ".join(texte))

		
@bot.command()	#commande !clear
@commands.guild_only()
@commands.has_any_role(875739322651914242,883374263543926836)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

	server = ctx.guild

	embed = discord.Embed(title="**Supression de message!!!**", color=0xec0000)
	embed.set_thumbnail(url="https://i.redd.it/281fjxdrbfa21.png")
	embed.add_field(name="Décision du staff", value="Le staff a décidé de suprimmer des messages", inline=False)

	await ctx.send(embed=embed)

@clear.error #erreur commande
async def erreurClear(ctx, erreur):
	with open("./bot.log","a",encoding="utf8")as file:
		file.write(f"Une erreur est survenu dans la commande clear.utilisateur:{ctx.author.display_name}\n")


	
@bot.command()	#commande !kick
@commands.guild_only()
@commands.has_any_role(875739322651914242,883374263543926836,874649832420155412)
async def kick(ctx, user : discord.User,*,reason = None):
	await ctx.guild.kick(user, reason = reason)
	
	server = ctx.guild

	embed = discord.Embed(title="Kick!!!")
	embed.set_thumbnail(url="https://i.redd.it/281fjxdrbfa21.png")
	embed.add_field(name="Décision du staff", value="Est rejeter de la patrie", inline=False)
	
	await ctx.send(embed=embed)

@kick.error  #erreur commande
async def erreurKick(ctx, erreur):
	with open("./bot.log","a",encoding="utf8")as file:
		file.write(f"Une erreur est survenu dans la commande kick.utilisateur:{ctx.author.display_name}\n")


	
@bot.command()	#commande !ban
@commands.guild_only()
@commands.has_any_role(875739322651914242,883374263543926836)
async def ban(ctx, user : discord.Member,*,reason = None):
	if reason is None:
  		await user.ban()
	else:
  		await user.ban(reason = reason)
	await ctx.send(f"{user} est mort par la main de la justice: {reason}.")

@ban.error  #erreur commande
async def erreurBan(ctx, erreur):
	with open("./bot.log","a",encoding="utf8")as file:
		file.write(f"Une erreur est survenu dans la commande ban.utilisateur:{ctx.author.display_name}\n")


	
@bot.command()	#commande !unban
@commands.guild_only()
@commands.has_any_role(875739322651914242,883374263543926836)
async def unban(ctx, user):
	print(user.split("#"))
	userName = user.split("#")[0]
	userId = user.split("#")[1]
	
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user)
			await ctx.send(f"{user} est revenu a la vie!!!")
			return
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@unban.error   #erreur commande
async def erreurUnban(ctx, erreur):
	with open("./bot.log","a",encoding="utf8")as file:
		file.write(f"Une erreur est survenu dans la commande unban.utilisateur:{ctx.author.display_name}\n")



@bot.command()	#commande !unmute
@commands.guild_only()
@commands.has_any_role(875739322651914242,883374263543926836)
async def unmute(ctx, member : discord.Member, *, reason ="Aucune raison n a était renseigné"):
	mutedRole = await getMutedRole(ctx)
	await member.remove_roles(mutedRole, reason = reason)
	
	server = ctx.guild

	embed = discord.Embed(title="**Unmute!!!**", color=0xec0000)
	embed.set_thumbnail(url="https://i.redd.it/281fjxdrbfa21.png")
	embed.add_field(name="Décision du staff", value="A retrouvé sa langue !", inline=False)
	
	await ctx.send(embed=embed)


	pass#commande !mute
async def createMutedRole(ctx:commands.Context):
	mutedRole = await ctx.guild.create_role(
		name = "Muted", 
		permissions = discord.Permissions (	
			send_messages = False,
			speak = False),
			reason = "Creation du role Muted pour mute des gens.")		
	for channel in ctx.guild.channels:
		await channel.set_permissions(mutedRole, send_messages = False, speak = False)														
	return mutedRole
	
async def getMutedRole(ctx):
	roles =  ctx.guild.roles
	for role in roles:
		if role.name == "Muted":
			return role

	return await createMutedRole(ctx)

		
@bot.command()
@commands.guild_only()
@commands.has_any_role(875739322651914242,883374263543926836)
async def mute(ctx, member : discord.Member, *, reason ="Aucune raison renseignée"):
	mutedRole = await getMutedRole(ctx)
	await member.add_roles(mutedRole, reason = reason)
	
	server = ctx.guild
	
	embed = discord.Embed(title="**Mute!!!**", color=0xec0000)
	embed.set_thumbnail(url="https://i.redd.it/281fjxdrbfa21.png")
	embed.add_field(name="Décision du staff", value="C est fait volé sa langue !", inline=False)

	await ctx.send(embed=embed)

@unmute.error  #erreur commande
async def erreurUnmute(ctx, erreur):
	with open("./bot.log","a",encoding="utf8")as file:
		file.write(f"Une erreur est survenu dans la commande unmute.utilisateur:{ctx.author.display_name}\n")

	

@bot.command() #commande !server_Info
@commands.guild_only()
async def server_Info(ctx):

	await ctx.message.delete()

	server = ctx.guild

	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	icon_url = ctx.guild.icon_url
	
	embed = discord.Embed(title="**Server Info**", description=f"Informations du serveur :", color=0xec0000)
	embed.set_thumbnail(url="https://i.redd.it/281fjxdrbfa21.png")
	embed.add_field(name="__Nombre de membres :__", value=numberOfPerson)
	embed.add_field(name="__Nombre de salons textuels :__", value=len(server.text_channels))
	embed.add_field(name="__Nombre de salons vocaux :__", value=len(server.voice_channels))
	embed.set_footer(text=str(serverName), icon_url=ctx.guild.icon_url)
	await ctx.send(embed=embed)


@bot.command() #commande !réglement
@commands.guild_only()
async def réglement(ctx):

	await ctx.message.delete()

	server = ctx.guild

	serverName = server.name

	embed = discord.Embed(title="**Réglement**", description=f"Réglement du serveur :", color=0xec0000)
	embed.set_thumbnail(url="https://i.redd.it/281fjxdrbfa21.png")
	embed.add_field(name="Règle 1", value="Respect envers tout les membres même ceux avec qui vous ne vous entendez pas.", inline=False)
	embed.add_field(name="Règle 2", value="Utilisez les bots dans les salons qui leurs sont attribués.", inline=False)
	embed.add_field(name="Règle 3", value="Si vous vous disputez merci de vous dirigez en mp.", inline=False)
	embed.add_field(name="Règle 4", value="Si vous voulez poster la photo d'une personne sur le serveur veuillez d'abord lui demander son autorisation.", inline=False)
	embed.add_field(name="Règle 5", value="Aucun harcèlement, insulte, ect ne sera tolérée bien évidemment ou sinon pour sanction mute, expulsion ou ban concernant la gravité des faits.", inline=False)
	embed.set_footer(text=str(server), icon_url=ctx.guild.icon_url)
	
	await ctx.send(embed=embed)




@bot.command() #commmande !gadget
@commands.guild_only()
async def gadget(ctx):
	
	
	server = ctx.guild

	embed = discord.Embed(title="Gadget")
	embed.set_image(url=image[random.randint(0,len(image)-1)])



	await ctx.send(embed=embed)






	
	

















































































bot.run("ODgyNjY3NjM3NzY5OTI0NzE4.YS-uTA.dmMmlhxTPKkxARDglcM3nwRB1-s")