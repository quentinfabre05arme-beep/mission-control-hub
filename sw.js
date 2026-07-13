/**
 * Mission Control v9.1 Service Worker
 * Provides offline capability, background sync, and push notifications
 * 
 * @version 9.1.0
 * @author Mission Control Team
 */

// ============================================
// CONFIGURATION
// ============================================

const CACHE_VERSION = 'v9.1.0';
const STATIC_CACHE = `mission-control-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `mission-control-dynamic-${CACHE_VERSION}`;
const IMAGE_CACHE = `mission-control-images-${CACHE_VERSION}`;

// URLs to cache on install
const STATIC_ASSETS = [
    '/',
    '/mission_control_mobile_pwa.html',
    '/manifest.json',
    // CDN resources - these will be cached on first fetch
];

// URLs to never cache
const NETWORK_ONLY = [
    '/api/sync',
    '/api/realtime',
    '/api/auth'
];

// Cache duration strategies (in milliseconds)
const CACHE_STRATEGIES = {
    static: { maxAge: 30 * 24 * 60 * 60 * 1000, maxEntries: 100 },    // 30 days
    dynamic: { maxAge: 7 * 24 * 60 * 60 * 1000, maxEntries: 200 },   // 7 days
    images: { maxAge: 30 * 24 * 60 * 60 * 1000, maxEntries: 300 }    // 30 days
};

// ============================================
// INSTALL EVENT
// ============================================

self.addEventListener('install', (event) => {
    console.log('[SW] Installing Service Worker v9.1.0...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('[SW] Caching static assets...');
                // Cache the main app shell
                return cache.addAll(STATIC_ASSETS).catch(err => {
                    console.warn('[SW] Some assets failed to cache:', err);
                });
            })
            .then(() => {
                console.log('[SW] Static assets cached successfully');
                return self.skipWaiting();
            })
            .catch((error) => {
                console.error('[SW] Installation failed:', error);
            })
    );
});

// ============================================
// ACTIVATE EVENT
// ============================================

self.addEventListener('activate', (event) => {
    console.log('[SW] Activating Service Worker...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                // Delete old caches
                return Promise.all(
                    cacheNames
                        .filter((name) => {
                            return name.startsWith('mission-control-') && 
                                   !name.includes(CACHE_VERSION);
                        })
                        .map((name) => {
                            console.log('[SW] Deleting old cache:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW] Old caches cleaned up');
                return self.clients.claim();
            })
    );
});

// ============================================
// FETCH EVENT - CACHING STRATEGIES
// ============================================

self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }
    
    // Skip network-only URLs
    if (NETWORK_ONLY.some(path => url.pathname.includes(path))) {
        event.respondWith(fetch(request));
        return;
    }
    
    // Skip chrome-extension and other non-http(s) requests
    if (!url.protocol.startsWith('http')) {
        return;
    }
    
    // Strategy based on request type
    if (isStaticAsset(url)) {
        event.respondWith(staleWhileRevalidate(request, STATIC_CACHE));
    } else if (isImage(request)) {
        event.respondWith(cacheFirst(request, IMAGE_CACHE));
    } else if (isAPI(request)) {
        event.respondWith(networkFirst(request, DYNAMIC_CACHE));
    } else {
        event.respondWith(networkFirst(request, DYNAMIC_CACHE));
    }
});

// ============================================
// CACHING STRATEGY IMPLEMENTATIONS
// ============================================

/**
 * Cache First Strategy - Good for images
 * Returns cache if available, otherwise fetches and caches
 */
async function cacheFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    
    if (cached) {
        // Return cached but refresh in background
        refreshCache(request, cacheName);
        return cached;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            await cache.put(request, response.clone());
            await cleanCache(cacheName, CACHE_STRATEGIES.images.maxEntries);
        }
        return response;
    } catch (error) {
        console.error('[SW] Fetch failed:', error);
        // Return offline fallback for images
        return new Response('', { status: 404, statusText: 'Not cached' });
    }
}

/**
 * Network First Strategy - Good for API calls and dynamic content
 * Tries network first, falls back to cache
 */
async function networkFirst(request, cacheName) {
    const cache = await caches.open(cacheName);
    
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            await cache.put(request, networkResponse.clone());
            await cleanCache(cacheName, CACHE_STRATEGIES.dynamic.maxEntries);
        }
        
        return networkResponse;
    } catch (error) {
        console.log('[SW] Network failed, trying cache:', request.url);
        const cached = await cache.match(request);
        
        if (cached) {
            // Add header to indicate cached response
            const headers = new Headers(cached.headers);
            headers.set('X-SW-Cache', 'HIT');
            
            return new Response(cached.body, {
                status: cached.status,
                statusText: cached.statusText,
                headers: headers
            });
        }
        
        // Return offline page for HTML requests
        if (request.headers.get('Accept')?.includes('text/html')) {
            return cache.match('/mission_control_mobile_pwa.html');
        }
        
        throw error;
    }
}

/**
 * Stale While Revalidate Strategy - Good for static assets
 * Returns cached version immediately, updates cache in background
 */
async function staleWhileRevalidate(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cached = await cache.match(request);
    
    const fetchPromise = fetch(request)
        .then((response) => {
            if (response.ok) {
                cache.put(request, response.clone());
            }
            return response;
        })
        .catch(() => cached);
    
    return cached || fetchPromise;
}

/**
 * Background cache refresh
 */
async function refreshCache(request, cacheName) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            const cache = await caches.open(cacheName);
            await cache.put(request, response);
        }
    } catch (error) {
        // Silent fail - we already returned cached version
    }
}

// ============================================
// CACHE MANAGEMENT
// ============================================

async function cleanCache(cacheName, maxEntries) {
    const cache = await caches.open(cacheName);
    const keys = await cache.keys();
    
    if (keys.length > maxEntries) {
        // Remove oldest entries (FIFO)
        const keysToDelete = keys.slice(0, keys.length - maxEntries);
        await Promise.all(keysToDelete.map(key => cache.delete(key)));
        console.log('[SW] Cleaned cache:', cacheName, 'removed', keysToDelete.length, 'entries');
    }
}

function isStaticAsset(url) {
    const staticExtensions = ['.js', '.css', '.json', '.woff', '.woff2'];
    return staticExtensions.some(ext => url.pathname.endsWith(ext));
}

function isImage(request) {
    const imageTypes = ['image/', 'img', 'pic'];
    const accept = request.headers.get('Accept') || '';
    const url = request.url.toLowerCase();
    
    return imageTypes.some(type => accept.includes(type) || url.includes(type));
}

function isAPI(request) {
    const url = new URL(request.url);
    return url.pathname.includes('/api/') || 
           url.pathname.includes('/data/') ||
           request.headers.get('Accept')?.includes('application/json');
}

// ============================================
// BACKGROUND SYNC
// ============================================

self.addEventListener('sync', (event) => {
    console.log('[SW] Background sync triggered:', event.tag);
    
    if (event.tag === 'sync-data') {
        event.waitUntil(syncData());
    } else if (event.tag === 'sync-posts') {
        event.waitUntil(syncPendingPosts());
    } else if (event.tag === 'sync-analytics') {
        event.waitUntil(syncAnalytics());
    }
});

async function syncData() {
    try {
        // Notify clients that sync is complete
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'SYNC_COMPLETE',
                timestamp: Date.now()
            });
        });
        
        console.log('[SW] Data sync completed');
    } catch (error) {
        console.error('[SW] Data sync failed:', error);
        throw error;
    }
}

async function syncPendingPosts() {
    // Implementation for syncing pending posts
    console.log('[SW] Syncing pending posts...');
}

async function syncAnalytics() {
    // Implementation for syncing analytics
    console.log('[SW] Syncing analytics...');
}

// ============================================
// PUSH NOTIFICATIONS
// ============================================

self.addEventListener('push', (event) => {
    console.log('[SW] Push received:', event);
    
    let data = {};
    try {
        data = event.data ? event.data.json() : {};
    } catch (e) {
        data = { title: 'Mission Control', body: event.data?.text() || 'New update' };
    }
    
    const options = {
        body: data.body || 'You have a new notification',
        icon: data.icon || '/icons/icon-192x192.png',
        badge: data.badge || '/icons/icon-72x72.png',
        tag: data.tag || 'mission-control',
        requireInteraction: data.requireInteraction || false,
        silent: data.silent || false,
        vibrate: data.vibrate || [200, 100, 200],
        actions: data.actions || [
            {
                action: 'open',
                title: 'Open',
                icon: '/icons/action-open.png'
            },
            {
                action: 'dismiss',
                title: 'Dismiss',
                icon: '/icons/action-dismiss.png'
            }
        ],
        data: {
            url: data.url || '/mission_control_mobile_pwa.html',
            timestamp: Date.now(),
            ...data.data
        }
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'Mission Control', options)
    );
});

// ============================================
// NOTIFICATION CLICK HANDLING
// ============================================

self.addEventListener('notificationclick', (event) => {
    console.log('[SW] Notification clicked:', event);
    
    event.notification.close();
    
    const { action, notification } = event;
    const data = notification.data || {};
    
    if (action === 'dismiss') {
        return;
    }
    
    // Default action: open app
    event.waitUntil(
        self.clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // Focus existing window if available
                for (const client of clientList) {
                    if (client.url.includes('mission_control') && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Open new window
                if (self.clients.openWindow) {
                    return self.clients.openWindow(data.url || '/mission_control_mobile_pwa.html');
                }
            })
    );
});

// ============================================
// MESSAGE HANDLING (from main thread)
// ============================================

self.addEventListener('message', (event) => {
    console.log('[SW] Message received:', event.data);
    
    const { type, payload } = event.data;
    
    switch (type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'CLEAR_CACHE':
            event.waitUntil(clearAllCaches());
            break;
            
        case 'GET_CACHE_SIZE':
            event.waitUntil(
                getCacheSize().then(size => {
                    event.ports[0].postMessage({ size });
                })
            );
            break;
            
        case 'SCHEDULE_NOTIFICATION':
            // Store notification for later
            scheduleNotification(payload);
            break;
            
        default:
            console.log('[SW] Unknown message type:', type);
    }
});

async function clearAllCaches() {
    const cacheNames = await caches.keys();
    await Promise.all(cacheNames.map(name => caches.delete(name)));
    console.log('[SW] All caches cleared');
}

async function getCacheSize() {
    let totalSize = 0;
    const cacheNames = await caches.keys();
    
    for (const name of cacheNames) {
        const cache = await caches.open(name);
        const requests = await cache.keys();
        
        for (const request of requests) {
            const response = await cache.match(request);
            if (response) {
                const blob = await response.blob();
                totalSize += blob.size;
            }
        }
    }
    
    return totalSize;
}

// Store scheduled notifications (simple in-memory store)
const scheduledNotifications = new Map();

function scheduleNotification(payload) {
    const { id, title, body, timestamp, delay } = payload;
    
    if (delay && delay > 0) {
        setTimeout(() => {
            self.registration.showNotification(title, {
                body,
                icon: '/icons/icon-192x192.png',
                badge: '/icons/icon-72x72.png',
                tag: id,
                data: { scheduled: true, originalTimestamp: timestamp }
            });
            scheduledNotifications.delete(id);
        }, delay);
        
        scheduledNotifications.set(id, payload);
    }
}

// ============================================
// PERIODIC BACKGROUND SYNC (if supported)
// ============================================

self.addEventListener('periodicsync', (event) => {
    console.log('[SW] Periodic sync triggered:', event.tag);
    
    if (event.tag === 'refresh-content') {
        event.waitUntil(refreshContent());
    }
});

async function refreshContent() {
    // Background content refresh
    console.log('[SW] Refreshing content in background...');
    
    // Pre-cache critical resources
    const cache = await caches.open(DYNAMIC_CACHE);
    // Add specific refresh logic here
}

// ============================================
// ERROR HANDLING
// ============================================

self.addEventListener('error', (event) => {
    console.error('[SW] Error:', event.message, event.filename, event.lineno);
});

self.addEventListener('unhandledrejection', (event) => {
    console.error('[SW] Unhandled rejection:', event.reason);
});

console.log('[SW] Service Worker script loaded v9.1.0');
