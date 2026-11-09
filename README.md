# Velo Client · Server Mappings

Tell [Velo Client](https://velo-client.com) about your Minecraft server: its name, logo and the addresses players
join with. Velo players on your server then show **your server's name and logo in their Discord status**, and your
server gets a proper card on [velo-client.com/library/server](https://velo-client.com/library/server).

## Add your server

**The easy way:** [velo-client.com/library/servers](https://velo-client.com/library/servers) - enter your address, put
the code it gives you into your MOTD for a moment (that proves you run the server), fill in the details, upload your
logo and banner. It opens the pull request here for you.

**By hand:**

1. Fork this repo.
2. Create `servers/<id>/` (lower case, letters, digits and `-`), with:
   - `metadata.json` - see the example below and [`schema.json`](schema.json) for every field.
   - `logo.png` - **required**, square, 128-1024 px (512 recommended), under 512 KB. It's the big picture in
     players' Discord status.
   - `banner.png` - **required**, wide (16:9 to 5:1, e.g. 1920x1080 or 1600x480), under 2 MB. Your server card.
3. Open a pull request. The check tells you if anything is off. Only add servers you own or run.

```json
{
  "id": "example",
  "name": "Example Network",
  "description": "Minigames and survival since 2020.",
  "addresses": ["example.net", "*.example.net"],
  "primaryAddress": "play.example.net",
  "website": "https://example.net",
  "discord": "https://discord.gg/example",
  "primaryColor": "#5aa9ff",
  "gameTypes": ["minigames", "survival"],
  "regions": ["EU"],
  "minecraftVersions": { "min": "1.8", "recommended": "1.21" },
  "presence": {
    "details": "Playing on %name%",
    "largeImageText": "Example Network",
    "buttons": [{ "label": "Join our Discord", "url": "https://discord.gg/example" }]
  }
}
```

Run the check yourself: `pip install pillow jsonschema && python scripts/validate.py`.

## Use the data

Everything is served by the Velo Library API (free, no key needed for light use):

- `GET https://velo-client.com/v2/servers` - every mapped server
- `GET https://velo-client.com/v2/servers/lookup?address=play.example.net` - the mapping for an address
- `GET https://velo-client.com/v2/servers/<id>/logo.png` and `/banner.png`

Servers running the [Velo Bridge plugin](https://dev.velo-client.com) can also set the Discord status live.

Licensed CC0 - the data is free for anyone.
