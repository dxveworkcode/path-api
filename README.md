# Path

Resolve web URLs into mobile deep-link schemes. One HTTP call. Five platforms.

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
  "detail": "No deep-link resolver found for 'reddit.com'..."
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

| Platform  | Scheme format                          | URL patterns                                         |
|-----------|----------------------------------------|------------------------------------------------------|
| Amazon    | `amzn://dp/{ASIN}`                     | `/dp/{ASIN}`, `/gp/product/{ASIN}`, `amzn.to/`      |
| Instagram | `instagram://media?id={id}`            | `/p/{id}`, `/reel/{id}`, `/{username}`               |
| Spotify   | `spotify:{type}:{id}`                  | `/track/`, `/album/`, `/artist/`, `/playlist/`       |
| TikTok    | `snssdk1128://aweme/detail/{video_id}` | `/@user/video/{id}`, `vm.tiktok.com`                 |
| YouTube   | `vnd.youtube:{video_id}`               | `/watch?v=`, `youtu.be/`, `/channel/`, `/@handle`    |

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
