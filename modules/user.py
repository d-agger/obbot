from datetime import datetime

from discord import AllowedMentions
from discord.ext.commands import Context
from pycountry import countries
from pycountry.db import Country
import country_converter as cc

from db import ObDB, DbName
from obbot import obbot
from strings import ObStrings
from util import is_ping, id_from_ping

with ObDB(DbName.USERS) as db:
    db.create_table(
        "id TEXT PRIMARY KEY",
        "birthday TEXT",
        "height TEXT",
        "country TEXT",
        "money REAL"
    )


@obbot.group()
async def user(ctx: Context):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"mate you need to provide a subcommand")


@user.command(name="birthday")
async def command_birthday(ctx: Context, date: str | None):
    """
    Commands for setting, checking and deleting your birthday.

    :ob user birthday                  Gives you your birthday or tells you if you haven't set it yet.
    :ob user birthday [dd-MMM-YYYY]    Sets your birthday.
    :ob user birthday delete           Deletes your birthday from the database (sets it to NULL).
    :ob user birthday <@id>            Gives you the birthday of user <@id>.
    """
    author = ctx.author

    if is_ping(date) or not date:
        query_id = id_from_ping(date) if is_ping(date) else author.id
        bday = None
        with ObDB(DbName.USERS) as users_db:
            bday = users_db.read(query_id, "birthday")
            if bday is None:
                await ctx.send(
                    ObStrings().BIRTHDAY_NOT_SET_OTHER_USER(date)
                    if is_ping(date) else
                    ObStrings().BIRTHDAY_NOT_SET(author.mention),
                    allowed_mentions=AllowedMentions(users=not is_ping(date))
                )
                return
        await ctx.send(
            ObStrings().BIRTHDAY_PRINT_OTHER_USER(date, bday)
            if is_ping(date) else
            ObStrings().BIRTHDAY_PRINT(author.mention, bday),
            allowed_mentions=AllowedMentions(users=not is_ping(date))
        )
        return

    if date == "delete":
        with ObDB(DbName.USERS) as users_db:
            users_db.upsert(author.id, birthday=None)
        await ctx.send(ObStrings().BIRTHDAY_DELETE(author.mention))
        return

    birthday_date = None
    for fmt in ("%d-%b-%Y", "%d-%b-%y"):
        try:
            birthday_date = datetime.strptime(date, fmt).date()
        except ValueError:
            continue
    if birthday_date is None:
        await ctx.send(ObStrings().BIRTHDAY_WRONG_FORMAT(author.mention))
        return
    birthday_date = birthday_date.strftime("%d-%b-%Y")
    with ObDB(DbName.USERS) as users_db:
        users_db.upsert(author.id, birthday=birthday_date)
    await ctx.send(ObStrings().BIRTHDAY_SET(author.mention, birthday_date))


@user.command(name="country")
async def command_country(ctx: Context, *country: str | None):
    """
    Commands for setting, checking and deleting your country.

    :ob user country
    :ob user country [country]    Sets your country using its (English) name.
    :ob user country [code]       Sets your country using its country code (2-letter or 3-letter).
    :ob user country delete       Deletes your country from the database (sets it to NULL).
    :ob user country <@id>        Gives you the country of user <@id>.
    """
    author = ctx.author

    if len(country) > 1:
        if country[0] != "delete" and not is_ping(country[0]):
            country = " ".join(country)
        else:
            # Trim everything after one of the above non-country matching cases
            country = country[0]

    if is_ping(country) or not country:
        query_id = id_from_ping(country) if is_ping(country) else author.id
        c_obj: Country
        with ObDB(DbName.USERS) as users_db:
            c_code = users_db.read(query_id, "country")
            if c_code is None:
                await ctx.send(
                    ObStrings().COUNTRY_NOT_SET_OTHER_USER(country)
                    if is_ping(country) else
                    ObStrings().COUNTRY_NOT_SET(author.mention),
                    allowed_mentions=AllowedMentions(users=not is_ping(country))
                )
                return
            c_obj = countries.get(alpha_3=c_code)
        await ctx.send(
            ObStrings().COUNTRY_PRINT_OTHER_USER(country, c_obj.flag, c_obj.name, c_obj.alpha_3)
            if is_ping(country) else
            ObStrings().COUNTRY_PRINT(author.mention, c_obj.flag, c_obj.name, c_obj.alpha_3),
            allowed_mentions=AllowedMentions(users=not is_ping(country))
        )
        return

    if country == "delete":
        with ObDB(DbName.USERS) as users_db:
            users_db.upsert(author.id, country=None)
        await ctx.send(ObStrings().COUNTRY_DELETE(author.mention))
        return

    c_code = cc.convert(country, to="ISO3")
    if c_code == "not found":
        await ctx.send(ObStrings().COUNTRY_NOT_FOUND(author.mention, country))
        return
    c_obj = countries.get(alpha_3=c_code)
    with ObDB(DbName.USERS) as users_db:
        users_db.upsert(author.id, country=c_code)
    await ctx.send(ObStrings().COUNTRY_SET(author.mention, c_obj.flag, c_obj.name, c_obj.alpha_3))