package dev.bloodstone.mineager

import mu.KotlinLogging
import picocli.CommandLine
import java.io.IOException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.concurrent.Callable
import kotlin.system.exitProcess

private val logger = KotlinLogging.logger {};
/* Uninstall directories
user.home/.config/mineager
for server in serverFolderList
 */
@CommandLine.Command(
    name = "Mineager", mixinStandardHelpOptions = true, version = ["1.0.0"],
    description = ["Package Manager for Bukkit/Spigot/PaperSpigot/Waterfall."]
)
class Main : Callable<Int> {

//    @CommandLine.Parameters(index = "0", description = ["Path to server folder"])
//    lateinit var name: String

    @CommandLine.Option(
        names = ["-a", "--add"],
        description = ["Adds a server to the list of servers, if -n or --name are not specified the first server's " +
                "name will default to \"main\" and subsequent servers will default to server1, server2, etc..."]
    )
    lateinit var serverDir : Path

    @CommandLine.Option(
        names = ["-n", "--name"],
        description = ["Specifies the name of the server which is used internally for actions such as adding the " +
                "server to the serverlist and installing plugins. This value can be changed."]
    )
    lateinit var serverName : String

    @CommandLine.Option(
        names = ["-c", "--configDir"],
        description = ["Change the directory where configuration files are stored, defaults to home directory + .config/mineager"]
    )
    var configFolder : Path = Paths.get(System.getProperty("user.home"), ".config", "mineager")

    @CommandLine.Parameters(paramLabel = "plugin(s)...", description = ["name of one or more plugins to install"])
    lateinit var plugins: Array<String>;

    @CommandLine.Option(
        names = ["-p", "--proxy"],
        description = ["Proxy URI, for example, socks5://127.0.0.1:9050"]
    )
    lateinit var proxy: String

    override fun call(): Int {
        if (!Files.exists(configFolder)) {
            logger.info { "Config folder doesn't exist, creating config folder..." }
            try {
                Files.createDirectories(configFolder)
            } catch (e: IOException) {
                logger.error {"Couldn't create config folder\n" + e}
            }
        }

        // If server directory is specified
        if (this::serverDir.isInitialized) {
            //if serverDir is not valid system path {return 3; logger.error{"Specified server directory is invalid"}}



            //And the directory exists
            if (Files.exists(serverDir)) {


            // And the directory does not exist
            } else {
                logger.info { "Server directory does not exist, creating folder..." }
                try {
                    Files.createDirectories(serverDir)
                } catch (e: IOException) {
                    logger.error { "Could not create server directory folder" }
                }
            }
        }

        if (this::plugins.isInitialized)
            for (element in plugins) { println(element) }
        return 0
    }
}

fun main(args: Array<String>) : Unit = exitProcess(CommandLine(Main()).execute(*args))