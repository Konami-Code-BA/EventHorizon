//
//  Event_HorizonApp.swift
//  Event Horizon
//
//  Created by user216955 on 3/15/22.
//

import SwiftUI
import Firebase
import FirebaseMessaging
import UserNotifications

@main
struct Event_HorizonApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    var body: some Scene {
        WindowGroup {
            WebView(url: URL(string: "https://www.eventhorizon.vip")!)
            
        }
    }
}

class AppDelegate: UIResponder, UIApplicationDelegate, MessagingDelegate, UNUserNotificationCenterDelegate {
    var window: UIWindow?
    let gcmMessageIDKey = "gcm.message_id"

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        FirebaseApp.configure()
        Messaging.messaging().delegate = self
        UNUserNotificationCenter.current().delegate = self
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { success, _ in
            guard success else {
                return
            }
            print("Success in APNS registry")
        }
        application.registerForRemoteNotifications()
        return true}
    
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        messaging.token { token, _ in
            guard let token = token else {
                return
            }
            print("Token: \(token)")
        }
    }
}
