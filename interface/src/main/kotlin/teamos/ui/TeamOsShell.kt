package teamos.ui

/**
 * Early TeamOS shell model.
 *
 * The interface is intentionally written with Android-style Kotlin structure.
 * The Linux-based internals can later connect these screens to real system
 * services for battery, Wi-Fi, display, sound, privacy, and assistant control.
 */
class TeamOsShell(
    private val navigator: Navigator,
) {
    var currentScreen: Screen = Screen.LoginEmail
        private set


    fun submitLoginEmail(email: String): LoginProfile {
        val profile = LoginProfile(
            email = email.trim().lowercase(),
            displayName = displayNameFromEmail(email),
        )
        currentScreen = Screen.LoginGreeting
        navigator.open(Screen.LoginGreeting)
        return profile
    }

    fun continueToPinCreation() {
        currentScreen = Screen.PinCreation
        navigator.open(Screen.PinCreation)
    }

    fun finishPinCreation() {
        currentScreen = Screen.Home
        navigator.open(Screen.Home)
    }

    fun openSettings() {
        currentScreen = Screen.Settings
        navigator.open(Screen.Settings)
    }

    fun returnHome() {
        currentScreen = Screen.Home
        navigator.open(Screen.Home)
    }

    fun submitSearch(input: String): BrowserTarget {
        val trimmedInput = input.trim()
        val target = if (looksLikeUrl(trimmedInput)) {
            BrowserTarget.DirectUrl(normalizeUrl(trimmedInput))
        } else {
            BrowserTarget.PullSearch(trimmedInput)
        }

        navigator.openBrowser(target)
        return target
    }


    private fun displayNameFromEmail(email: String): String {
        val localPart = email.substringBefore('@').trim()
        if (localPart.isEmpty()) {
            return "usuário"
        }
        return localPart
            .replace('.', ' ')
            .replace('_', ' ')
            .replace('-', ' ')
            .split(' ')
            .filter { it.isNotBlank() }
            .joinToString(" ") { word ->
                word.replaceFirstChar { char -> char.uppercase() }
            }
    }

    private fun looksLikeUrl(value: String): Boolean {
        return value.startsWith("https://") ||
            value.startsWith("http://") ||
            (value.contains('.') && !value.contains(' '))
    }

    private fun normalizeUrl(value: String): String {
        return when {
            value.startsWith("https://") || value.startsWith("http://") -> value
            else -> "https://$value"
        }
    }
}

interface Navigator {
    fun open(screen: Screen)
    fun openBrowser(target: BrowserTarget)
}

sealed class Screen {
    object LoginEmail : Screen()
    object LoginGreeting : Screen()
    object PinCreation : Screen()
    object Home : Screen()
    object Settings : Screen()
}

sealed class BrowserTarget {
    data class DirectUrl(val url: String) : BrowserTarget()
    data class PullSearch(val query: String) : BrowserTarget()
}

data class LoginProfile(
    val email: String,
    val displayName: String,
)

data class HomeShortcut(
    val title: String,
    val url: String,
    val iconLabel: String,
)

data class SettingsSection(
    val id: String,
    val title: String,
    val description: String,
)

object TeamOsDefaults {
    const val slogan = "pesquise quanto quiser"
    const val searchHint = "Pesquisar ou acessar"
    const val pullSearchTemplate = "https://pull-search.genmb.com/?q=%s#"
    const val emailHint = "Digite seu e-mail"
    const val pinHint = "Crie um PIN"

    val recentSites = listOf(
        HomeShortcut("YouTube", "https://youtube.com", "YT"),
        HomeShortcut("ChatGusto", "https://chatgusto-ai.genmb.com", "GPT"),
        HomeShortcut("GitHub", "https://github.com", "Git"),
        HomeShortcut("Wiki", "https://wikipedia.org", "Wiki"),
        HomeShortcut("Mail", "https://mail.google.com", "Mail"),
        HomeShortcut("Pull", "https://pull-search.genmb.com", "Pull"),
    )

    val settingsSections = listOf(
        SettingsSection("about", "Sobre o TeamOS", "Versão, licença e informações do sistema."),
        SettingsSection("battery", "Bateria", "Uso de energia, porcentagem e economia de bateria."),
        SettingsSection("network", "Rede e Wi-Fi", "Wi-Fi, conexão, sinal e dados de rede."),
        SettingsSection("display", "Tela", "Brilho, tema, wallpaper e tamanho da interface."),
        SettingsSection("sound", "Som", "Volume, notificações e saída de áudio."),
        SettingsSection("privacy", "Privacidade e segurança", "Permissões, scanner e proteção do sistema."),
        SettingsSection("assistant", "ChatGusto", "Assistente, atalho do botão power e Modo Agente."),
        SettingsSection("system", "Sistema", "Atualizações, armazenamento, idioma e reinicialização."),
    )
}
