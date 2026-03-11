from collections.abc import Callable
from urllib.parse import ParseResult

from resolvers import (
    amazon, instagram, spotify, tiktok, youtube,
    twitter, threads, pinterest, snapchat, reddit, linkedin,
    twitch, netflix, disney_plus, hulu, apple_tv,
    soundcloud, apple_music, tidal, deezer, shazam, vimeo, dailymotion,
    telegram, whatsapp, discord, slack, zoom,
    etsy, ebay, walmart, target, airbnb, booking, yelp, tripadvisor,
    uber, lyft, doordash, uber_eats,
    ticketmaster, eventbrite,
    medium, github, strava, goodreads, duolingo, bereal, substack, kwai,
)
from core.models import ResolveResponse

ResolverFn = Callable[[ParseResult], ResolveResponse]

RESOLVER_MAP: dict[str, ResolverFn] = {
    # ── Amazon ──────────────────────────────────────────────────────────
    "amazon.com": amazon.resolve,
    "www.amazon.com": amazon.resolve,
    "amzn.to": amazon.resolve,
    # ── Instagram ───────────────────────────────────────────────────────
    "instagram.com": instagram.resolve,
    "www.instagram.com": instagram.resolve,
    # ── TikTok ──────────────────────────────────────────────────────────
    "tiktok.com": tiktok.resolve,
    "www.tiktok.com": tiktok.resolve,
    "vm.tiktok.com": tiktok.resolve,
    # ── YouTube ─────────────────────────────────────────────────────────
    "youtube.com": youtube.resolve,
    "www.youtube.com": youtube.resolve,
    "youtu.be": youtube.resolve,
    "m.youtube.com": youtube.resolve,
    # ── Spotify ─────────────────────────────────────────────────────────
    "open.spotify.com": spotify.resolve,
    # ── X / Twitter ─────────────────────────────────────────────────────
    "twitter.com": twitter.resolve,
    "www.twitter.com": twitter.resolve,
    "x.com": twitter.resolve,
    "www.x.com": twitter.resolve,
    # ── Threads ─────────────────────────────────────────────────────────
    "threads.net": threads.resolve,
    "www.threads.net": threads.resolve,
    # ── Pinterest ────────────────────────────────────────────────────────
    "pinterest.com": pinterest.resolve,
    "www.pinterest.com": pinterest.resolve,
    "pin.it": pinterest.resolve,
    # ── Snapchat ────────────────────────────────────────────────────────
    "snapchat.com": snapchat.resolve,
    "www.snapchat.com": snapchat.resolve,
    # ── Reddit ──────────────────────────────────────────────────────────
    "reddit.com": reddit.resolve,
    "www.reddit.com": reddit.resolve,
    "old.reddit.com": reddit.resolve,
    # ── LinkedIn ────────────────────────────────────────────────────────
    "linkedin.com": linkedin.resolve,
    "www.linkedin.com": linkedin.resolve,
    # ── Twitch ──────────────────────────────────────────────────────────
    "twitch.tv": twitch.resolve,
    "www.twitch.tv": twitch.resolve,
    "clips.twitch.tv": twitch.resolve,
    # ── Netflix ─────────────────────────────────────────────────────────
    "netflix.com": netflix.resolve,
    "www.netflix.com": netflix.resolve,
    # ── Disney+ ─────────────────────────────────────────────────────────
    "disneyplus.com": disney_plus.resolve,
    "www.disneyplus.com": disney_plus.resolve,
    # ── Hulu ────────────────────────────────────────────────────────────
    "hulu.com": hulu.resolve,
    "www.hulu.com": hulu.resolve,
    # ── Apple TV ────────────────────────────────────────────────────────
    "tv.apple.com": apple_tv.resolve,
    # ── SoundCloud ──────────────────────────────────────────────────────
    "soundcloud.com": soundcloud.resolve,
    "www.soundcloud.com": soundcloud.resolve,
    # ── Apple Music ─────────────────────────────────────────────────────
    "music.apple.com": apple_music.resolve,
    # ── Tidal ───────────────────────────────────────────────────────────
    "tidal.com": tidal.resolve,
    "www.tidal.com": tidal.resolve,
    # ── Deezer ──────────────────────────────────────────────────────────
    "deezer.com": deezer.resolve,
    "www.deezer.com": deezer.resolve,
    # ── Shazam ──────────────────────────────────────────────────────────
    "shazam.com": shazam.resolve,
    "www.shazam.com": shazam.resolve,
    # ── Vimeo ───────────────────────────────────────────────────────────
    "vimeo.com": vimeo.resolve,
    "www.vimeo.com": vimeo.resolve,
    # ── Dailymotion ─────────────────────────────────────────────────────
    "dailymotion.com": dailymotion.resolve,
    "www.dailymotion.com": dailymotion.resolve,
    # ── Telegram ────────────────────────────────────────────────────────
    "t.me": telegram.resolve,
    "telegram.me": telegram.resolve,
    # ── WhatsApp ────────────────────────────────────────────────────────
    "wa.me": whatsapp.resolve,
    "whatsapp.com": whatsapp.resolve,
    "www.whatsapp.com": whatsapp.resolve,
    # ── Discord ─────────────────────────────────────────────────────────
    "discord.com": discord.resolve,
    "discord.gg": discord.resolve,
    # ── Slack ───────────────────────────────────────────────────────────
    "slack.com": slack.resolve,
    # ── Zoom ────────────────────────────────────────────────────────────
    "zoom.us": zoom.resolve,
    # ── LinkedIn (already added above) ──────────────────────────────────
    # ── Etsy ────────────────────────────────────────────────────────────
    "etsy.com": etsy.resolve,
    "www.etsy.com": etsy.resolve,
    # ── eBay ────────────────────────────────────────────────────────────
    "ebay.com": ebay.resolve,
    "www.ebay.com": ebay.resolve,
    # ── Walmart ─────────────────────────────────────────────────────────
    "walmart.com": walmart.resolve,
    "www.walmart.com": walmart.resolve,
    # ── Target ──────────────────────────────────────────────────────────
    "target.com": target.resolve,
    "www.target.com": target.resolve,
    # ── Airbnb ──────────────────────────────────────────────────────────
    "airbnb.com": airbnb.resolve,
    "www.airbnb.com": airbnb.resolve,
    # ── Booking ─────────────────────────────────────────────────────────
    "booking.com": booking.resolve,
    "www.booking.com": booking.resolve,
    # ── Yelp ────────────────────────────────────────────────────────────
    "yelp.com": yelp.resolve,
    "www.yelp.com": yelp.resolve,
    # ── Tripadvisor ─────────────────────────────────────────────────────
    "tripadvisor.com": tripadvisor.resolve,
    "www.tripadvisor.com": tripadvisor.resolve,
    # ── Uber ────────────────────────────────────────────────────────────
    "uber.com": uber.resolve,
    "www.uber.com": uber.resolve,
    # ── Lyft ────────────────────────────────────────────────────────────
    "lyft.com": lyft.resolve,
    "www.lyft.com": lyft.resolve,
    # ── DoorDash ────────────────────────────────────────────────────────
    "doordash.com": doordash.resolve,
    "www.doordash.com": doordash.resolve,
    # ── Uber Eats ───────────────────────────────────────────────────────
    "ubereats.com": uber_eats.resolve,
    "www.ubereats.com": uber_eats.resolve,
    # ── Ticketmaster ────────────────────────────────────────────────────
    "ticketmaster.com": ticketmaster.resolve,
    "www.ticketmaster.com": ticketmaster.resolve,
    # ── Eventbrite ──────────────────────────────────────────────────────
    "eventbrite.com": eventbrite.resolve,
    "www.eventbrite.com": eventbrite.resolve,
    # ── Medium ──────────────────────────────────────────────────────────
    "medium.com": medium.resolve,
    # ── GitHub ──────────────────────────────────────────────────────────
    "github.com": github.resolve,
    # ── Strava ──────────────────────────────────────────────────────────
    "strava.com": strava.resolve,
    "www.strava.com": strava.resolve,
    # ── Goodreads ───────────────────────────────────────────────────────
    "goodreads.com": goodreads.resolve,
    "www.goodreads.com": goodreads.resolve,
    # ── Duolingo ────────────────────────────────────────────────────────
    "duolingo.com": duolingo.resolve,
    "www.duolingo.com": duolingo.resolve,
    # ── BeReal ──────────────────────────────────────────────────────────
    "bere.al": bereal.resolve,
    # ── Substack ────────────────────────────────────────────────────────
    "substack.com": substack.resolve,
    # ── Kwai ────────────────────────────────────────────────────────────
    "kwai.com": kwai.resolve,
    "www.kwai.com": kwai.resolve,
}
