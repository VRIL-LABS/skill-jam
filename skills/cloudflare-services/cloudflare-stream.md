---
name: Cloudflare Stream
description: |
  Cloudflare Stream is a video hosting and streaming platform with encoding, storage, and adaptive delivery.
  Trigger phrases: "video streaming", "video hosting", "live stream", "video encoding", "adaptive bitrate", "cloudflare stream"
license: MIT
---

# Cloudflare Stream

Cloudflare Stream is an integrated video platform that handles encoding, storage, and delivery of on-demand and live video content. Stream automatically optimizes video for any device, provides analytics, and delivers content through Cloudflare's global network.

## When to Use

Use Cloudflare Stream when you need to:
- **Host videos**: Upload and store video content without managing infrastructure
- **Stream on-demand content**: Deliver pre-recorded videos with adaptive bitrate streaming
- **Live streaming**: Broadcast real-time video events with low latency
- **Optimize delivery**: Automatically transcode and deliver optimal quality for each viewer
- **Protect content**: Control access with signed URLs and domain restrictions
- **Add captions/subtitles**: Support multiple languages and accessibility
- **Track engagement**: Monitor video performance and viewer analytics
- **Build video apps**: Create video platforms, courses, or content libraries

## Official Documentation

- **Main Documentation**: https://developers.cloudflare.com/stream/
- **Getting Started**: https://developers.cloudflare.com/stream/get-started/
- **Upload Videos**: https://developers.cloudflare.com/stream/uploading-videos/
- **Playback**: https://developers.cloudflare.com/stream/viewing-videos/
- **Live Streams**: https://developers.cloudflare.com/stream/stream-live/
- **API Reference**: https://developers.cloudflare.com/api/operations/stream-videos-list-videos
- **Pricing**: https://developers.cloudflare.com/stream/platform/pricing/

## Quick Start

### 1. Upload a Video

Using curl:

```bash
# Upload via URL
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/copy" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/video.mp4",
    "meta": {
      "name": "My First Video"
    }
  }'

# Upload via file
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/{account_id}/stream" \
  -H "Authorization: Bearer {api_token}" \
  -F file=@video.mp4 \
  -F 'meta={"name":"My Video"}'
```

### 2. Get Video Details

```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video_id}" \
  -H "Authorization: Bearer {api_token}"
```

Response:

```json
{
  "result": {
    "uid": "abc123",
    "thumbnail": "https://customer-xyz.cloudflarestream.com/abc123/thumbnails/thumbnail.jpg",
    "playback": {
      "hls": "https://customer-xyz.cloudflarestream.com/abc123/manifest/video.m3u8",
      "dash": "https://customer-xyz.cloudflarestream.com/abc123/manifest/video.mpd"
    },
    "status": {
      "state": "ready"
    },
    "meta": {
      "name": "My Video"
    },
    "duration": 120.5
  }
}
```

### 3. Embed Video

```html
<stream
  src="abc123"
  controls
  preload="auto"
></stream>

<script
  data-cfasync="false"
  defer
  type="text/javascript"
  src="https://embed.cloudflarestream.com/embed/sdk.latest.js"
></script>
```

### 4. Create Live Stream

```bash
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/live_inputs" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "name": "My Live Stream"
    },
    "recording": {
      "mode": "automatic"
    }
  }'
```

## Core Features

### Video Upload

#### Upload from URL

```javascript
async function uploadVideoFromURL(accountId, apiToken, videoURL, metadata) {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${accountId}/stream/copy`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: videoURL,
        meta: metadata,
        requireSignedURLs: false,
        allowedOrigins: ['example.com'],
      }),
    }
  );
  
  return response.json();
}

// Usage
const result = await uploadVideoFromURL(
  'account-id',
  'api-token',
  'https://example.com/video.mp4',
  {
    name: 'Product Demo',
    description: 'Demo of new product features',
  }
);

console.log('Video ID:', result.result.uid);
console.log('Status:', result.result.status.state); // 'pending' or 'ready'
```

#### Upload from File (Worker)

```javascript
export default {
  async fetch(request, env) {
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }
    
    const formData = await request.formData();
    const file = formData.get('video');
    const metadata = JSON.parse(formData.get('meta') || '{}');
    
    // Upload to Stream
    const uploadFormData = new FormData();
    uploadFormData.append('file', file);
    uploadFormData.append('meta', JSON.stringify(metadata));
    
    const response = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.STREAM_API_TOKEN}`,
        },
        body: uploadFormData,
      }
    );
    
    const result = await response.json();
    
    return Response.json({
      videoId: result.result.uid,
      status: result.result.status.state,
      thumbnail: result.result.thumbnail,
    });
  },
};
```

#### Direct Creator Upload (User Uploads)

```javascript
// Generate upload URL for users
async function createDirectUploadURL(env) {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream/direct_upload`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STREAM_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        maxDurationSeconds: 3600, // 1 hour max
        expiry: new Date(Date.now() + 3600000).toISOString(), // 1 hour
        requireSignedURLs: true,
        meta: {
          uploadedBy: 'user-123',
        },
      }),
    }
  );
  
  const result = await response.json();
  
  return {
    uploadURL: result.result.uploadURL,
    uid: result.result.uid,
  };
}

// Client-side upload
async function uploadVideo(file, uploadURL) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(uploadURL, {
    method: 'POST',
    body: formData,
  });
  
  return response.json();
}
```

### Video Playback

#### HTML5 Player

```html
<!DOCTYPE html>
<html>
<head>
  <title>Video Player</title>
  <style>
    stream {
      width: 100%;
      max-width: 800px;
      aspect-ratio: 16/9;
    }
  </style>
</head>
<body>
  <stream
    src="video-id-here"
    controls
    preload="auto"
    autoplay
    muted
    loop
    poster="https://customer-xyz.cloudflarestream.com/video-id/thumbnails/thumbnail.jpg?time=10s"
  ></stream>
  
  <script
    data-cfasync="false"
    defer
    type="text/javascript"
    src="https://embed.cloudflarestream.com/embed/sdk.latest.js"
  ></script>
</body>
</html>
```

#### Custom Player with JavaScript

```html
<video id="player" controls></video>

<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script>
  const video = document.getElementById('player');
  const src = 'https://customer-xyz.cloudflarestream.com/video-id/manifest/video.m3u8';
  
  if (video.canPlayType('application/vnd.apple.mpegurl')) {
    // Native HLS support (Safari)
    video.src = src;
  } else if (Hls.isSupported()) {
    // HLS.js for other browsers
    const hls = new Hls();
    hls.loadSource(src);
    hls.attachMedia(video);
    
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      video.play();
    });
  }
</script>
```

#### Signed URLs (Protected Content)

```javascript
// Generate signed token
async function generateSignedToken(videoId, env) {
  const encoder = new TextEncoder();
  const data = encoder.encode(videoId);
  
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(env.STREAM_SIGNING_KEY),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  
  const signature = await crypto.subtle.sign('HMAC', key, data);
  const token = btoa(String.fromCharCode(...new Uint8Array(signature)));
  
  return token;
}

// Worker serving signed videos
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const videoId = url.searchParams.get('v');
    
    // Verify user is authorized
    const userId = await authenticateUser(request);
    if (!userId) {
      return new Response('Unauthorized', { status: 401 });
    }
    
    // Generate signed token
    const token = await generateSignedToken(videoId, env);
    const exp = Math.floor(Date.now() / 1000) + 3600; // 1 hour
    
    const streamURL = `https://customer-xyz.cloudflarestream.com/${videoId}/manifest/video.m3u8?token=${token}&exp=${exp}`;
    
    return Response.json({ streamURL });
  },
};
```

### Live Streaming

#### Create Live Input

```javascript
async function createLiveStream(env, metadata) {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream/live_inputs`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.STREAM_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        meta: metadata,
        recording: {
          mode: 'automatic',
          timeoutSeconds: 10,
        },
      }),
    }
  );
  
  const result = await response.json();
  
  return {
    uid: result.result.uid,
    rtmps: {
      url: result.result.rtmps.url,
      streamKey: result.result.rtmps.streamKey,
    },
    webRTC: {
      url: result.result.webRTC.url,
    },
    playback: {
      hls: `https://customer-xyz.cloudflarestream.com/${result.result.uid}/manifest/video.m3u8`,
    },
  };
}

// Usage
const liveStream = await createLiveStream(env, {
  name: 'Product Launch Event',
  description: 'Live product launch',
});

console.log('Stream to:', liveStream.rtmps.url);
console.log('Stream key:', liveStream.rtmps.streamKey);
console.log('Watch at:', liveStream.playback.hls);
```

#### Embed Live Stream

```html
<stream
  src="live-stream-id"
  controls
  autoplay
  muted
></stream>

<script
  data-cfasync="false"
  defer
  type="text/javascript"
  src="https://embed.cloudflarestream.com/embed/sdk.latest.js"
></script>

<script>
  const stream = document.querySelector('stream');
  
  // Listen for live stream events
  stream.addEventListener('stream-adtargeting', (e) => {
    console.log('Ad break opportunity');
  });
  
  stream.addEventListener('loadedmetadata', () => {
    console.log('Live stream connected');
  });
</script>
```

#### WebRTC Live Streaming

```html
<video id="localVideo" autoplay muted></video>
<video id="remoteVideo" autoplay></video>
<button id="startStream">Start Streaming</button>

<script>
  const startButton = document.getElementById('startStream');
  const localVideo = document.getElementById('localVideo');
  
  startButton.addEventListener('click', async () => {
    // Get user media
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    
    localVideo.srcObject = stream;
    
    // Connect to Cloudflare Stream WebRTC
    const response = await fetch('/api/create-webrtc-stream', {
      method: 'POST',
    });
    
    const { sessionDescription } = await response.json();
    
    // Set up WebRTC connection
    const pc = new RTCPeerConnection();
    
    stream.getTracks().forEach(track => {
      pc.addTrack(track, stream);
    });
    
    await pc.setRemoteDescription(sessionDescription);
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    
    // Send answer back to server
    await fetch('/api/webrtc-answer', {
      method: 'POST',
      body: JSON.stringify({ answer: pc.localDescription }),
    });
  });
</script>
```

### Captions and Subtitles

```javascript
// Add captions to video
async function addCaptions(videoId, language, file, env) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream/${videoId}/captions/${language}`,
    {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${env.STREAM_API_TOKEN}`,
      },
      body: formData,
    }
  );
  
  return response.json();
}

// Usage
await addCaptions('video-id', 'en', captionsFile, env);
await addCaptions('video-id', 'es', spanishCaptionsFile, env);

// List captions
const response = await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream/${videoId}/captions`,
  {
    headers: { 'Authorization': `Bearer ${env.STREAM_API_TOKEN}` },
  }
);
```

### Video Analytics

```javascript
async function getVideoAnalytics(videoId, env) {
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream/${videoId}/analytics`,
    {
      headers: {
        'Authorization': `Bearer ${env.STREAM_API_TOKEN}`,
      },
    }
  );
  
  const result = await response.json();
  
  return {
    views: result.result.views,
    minutesViewed: result.result.minutesViewed,
    uniqueViewers: result.result.uniqueViewers,
  };
}

// GraphQL for advanced analytics
const query = `
  query {
    viewer {
      accounts(filter: { accountTag: "${accountId}" }) {
        streamMinutesViewedAdaptiveGroups(
          filter: {
            date_geq: "2024-01-01"
            date_lt: "2024-01-31"
          }
          limit: 100
        ) {
          dimensions {
            uid
            date
          }
          sum {
            minutesViewed
          }
          count {
            views
          }
        }
      }
    }
  }
`;
```

## Common Use Cases

### Video Course Platform

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === '/courses/video') {
      const videoId = url.searchParams.get('id');
      const userId = await authenticateUser(request, env);
      
      // Check if user has access
      const hasAccess = await checkCourseAccess(userId, videoId, env);
      if (!hasAccess) {
        return new Response('Access denied', { status: 403 });
      }
      
      // Generate signed URL
      const token = await generateSignedToken(videoId, env);
      const exp = Math.floor(Date.now() / 1000) + 7200; // 2 hours
      
      // Get video details
      const videoResponse = await fetch(
        `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream/${videoId}`,
        {
          headers: { 'Authorization': `Bearer ${env.STREAM_API_TOKEN}` },
        }
      );
      
      const video = await videoResponse.json();
      
      return Response.json({
        title: video.result.meta.name,
        streamURL: `https://customer-xyz.cloudflarestream.com/${videoId}/manifest/video.m3u8?token=${token}&exp=${exp}`,
        thumbnail: video.result.thumbnail,
        duration: video.result.duration,
      });
    }
    
    return new Response('Not found', { status: 404 });
  },
};
```

### Live Event Broadcasting

```javascript
// Admin creates live event
export default {
  async fetch(request, env) {
    if (request.url.endsWith('/admin/create-event')) {
      const { title, scheduledTime } = await request.json();
      
      // Create live input
      const liveStream = await createLiveStream(env, {
        name: title,
        scheduledTime,
      });
      
      // Store in database
      await env.DB.prepare(
        'INSERT INTO events (id, title, stream_id, rtmps_url, stream_key, scheduled_at) VALUES (?, ?, ?, ?, ?, ?)'
      ).bind(
        crypto.randomUUID(),
        title,
        liveStream.uid,
        liveStream.rtmps.url,
        liveStream.rtmps.streamKey,
        scheduledTime
      ).run();
      
      return Response.json({
        streamId: liveStream.uid,
        rtmpsURL: liveStream.rtmps.url,
        streamKey: liveStream.rtmps.streamKey,
      });
    }
    
    // Viewer watches event
    if (request.url.endsWith('/watch')) {
      const eventId = new URL(request.url).searchParams.get('id');
      
      const event = await env.DB.prepare(
        'SELECT * FROM events WHERE id = ?'
      ).bind(eventId).first();
      
      if (!event) {
        return new Response('Event not found', { status: 404 });
      }
      
      return new Response(`
        <!DOCTYPE html>
        <html>
          <body>
            <h1>${event.title}</h1>
            <stream src="${event.stream_id}" controls autoplay></stream>
            <script src="https://embed.cloudflarestream.com/embed/sdk.latest.js"></script>
          </body>
        </html>
      `, {
        headers: { 'Content-Type': 'text/html' },
      });
    }
  },
};
```

### User-Generated Content Platform

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Generate upload URL for users
    if (url.pathname === '/api/upload-url') {
      const userId = await authenticateUser(request, env);
      
      const uploadURL = await createDirectUploadURL(env);
      
      // Store pending upload
      await env.KV.put(
        `upload:${uploadURL.uid}`,
        JSON.stringify({ userId, status: 'pending' }),
        { expirationTtl: 3600 }
      );
      
      return Response.json(uploadURL);
    }
    
    // Webhook from Stream when upload completes
    if (url.pathname === '/api/webhook/upload-complete') {
      const webhook = await request.json();
      const videoId = webhook.uid;
      
      const uploadData = await env.KV.get(`upload:${videoId}`, 'json');
      
      if (uploadData) {
        // Save to database
        await env.DB.prepare(
          'INSERT INTO videos (id, user_id, stream_id, title, status) VALUES (?, ?, ?, ?, ?)'
        ).bind(
          crypto.randomUUID(),
          uploadData.userId,
          videoId,
          webhook.meta.name,
          'ready'
        ).run();
        
        // Notify user
        await notifyUser(uploadData.userId, 'Your video is ready!', env);
      }
      
      return new Response('OK');
    }
    
    return new Response('Not found', { status: 404 });
  },
};
```

## Integration

### With Workers

Direct integration shown in examples above.

### With Pages

```javascript
// pages/functions/videos/[id].js
export async function onRequest(context) {
  const videoId = context.params.id;
  
  const response = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${context.env.ACCOUNT_ID}/stream/${videoId}`,
    {
      headers: {
        'Authorization': `Bearer ${context.env.STREAM_API_TOKEN}`,
      },
    }
  );
  
  const video = await response.json();
  
  return new Response(`
    <!DOCTYPE html>
    <html>
      <head><title>${video.result.meta.name}</title></head>
      <body>
        <h1>${video.result.meta.name}</h1>
        <stream src="${videoId}" controls></stream>
        <script src="https://embed.cloudflarestream.com/embed/sdk.latest.js"></script>
      </body>
    </html>
  `, {
    headers: { 'Content-Type': 'text/html' },
  });
}
```

### With R2

```javascript
// Store original files in R2, processed videos in Stream
export default {
  async fetch(request, env) {
    const formData = await request.formData();
    const file = formData.get('video');
    
    // Store original in R2
    const key = `originals/${Date.now()}-${file.name}`;
    await env.BUCKET.put(key, file);
    
    // Upload to Stream for processing
    const streamFormData = new FormData();
    streamFormData.append('file', file);
    streamFormData.append('meta', JSON.stringify({
      originalKey: key,
      uploadedAt: new Date().toISOString(),
    }));
    
    const streamResponse = await fetch(
      `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/stream`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.STREAM_API_TOKEN}`,
        },
        body: streamFormData,
      }
    );
    
    return streamResponse;
  },
};
```

## Best Practices

### Video Optimization

```javascript
// Set appropriate metadata
await uploadVideo(url, {
  name: 'Product Demo',
  requireSignedURLs: true,        // Protect content
  allowedOrigins: ['example.com'], // Restrict domains
  thumbnailTimestampPct: 0.5,      // Thumbnail at 50%
});
```

### Access Control

```javascript
// Implement proper authentication
export default {
  async fetch(request, env) {
    const userId = await authenticateUser(request);
    const videoId = new URL(request.url).searchParams.get('v');
    
    // Check user subscription/purchase
    const hasAccess = await checkUserAccess(userId, videoId, env);
    
    if (!hasAccess) {
      return new Response('Access denied', { status: 403 });
    }
    
    // Return signed URL with expiration
    const signedURL = await generateSignedURL(videoId, 3600, env);
    return Response.json({ url: signedURL });
  },
};
```

### Performance

```html
<!-- Preload video metadata -->
<link
  rel="preload"
  as="fetch"
  href="https://customer-xyz.cloudflarestream.com/video-id/manifest/video.m3u8"
>

<!-- Use poster image for faster perceived load -->
<stream
  src="video-id"
  poster="https://customer-xyz.cloudflarestream.com/video-id/thumbnails/thumbnail.jpg?time=0s"
  preload="metadata"
  controls
></stream>
```

## Troubleshooting

### Video Not Playing

1. Check video status:

```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/stream/{video_id}" \
  -H "Authorization: Bearer {api_token}"
```

2. Verify allowed origins:

```javascript
// Update allowed origins
await fetch(
  `https://api.cloudflare.com/client/v4/accounts/${accountId}/stream/${videoId}`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      allowedOrigins: ['https://example.com'],
    }),
  }
);
```

### Upload Failures

Check file format and size:
- Supported formats: MP4, MOV, MKV, AVI, FLV, MPEG-2 TS, MPEG-2 PS, MXF, LXF, GXF, 3GP, WebM, MPG, QuickTime
- Maximum file size: 30 GB
- Maximum duration: 6 hours

### Live Stream Issues

Verify RTMPS settings:
```bash
# Test with OBS Studio or FFmpeg
ffmpeg -re -i input.mp4 -c copy -f flv \
  "rtmps://live.cloudflare.com:443/live/{stream_key}"
```

## See Also

- [Cloudflare Workers](./cloudflare-workers.md) - Serverless compute platform
- [Cloudflare R2](./cloudflare-r2.md) - Object storage for originals
- [Cloudflare Images](./cloudflare-images.md) - Image optimization
