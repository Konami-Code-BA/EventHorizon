package com.example.EventHorizon

import android.content.ClipData
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val webView: WebView = findViewById(R.id.webview)
        webView.webViewClient = WebViewClient()
        webView.settings.javaScriptEnabled = true;
        webView.addJavascriptInterface(WebAppInterface(this), "NativeAndroid")
        webView.settings.loadWithOverviewMode = true;
        webView.settings.useWideViewPort = true;
        webView.settings.displayZoomControls = false;//Whether to use the built-in zoom mechanism
        webView.settings.setSupportZoom(true);//  Whether to support zoom
        webView.setInitialScale(100);//  Zoom on initialization
        webView.loadUrl("https://event-horizon-test.herokuapp.com")
//        webView.loadUrl("https://www.eventhorizon.vip")
    }

    class WebAppInterface(private val mainActivity: MainActivity) {
      @JavascriptInterface
      fun copyToClipboard(text: String?) {
        val clipboard: android.content.ClipboardManager? = this.mainActivity.getSystemService(CLIPBOARD_SERVICE) as android.content.ClipboardManager?
        val clip = ClipData.newPlainText("demo", text)
        clipboard?.setPrimaryClip(clip)
      }
    }
}
