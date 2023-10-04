package org.teel.obbot

import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.Permission
import dev.kord.common.entity.Permissions
import dev.kord.common.entity.PresenceStatus
import me.jakejmattson.discordkt.arguments.IntegerArg
import me.jakejmattson.discordkt.commands.commands
import me.jakejmattson.discordkt.dsl.bot
import kotlin.system.exitProcess

@KordPreview
fun main(args: Array<String>) {
    val token = System.getenv("BOT_TOKEN")

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

fun cmd() = commands("sample") {
    slash("add", description = "Adds two numbers together") {
        execute(IntegerArg("first"), IntegerArg("second")) {
            val (a, b) = args
            val sum = a + b
            respond("$a + $b = $sum")
        }
    }
}