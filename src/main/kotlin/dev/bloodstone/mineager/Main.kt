package dev.bloodstone.mineager

import picocli.CommandLine
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.concurrent.Callable
import kotlin.system.exitProcess

@CommandLine.Command(
    name = "Mineager", mixinStandardHelpOptions = true, version = ["1.0.0"],
    description = ["Package Manager for Bukkit/Spigot/PaperSpigot/Waterfall."]
)
class Main : Callable<Int> {

    @CommandLine.Parameters(index = "0", description = ["Path to server folder"])
    lateinit var serverFolder: Path

    @CommandLine.Option(
        names = ["-c", "--configDir"],
        description = ["Change the directory where configuration files are stored, defaults to home directory + .config/mineager"]
    )
    var configFolder : Path = Paths.get(System.getProperty("user.home"), ".config", "mineager")

    @CommandLine.Option(
        names = ["-p", "--proxy"],
        description = ["Proxy URI socks5://127.0.0.1:9050"]
    )
    lateinit var proxy: String

    override fun call(): Int {
        if (!Files.exists(configFolder)) {
            try {
                Files.createDirectories(configFolder)
            } catch (e: IOException) {
            }
        }
        return 0
    }
}

fun main(args: Array<String>) : Unit = exitProcess(CommandLine(Main()).execute(*args))