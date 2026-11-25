"""Wednesday 25 November 2026: 48 stories, each from our own scan of 41 wire feeds.

Every row below is one item this session read in an RSS feed between 00:00Z and
05:35Z on 25 November 2026 (UTC stamp in `utc`, outlets in `src`). Nothing is
invented: where two feed items reported the same event they were merged into one
story and both outlets are named; an item that carried only an analysis question
was dropped rather than turned into news.
"""

DAY = "WEDNESDAY 25 NOVEMBER 2026"
DAY_SHORT = "WED 25 NOV 2026"
EDITION = "0545 GMT EDITION"
STAMP = "OUR OWN SCAN OF 41 WIRE FEEDS · 00:00-05:35 GMT"

# place, region, desk, status, headline, outlets, utc, scene
STORIES = [
    # ---------------------------------------------------------- MIDDLE EAST
    ("HODEIDAH", "MIDDLE EAST", "WAR", "ALERT", "Coalition raids hit Yemen's main port",
     "Al Jazeera · MEE · CNA", "02:46", "ship"),
    ("STRAIT OF HORMUZ", "MIDDLE EAST", "SECURITY", "CLAIM", "Two tankers strike mines in the strait",
     "MEE", "04:52", "ship"),
    ("STRAIT OF HORMUZ", "MIDDLE EAST", "DEFENCE", "CLAIM", "Iran says it downed a US MQ-9",
     "MEE", "04:56", "drone"),
    ("EASTERN PROVINCE", "MIDDLE EAST", "WAR", "OFFICIAL", "Saudi forces down four drones",
     "MEE", "03:06", "drone"),
    ("JEDDAH", "MIDDLE EAST", "WAR", "THREAT", "Houthis warn Saudi Red Sea ports",
     "Straits Times", "02:47", "port"),
    ("GAZA CITY", "MIDDLE EAST", "WAR", "CONFIRMED", "Strike on a flat kills four",
     "MEE · Al Jazeera", "03:08", "blast"),
    ("GAZA CITY", "MIDDLE EAST", "HEALTH", "ALERT", "Meningitis alert as clinics run dry",
     "MEE", "02:31", "virus"),
    ("GAZA", "MIDDLE EAST", "RIGHTS", "REPORTED", "Amnesty seeks an ICC genocide probe",
     "AFP", "04:01", "gavel"),
    ("JERUSALEM", "MIDDLE EAST", "POLITICS", "CONFIRMED", "Eisenkot signs his first coalition deal",
     "Al Jazeera", "01:30", "ballot"),
    ("QUNEITRA", "MIDDLE EAST", "SECURITY", "REPORTED", "Israeli raid detains a civilian",
     "MEE", "01:32", "person"),
    ("TEHRAN", "MIDDLE EAST", "RIGHTS", "CONFIRMED", "Singer flogged 74 times over a concert",
     "Al Jazeera", "01:21", "megaphone"),
    # ---------------------------------------------------------------- EUROPE
    ("KYIV", "EUROPE", "ECONOMY", "CONFIRMED", "Ukraine asks for €115bn for 2027",
     "France 24", "01:19", "money"),
    ("ODESA", "EUROPE", "WAR", "CONFIRMED", "Russian strike kills two in the region",
     "Straits Times", "01:27", "fire"),
    ("TALLINN", "EUROPE", "SECURITY", "OFFICIAL", "Estonia shuts its last road border",
     "CNA", "02:56", "flag"),
    ("LONDON", "EUROPE", "SECURITY", "OFFICIAL", "UK warns firms of Russian sabotage",
     "Al Jazeera", "04:48", "megaphone"),
    ("LONDON", "EUROPE", "POLITICS", "OFFICIAL", "Probe into decades of nuclear tests",
     "Straits Times", "00:35", "chart"),
    ("ISTANBUL", "EUROPE", "SPORT", "REPORTED", "Galatasaray says Israel went to UEFA",
     "Al Jazeera", "04:12", "trophy"),
    ("MADRID", "EUROPE", "MIGRATION", "CONFIRMED", "Abrego Garcia self-deports to Spain",
     "Al Jazeera", "02:40", "plane"),
    # ------------------------------------------------------------- EAST ASIA
    ("JIUQUAN", "EAST ASIA", "SPACE", "CONFIRMED", "Shenzhou-24 carries a Pakistani astronaut",
     "Al Jazeera · CNA", "02:44", "rocket"),
    ("NEW YORK", "EAST ASIA", "JUSTICE", "REPORTED", "Huawei vows to fight its conviction",
     "CNA", "02:52", "gavel"),
    ("BEIJING", "EAST ASIA", "BUSINESS", "CONFIRMED", "China Southern orders 50 Boeing jets",
     "CNA", "02:59", "plane"),
    ("TOKYO", "EAST ASIA", "BUSINESS", "REPORTED", "Starbucks to sell its Japan business",
     "CNA", "03:32", "money"),
    ("PYONGYANG", "EAST ASIA", "DIPLOMACY", "CONFIRMED", "North Korea expels the Swiss envoy",
     "CNA", "03:52", "flag"),
    ("TAIPEI", "EAST ASIA", "TECH", "REPORTED", "Chip 'underworld' reports as Huang returns",
     "ABC", "03:43", "chip"),
    # ------------------------------------------------------------- S-E ASIA
    ("KUALA LUMPUR", "S-E ASIA", "CULTURE", "CONFIRMED", "A Samad Said dies at 91",
     "CNA", "03:25", "person"),
    ("KUALA LUMPUR", "S-E ASIA", "BUSINESS", "CONFIRMED", "Malaysia Airlines buys 10 787s",
     "CNA", "05:06", "plane"),
    ("JAKARTA", "S-E ASIA", "ACCIDENT", "ALERT", "Rescuers dig for dozens in a mine",
     "CNA · ABC", "05:15", "mine"),
    ("SINGAPORE", "S-E ASIA", "LAW", "OFFICIAL", "Chief Justice defends the rule of law",
     "CNA", "03:13", "gavel"),
    ("SINGAPORE", "S-E ASIA", "SECURITY", "REPORTED", "Terror drill staged at Esplanade",
     "CNA", "04:01", "blast"),
    # ------------------------------------------------------------ SOUTH ASIA
    ("DHAKA", "SOUTH ASIA", "LABOUR", "CONFIRMED", "Garment wage raised 36% after protests",
     "CNA", "04:11", "megaphone"),
    # -------------------------------------------------------------- OCEANIA
    ("HONIARA", "OCEANIA", "DIPLOMACY", "CONFIRMED", "Solomon Islands sign a security pact",
     "CNA", "04:34", "flag"),
    ("PERTH", "OCEANIA", "ENERGY", "OFFICIAL", "Chevron 'knowingly' vented methane",
     "ABC", "03:00", "fire"),
    ("SYDNEY", "OCEANIA", "JUSTICE", "REPORTED", "'Boys' club' culture in NSW prisons",
     "ABC", "02:30", "person"),
    ("CANBERRA", "OCEANIA", "TECH", "REPORTED", "US criticises the social media law",
     "Straits Times", "02:56", "chip"),
    ("DARWIN", "OCEANIA", "LAW", "REPORTED", "NT moves on a 'castle law' defence",
     "ABC", "03:05", "gavel"),
    # --------------------------------------------------------------- AFRICA
    ("DAKAR", "AFRICA", "SPORT", "CONFIRMED", "Senegal celebrate the AFCON ruling",
     "Al Jazeera", "01:39", "trophy"),
    ("BENGHAZI", "AFRICA", "WAR", "REPORTED", "Strike on Russian ships kills two Libyans",
     "Zelensky account", "03:46", "ship"),
    ("BANJUL", "AFRICA", "POLITICS", "REPORTED", "Gambia votes on a decade of promises",
     "Al Jazeera", "05:03", "ballot"),
    ("GOMA", "AFRICA", "HEALTH", "REPORTED", "Ebola zone reports a surge in abuse",
     "ABC", "04:58", "cross"),
    # ------------------------------------------------------------- AMERICAS
    ("CARTAGENA", "AMERICAS", "SECURITY", "ALERT", "Gunmen hold dozens hostage in a store",
     "Al Jazeera", "00:49", "person"),
    ("QUITO", "AMERICAS", "DEFENCE", "REPORTED", "US pauses joint military operations",
     "Straits Times", "01:08", "flag"),
    ("WASHINGTON", "AMERICAS", "POLITICS", "CONFIRMED", "Alaska ends its voter-records deal",
     "Al Jazeera", "00:28", "ballot"),
    ("WASHINGTON", "AMERICAS", "TRADE", "REPORTED", "Tariffs readied on 16 economies",
     "Sky News · Straits Times", "02:45", "chart"),
    ("NEW YORK", "AMERICAS", "MARKETS", "CONFIRMED", "AI doubts sink Asian markets",
     "Al Jazeera · CNA", "03:31", "chart"),
    ("SANTA CLARA", "AMERICAS", "BUSINESS", "REPORTED", "Nvidia's Huang admits a code breach",
     "Straits Times · RNZ", "04:27", "chip"),
    ("HAVANA", "AMERICAS", "HEALTH", "REPORTED", "WHO urges an end to the fuel blockade",
     "Al Jazeera", "02:23", "cross"),
    ("CARACAS", "AMERICAS", "POLITICS", "REPORTED", "Protesters clash over the minimum wage",
     "Al Jazeera", "04:27", "megaphone"),
    ("BRASILIA", "AMERICAS", "SCIENCE", "REPORTED", "A Spix's macaw chick is born in a zoo",
     "Straits Times", "02:05", "planet"),
]

NUMBERS = [
    ("74", "lashes for a singer"),
    ("€115bn", "Ukraine asks for 2027"),
    ("50", "Boeing jets for China"),
    ("36%", "garment wage rise"),
    ("16", "economies facing tariffs"),
]

REGION_COLOURS = {
    "MIDDLE EAST": (150, 34, 32),
    "EAST ASIA": (28, 78, 130),
    "SOUTH ASIA": (120, 74, 20),
    "S-E ASIA": (18, 100, 96),
    "OCEANIA": (30, 92, 60),
    "EUROPE": (66, 52, 120),
    "AFRICA": (140, 88, 24),
    "AMERICAS": (110, 34, 74),
}


def counts():
    tally = {}
    for s in STORIES:
        tally[s[1]] = tally.get(s[1], 0) + 1
    return tally


if __name__ == "__main__":
    t = counts()
    print("stories:", len(STORIES))
    for k in sorted(t):
        print(" ", k, t[k])
    print("sum", sum(t.values()))
