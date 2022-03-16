package com.example.EventHorizon

import android.content.ClipData
import android.content.Context
import android.content.Context.CLIPBOARD_SERVICE
import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat.getSystemService


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val webView: WebView = findViewById(R.id.webview)
        webView.webViewClient = WebViewClient()
        webView.getSettings().setJavaScriptEnabled(true)
        webView.addJavascriptInterface(WebAppInterface(), "NativeAndroid")
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setDisplayZoomControls(false);//Whether to use the built-in zoom mechanism
        webView.getSettings().setSupportZoom(true);//  Whether to support zoom
        webView.setInitialScale(100);//  Zoom on initialization
        webView.loadUrl("https://event-horizon-test.herokuapp.com")
//        webView.loadUrl("https://www.eventhorizon.vip")
    }
}
class WebAppInterface {
  @JavascriptInterface
  fun copyToClipboard(text: String?) {
    val clipboard: android.content.ClipboardManager? = getSystemService<String>(CLIPBOARD_SERVICE) as android.content.ClipboardManager?
    val clip = ClipData.newPlainText("demo", text)
    clipboard.setPrimaryClip(clip)
  }
}
