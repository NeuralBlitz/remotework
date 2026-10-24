---
name: mobile
description: >
  Expert guidance on mobile app development for iOS and Android. Use for: native app 
  development with Swift/SwiftUI and Kotlin/Jetpack Compose, cross-platform development 
  with React Native and Flutter, mobile UI/UX design, device APIs, push notifications, 
  offline-first architecture, app store submission, and mobile performance optimization.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: mobile-development
  tags: [ios, android, react-native, flutter, mobile]
---

# Mobile Development — Implementation Guide

Covers: **Native iOS · Native Android · React Native · Flutter · Device APIs · Performance**

-----

## Platform Overview

### Choosing Your Approach

| Approach | Languages | Pros | Cons |
|----------|-----------|------|------|
| **Native iOS** | Swift, SwiftUI | Best performance, full API access | Single platform |
| **Native Android** | Kotlin, Jetpack Compose | Best performance, full API access | Single platform |
| **React Native** | JavaScript/TypeScript | Cross-platform, large ecosystem | Performance overhead |
| **Flutter** | Dart | Cross-platform, excellent UI | Larger app size |

### When to Use Each

**Native Development** is ideal for apps requiring maximum performance, complex animations, intensive computations, or deep integration with platform-specific features like AR, advanced camera capabilities, or system-level access.

**Cross-Platform** works well for business apps, content-focused applications, and startups needing to reach both platforms quickly with limited resources.

-----

## Native iOS Development

### SwiftUI Fundamentals

```swift
import SwiftUI

struct ContentView: View {
    @State private var isLoggedIn = false
    @StateObject private var viewModel = AppViewModel()
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Image(systemName: "star.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.yellow)
                
                Text("Welcome to My App")
                    .font(.title)
                    .fontWeight(.bold)
                
                Button(action: {
                    isLoggedIn.toggle()
                }) {
                    Text(isLoggedIn ? "Logout" : "Login")
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(isLoggedIn ? Color.red : Color.blue)
                        .cornerRadius(10)
                }
            }
            .padding()
            .navigationTitle("Home")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {}) {
                        Image(systemName: "gear")
                    }
                }
            }
        }
    }
}

@MainActor
class AppViewModel: ObservableObject {
    @Published var user: User?
    @Published var isLoading = false
    
    func fetchUser() async {
        isLoading = true
        // API call
        isLoading = false
    }
}
```

### SwiftUI Navigation

```swift
// NavigationStack with programmatic navigation
struct RootView: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink(value: "details") {
                    Text("Go to Details")
                }
                NavigationLink(value: 42) {
                    Text("Item 42")
                }
            }
            .navigationDestination(for: String.self) { value in
                DetailView(text: value)
            }
            .navigationDestination(for: Int.self) { value in
                ItemDetailView(id: value)
            }
        }
    }
}

// TabView for bottom navigation
struct MainTabView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)
            
            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(2)
        }
    }
}
```

### iOS Data Persistence

```swift
import Foundation

// UserDefaults for simple data
class UserDefaultsManager {
    private let defaults = UserDefaults.standard
    
    func saveToken(_ token: String) {
        defaults.set(token, forKey: "auth_token")
    }
    
    func getToken() -> String? {
        return defaults.string(forKey: "auth_token")
    }
    
    func clearAll() {
        let domain = Bundle.main.bundleIdentifier!
        defaults.removePersistentDomain(forName: domain)
    }
}

// Core Data for complex data
import CoreData

class CoreDataManager {
    static let shared = CoreDataManager()
    
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Unable to load persistent stores: \(error)")
            }
        }
        return container
    }()
    
    var context: NSManagedObjectContext {
        persistentContainer.viewContext
    }
    
    func saveContext() {
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                let nsError = error as NSError
                print("Unresolved error \(nsError), \(nsError.userInfo)")
            }
        }
    }
}

// SwiftData (iOS 17+)
import SwiftData

@Model
class TodoItem {
    var title: String
    var isCompleted: Bool
    var createdAt: Date
    
    init(title: String, isCompleted: Bool = false) {
        self.title = title
        self.isCompleted = isCompleted
        self.createdAt = Date()
    }
}
```

### iOS Networking

```swift
import Foundation

class NetworkManager {
    static let shared = NetworkManager()
    
    private let session: URLSession
    
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        session = URLSession(configuration: config)
    }
    
    func fetch<T: Decodable>(_ type: T.Type, from url: URL) async throws -> T {
        let (data, response) = try await session.data(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidResponse
        }
        
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        return try decoder.decode(T.self, from: data)
    }
}

enum NetworkError: Error {
    case invalidResponse
    case decodingError
    case networkError(Error)
}
```

-----

## Native Android Development

### Jetpack Compose

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun MainScreen(
    viewModel: MainViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
) {
    var text by remember { mutableStateOf("") }
    val uiState by viewModel.uiState.collectAsState()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Welcome to My App",
            style = MaterialTheme.typography.headlineMedium
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        OutlinedTextField(
            value = text,
            onValueChange = { text = it },
            label = { Text("Enter your name") }
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = { viewModel.submitName(text) },
            enabled = text.isNotEmpty()
        ) {
            Text("Submit")
        }
        
        if (uiState.isLoading) {
            CircularProgressIndicator()
        }
    }
}

data class UiState(
    val isLoading: Boolean = false,
    val result: String? = null,
    val error: String? = null
)
```

### Android ViewModel & State

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
    
    fun submitName(name: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            try {
                // Simulate API call
                val result = apiService.submitName(name)
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    result = result
                )
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = e.message
                )
            }
        }
    }
}
```

### Android Navigation

```kotlin
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    
    NavHost(
        navController = navController,
        startDestination = "home"
    ) {
        composable("home") {
            HomeScreen(
                onNavigateToDetail = { itemId ->
                    navController.navigate("detail/$itemId")
                }
            )
        }
        
        composable(
            route = "detail/{itemId}",
            arguments = listOf(
                navArgument("itemId") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val itemId = backStackEntry.arguments?.getString("itemId") ?: ""
            DetailScreen(itemId = itemId)
        }
        
        composable("settings") {
            SettingsScreen()
        }
    }
}
```

### Android Data Storage

```kotlin
import android.content.Context
import android.content.SharedPreferences

// SharedPreferences
class PreferencesManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences(
        "my_app_prefs",
        Context.MODE_PRIVATE
    )
    
    var authToken: String?
        get() = prefs.getString("auth_token", null)
        set(value) = prefs.edit().putString("auth_token", value).apply()
    
    var userId: Long
        get() = prefs.getLong("user_id", -1)
        set(value) = prefs.edit().putLong("user_id", value).apply()
    
    fun clear() = prefs.edit().clear().apply()
}

// Room Database
import androidx.room.*

@Entity(tableName = "users")
data class User(
    @PrimaryKey val id: Long,
    val name: String,
    val email: String,
    val avatarUrl: String?
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    suspend fun getAllUsers(): List<User>
    
    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: Long): User?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)
    
    @Delete
    suspend fun deleteUser(user: User)
}

@Database(entities = [User::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

-----

## React Native

### Component Structure

```tsx
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';

interface User {
  id: string;
  name: string;
  email: string;
}

export const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('https://api.example.com/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredUsers = users.filter(
    (user) =>
      user.name.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase())
  );

  const renderItem = ({ item }: { item: User }) => (
    <View style={styles.userCard}>
      <Text style={styles.userName}>{item.name}</Text>
      <Text style={styles.userEmail}>{item.email}</Text>
    </View>
  );

  if (loading) {
    return <ActivityIndicator size="large" />;
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.searchInput}
        placeholder="Search users..."
        value={search}
        onChangeText={setSearch}
      />
      <FlatList
        data={filteredUsers}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  searchInput: {
    margin: 10,
    padding: 10,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
  },
  userCard: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  userName: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  userEmail: {
    color: '#666',
  },
});
```

### React Navigation

```tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Text } from 'react-native';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeScreen() {
  return <Text>Home Screen</Text>;
}

function ProfileScreen() {
  return <Text>Profile Screen</Text>;
}

function SettingsScreen() {
  return <Text>Settings Screen</Text>;
}

function FeedScreen() {
  return <Text>Feed Screen</Text>;
}

function TabNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Feed" component={FeedScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Main"
          component={TabNavigator}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="UserDetail"
          component={UserDetailScreen}
          options={{ title: 'User Details' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

function UserDetailScreen({ route }: any) {
  const { userId } = route.params;
  return <Text>User ID: {userId}</Text>;
}
```

### State Management

```tsx
import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Define state and actions
interface AppState {
  user: User | null;
  isLoading: boolean;
  theme: 'light' | 'dark';
}

type AppAction =
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'TOGGLE_THEME' };

// Create context
const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

// Reducer
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'TOGGLE_THEME':
      return {
        ...state,
        theme: state.theme === 'light' ? 'dark' : 'light',
      };
    default:
      return state;
  }
}

// Provider
export function AppProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, {
    user: null,
    isLoading: false,
    theme: 'light',
  });

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// Custom hook
export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
```

-----

## Push Notifications

### iOS (APNs)

```swift
import UserNotifications
import UIKit

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        UNUserNotificationCenter.current().delegate = self
        requestNotificationPermission()
        return true
    }
    
    func requestNotificationPermission() {
        UNUserNotificationCenter.current().requestAuthorization(
            options: [.alert, .badge, .sound]
        ) { granted, _ in
            if granted {
                DispatchQueue.main.async {
                    UIApplication.shared.registerForRemoteNotifications()
                }
            }
        }
    }
    
    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
        // Send token to server
        APIClient.shared.registerDevice(token: token)
    }
}

extension AppDelegate: UNUserNotificationCenterDelegate {
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        return [.banner, .badge, .sound]
    }
    
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        let userInfo = response.notification.request.content.userInfo
        // Handle notification tap
    }
}
```

### Android (FCM)

```kotlin
import com.google.firebase.messaging.FirebaseMessagingService
import com.google.firebase.messaging.RemoteMessage

class MyFirebaseMessagingService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Send token to server
        sendTokenToServer(token)
    }
    
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        // Handle data payload
        remoteMessage.data.isNotEmpty().let {
            handleDataMessage(remoteMessage.data)
        }
        
        // Handle notification
        remoteMessage.notification?.let {
            showNotification(it.title, it.body)
        }
    }
    
    private fun showNotification(title: String?, body: String?) {
        // Show local notification
    }
}
```

### React Native Push Notifications

```tsx
import React, { useEffect } from 'react';
import { PermissionsAndroid, Platform } from 'react-native';
import PushNotification from 'react-native-push-notification';

PushNotification.configure({
  onRegister: function (token) {
    console.log('TOKEN:', token);
    // Send to server
  },
  onNotification: function (notification) {
    console.log('NOTIFICATION:', notification);
  },
  permissions: {
    alert: true,
    badge: true,
    sound: true,
  },
  popInitialNotification: true,
  requestPermissions: Platform.OS === 'ios',
});

export function PushNotificationProvider({ children }) {
  useEffect(() => {
    if (Platform.OS === 'android') {
      PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS
      );
    }
  }, []);

  return children;
}
```

-----

## Offline-First Architecture

### Local Database + Sync

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useEffect, useState } from 'react';

interface OfflineFirstOptions<T> {
  cacheKey: string;
  fetchData: () => Promise<T>;
  transform?: (data: T) => T;
}

function useOfflineFirst<T>({
  cacheKey,
  fetchData,
  transform,
}: OfflineFirstOptions<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    loadData();
  }, [cacheKey]);

  const loadData = async () => {
    try {
      // Try to fetch fresh data
      const freshData = await fetchData();
      const processed = transform ? transform(freshData) : freshData;
      
      // Cache it
      await AsyncStorage.setItem(cacheKey, JSON.stringify(processed));
      
      setData(processed);
    } catch (e) {
      // Fall back to cached data
      const cached = await AsyncStorage.getItem(cacheKey);
      if (cached) {
        setData(JSON.parse(cached));
      } else {
        setError(e as Error);
      }
    } finally {
      setLoading(false);
    }
  };

  const refresh = async () => {
    setLoading(true);
    await loadData();
  };

  return { data, loading, error, refresh };
}
```

### SQLite for Complex Data

```typescript
import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabaseSync('app.db');

export function initDatabase() {
  db.execAsync(`
    CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY,
      title TEXT,
      body TEXT,
      userId INTEGER,
      synced INTEGER DEFAULT 0
    );
    
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      name TEXT,
      email TEXT
    );
  `);
}

export async function getPosts() {
  return db.getAllAsync('SELECT * FROM posts');
}

export async function insertPost(post: any) {
  return db.runAsync(
    'INSERT INTO posts (title, body, userId, synced) VALUES (?, ?, ?, 0)',
    [post.title, post.body, post.userId]
  );
}

export async function getUnsyncedPosts() {
  return db.getAllAsync('SELECT * FROM posts WHERE synced = 0');
}

export async function markPostSynced(id: number) {
  return db.runAsync('UPDATE posts SET synced = 1 WHERE id = ?', [id]);
}
```

-----

## Best Practices

1. **Design for Multiple Screen Sizes** — Use responsive layouts that work on phones and tablets.

2. **Optimize Images** — Use appropriate sizes and formats for mobile.

3. **Handle Network States** — Gracefully handle offline, slow, and failed connections.

4. **Follow Platform Guidelines** — Respect iOS Human Interface Guidelines and Material Design.

5. **Test on Real Devices** — Emulators don't reflect real-world performance.

6. **Implement Proper Security** — Store sensitive data securely, use SSL pinning.

7. **Monitor Performance** — Track startup time, memory usage, and battery impact.

8. **Plan for App Store** — Understand review guidelines and prepare screenshots.
