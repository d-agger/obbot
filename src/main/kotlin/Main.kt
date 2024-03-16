package org.teel.obbot

import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.*
import dev.kord.core.cache.data.EmojiData
import dev.kord.core.entity.Attachment
import dev.kord.core.entity.GuildEmoji
import dev.kord.core.event.message.MessageCreateEvent
import dev.kord.rest.builder.message.EmbedBuilder
import kotlinx.coroutines.flow.toList
import me.jakejmattson.discordkt.arguments.IntegerArg
import me.jakejmattson.discordkt.commands.commands
import me.jakejmattson.discordkt.dsl.bot
import me.jakejmattson.discordkt.dsl.listeners
import me.jakejmattson.discordkt.extensions.fullName
import kotlin.system.exitProcess

@KordPreview
fun main() {
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
//113
            val channel = context.channel
            val pins = channel.pinnedMessages.toList()
            val pin = pins.getOrNull(first)

            if (pin != null) {
                val link = "https://discord.com/channels/${context.guild?.id}/${channel.id}/${pin.id}"

                val content = buildString {
                    appendLine("**By: ${pin.author?.fullName}**")
                    appendLine(pin.content)

                    val videoAttachments = pin.attachments.filter { it.isVideo() }
                    videoAttachments.forEachIndexed { index, attachment ->
                        appendLine(attachment.url)
                    }

                    val mp3Attachments = pin.attachments.filter { it.isMp3() }
                    mp3Attachments.forEachIndexed { index, attachment ->
                        appendLine(attachment.url)
                    }

                    val otherAttachments = pin.attachments.filterNot { it.isVideo() }
                    otherAttachments.forEachIndexed { index, attachment ->
                        appendLine(attachment.url)
                    }

                    appendLine("Link: $link")
                }
                respondPublic(content)
            } else {
                respondPublic("Pin not found.")
            }
        }
    }
}

fun Attachment.isVideo(): Boolean {
    return this.contentType!!.startsWith("video/")
}

fun Attachment.isMp3(): Boolean {
    return this.contentType!!.lowercase() == "audio/mpeg"
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