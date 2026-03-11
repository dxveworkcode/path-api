# Path

Resolve web URLs into mobile deep-link schemes. One HTTP call. 50+ platforms.

---

## Endpoint

### `GET /v1/resolve`

**Query parameter**

| Name | Type   | Required | Description              |
|------|--------|----------|--------------------------|
| url  | string | yes      | Full web URL to resolve. |

**200 — Success**

```json
{
  "url": "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT",
  "scheme": "spotify:track:4cOdK2wGLETKBW3PvgPWqT",
  "app_name": "Spotify",
  "platform": "spotify",
  "extracted_id": "4cOdK2wGLETKBW3PvgPWqT"
}
```

**Error**

```json
{
  "error": "unsupported_app",
  "detail": "No deep-link resolver found for 'example.com'..."
}
```

| Code | Key              | Cause                                 |
|------|------------------|---------------------------------------|
| 400  | invalid_url      | Malformed URL or missing scheme.      |
| 404  | unsupported_app  | Hostname not in the resolver registry.|
| 422  | validation error | Query parameter missing or wrong type.|

---

### `GET /v1/apps`

Returns every supported hostname grouped by platform.

---

## Supported Platforms

### Social
| Platform  | Scheme                                  | URL patterns                                      |
|-----------|-----------------------------------------|---------------------------------------------------|
| Amazon    | `amzn://dp/{ASIN}`                      | `/dp/{ASIN}`, `/gp/product/{ASIN}`, `amzn.to/`   |
| Instagram | `instagram://media?id={id}`             | `/p/{id}`, `/reel/{id}`, `/{username}`            |
| TikTok    | `snssdk1128://aweme/detail/{id}`        | `/@user/video/{id}`, `vm.tiktok.com`              |
| X/Twitter | `twitter://status?id={id}`              | `/status/{id}`, `/{username}`                     |
| Threads   | `threads://user?username={u}`           | `/@{username}`, `/t/{id}`                         |
| Pinterest | `pinterest://pin/{id}`                  | `/pin/{id}`, `/{user}`, `/{user}/{board}`         |
| Snapchat  | `snapchat://add/{username}`             | `/add/{username}`, `/stories/{username}`          |
| Reddit    | `reddit://reddit.com/r/{sub}`           | `/r/{sub}`, `/r/.../comments/{id}`, `/u/{user}`   |
| LinkedIn  | `linkedin://profile/{id}`               | `/in/{id}`, `/company/{slug}`, `/posts/{id}`      |
| BeReal    | `berealmobile://user/{user}`            | `/{username}`, `/moments/{id}`                    |
| Kwai      | `kwai://video/{id}`                     | `/video/{id}`, `/{username}`                      |

### Streaming & Video
| Platform    | Scheme                                  | URL patterns                          |
|-------------|-----------------------------------------|---------------------------------------|
| YouTube     | `vnd.youtube:{video_id}`                | `/watch?v=`, `youtu.be/`, `/channel/` |
| Twitch      | `twitch://open/?stream={ch}`            | `/{channel}`, `/clip/{id}`            |
| Netflix     | `nflx://www.netflix.com/title/{id}`     | `/title/{id}`                         |
| Disney+     | `disneyplus://content/{id}`             | `/series/{id}`, `/content/{id}`       |
| Hulu        | `hulu://www.hulu.com/watch/{id}`        | `/watch/{id}`, `/series/{id}/`        |
| Apple TV    | `videos://tv.apple.com/content/{id}`    | `/id{id}`, `/show/{id}`               |
| Vimeo       | `vimeo://app.vimeo.com/videos/{id}`     | `/{id}`, `/channel/{id}`              |
| Dailymotion | `dailymotion://video/{id}`              | `/video/{id}`, `/{username}`          |

### Music
| Platform    | Scheme                    | URL patterns                                   |
|-------------|---------------------------|------------------------------------------------|
| Spotify     | `spotify:{type}:{id}`     | `/track/`, `/album/`, `/artist/`, `/playlist/` |
| Apple Music | `music://song/{id}`       | `/song/{id}`, `/album/{id}`, `/artist/{id}`    |
| SoundCloud  | `soundcloud://tracks/{id}`| `/tracks/{id}`, `/{user}/sets/{pl}`            |
| Tidal       | `tidal://track/{id}`      | `/track/`, `/album/`, `/artist/`, `/playlist/` |
| Deezer      | `deezer://track/{id}`     | `/track/`, `/album/`, `/artist/`, `/playlist/` |
| Shazam      | `shazam://track/{id}`     | `/track/{id}`, `/artist/{id}`                  |

### Messaging & Productivity
| Platform  | Scheme                           | URL patterns                       |
|-----------|----------------------------------|------------------------------------|
| Telegram  | `tg://resolve?domain={username}` | `t.me/{user}`, `/joinchat/{hash}`  |
| WhatsApp  | `whatsapp://send?phone={num}`    | `wa.me/{phone}`                    |
| Discord   | `discord://discord.com/invite/`  | `/{invite}`, `/channels/{g}/{c}`   |
| Slack     | `slack://open?team={id}`         | `/{workspace}`                     |
| Zoom      | `zoommtg://zoom.us/join?confno=` | `/j/{meeting_id}`                  |

### Commerce
| Platform  | Scheme                          | URL patterns                  |
|-----------|---------------------------------|-------------------------------|
| Etsy      | `etsy://listing/{id}`           | `/listing/{id}`, `/shop/{n}`  |
| eBay      | `ebay://launch?nav=item.view`   | `/itm/{id}`, `/usr/{user}`    |
| Walmart   | `walmart://product/{id}`        | `/ip/{id}`                    |
| Target    | `target://product/{id}`         | `/p/{name}/{id}`              |

### Travel & Local
| Platform   | Scheme                            | URL patterns                      |
|------------|-----------------------------------|-----------------------------------|
| Airbnb     | `airbnb://rooms/{id}`             | `/rooms/{id}`, `/experiences/{id}`|
| Booking    | `booking://hotel/{slug}`          | `/hotel/{slug}.html`              |
| Tripadvisor| `tripadvisor://attraction/{id}`   | Hotel/Restaurant/Attraction URLs  |
| Yelp       | `yelp://biz/{alias}`              | `/biz/{alias}`                    |

### Food & Rides
| Platform  | Scheme                    | URL patterns      |
|-----------|---------------------------|-------------------|
| Uber Eats | `ubereats://store/{id}`   | `/store/{id}`     |
| DoorDash  | `doordash://store/{id}`   | `/store/{id}`     |
| Uber      | `uber://`                 | uber.com links    |
| Lyft      | `lyft://ridetype?id=lyft` | lyft.com links    |

### Events
| Platform    | Scheme                       | URL patterns          |
|-------------|------------------------------|-----------------------|
| Ticketmaster| `ticketmaster://event/{id}`  | `/event/{id}`         |
| Eventbrite  | `eventbrite://event/{id}`    | `/event/{name}-{id}`  |

### Misc
| Platform  | Scheme                        | URL patterns                  |
|-----------|-------------------------------|-------------------------------|
| GitHub    | `github://repo/{owner}/{repo}`| `/{owner}/{repo}`, `/{user}`  |
| Medium    | `medium://p/{post_id}`        | `/{user}`, `/{user}/{post}`   |
| Strava    | `strava://activities/{id}`    | `/activities/`, `/athletes/`  |
| Goodreads | `goodreads://book/{id}`       | `/book/show/{id}`             |
| Duolingo  | `duolingo://`                 | duolingo.com links            |
| Substack  | `substack://post/{slug}`      | `/p/{slug}`, `/{username}`    |

---

## Plans

| Plan  | Price    | Volume              |
|-------|----------|---------------------|
| Basic | Free     | 50 requests / day   |
| Pro   | $19 / mo | 10,000 / month      |
| Ultra | $49 / mo | 100,000 / month     |
| Mega  | $129 / mo| Unlimited           |

Contact `dxveworkcode@gmail.com` to upgrade.

---

Available via [RapidAPI](https://rapidapi.com). Interactive docs at `/`. Auto-generated schema at `/docs`.
