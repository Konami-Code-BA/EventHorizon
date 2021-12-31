package com.example.EventHorizon

import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val webView: WebView = findViewById(R.id.webview)
        webView.webViewClient = WebViewClient()
        webView.getSettings().setJavaScriptEnabled(true)
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setDisplayZoomControls(false);//Whether to use the built-in zoom mechanism
        webView.getSettings().setSupportZoom(true);//  Whether to support zoom
        webView.setInitialScale(100);//  Zoom on initialization
        webView.loadUrl("https://event-horizon-test.herokuapp.com")
//        webView.loadUrl("https://www.eventhorizon.vip")
    }
}
