# Image declarations
# Ren'Py looks for images relative to the game/ folder.
# game/images is a directory junction -> ../../images (the shared asset folder).

# Locations
image cheaphouse_day   = "images/locations/cheaphouse_day.png"
image cheaphouse_night = "images/locations/cheaphouse_night.png"
image goodhomeday      = "images/locations/goodhomeday.png"
image goodhomenight    = "images/locations/goodhomenight.png"
image richhomeday      = "images/locations/richhomeday.png"
image richhomenight    = "images/locations/richhomenight.png"

image cafeday          = "images/locations/cafeday.png"
image cafenight        = "images/locations/cafenight.png"
image bar              = "images/locations/bar.png"
image restaurantday    = "images/locations/restaurantday.png"
image restaurantnight  = "images/locations/restaurantnight.png"

image gymdaypeople     = "images/locations/gymdaypeople.png"
image gymdaynopeople   = "images/locations/gymdaynopeople.png"

image libraryday       = "images/locations/libraryday.png"
image librarynight     = "images/locations/librarynight.png"

image mallday          = "images/locations/mallday.png"
image mallnight        = "images/locations/mallnight.png"
image clothesshop      = "images/locations/clothesshop.png"
image electronicsshop  = "images/locations/electronicsshop.png"
image giftshop         = "images/locations/giftshop.png"

image parkday          = "images/locations/parkday.png"
image parknight        = "images/locations/parknight.png"
image beachday         = "images/locations/beachday.png"
image beachnight       = "images/locations/beachnight.png"

image goodoffice1      = "images/locations/goodoffice1.png"
image mediumoffice1    = "images/locations/mediumoffice1.png"
image pooroffice1      = "images/locations/pooroffice1.png"
image officelobby1     = "images/locations/officelobby1.png"
image warehouse        = "images/locations/warehouse.png"
image carworkshop      = "images/locations/carworkshop.png"
image hospital1        = "images/locations/hospital1.png"
image schoolhall       = "images/locations/schoolhall.png"
image classroom        = "images/locations/class.png"

# Source is 5068x2764 — force to the 1920x1080 game resolution so it fills the screen.
# ponytail: ~3% horizontal squeeze (map is 1.834 vs 16:9 1.778); imperceptible.
# Upgrade path: downscale the PNG to 1920x1080 to cut the 28MB / 56MB-VRAM load.
image map_city = Transform("images/locations/map_city.png", size=(1920, 1080))

# Zoe sprites
image zoe_street_neutral   = "images/characters/zoe/zoe_street_neutral.png"
image zoe_street_smile     = "images/characters/zoe/zoe_street_smile.png"
image zoe_street_talk      = "images/characters/zoe/zoe_street_talk.png"
image zoe_street_surprised = "images/characters/zoe/zoe_street_surprised.png"
image zoe_street_full      = "images/characters/zoe/zoe_street_full.png"
image zoe_punk_smile       = "images/characters/zoe/zoe_punk_smile.png"
image zoe_hoodie_smile     = "images/characters/zoe/zoe_hoodie_smile.png"
image zoe_coat_smile       = "images/characters/zoe/zoe_coat_smile.png"
