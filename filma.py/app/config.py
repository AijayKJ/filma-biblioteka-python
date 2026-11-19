# =====================================================
# DATUBĀZU KONFIGURĀCIJA
# =====================================================
DB_FAILS = "filmu_biblioteka.db"

TABULAS = {
    "movies": [
        "title", "release_year", "genre_id", "director_id",
        "runtime_minutes", "synopsis", "studio_id"
    ],
    "actors": [
        "name", "birthday", "nationality"
    ],
    "directors": [
        "name", "birthday", "nationality"
    ],
    "genres": [
        "name", "description"
    ],
    "studios": [
        "name", "country", "founded_year", "website"
    ],
    "users": [
        "username", "email", "password_hash", "full_name"
    ],
    "watchlist_items": [
        "user_id", "movie_id"
    ],
    "reviews": [
        "user_id", "movie_id", "rating", "body"
    ],
    "movie_cast": [
        "movie_id", "actor_id", "character_name", "billing_order"
    ],
    "movie_awards": [
        "movie_id", "actor_id", "award_name", "category",
        "award_year", "won"
    ]
}

NOSAUKUMI = {
    "movies": "Filmas",
    "actors": "Aktieri",
    "directors": "Režisori",
    "genres": "Žanri",
    "studios": "Studijas",
    "users": "Lietotāji",
    "watchlist_items": "Skatīšanās saraksti",
    "reviews": "Atsauksmes",
    "movie_cast": "Filmu lomas",
    "movie_awards": "Filmu balvas"
}

FK = {
    "genre_id": ("genres", "name"),
    "director_id": ("directors", "name"),
    "studio_id": ("studios", "name"),
    "user_id": ("users", "username"),
    "movie_id": ("movies", "title"),
    "actor_id": ("actors", "name")
}

LAUKU_NOSAUKUMI = {
    "title": "Filmas nosaukums",
    "release_year": "Izdošanas gads",
    "genre_id": "Žanrs",
    "director_id": "Režisors",
    "runtime_minutes": "Ilgums (min)",
    "synopsis": "Apraksts",
    "studio_id": "Studija",
    "name": "Nosaukums",
    "birthday": "Dzimšanas datums",
    "nationality": "Valstiskā piederība",
    "description": "Apraksts",
    "country": "Valsts",
    "founded_year": "Dibināšanas gads",
    "website": "Tīmekļa vietne",
    "username": "Lietotājvārds",
    "email": "E-pasts",
    "password_hash": "Paroles jaucējvērtība",
    "full_name": "Pilns vārds",
    "user_id": "Lietotājs",
    "movie_id": "Filma",
    "actor_id": "Aktieris",
    "rating": "Vērtējums (1–10)",
    "body": "Atsauksmes teksts",
    "character_name": "Tēla vārds",
    "billing_order": "Lomas secība",
    "award_name": "Balvas nosaukums",
    "category": "Kategorija",
    "award_year": "Balvas gads",
    "won": "Balva iegūta (0/1)"
}
