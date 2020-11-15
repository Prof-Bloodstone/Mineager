package dev.bloodstone.mineager.core.download

import com.google.gson.JsonParser
import java.io.IOException
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class HTTPSDownloader {
    fun spiget() {
        try {
            val url = URL(REQUEST_URL)
            val connection = url.openConnection() as HttpURLConnection
            connection.addRequestProperty("User-Agent", USER_AGENT) // Set User-Agent

            // If you're not sure if the request will be successful,
            // you need to check the response code and use #getErrorStream if it returned an error code
            val inputStream = connection.inputStream
            val reader = InputStreamReader(inputStream)

            // This could be either a JsonArray or JsonObject
            val element = JsonParser().parse(reader)
            if (element.isJsonArray) {
                // Is JsonArray
            } else if (element.isJsonObject) {
                // Is JsonObject
            } else {
                // wut?!
            }

            // TODO: process element
            println(element)
        } catch (e: IOException) {
            // TODO: handle exception
            e.printStackTrace()
        }
    }

    companion object {
        private const val USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
        private const val REQUEST_URL = "https://api.spiget.org/v2/resources/2"
    }
}