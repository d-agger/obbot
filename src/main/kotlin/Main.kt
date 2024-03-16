package org.teel.obbot

import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.*
import dev.kord.core.cache.data.EmojiData
import dev.kord.core.entity.GuildEmoji
import dev.kord.core.event.message.MessageCreateEvent
import kotlinx.coroutines.flow.toList
import me.jakejmattson.discordkt.arguments.IntegerArg
import me.jakejmattson.discordkt.commands.commands
import me.jakejmattson.discordkt.dsl.bot
import me.jakejmattson.discordkt.dsl.listeners
import me.jakejmattson.discordkt.extensions.addField
import me.jakejmattson.discordkt.extensions.fullName
import me.jakejmattson.discordkt.extensions.pfpUrl
import me.jakejmattson.discordkt.extensions.profileLink
import kotlin.system.exitProcess

@KordPreview
fun main(args: Array<String>) {
    val token = System.getenv("BOT_TOKEN_HLVK")

    if (token == null) {
        System.err.println("Bot token not provided")
        exitProcess(1)
    }

    bot(token) {
        presence {
            status = PresenceStatus.DoNotDisturb
            competing("fuck all")
        }
        configure {
            prefix { "" }
            commandReaction = null
            defaultPermissions = Permissions(Permission.UseApplicationCommands)
        }
    }
}

fun cmdPins() = commands("pins") {
    slash("pins", description = "Blows up planet Earth", requiredPermissions = Permissions(Permission.ManageMessages)) {
        execute {
            val channel = context.channel
            val pins = channel.pinnedMessages.toList()
            val links = pins.map { "https://discord.com/channels/${context.guild?.id}/${channel.id}/${it.id}" }
            links.forEach { println(it) }
            respond(
                message = """
                    |Total pins: ${links.size}
                    |10 most recent:
                    |${links.take(10).joinToString("\n")}
                """.trimMargin().trimIndent()
            )
        }
    }
    slash("pin_preview", requiredPermissions = Permissions(Permission.ManageMessages)) {
        execute(IntegerArg("index")) {
            val (first) = args

            val channel = context.channel
            val pins = channel.pinnedMessages.toList()
            val links = pins.map { "https://discord.com/channels/${context.guild?.id}/${channel.id}/${it.id}" }

            val pin = pins[first]
            val link = links[first]

            val imgUrl = if (pin.embeds.isEmpty()) {
                null
            } else {
                pin.embeds[0].image?.url
            } ?: if (pin.attachments.isEmpty()) {
                null
            } else {
                pin.attachments.first().url
            }

            respondPublic {
                addField("", link)
                description = pin.content
                image = imgUrl
                author {
                    name = pin.author?.fullName ?: pin.author?.username
                    url = pin.author?.profileLink
                    icon = pin.author?.pfpUrl
                }
            }
        }
    }
}

fun listenersFunny() = listeners {
    on<MessageCreateEvent> {
        if (!message.content.lowercase().startsWith("good morning")) {
            return@on
        }
        println(message.content)
        message.addReaction(GuildEmoji(kord = kord,
            data = EmojiData(id = Snowflake(1168554374717505636),
                guildId = Snowflake(682277255225016352), name = "s")))
    }
}