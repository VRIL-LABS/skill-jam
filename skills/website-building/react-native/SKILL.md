---
name: website-building-react-native
description: React Native & Expo styling guidance — NativeWind, design tokens, navigation, platform-specific UI. Use alongside the parent website-building skill's design foundations.
user-invocable: false
---

# React Native & Expo — Styling & Design

Framework-specific guidance for **React Native 0.81+ / Expo SDK 54+** projects. Read alongside the parent `website-building` skill's `shared/01-design-tokens.md` and `shared/02-typography.md` for color palette and typography principles.

## Version Requirements

- **React Native**: 0.81 (New Architecture on by default)
- **Expo SDK**: 54 (recommended — XCFrameworks for iOS, React 19 support)
- **React**: 19.2
- **NativeWind**: 4.x (Tailwind CSS for React Native)
- **Expo Router**: v4 (file-based navigation)

## Creating a New Project

```bash
# Expo (recommended — managed workflow, easier setup)
npx create-expo-app@latest my-app
cd my-app
npx expo start

# With Expo Router template (file-based routing):
npx create-expo-app@latest my-app --template tabs
```

## Tailwind for React Native — NativeWind v4

NativeWind brings Tailwind utility classes to React Native. It compiles Tailwind classes to StyleSheet at build time.

### Installation

```bash
npm install nativewind
npm install --save-dev tailwindcss@^3 postcss
npx tailwindcss init
```

> **Note:** NativeWind v4 uses Tailwind CSS v3 under the hood (not v4). Do not use Tailwind v4 with NativeWind yet.

### Configuration

**`tailwind.config.js`:**
```js
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Nexus palette for React Native
        background: "#F7F6F2",
        surface: "#F9F8F5",
        border: "#D4D1CA",
        "text-primary": "#28251D",
        "text-muted": "#7A7974",
        primary: "#01696F",
        "primary-dark": "#4F98A3", // dark mode variant
      },
    },
  },
  plugins: [],
}
```

**`babel.config.js`:**
```js
module.exports = {
  presets: [
    ["babel-preset-expo", { jsxImportSource: "nativewind" }],
    "nativewind/babel",
  ],
}
```

**`app/_layout.tsx`:**
```tsx
import { cssInterop } from "nativewind"
// Register components you want to accept className prop
cssInterop(Image, { className: "style" })
```

### Using NativeWind Classes

```tsx
import { View, Text, TouchableOpacity } from "react-native"

export function Card({ title, onPress }) {
  return (
    <View className="bg-surface rounded-lg p-4 border border-border shadow-sm">
      <Text className="text-text-primary text-base font-semibold mb-2">
        {title}
      </Text>
      <TouchableOpacity
        className="bg-primary rounded-md py-2 px-4 active:opacity-80"
        onPress={onPress}
      >
        <Text className="text-white text-sm font-medium text-center">
          Tap me
        </Text>
      </TouchableOpacity>
    </View>
  )
}
```

## Navigation — Expo Router v4

Expo Router uses file-based routing (like Next.js App Router, but for React Native).

```
app/
├── _layout.tsx        # Root layout
├── index.tsx          # / (Home screen)
├── (tabs)/
│   ├── _layout.tsx    # Tab bar layout
│   ├── home.tsx       # /home tab
│   └── profile.tsx    # /profile tab
└── [id].tsx           # Dynamic route
```

### Stack Navigation

```tsx
// app/_layout.tsx
import { Stack } from "expo-router"

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Home" }} />
      <Stack.Screen name="detail/[id]" options={{ title: "Detail" }} />
    </Stack>
  )
}
```

### Tab Navigation

```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from "expo-router"
import { House, User, Settings } from "lucide-react-native"

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: "#01696F" }}>
      <Tabs.Screen
        name="home"
        options={{
          title: "Home",
          tabBarIcon: ({ color }) => <House size={24} color={color} />,
        }}
      />
    </Tabs>
  )
}
```

## Design System for React Native

### Core Differences from Web

| Web | React Native |
|---|---|
| `div` | `View` |
| `p`, `span` | `Text` (ALL text must be in `<Text>`) |
| `img` | `Image` |
| `button` | `TouchableOpacity` or `Pressable` |
| CSS Flexbox (row default) | Flexbox (column default) |
| `px`, `em`, `rem` | Unitless numbers (device-independent pixels) |
| `position: fixed` | N/A — use absolute + SafeAreaView |
| `overflow: scroll` | `ScrollView` or `FlatList` |

### Typography in React Native

```tsx
import { Text, StyleSheet } from "react-native"

// Scale equivalent to design tokens (use sp units via StyleSheet)
const styles = StyleSheet.create({
  heroText:    { fontSize: 48, fontWeight: "900", lineHeight: 56 },
  h1:          { fontSize: 32, fontWeight: "700", lineHeight: 40 },
  h2:          { fontSize: 24, fontWeight: "700", lineHeight: 32 },
  body:        { fontSize: 16, fontWeight: "400", lineHeight: 24 },
  small:       { fontSize: 14, fontWeight: "400", lineHeight: 20 },
  caption:     { fontSize: 12, fontWeight: "400", lineHeight: 16 },
})
```

**NativeWind equivalent:**
```tsx
<Text className="text-4xl font-black leading-tight">Hero</Text>  {/* 36px */}
<Text className="text-2xl font-bold">Heading</Text>              {/* 24px */}
<Text className="text-base">Body text</Text>                     {/* 16px */}
<Text className="text-sm text-text-muted">Caption</Text>         {/* 14px */}
```

### Touch Targets

- **Minimum 44×44dp** for all interactive elements (iOS HIG and Android guidelines)
- Use `hitSlop` for small icons:

```tsx
<TouchableOpacity
  hitSlop={{ top: 12, right: 12, bottom: 12, left: 12 }}
  onPress={onPress}
>
  <ChevronRight size={20} />
</TouchableOpacity>
```

### Safe Areas

Always account for notches, home indicators, and status bars:

```bash
npx expo install react-native-safe-area-context
```

```tsx
import { SafeAreaView } from "react-native-safe-area-context"

export default function Screen() {
  return (
    <SafeAreaView className="flex-1 bg-background">
      {/* content */}
    </SafeAreaView>
  )
}
```

### Platform-Specific Styling

```tsx
import { Platform, StyleSheet } from "react-native"

// Method 1: Platform.select
const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: "#000",
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.12,
      shadowRadius: 6,
    },
    android: {
      elevation: 4,
    },
  }),
})

// Method 2: Platform-specific files
// Button.ios.tsx → used on iOS
// Button.android.tsx → used on Android
// Button.tsx → fallback
```

### Dark Mode in React Native

```tsx
import { useColorScheme } from "react-native"

// Or with NativeWind (automatically respects system dark mode):
// className="bg-background dark:bg-background-dark"

// Programmatic:
const colorScheme = useColorScheme() // 'light' | 'dark'
const isDark = colorScheme === "dark"
```

## Icons in React Native

```bash
npx expo install lucide-react-native react-native-svg
```

```tsx
import { Home, User, Settings } from "lucide-react-native"

// <Home size={24} color="#01696F" />
// <User size={20} color={colors.textMuted} strokeWidth={1.5} />
```

## Performance Best Practices

- **FlatList over ScrollView** for long lists — virtualized rendering
- **`React.memo`** for components that re-render often
- **`useCallback`/`useMemo`** for stable references passed to list items
- **New Architecture (Fabric + JSI)** is on by default in RN 0.81 — avoid legacy bridge APIs
- **Hermes engine** (default) — faster startup, better memory

## Expo-Specific Features

### Expo Router Link (like Next.js Link)

```tsx
import { Link } from "expo-router"

// <Link href="/profile">
//   <Text>Go to Profile</Text>
// </Link>

// <Link href="/user/123" asChild>
//   <TouchableOpacity>
//     <Text>View User</Text>
//   </TouchableOpacity>
// </Link>
```

### Expo Image (optimized, like next/image)

```bash
npx expo install expo-image
```

```tsx
import { Image } from "expo-image"

// <Image
//   source="https://example.com/photo.jpg"
//   style={{ width: 200, height: 200 }}
//   contentFit="cover"
//   transition={300}
//   placeholder={blurhash}
// />
```

## Checklist for React Native / Expo Projects

- [ ] Using Expo SDK 54+ with React Native 0.81
- [ ] NativeWind v4 installed and configured (uses Tailwind v3 config)
- [ ] Expo Router v4 for file-based navigation
- [ ] All text inside `<Text>` components (React Native requirement)
- [ ] Touch targets ≥ 44×44dp everywhere
- [ ] SafeAreaView wrapping all screens
- [ ] Platform-specific shadows (iOS shadowProps vs Android elevation)
- [ ] Dark mode via `useColorScheme` or NativeWind dark: variant
- [ ] `expo-image` for optimized image loading
- [ ] `lucide-react-native` for icons
