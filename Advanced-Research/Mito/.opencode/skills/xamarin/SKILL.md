-----

## name: xamarin
description: >
Expert Xamarin and .NET MAUI cross-platform mobile development with C#. Use this skill
whenever the user mentions Xamarin, Xamarin.Forms, Xamarin.iOS, Xamarin.Android, .NET MAUI,
MVVM for mobile, DependencyService, Custom Renderers, Effects, or any C#/.NET mobile development.
Also trigger for: migrating Xamarin to MAUI, binding NuGet packages for mobile, platform-specific
implementations in C#, or building enterprise mobile apps with Azure backend integration.
Prefer this skill over generic C# advice for any mobile or cross-platform .NET scenario.
license: MIT
compatibility: opencode
metadata:
audience: mobile-developers
category: mobile-development

# Xamarin & .NET MAUI Development

> ⚠️ **Important**: Xamarin reached end-of-life in **May 2024**. For new projects, use **.NET MAUI** (its successor). This skill covers both — see the [Migration section](#xamarin-to-net-maui-migration) if you need to upgrade.

-----

## Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│                  Shared C# Code                        │
│   ViewModels · Services · Models · Business Logic      │
│          (Xamarin.Forms / .NET MAUI UI layer)          │
└────────────────┬───────────────────┬───────────────────┘
                 │                   │
     ┌───────────▼──────┐  ┌─────────▼──────────┐
     │  Xamarin.iOS /   │  │  Xamarin.Android /  │
     │   MAUI iOS       │  │   MAUI Android      │
     │  (AOT compiled)  │  │   (Mono runtime)    │
     └──────────────────┘  └────────────────────┘
```

-----

## MVVM Pattern (Standard Approach)

MVVM is the idiomatic pattern for Xamarin/MAUI. Always use it unless the project is a trivial prototype.

### ViewModel Base

```csharp
public class BaseViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));

    protected bool SetProperty<T>(ref T backingStore, T value,
        [CallerMemberName] string propertyName = "")
    {
        if (EqualityComparer<T>.Default.Equals(backingStore, value))
            return false;
        backingStore = value;
        OnPropertyChanged(propertyName);
        return true;
    }

    bool _isBusy;
    public bool IsBusy
    {
        get => _isBusy;
        set => SetProperty(ref _isBusy, value);
    }
}
```

### ViewModel with Commands and Async

```csharp
public class ProductListViewModel : BaseViewModel
{
    readonly IProductService _service;
    ObservableCollection<Product> _products = new();

    public ObservableCollection<Product> Products
    {
        get => _products;
        set => SetProperty(ref _products, value);
    }

    public ICommand LoadCommand { get; }
    public ICommand SelectCommand { get; }

    public ProductListViewModel(IProductService service)
    {
        _service = service;
        LoadCommand = new Command(async () => await LoadProductsAsync());
        SelectCommand = new Command<Product>(async p => await OnProductSelectedAsync(p));
    }

    async Task LoadProductsAsync()
    {
        if (IsBusy) return;
        IsBusy = true;
        try
        {
            Products.Clear();
            var items = await _service.GetProductsAsync();
            foreach (var item in items) Products.Add(item);
        }
        catch (Exception ex)
        {
            // Handle error — show alert, log, etc.
            Debug.WriteLine(ex);
        }
        finally { IsBusy = false; }
    }

    async Task OnProductSelectedAsync(Product product)
    {
        if (product == null) return;
        await Shell.Current.GoToAsync($"{nameof(ProductDetailPage)}?id={product.Id}");
    }
}
```

### XAML View (Xamarin.Forms)

```xml
<ContentPage xmlns="http://xamarin.com/schemas/2014/forms"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.ProductListPage">

    <ContentPage.BindingContext>
        <vm:ProductListViewModel />
    </ContentPage.BindingContext>

    <Shell.TitleView>
        <Label Text="Products" FontSize="18" FontAttributes="Bold" />
    </Shell.TitleView>

    <Grid>
        <CollectionView ItemsSource="{Binding Products}"
                        SelectionMode="Single"
                        SelectionChangedCommand="{Binding SelectCommand}"
                        SelectionChangedCommandParameter="{Binding SelectedItem,
                            Source={RelativeSource Self}}">
            <CollectionView.ItemTemplate>
                <DataTemplate>
                    <Grid Padding="16,8">
                        <Label Text="{Binding Name}" FontSize="16" />
                        <Label Text="{Binding Price, StringFormat='{0:C}'}"
                               HorizontalOptions="End" />
                    </Grid>
                </DataTemplate>
            </CollectionView.ItemTemplate>
        </CollectionView>
        <ActivityIndicator IsRunning="{Binding IsBusy}"
                           IsVisible="{Binding IsBusy}" />
    </Grid>
</ContentPage>
```

-----

## Dependency Injection & Services

### Interface + Platform Implementation Pattern

```csharp
// Shared interface
public interface IDeviceInfoService
{
    string GetDeviceId();
    bool IsTablet();
}

// Register with DI (MAUI style)
builder.Services.AddSingleton<IDeviceInfoService, DeviceInfoService>();
builder.Services.AddSingleton<IProductService, ProductService>();
builder.Services.AddTransient<ProductListViewModel>();
builder.Services.AddTransient<ProductListPage>();
```

> **Xamarin.Forms**: Use `DependencyService.Get<IDeviceInfoService>()` or a DI container like Prism/Splat.  
> **.NET MAUI**: Use built-in `Microsoft.Extensions.DependencyInjection`.

-----

## Shell Navigation

### Route Registration (.NET MAUI / Xamarin.Forms 5+)

```csharp
public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();
        Routing.RegisterRoute(nameof(ProductDetailPage), typeof(ProductDetailPage));
        Routing.RegisterRoute(nameof(CheckoutPage), typeof(CheckoutPage));
    }
}
```

### Navigate with Query Parameters

```csharp
// Navigate to detail page
await Shell.Current.GoToAsync($"{nameof(ProductDetailPage)}?id={product.Id}");

// Receive in target ViewModel
[QueryProperty(nameof(ProductId), "id")]
public class ProductDetailViewModel : BaseViewModel
{
    string _productId;
    public string ProductId
    {
        get => _productId;
        set
        {
            _productId = value;
            LoadProductCommand.Execute(null);
        }
    }
}
```

-----

## Platform-Specific Customization

### Effects (Lightweight — preferred for simple tweaks)

```csharp
// Shared: declare the effect
public class ShadowEffect : RoutingEffect
{
    public float Radius { get; set; } = 8;
    public Color Color { get; set; } = Color.Black;
    public ShadowEffect() : base("MyCompany.ShadowEffect") { }
}

// iOS platform implementation
[assembly: ResolutionGroupName("MyCompany")]
[assembly: ExportEffect(typeof(iOSShadowEffect), nameof(ShadowEffect))]
public class iOSShadowEffect : PlatformEffect
{
    protected override void OnAttached()
    {
        Control.Layer.ShadowColor = UIColor.Black.CGColor;
        Control.Layer.ShadowRadius = 8;
        Control.Layer.ShadowOpacity = 0.5f;
        Control.Layer.ShadowOffset = new CGSize(0, 4);
    }
    protected override void OnDetached() { }
}
```

### Custom Renderers (Full control over native rendering)

```csharp
// Shared custom control
public class RoundedEntry : Entry { }

// Android renderer
[assembly: ExportRenderer(typeof(RoundedEntry), typeof(RoundedEntryRenderer))]
public class RoundedEntryRenderer : EntryRenderer
{
    protected override void OnElementChanged(ElementChangedEventArgs<Entry> e)
    {
        base.OnElementChanged(e);
        if (Control != null)
        {
            var shape = new GradientDrawable();
            shape.SetCornerRadius(24f);
            shape.SetStroke(2, Android.Graphics.Color.Gray);
            Control.SetBackground(shape);
            Control.SetPadding(32, 16, 32, 16);
        }
    }
}
```

> **MAUI equivalent**: Use `IContentViewHandler` / `ConfigureMauiHandlers` — Renderers are replaced by Handlers in MAUI.

-----

## Data & Storage

### SQLite Local Database

```csharp
public class LocalDatabase
{
    readonly SQLiteAsyncConnection _db;

    public LocalDatabase(string dbPath)
    {
        _db = new SQLiteAsyncConnection(dbPath);
        _db.CreateTableAsync<Product>().Wait();
    }

    public Task<List<Product>> GetProductsAsync()
        => _db.Table<Product>().ToListAsync();

    public Task<int> SaveProductAsync(Product product)
        => product.Id == 0
            ? _db.InsertAsync(product)
            : _db.UpdateAsync(product);

    public Task<int> DeleteProductAsync(Product product)
        => _db.DeleteAsync(product);
}

// Register as singleton with platform DB path
string dbPath = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
    "myapp.db3");
builder.Services.AddSingleton(new LocalDatabase(dbPath));
```

### Secure Storage

```csharp
// Store
await SecureStorage.SetAsync("auth_token", token);

// Retrieve
var token = await SecureStorage.GetAsync("auth_token");

// Remove
SecureStorage.Remove("auth_token");
```

-----

## Azure Integration

```csharp
// Azure App Service Easy Auth + API call
public class AzureApiService
{
    readonly HttpClient _client;

    public AzureApiService()
    {
        _client = new HttpClient { BaseAddress = new Uri("https://myapp.azurewebsites.net") };
    }

    public async Task<List<Product>> GetProductsAsync(string token)
    {
        _client.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", token);
        var response = await _client.GetAsync("/api/products");
        response.EnsureSuccessStatusCode();
        var json = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<List<Product>>(json);
    }
}

// Azure Push Notifications (via Notification Hubs)
// In AppDelegate.cs (iOS):
public override void RegisteredForRemoteNotifications(
    UIApplication app, NSData token)
{
    var hub = new SBNotificationHub(connectionString, hubName);
    hub.RegisterNativeAsync(token, null, err => { /* handle */ });
}
```

-----

## Xamarin to .NET MAUI Migration

Key changes when migrating:

|Xamarin.Forms                   |.NET MAUI                           |
|--------------------------------|------------------------------------|
|`Application.Current.MainPage`  |`Window.Page`                       |
|`DependencyService`             |`Microsoft.Extensions.DI`           |
|Custom Renderers                |Handlers                            |
|`Device.BeginInvokeOnMainThread`|`MainThread.BeginInvokeOnMainThread`|
|`AssemblyInfo.cs` attributes    |`MauiProgram.cs` builder            |
|`Xamarin.Essentials`            |Built into MAUI                     |

### Migration Checklist

1. Upgrade to latest Xamarin.Forms (5.x) first
1. Update to .NET 6+ and remove `Xamarin.*` NuGet packages
1. Replace `App.xaml.cs` with `MauiProgram.cs`
1. Convert `DependencyService` registrations to `builder.Services`
1. Migrate Custom Renderers → Handlers (`Microsoft.Maui.Handlers`)
1. Replace `Device.RuntimePlatform` with `DeviceInfo.Platform`
1. Update XAML namespaces: `http://xamarin.com/schemas/2014/forms` → `http://schemas.microsoft.com/dotnet/2021/maui`

-----

## Common Patterns Quick Reference

- **Loading state**: Use `IsBusy` + `ActivityIndicator` bound to it
- **Error handling**: Try/catch in ViewModels, surface via `DisplayAlert` or an error service
- **Platform checks**: `DeviceInfo.Platform == DevicePlatform.iOS`
- **Connectivity**: `Connectivity.NetworkAccess == NetworkAccess.Internet`
- **File paths**: Always use `Environment.GetFolderPath()` — never hardcode paths
- **Main thread**: `MainThread.BeginInvokeOnMainThread(() => { ... })` for UI updates from background threads
- **Image caching**: Use `FFImageLoading` (Xamarin) or built-in `Image` caching (MAUI)