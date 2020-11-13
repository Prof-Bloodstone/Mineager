package dev.bloodstone.mineager.download

import io.github.bonigarcia.wdm.WebDriverManager
import io.github.bonigarcia.wdm.managers.FirefoxDriverManager
import org.openqa.selenium.WebDriver


class SeleniumBrowser {
    fun setupClass() {
        WebDriverManager.firefoxdriver().setup()
    }
}