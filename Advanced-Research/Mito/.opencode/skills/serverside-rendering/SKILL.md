---
name: serverside-rendering
description: >
  Expert guidance on server-side rendering for improved performance and SEO. Use for: 
  React SSR with Next.js, Vue SSR with Nuxt, hydration strategies, server state management, 
  streaming SSR, edge rendering, caching strategies, SEO optimization, and building 
  performance-critical web applications.
license: MIT
compatibility: opencode
metadata:
  audience: web-developers
  category: web-development
  tags: [ssr, nextjs, hydration, seo, rendering]
---

# Server-Side Rendering — Implementation Guide

Covers: **Next.js SSR · Nuxt SSR · Hydration · Streaming · Edge Rendering · SEO Optimization · Caching**

-----

## Understanding SSR

### How Server-Side Rendering Works

Server-side rendering generates complete HTML pages on the server in response to client requests. Unlike client-side rendering where the browser builds the page after downloading JavaScript, SSR delivers ready-to-render HTML that improves perceived performance, enables better SEO, and provides optimal experience on slow devices.

The rendering process involves multiple steps: the server receives a request for a page, executes the application code to generate the component tree, fetches any required data from databases or APIs, renders the components to HTML, and sends the complete HTML document to the browser. The browser can display this HTML immediately while downloading and executing JavaScript for hydration.

**Key Benefits:**

- **Faster First Contentful Paint** — Users see content before JavaScript loads.
- **Better SEO** — Search engines can crawl fully rendered content.
- **Improved Performance on Slow Devices** — Less JavaScript processing on client.
- **Social Media Previews** — Open Graph tags work reliably.

**Trade-offs:**

- **Increased Server Load** — Each request requires server rendering.
- **Time to First Byte** — Server processing adds latency.
- **Complex Caching** — Requires careful cache strategy.
- **Hydration Cost** — Client must still process JavaScript.

### SSR vs SSG vs ISR

| Approach | When HTML Generated | Use Case |
|----------|-------------------|----------|
| **SSR** (Server-Side Rendering) | Request time | Dynamic, personalized content |
| **SSG** (Static Site Generation) | Build time | Documentation, blogs, marketing |
| **ISR** (Incremental Static Regeneration) | Request + background | Content that updates periodically |
| **Edge Rendering** | Edge location | Global, low-latency content |

-----

## Next.js SSR

### App Router (Next.js 13+)

```javascript
// app/page.tsx - Server Component by default
import { getData } from '@/lib/api';

async function getServerData() {
  const res = await fetch('https://api.example.com/data', {
    // Cache configuration
    cache: 'no-store',  // Don't cache, fetch fresh each time
    // or: cache: 'force-cache'  // Static generation
    // or: next: { revalidate: 3600 }  // ISR - revalidate every hour
  });
  
  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }
  
  return res.json();
}

export default async function Page() {
  // This component runs on the server
  const data = await getData();
  
  return (
    <main>
      <h1>{data.title}</h1>
      <p>{data.description}</p>
      <ul>
        {data.items.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </main>
  );
}
```

### Client Components with SSR

```javascript
// app/components/Counter.tsx - Client Component
'use client';

import { useState } from 'react';

export default function Counter({ initialCount = 0 }) {
  const [count, setCount] = useState(initialCount);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}

// app/page.tsx - Using client component in server component
import Counter from './components/Counter';
import { getInitialCount } from '@/lib/api';

export default async function Page() {
  const initialCount = await getInitialCount();
  
  return (
    <main>
      <h1>Server-Rendered Page</h1>
      <Counter initialCount={initialCount} />
    </main>
  );
}
```

### Data Fetching Patterns

```javascript
// Parallel data fetching - fetch in parallel for performance
import { getUser, getPosts } from '@/lib/api';

export default async function Page() {
  // Start both fetches simultaneously
  const userData = getUser();
  const postsData = getPosts();
  
  // Wait for both
  const [user, posts] = await Promise.all([userData, postsData]);
  
  return (
    <div>
      <h1>{user.name}</h1>
      <PostsList posts={posts} />
    </div>
  );
}

// Sequential fetching - when data depends on previous
export default async function Page() {
  const user = await getCurrentUser();
  
  if (!user) {
    redirect('/login');
  }
  
  const settings = await getUserSettings(user.id);
  
  return <SettingsPage user={user} settings={settings} />;
}

// Streaming with Suspense - show shell while loading
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<PostsSkeleton />}>
        <PostsList />
      </Suspense>
      <Suspense fallback={<CommentsSkeleton />}>
        <CommentsList />
      </Suspense>
    </div>
  );
}

async function PostsList() {
  const posts = await getPosts();
  return <PostCards posts={posts} />;
}
```

### Route Handlers (API Routes)

```javascript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = searchParams.get('page') || '1';
  const limit = searchParams.get('limit') || '10';
  
  const users = await fetchUsers(parseInt(page), parseInt(limit));
  
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  // Validate
  if (!body.email || !body.name) {
    return NextResponse.json(
      { error: 'Missing required fields' },
      { status: 400 }
    );
  }
  
  const user = await createUser(body);
  
  return NextResponse.json(user, { status: 201 });
}

// With caching
export async function GET() {
  const data = await getExpensiveData();
  
  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400'
    }
  });
}
```

-----

## Hydration Strategies

### Understanding Hydration

Hydration is the process where client-side JavaScript takes over the server-rendered HTML, attaching event listeners and making the page interactive. Understanding hydration is crucial for optimizing performance, as poorly optimized hydration can lead to slow Time to Interactive (TTI).

**Hydration Challenges:**

- Large bundle sizes delay interactivity
- Component trees with many nodes take time to hydrate
- Third-party scripts compete for resources
- Heavy computation during hydration blocks interaction

### Partial Hydration

```javascript
// Strategy 1: Lazy load non-critical components
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(
  () => import('./HeavyChart'),
  { 
    loading: () => <ChartSkeleton />,
    ssr: false  // Don't render on server
  }
);

export default function Dashboard({ data }) {
  return (
    <div>
      <SummaryCards data={data} />
      {/* Chart loads after initial render */}
      <HeavyChart data={data.chartData} />
    </div>
  );
}

// Strategy 2: use client boundary
// components/InteractiveMap.tsx
'use client';

import { useState, useEffect } from 'react';

export default function InteractiveMap({ markers }) {
  const [map, setMap] = useState(null);
  
  useEffect(() => {
    // Load map library only on client
    initMap().then(setMap);
  }, []);
  
  return <div id="map" />;
}

// Only hydrate the interactive part
```

### Selective Hydration

```javascript
// components/CommentSection.tsx
'use client';

import { useState } from 'react';

export default function CommentSection({ initialComments }) {
  const [comments, setComments] = useState(initialComments);
  
  // Only interactive parts hydrate
  return (
    <div>
      {comments.map(comment => (
        <Comment key={comment.id} data={comment} />
      ))}
      
      <AddCommentForm onSubmit={addComment} />
    </div>
  );
}

// components/Comment.tsx - Can stay static if no interactivity
export default function Comment({ data }) {
  // Static display - no client JS needed
  return (
    <article>
      <strong>{data.author}</strong>
      <p>{data.text}</p>
    </article>
  );
}
```

### Hydration Error Handling

```javascript
// lib/hydration-manager.tsx
'use client';

import { useState, useEffect } from 'react';

export function useHydrated() {
  const [hydrated, setHydrated] = useState(false);
  
  useEffect(() => {
    setHydrated(true);
  }, []);
  
  return hydrated;
}

export function ClientOnly({ children, fallback = null }) {
  const hydrated = useHydrated();
  
  return hydrated ? children : fallback;
}

// Usage
import { ClientOnly } from '@/lib/hydration-manager';

export default function Page() {
  return (
    <div>
      <ServerRenderedContent />
      
      <ClientOnly fallback={<Skeleton />}>
        <ClientSideOnlyComponent />
      </ClientOnly>
    </div>
  );
}
```

-----

## Streaming and Suspense

### Streaming SSR

```javascript
// Enable streaming in Next.js (default in App Router)
// Just use Suspense boundaries

import { Suspense } from 'react';

export default function Page() {
  return (
    <div className="layout">
      <Header />  {/* Immediate render */}
      
      <Suspense fallback={<FeedSkeleton />}>
        <Feed />  {/* Streams in when ready */}
      </Suspense>
      
      <Suspense fallback={<SidebarSkeleton />}>
        <Sidebar />  {/* Independent stream */}
      </Suspense>
      
      <Footer />  {/* Immediate render */}
    </div>
  );
}

// components/Feed.tsx
async function Feed() {
  const posts = await getPosts();
  
  return (
    <ul>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </ul>
  );
}
```

### Suspense with Error Boundaries

```javascript
// components/ErrorBoundary.tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: any) {
    console.error('Error in component:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    
    return this.props.children;
  }
}

// Usage with Suspense
export default function Page() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <Suspense fallback={<Loading />}>
        <Content />
      </Suspense>
    </ErrorBoundary>
  );
}
```

-----

## Edge Rendering

### Edge Functions

```javascript
// app/api/hello/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  return new Response('Hello from the edge!', {
    headers: { 'content-type': 'text/plain' }
  });
}

// Edge middleware
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Geo-based routing
  const country = request.geo?.country || 'US';
  
  if (country === 'DE') {
    return NextResponse.redirect(new URL('/de', request.url));
  }
  
  // A/B testing
  const bucket = Math.random() < 0.5 ? 'a' : 'b';
  const response = NextResponse.next();
  response.cookies.set('ab-test', bucket);
  
  return response;
}

export const config = {
  matcher: '/:path*',
};
```

### Edge Caching Strategies

```javascript
// app/products/[id]/page.tsx
export const runtime = 'edge';
export const dynamic = 'force-dynamic';

export default async function ProductPage({ params }) {
  const product = await getProduct(params.id);
  
  return <ProductDetails product={product} />;
}

// For static content with edge caching
export async function generateStaticParams() {
  const products = await getAllProducts();
  
  return products.map((product) => ({
    id: product.id,
  }));
}

export const revalidate = 3600;  // Revalidate at edge every hour
```

-----

## Caching Strategies

### Route Cache Configuration

```javascript
// app/blog/[slug]/page.tsx

// Static generation at build time
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

// ISR - revalidate every hour
export const revalidate = 3600;

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  
  return <Article post={post} />;
}

// Cache tags for on-demand revalidation
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id);
  
  return <Product product={product} />;
}

export async function generateStaticParams() {
  const products = await getAllProducts();
  return products.map((p) => ({ id: p.id }));
}

// Using fetch cache options
const res = await fetch(`https://api.example.com/products/${params.id}`, {
  next: {
    revalidate: 60,  // Cache for 60 seconds
    tags: ['products'],  // For on-demand invalidation
  },
});
```

### On-Demand Revalidation

```javascript
// app/api/revalidate/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { revalidateTag, revalidatePath } from 'next/cache';

export async function POST(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get('secret');
  
  // Verify secret token
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ message: 'Invalid token' }, { status: 401 });
  }
  
  const body = await request.json();
  const { tag, path } = body;
  
  if (tag) {
    revalidateTag(tag);
    return NextResponse.json({ revalidated: true, tag });
  }
  
  if (path) {
    revalidatePath(path);
    return NextResponse.json({ revalidated: true, path });
  }
  
  return NextResponse.json({ message: 'Missing tag or path' }, { status: 400 });
}

// Webhook handler for CMS updates
// app/api/cms-webhook/route.ts
export async function POST(request: NextRequest) {
  const body = await request.json();
  
  if (body.type === 'post_updated') {
    revalidateTag('posts');
    revalidatePath('/blog');
  }
  
  return NextResponse.json({ received: true });
}
```

-----

## SEO Optimization

### Metadata API

```javascript
// app/layout.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'My Awesome Site',
    template: '%s | My Awesome Site',
  },
  description: 'Description of my awesome website',
  openGraph: {
    title: 'My Awesome Site',
    description: 'Description of my awesome website',
    url: 'https://myawesomesite.com',
    siteName: 'My Awesome Site',
    images: [
      {
        url: 'https://myawesomesite.com/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'My Awesome Site',
    creator: '@username',
  },
  robots: {
    index: true,
    follow: true,
  },
};

// Dynamic metadata
export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await getProduct(params.id);
  
  return {
    title: product.name,
    description: product.description,
    openGraph: {
      images: [product.image],
    },
  };
}
```

### Structured Data

```javascript
// components/ProductSchema.tsx
export function ProductSchema({ product }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.images,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: product.currency,
      availability: product.inStock 
        ? 'https://schema.org/InStock' 
        : 'https://schema.org/OutOfStock',
    },
    aggregateRating: product.rating ? {
      '@type': 'AggregateRating',
      ratingValue: product.rating.value,
      reviewCount: product.rating.count,
    } : undefined,
  };
  
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

// JSON-LD for organization
export function OrganizationSchema() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Company Name',
    url: 'https://company.com',
    logo: 'https://company.com/logo.png',
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+1-555-555-5555',
      contactType: 'customer service',
    },
  };
  
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

### Sitemap Generation

```javascript
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://myawesomesite.com';
  
  // Fetch dynamic content
  const posts = await getAllPosts();
  const products = await getAllProducts();
  
  const staticPages = [
    '',
    '/about',
    '/contact',
    '/pricing',
  ].map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority: route === '' ? 1 : 0.8,
  }));
  
  const blogPosts = posts.map((post) => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));
  
  const productPages = products.map((product) => ({
    url: `${baseUrl}/products/${product.id}`,
    lastModified: new Date(product.updatedAt),
    changeFrequency: 'daily' as const,
    priority: 0.9,
  }));
  
  return [...staticPages, ...blogPosts, ...productPages];
}
```

-----

## Performance Optimization

### Bundle Analysis

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  experimental: {
    optimizePackageImports: ['lodash', 'moment', 'antd'],
  },
  webpack: (config, { isServer }) => {
    // Optimize third-party imports
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
});
```

### Font Optimization

```javascript
// app/layout.tsx
import { Inter, JetBrains_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

### Image Optimization

```javascript
// components/OptimizedImage.tsx
import Image from 'next/image';

export function ProductImage({ src, alt, priority = false }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={600}
      height={400}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      priority={priority}
      placeholder="blur"
      blurDataURL={generateBlurPlaceholder(src)}
    />
  );
}

// Use responsive sizes properly
export function Gallery({ images }) {
  return (
    <div className="gallery">
      {images.map((img) => (
        <Image
          key={img.id}
          src={img.src}
          alt={img.alt}
          fill
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          style={{ objectFit: 'cover' }}
        />
      ))}
    </div>
  );
}
```

-----

## Best Practices

1. **Default to Server Components** — Only use client components when necessary for interactivity.

2. **Minimize Client Bundle** — Import server-only modules at the top level.

3. **Use Streaming Strategically** — Wrap slow data fetches in Suspense boundaries.

4. **Implement Proper Caching** — Use appropriate cache strategies for each data type.

5. **Optimize Images and Fonts** — Use Next.js built-in optimizations.

6. **Monitor Core Web Vitals** — Track LCP, FID, and CLS in production.

7. **Use Edge Functions Judiciously** — They're fast but have limits on computation.

8. **Plan for Incremental Migration** — You don't need to convert everything at once.
