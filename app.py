from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# рабочий ключ 
WEATHER_API_KEY = "3f163ecfd4ef4072b31160829260710"


OUTFIT_IMAGES = {
    "casual": {
        "freezing": ["casual_freezing_left.jpg", "casual_freezing_right.jpg"],
        "cold": ["casual_cold_left.jpg", "casual_cold_right.jpg"],
        "chilly": ["casual_chilly_left.jpg", "casual_chilly_right.jpg"],
        "warm": ["casual_warm_left.jpg", "casual_warm_right.jpg"],
        "hot": ["casual_hot_left.jpg", "casual_hot_right.jpg"],
    },
    "business": {
        "freezing": [
            "business_freezing_left.jpg",
            "business_freezing_right.jpg",
        ],
        "cold": ["business_cold_left.jpg", "business_cold_right.jpg"],
        "chilly": ["business_chilly_left.jpg", "business_chilly_right.jpg"],
        "warm": ["business_warm_left.jpg", "business_warm_right.jpg"],
        "hot": ["business_hot_left.jpg", "business_hot_right.jpg"],
    },
    "streetwear": {
        "freezing": [
            "streetwear_freezing_left.jpg",
            "streetwear_freezing_right.jpg",
        ],
        "cold": ["streetwear_cold_left.jpg", "streetwear_cold_right.jpg"],
        "chilly": ["streetwear_chilly_left.jpg", "streetwear_chilly_right.jpg"],
        "warm": ["streetwear_warm_left.jpg", "streetwear_warm_right.jpg"],
        "hot": ["streetwear_hot_left.jpg", "streetwear_hot_right.jpg"],
    },
}

DEFAULT_IMAGES = ["default_1.jpg", "default_2.jpg"]


def get_weather(city, lang):
    if not city:
        return None
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang={lang}"
    try:
        response = requests.get(url, timeout=10) 
        if response.status_code == 200:
            data = response.json()
            return {
                "temperature": round(data["current"]["temp_c"]),
                "description": data["current"]["condition"]["text"],
            }
    except Exception:
       pass 
    return None



TEXTS = {
    "ru": {
        "title": "Умный стилист",
        "subtitle": "Персональный капсульный гардероб по прогнозу погоды",
        "language": "Язык интерфейса",
        "city": "Город",
        "city_placeholder": "Введите город (Paris, Moscow...)",
        "style": "Стиль одежды",
        "casual": "Повседневный (Casual)",
        "business": "Деловой (Business Chic)",
        "streetwear": "Уличный (Streetwear)",
        "button": "Сформировать капсулу",
        "result": "Рекомендованный комплект вещей:",
        "weather": "Погода сейчас",
        "error": "Город не найден. Попробуйте ввести название латиницей!",
        "outfits": {
            "casual": {
                "freezing": "• Верх: Длинный пуховик с капюшоном, плотный шерстяной свитер.\n• Низ: Утепленные джинсы прямого кроя.\n• Обувь: Зимние ботинки на рифленой подошве.\n• Аксессуары: Объемный шарф крупной вязки, теплая шапка и варежки.",
                "cold": "• Верх: Драповое пальто длины миди, кашемировый джемпер.\n• Низ: Классические плотные джинсы.\n• Обувь: Кожаные ботильоны или челси.\n• Аксессуары: Мягкий палантин и кожаные перчатки.",
                "chilly": "• Верх: Классический тренч (trench coat), хлопковый лонгслив.\n• Низ: Джинсы свободного кроя (mom / wide-leg).\n• Обувь: Базовые белые кроссовки.\n• Аксессуары: Вместительная сумка-тоут (tote bag).",
                "warm": "• Верх: Облегченный кардиган или джинсовая куртка поверх базовой футболки.\n• Низ: Брюки-чинос или юбка-миди.\n• Обувь: Кеды или легкие лоферы.\n• Аксессуары: Солнцезащитные очки.",
                "hot": "• Верх: Свободная футболка из органического хлопка или топ.\n• Низ: Льняные шорты или легкая струящаяся юбка.\n• Обувь: Открытые сандалии или эспадрильи.\n• Аксессуары: Плетеная сумка и панама.",
            },
            "business": {
                "freezing": "• Верх: Шерстяное утепленное пальто строгого кроя, шерстяной джемпер поверх сорочки.\n• Низ: Утепленные классические брюки со стрелками.\n• Обувь: Утепленные ботинки оксфорды/челси.\n• Аксессуары: Кашемировый шарф сдержанного оттенка.",
                "cold": "• Верх: Классическое шерстяное пальто, пиджак (блейзер), рубашка.\n• Низ: Брюки прямого кроя из костюмной шерсти.\n• Обувь: Кожаные ботильоны или классические дерби.\n• Аксессуары: Структурированная кожаная сумка под документы.",
                "chilly": "• Верх: Двубортный тренчкот, классический блейзер, шелковая блуза.\n• Низ: Зауженные или прямые брюки.\n• Обувь: Элегантные закрытые лоферы.\n• Аксессуары: Минималистичные наручные часы.",
                "warm": "• Верх: Приталенная хлопковая рубашка или блуза с коротким рукавом.\n• Низ: Облегченные брюки или юбка-карандаш.\n• Обувь: Кожаные лоферы или балетки с заостренным мысом.\n• Аксессуары: Тонкий кожаный ремень.",
                "hot": "• Верх: Дышащая льняная рубашка пастельного тона.\n• Низ: Свободные льняные брюки палаццо.\n• Обувь: Открытые туфли с перфорацией или элегантные мюли.\n• Аксессуары: Легкий шелковый шейный платок.",
            },
            "streetwear": {
                "freezing": "• Верх: Объемный пуховик (oversized puffer), теплое худи на флисе.\n• Низ: Плотные брюки-карго с флисовой подкладкой.\n• Обувь: Массивные зимние хайкеры или утепленные кроссовки.\n• Аксессуары: Шапка-бини (beanie) и балаклава.",
                "cold": "• Верх: Укороченная куртка-пуховик, плотное оверсайз худи.\n• Низ: Свободные джинсы прямого кроя (baggy jeans).\n• Обувь: Кожаные высокие кроссовки (high-top sneakers).\n• Аксессуары: Текстильный шоппер с ярким принтом.",
                "chilly": "• Верх: Куртка-бомбер или оверсайз ветровка поверх свитшота.\n• Низ: Широкие штаны-джоггеры или джинсы карго.\n• Обувь: Ретро-кроссовки на толстой подошве.\n• Аксессуары: Бейсболка (кепка) и кросс-боди сумка.",
                "warm": "• Верх: Плотная оверсайз футболка с принтом поверх рубашки нараспашку.\n• Низ: Джинсовые свободные шорты (бермуды) или карго.\n• Обувь: Кеды для скейта (Vans / Converse).\n• Аксессуары: Солнцезащитные очки формы «вайфарер».",
                "hot": "• Верх: Майка свободного кроя или легкая футболка oversize.\n• Низ: Спортивные сетчатые шорты.\n• Обувь: Легкие тканевые кеды или спортивные сандалии.\n• Аксессуары: Панама (bucket hat) и поясная сумка.",
            },
        },
    },
    "en": {
        "title": "Smart Stylist",
        "subtitle": "Personal capsule wardrobe powered by real-time weather",
        "language": "Language",
        "city": "City",
        "city_placeholder": "Enter city (Paris, London, NYC...)",
        "style": "Style preference",
        "casual": "Casual",
        "business": "Business Chic",
        "streetwear": "Streetwear",
        "button": "Build Outfit",
        "result": "Recommended Outfit Details:",
        "weather": "Current weather",
        "error": "City not found. Please try again with Latin letters!",
        "outfits": {
            "casual": {
                "freezing": "• Top: Long hooded puffer coat, chunky wool knit sweater.\n• Bottom: Thermal straight-leg denim.\n• Shoes: Insulated lug-sole leather boots.\n• Accessories: Oversized ribbed scarf, knit beanie and gloves.",
                "cold": "• Top: Midi wool coat, cozy cashmere jumper.\n• Bottom: Classic dark-wash jeans.\n• Shoes: Leather Chelsea boots.\n• Accessories: Soft cashmere scarf and leather gloves.",
                "chilly": "• Top: Classic trench coat, cotton long-sleeve tee.\n• Bottom: Wide-leg or mom-fit jeans.\n• Shoes: Clean white sneakers.\n• Accessories: Structured leather tote bag.",
                "warm": "• Top: Light denim jacket or knit cardigan over a basic tee.\n• Bottom: Chino trousers or a midi skirt.\n• Shoes: Canvas sneakers or casual loafers.\n• Accessories: Minimal sunglasses.",
                "hot": "• Top: Breathable organic cotton T-shirt or tank top.\n• Bottom: Linen shorts or a flowy summer skirt.\n• Shoes: Strappy sandals or espadrilles.\n• Accessories: Woven straw bag and sunglasses.",
            },
            "business": {
                "freezing": "• Top: Tailored wool winter coat, merino knit over a collared shirt.\n• Bottom: Heavy wool tailored trousers.\n• Shoes: Shearling-lined dress boots or oxfords.\n• Accessories: Neutral tone cashmere scarf.",
                "cold": "• Top: Structured wool overcoat, blazer, crisp button-down shirt.\n• Bottom: Straight tailored suit trousers.\n• Shoes: Leather ankle boots or monk strap shoes.\n• Accessories: Leather briefcase or structured tote.",
                "chilly": "• Top: Double-breasted trench, modern blazer, silk blouse.\n• Bottom: Cigarette cut or pleated trousers.\n• Shoes: Polished leather loafers.\n• Accessories: Elegant wristwatch.",
                "warm": "• Top: Crisp cotton tailored shirt or short-sleeved blouse.\n• Bottom: Lightweight trousers or pencil skirt.\n• Shoes: Leather loafers or pointed-toe flats.\n• Accessories: Slim leather belt.",
                "hot": "• Top: Breathable linen shirt in neutral or pastel tone.\n• Bottom: Wide-leg linen palazzo trousers.\n• Shoes: Leather dress mules or perforated formal flats.\n• Accessories: Lightweight silk scarf.",
            },
            "streetwear": {
                "freezing": "• Top: Heavy oversized puffer jacket, fleece-lined hoodie.\n• Bottom: Thermal cargo pants.\n• Shoes: Insulated winter sneakers or chunky hiking boots.\n• Accessories: Knit beanie and winter balaclava.",
                "cold": "• Top: Cropped boxy puffer, heavyweight hoodie.\n• Bottom: Baggy skate jeans.\n• Shoes: High-top leather sneakers.\n• Accessories: Graphic canvas crossbody bag.",
                "chilly": "• Top: Oversized bomber jacket or windbreaker over a sweatshirt.\n• Bottom: Cargo pants or loose-fit sweatpants.\n• Shoes: Chunky retro sneakers.\n• Accessories: Dad cap and compact shoulder bag.",
                "warm": "• Top: Boxy graphic tee worn over an unbuttoned overshirt.\n• Bottom: Baggy denim bermuda shorts or cargo pants.\n• Shoes: Classic skate shoes.\n• Accessories: Retro sunglasses.",
                "hot": "• Top: Relaxed oversized graphic T-shirt or tank.\n• Bottom: Mesh shorts or lightweight nylon shorts.\n• Shoes: Breathable canvas low-tops.\n• Accessories: Streetwear bucket hat.",
            },
        },
    },
    "fr": {
        "title": "Styliste Chic",
        "subtitle": "Garde-robe capsule selon la météo en temps réel",
        "language": "Langue",
        "city": "Ville",
        "city_placeholder": "Entrez la ville (Paris, Lyon...)",
        "style": "Style",
        "casual": "Casual",
        "business": "Business Chic",
        "streetwear": "Streetwear",
        "button": "Créer le Look",
        "result": "Détails de la tenue conseillée :",
        "weather": "Météo actuelle",
        "error": "Ville introuvable. Veuillez vérifier l'orthographe !",
        "outfits": {
            "casual": {
                "freezing": "• Haut: Manteau matelassé long à capuche, gros pull en laine.\n• Bas: Jean épais doublé.\n• Chaussures: Bottines fourrées à semelle crantée.\n• Accessoires: Écharpe oversize en maille et bonnet.",
                "cold": "• Haut: Manteau droit en laine, pull en cachemire.\n• Bas: Jean brut droit classique.\n• Chaussures: Bottines Chelsea en cuir.\n• Accessoires: Foulard doux et gants en cuir.",
                "chilly": "• Haut: Trench-coat ceinturé classique, t-shirt manches longues.\n• Bas: Jean large ou coupe mom.\n• Chaussures: Baskets blanches minimalistes.\n• Accessoires: Grand sac cabas (tote bag).",
                "warm": "• Haut: Veste en jean ou cardigan léger sur t-shirt basique.\n• Bas: Pantalon chino ou jupe midi fluide.\n• Chaussures: Mocassins légers ou tennis en toile.\n• Accessoires: Lunettes de soleil élégantes.",
                "hot": "• Haut: T-shirt léger en coton bio ou débardeur.\n• Bas: Short en lin ou jupe d'été.\n• Chaussures: Sandales ouvertes ou espadrilles.\n• Accessoires: Sac en paille tressée et chapeau d'été.",
            },
            "business": {
                "freezing": "• Haut: Manteau d'hiver cintré en laine, pull mérinos sur chemise.\n• Bas: Pantalon de tailleur en flanelle de laine.\n• Chaussures: Bottines élégantes en cuir doublées.\n• Accessoires: Écharpe sobre en cachemire.",
                "cold": "• Haut: Manteau habillé en laine, blazer structuré, chemise blanche.\n• Bas: Pantalon droit habillé à pinces.\n• Chaussures: Richelieus ou bottines en cuir ciré.\n• Accessoires: Porte-documents chic.",
                "chilly": "• Haut: Trench chic, veste de tailleur, chemisier en soie.\n• Bas: Pantalon cigarette ou droit classique.\n• Chaussures: Mocassins fermés en cuir.\n• Accessoires: Montre fine et délicate.",
                "warm": "• Haut: Chemise ajustée en popeline de coton.\n• Bas: Pantalon tailleur léger ou jupe crayon.\n• Chaussures: Ballerines pointues ou mocassins souples.\n• Accessoires: Ceinture en cuir fine.",
                "hot": "• Haut: Chemise respirante en lin clair.\n• Bas: Pantalon palazzo ample en lin.\n• Chaussures: Mules en cuir ouvertes.\n• Accessoires: Petit carré de soie au cou.",
            },
            "streetwear": {
                "freezing": "• Haut: Doudoune oversize épaisse, hoodie polaire doublé.\n• Bas: Pantalon cargo thermique.\n• Chaussures: Baskets montantes d'hiver ou bottes de randonnée.\n• Accessoires: Bonnet beanie côtelé et cagoule urbaine.",
                "cold": "• Haut: Doudoune courte bouffante, sweat à capuche épais.\n• Bas: Jean large rétro (baggy jeans).\n• Chaussures: Baskets montantes en cuir.\n• Accessoires: Sacoche streetwear en toile.",
                "chilly": "• Haut: Bomber jacket ou coupe-vent oversize sur sweat.\n• Bas: Pantalon cargo ample ou bas de jogging molletonné.\n• Chaussures: Baskets rétro chunky.\n• Accessoires: Casquette classique et sac bandoulière.",
                "warm": "• Haut: T-shirt graphique oversize sur surchemise ouverte.\n• Bas: Bermuda large en denim ou pantalon cargo léger.\n• Chaussures: Baskets de skate en toile.\n• Accessoires: Lunettes de soleil rétro.",
                "hot": "• Haut: Débardeur streetwear ample ou t-shirt léger oversize.\n• Bas: Short de basket en mesh respirant.\n• Chaussures: Baskets basses ultra-légères.\n• Accessoires: Chapeau bob (bucket hat).",
            },
        },
    },
}


@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.values.get("lang", "ru")
    if lang not in TEXTS:
        lang = "ru"
    t = TEXTS[lang]

    result, weather_text, error, city, style = None, None, None, "", "casual"
    left_img, right_img = DEFAULT_IMAGES[0], DEFAULT_IMAGES[1]

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        style = request.form.get("style", "casual")
        weather_data = get_weather(city, lang)

        if weather_data is None:
            error = t["error"]
        else:
            temp = weather_data["temperature"]
            weather_text = f"{temp}°C, {weather_data['description']}"

            
            if temp <= 0:
                cat = "freezing"
            elif 1 <= temp <= 10:
                cat = "cold"
            elif 11 <= temp <= 17:
                cat = "chilly"
            elif 18 <= temp <= 23:
                cat = "warm"
            else:  # >= 24
                cat = "hot"

            result = t["outfits"][style][cat]
            left_img = OUTFIT_IMAGES[style][cat][0]
            right_img = OUTFIT_IMAGES[style][cat][1]

    return render_template(
        "index.html",
        t=t,
        lang=lang,
        city=city,
        style=style,
        result=result,
        weather_text=weather_text,
        error=error,
        left_img=left_img,
        right_img=right_img,
    )


if __name__ == "__main__":
    app.run(debug=True)
