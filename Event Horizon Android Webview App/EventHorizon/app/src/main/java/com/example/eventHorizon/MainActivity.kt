package com.example.eventHorizon

import android.content.ClipData
import android.content.Intent
import android.content.res.Configuration
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.webkit.*
import androidx.appcompat.app.AppCompatActivity


class MainActivity : AppCompatActivity() {

    private var mUploadMessage: ValueCallback<Uri>? = null
    private val fileChooserResultCode = 1

    override fun onCreate(savedInstanceState: Bundle?) {
				super.onCreate(savedInstanceState)
				setContentView(R.layout.activity_main)
				val webView: WebView = findViewById(R.id.webview)

        webView.settings.javaScriptEnabled = true
        webView.addJavascriptInterface(WebAppInterface(this), "NativeAndroid")

        webView.webChromeClient = object : WebChromeClient() {
            // For Android 3.0+
            fun openFileChooser(uploadMsg: ValueCallback<Uri>?) {
                print("I AM HERE1")
                mUploadMessage = uploadMsg
                val i = Intent(Intent.ACTION_GET_CONTENT)
                i.addCategory(Intent.CATEGORY_OPENABLE)
                i.type = "image/*"
                this@MainActivity.startActivityForResult(Intent.createChooser(i, "File Chooser"), fileChooserResultCode)
            }

            // For Android 3.0+
            fun openFileChooser(uploadMsg: ValueCallback<Uri>?, acceptType: String?) {
                print("I AM HERE2")
                mUploadMessage = uploadMsg
                val i = Intent(Intent.ACTION_GET_CONTENT)
                i.addCategory(Intent.CATEGORY_OPENABLE)
                i.type = "*/*"
                this@MainActivity.startActivityForResult(
                  Intent.createChooser(i, "File Browser"),
                  fileChooserResultCode)
            }

            //For Android 4.1
            fun openFileChooser(uploadMsg: ValueCallback<Uri>?, acceptType: String?, capture: String?) {
                print("I AM HERE3")
                mUploadMessage = uploadMsg
                val i = Intent(Intent.ACTION_GET_CONTENT)
                i.addCategory(Intent.CATEGORY_OPENABLE)
                i.type = "image/*"
                this@MainActivity.startActivityForResult(Intent.createChooser(i, "File Chooser"), fileChooserResultCode)
            }
        }

        webView.webViewClient = MyWebClient()
				webView.settings.loadWithOverviewMode = true
				webView.settings.useWideViewPort = true
				webView.settings.displayZoomControls = false // Whether to use the built-in zoom mechanism
				webView.settings.setSupportZoom(true) // Whether to support zoom
				webView.setInitialScale(100) // Zoom on initialization
				webView.loadUrl("https://event-horizon-test.herokuapp.com")
//        webView.loadUrl("https://www.eventhorizon.vip")
		}

    class WebAppInterface(private val mainActivity: MainActivity) {
        @JavascriptInterface
        fun copyToClipboard(text: String?) {
            val clipboard: android.content.ClipboardManager? = mainActivity.getSystemService(CLIPBOARD_SERVICE) as android.content.ClipboardManager?
            val clip = ClipData.newPlainText("demo", text)
            clipboard?.setPrimaryClip(clip)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, intent: Intent?) {
        super.onActivityResult(requestCode, resultCode, intent)
        if (requestCode == fileChooserResultCode) {
              if (null == mUploadMessage) return
              val result = if (intent == null || resultCode != RESULT_OK) null else intent.data
              mUploadMessage!!.onReceiveValue(result)
              mUploadMessage = null
          }
    }

    class MyWebClient : WebViewClient() {
        override fun onPageStarted(view: WebView, url: String, favicon: Bitmap?) {
            super.onPageStarted(view, url, favicon)
        }

        override fun shouldOverrideUrlLoading(view: WebView, url: String): Boolean {
            view.loadUrl(url)
            return true
        }
    }

    //flip-screen not loading again
    override fun onConfigurationChanged(newConfig: Configuration) {
        super.onConfigurationChanged(newConfig)
    }
}
