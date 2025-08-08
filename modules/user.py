import re
from datetime import datetime
from math import floor

from discord import AllowedMentions
from discord.ext.commands import Context
from pycountry import countries
from pycountry.db import Country
import country_converter as cc

from db import ObDB, DbName
from obbot import obbot
from strings import ObStrings
from util import is_mention, id_from_mention, mention, fancy_country_string, m_to_ft, ft_to_m

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
async def command_birthday(ctx: Context, param: str | None):
    """
    Commands for setting, checking and deleting your birthday.

    :ob user birthday                  Gives you your birthday or tells you if you haven't set it yet.
    :ob user birthday [dd-MMM-YYYY]    Sets your birthday.
    :ob user birthday delete           Deletes your birthday from the database (sets it to NULL).
    :ob user birthday <@id>            Gives you the birthday of user <@id>.
    """
    author = ctx.author
    ping_id = id_from_mention(param) if is_mention(param) else None

    if ping_id or not param:
        query_id = ping_id or author.id
        birthday = None
        with ObDB(DbName.USERS) as users_db:
            birthday = users_db.read(query_id, "birthday")
        if birthday is None:
            await ctx.send(
                ObStrings().INFO_NOT_SET_OTHER_USER(mention(ping_id), "birthday") if ping_id else
                ObStrings().INFO_NOT_SET(author.mention, "birthday"),
                allowed_mentions=AllowedMentions(users=ping_id is not None)
            )
            return
        birthday = birthday.replace("-", " ")
        await ctx.send(
            ObStrings().INFO_PRINT_OTHER_USER(mention(ping_id), "birthday", f"`{birthday}`") if ping_id else
            ObStrings().INFO_PRINT(author.mention, "birthday", f"`{birthday}`"),
            allowed_mentions=AllowedMentions(users=ping_id is not None)
        )
        return

    if param == "delete":
        with ObDB(DbName.USERS) as users_db:
            users_db.upsert(author.id, birthday=None)
        await ctx.send(ObStrings().INFO_DELETE(author.mention, "birthday"))
        return

    birthday_date = None
    for fmt in ("%d-%b-%Y", "%d-%b-%y"):
        try:
            birthday_date = datetime.strptime(param, fmt).date()
        except ValueError:
            continue
    if birthday_date is None:
        await ctx.send(ObStrings().BIRTHDAY_WRONG_FORMAT(author.mention))
        return
    with ObDB(DbName.USERS) as users_db:
        users_db.upsert(author.id, birthday=birthday_date.strftime("%d-%b-%Y"))
    await ctx.send(ObStrings().INFO_SET(author.mention, "birthday", f"`{birthday_date.strftime("%d %b %Y")}`"))


@user.command(name="country")
async def command_country(ctx: Context, *param: str | None):
    """
    Commands for setting, checking and deleting your country.

    :ob user country              Gives you your country or tells you if you haven't set it yet.
    :ob user country [country]    Sets your country using its (English) name.
    :ob user country [code]       Sets your country using its country code (2-letter or 3-letter).
    :ob user country delete       Deletes your country from the database (sets it to NULL).
    :ob user country <@id>        Gives you the country of user <@id>.
    """
    author = ctx.author

    if len(param) > 1:
        if param[0] != "delete" and not is_mention(param[0]):
            param = " ".join(param)
        else:
            # Trim everything after one of the above non-country matching cases
            param = param[0]

    ping_id = id_from_mention(param) if is_mention(param) else None

    if is_mention(param) or not param:
        query_id = ping_id or author.id
        c_obj: Country
        with ObDB(DbName.USERS) as users_db:
            c_code = users_db.read(query_id, "country")
        if c_code is None:
            await ctx.send(
                ObStrings().INFO_NOT_SET_OTHER_USER(mention(ping_id), "country") if ping_id else
                ObStrings().INFO_NOT_SET(author.mention, "country"),
                allowed_mentions=AllowedMentions(users=ping_id is not None)
            )
            return
        c_obj = countries.get(alpha_3=c_code)
        c_str = fancy_country_string(c_obj)
        await ctx.send(
            ObStrings().INFO_PRINT_OTHER_USER(mention(ping_id), "country", c_str) if ping_id else
            ObStrings().INFO_PRINT(author.mention, "country", c_str),
            allowed_mentions=AllowedMentions(users=ping_id is not None)
        )
        return

    if param == "delete":
        with ObDB(DbName.USERS) as users_db:
            users_db.upsert(author.id, country=None)
        await ctx.send(ObStrings().INFO_DELETE(author.mention, "country"))
        return

    c_code = cc.convert(param, to="ISO3")
    if c_code == "not found":
        await ctx.send(ObStrings().COUNTRY_NOT_FOUND(author.mention, param))
        return
    c_obj = countries.get(alpha_3=c_code)
    c_str = fancy_country_string(c_obj)
    with ObDB(DbName.USERS) as users_db:
        users_db.upsert(author.id, country=c_code)
    await ctx.send(ObStrings().INFO_SET(author.mention, "country", c_str))


@user.command(name="height")
async def command_height(ctx: Context, *, param: str | None):
    """
    Commands for setting, checking and deleting your height.

    :ob user height            Gives you your height or tells you if you haven't set it yet.
    :ob user height [X.XXm]    Sets your height in metric units.
    :ob user height [X'Y"]     Sets your height in imperial units.
    :ob user height delete     Deletes your height from the database (sets it to NULL).
    :ob user height <@id>      Gives you the height of user <@id>.
    """
    author = ctx.author
    ping_id = id_from_mention(param) if is_mention(param) else None

    if ping_id or not param:
        query_id = ping_id or author.id
        with ObDB(DbName.USERS) as users_db:
            height = users_db.read(query_id, "height")
        if height is None:
            await ctx.send(
                ObStrings().INFO_NOT_SET_OTHER_USER(mention(ping_id), "height") if ping_id else
                ObStrings().INFO_NOT_SET(author.mention, "height"),
                allowed_mentions=AllowedMentions(users=not ping_id)
            )
            return
        await ctx.send(
            ObStrings().INFO_PRINT_OTHER_USER(mention(ping_id), "height", f"`{height}`") if ping_id else
            ObStrings().INFO_PRINT(author.mention, "height", f"`{height}`"),
            allowed_mentions=AllowedMentions(users=not ping_id)
        )
        return

    if param == "delete":
        with ObDB(DbName.USERS) as users_db:
            users_db.upsert(author.id, height=None)
        await ctx.send(ObStrings().INFO_DELETE(author.mention, "height"))
        return

    metres = None
    feet, inches = None, None

    m = re.match(r'^(\d+(?:\.\d+)?)m?$', param) # literally took this straight from ChatGPT god i hate regex
    if m:
        metres = float(m.group(1))
    else:
        m = re.match(r"^(\d+)'(\d+)\"$", param)
        if m:
            feet, inches = map(int, m.groups())

    if metres is not None:
        feet, inches = m_to_ft(metres)
    elif feet is not None and inches is not None:
        metres = ft_to_m(feet, inches)
    else:
        await ctx.send(ObStrings().HEIGHT_WRONG_FORMAT(author.mention))
        return

    if metres > 2.5 or metres < 1.0:
        await ctx.send(ObStrings().INVALID_HEIGHT(author.mention))
        return

    height = f"""{floor(metres * 100) / 100:.02f}m ({feet}'{inches}")"""
    with ObDB(DbName.USERS) as users_db:
        users_db.upsert(author.id, height=height)
    await ctx.send(ObStrings().INFO_SET(author.mention, "height", f"`{height}`"))