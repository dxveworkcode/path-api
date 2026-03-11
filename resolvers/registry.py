from collections.abc import Callable
from urllib.parse import ParseResult

from resolvers import amazon, instagram, spotify, tiktok, youtube
from core.models import ResolveResponse

ResolverFn = Callable[[ParseResult], ResolveResponse]

RESOLVER_MAP: dict[str, ResolverFn] = {
    "amazon.com": amazon.resolve,
    "www.amazon.com": amazon.resolve,
    "amzn.to": amazon.resolve,
    "instagram.com": instagram.resolve,
    "www.instagram.com": instagram.resolve,
    "open.spotify.com": spotify.resolve,
    "tiktok.com": tiktok.resolve,
    "www.tiktok.com": tiktok.resolve,
    "vm.tiktok.com": tiktok.resolve,
    "youtube.com": youtube.resolve,
    "www.youtube.com": youtube.resolve,
    "youtu.be": youtube.resolve,
    "m.youtube.com": youtube.resolve,
}
