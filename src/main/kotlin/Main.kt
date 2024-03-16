package org.teel.obbot

import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.*
import dev.kord.core.cache.data.EmojiData
import dev.kord.core.entity.Attachment
import dev.kord.core.entity.GuildEmoji
import dev.kord.core.event.message.MessageCreateEvent
import kotlinx.coroutines.flow.toList
import me.jakejmattson.discordkt.arguments.IntegerArg
import me.jakejmattson.discordkt.commands.commands
import me.jakejmattson.discordkt.dsl.bot
import me.jakejmattson.discordkt.dsl.listeners
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

            val content = buildString {
                appendLine("Total pins: ${links.size}")
                appendLine("10 most recent:")
                appendLine(links.take(10).joinToString("\n"))
            }
            respond(message = content)
        }
    }
    slash("pin_preview", requiredPermissions = Permissions(Permission.ManageMessages)) {
        execute(IntegerArg("index")) {
            val (first) = args
            val channel = context.channel

            val pins = channel.pinnedMessages.toList()
            if (pins.isEmpty()) {
                respondPublic("There are no pins")
            }
            val pin = pins[first]

            val links = pins.map { "https://discord.com/channels/${context.guild?.id}/${channel.id}/${it.id}" }
            val link = links[first]

            val content = buildString {
                appendLine("## ${pin.author?.username} -> $link")
                appendLine(pin.content)

                val videoAttachments = pin.attachments.filter { it.isVideo() }
                videoAttachments.forEachIndexed { _, attachment ->
                    appendLine(attachment.url)
                }

                val audioAttachments = pin.attachments.filter { it.isAudio() }
                audioAttachments.forEachIndexed { _, attachment ->
                    appendLine(attachment.url)
                }

                val otherAttachments = pin.attachments.filterNot { it.isVideo() }.filterNot { it.isAudio() }
                otherAttachments.forEachIndexed { _, attachment ->
                    appendLine(attachment.url)
                }
            }

            respondPublic(message = content)
        }
    }
}

fun Attachment.isVideo(): Boolean {
    return this.contentType?.startsWith("video/") ?: false
}

fun Attachment.isAudio(): Boolean {
    return this.contentType?.startsWith("audio/") ?: false
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