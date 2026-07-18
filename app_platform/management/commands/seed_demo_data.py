import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.authtoken.models import Token

from app_offers.models import Offer, OfferDetails
from app_orders.models import Order
from app_reviews.models import Review

User = get_user_model()

BUSINESS_USERS = [
    {
        "username": "kreativstudio_anna",
        "first_name": "Anna",
        "last_name": "Berger",
        "email": "anna.berger@kreativstudio.example",
        "location": "Berlin",
        "description": "Freelance Grafikdesignerin mit Fokus auf Branding und Logodesign.",
        "working_hours": "Mo-Fr 9-17 Uhr",
        "offers": [
            {
                "title": "Professionelles Logodesign",
                "description": "Individuelles, modernes Logodesign für dein Unternehmen inklusive mehrerer Entwurfsvarianten.",
                "details": [
                    ("Basic", 1, 5, 60, ["1 Logo-Konzept", "1 Revision", "PNG-Datei"]),
                    ("Standard", 3, 4, 150, ["3 Logo-Konzepte", "3 Revisionen", "PNG & SVG-Datei"]),
                    ("Premium", 5, 3, 300, ["5 Logo-Konzepte", "Unbegrenzte Revisionen", "Alle Dateiformate", "Styleguide"]),
                ],
            },
            {
                "title": "Social-Media-Grafikpaket",
                "description": "Einheitliches Grafikpaket für Instagram, Facebook und LinkedIn.",
                "details": [
                    ("Basic", 5, 3, 80, ["5 Post-Vorlagen", "1 Revision"]),
                    ("Standard", 10, 3, 160, ["10 Post-Vorlagen", "3 Revisionen", "Story-Vorlagen"]),
                    ("Premium", 20, 5, 320, ["20 Post-Vorlagen", "Unbegrenzte Revisionen", "Story- & Highlight-Cover"]),
                ],
            },
        ],
    },
    {
        "username": "webdev_marco",
        "first_name": "Marco",
        "last_name": "Fischer",
        "email": "marco.fischer@webdev.example",
        "location": "München",
        "description": "Full-Stack-Entwickler spezialisiert auf React, Django und performante Webanwendungen.",
        "working_hours": "Mo-Sa 10-18 Uhr",
        "offers": [
            {
                "title": "Responsive Website-Entwicklung",
                "description": "Moderne, responsive Website nach Maß mit React oder klassischem HTML/CSS/JS.",
                "details": [
                    ("Basic", 2, 7, 300, ["Bis zu 3 Seiten", "Responsive Design", "2 Revisionen"]),
                    ("Standard", 4, 10, 700, ["Bis zu 6 Seiten", "Responsive Design", "SEO-Grundlagen", "4 Revisionen"]),
                    ("Premium", 8, 14, 1500, ["Unbegrenzte Seiten", "CMS-Integration", "SEO-Optimierung", "8 Revisionen"]),
                ],
            },
            {
                "title": "REST-API Entwicklung mit Django",
                "description": "Aufbau einer sauberen, dokumentierten REST-API mit Django REST Framework.",
                "details": [
                    ("Basic", 2, 5, 250, ["Bis zu 3 Endpunkte", "Basis-Authentifizierung"]),
                    ("Standard", 4, 8, 600, ["Bis zu 8 Endpunkte", "Token-Authentifizierung", "Tests"]),
                    ("Premium", 6, 12, 1200, ["Unbegrenzte Endpunkte", "JWT-Auth", "CI/CD-Setup", "Ausführliche Tests"]),
                ],
            },
        ],
    },
    {
        "username": "textwerk_julia",
        "first_name": "Julia",
        "last_name": "Hoffmann",
        "email": "julia.hoffmann@textwerk.example",
        "location": "Hamburg",
        "description": "Texterin für Webseiten, Blogartikel und SEO-optimierten Content.",
        "working_hours": "Di-Fr 8-14 Uhr",
        "offers": [
            {
                "title": "SEO-Blogartikel",
                "description": "Recherchierte und SEO-optimierte Blogartikel für deine Website.",
                "details": [
                    ("Basic", 1, 3, 40, ["500 Wörter", "1 Revision"]),
                    ("Standard", 2, 4, 90, ["1000 Wörter", "Keyword-Recherche", "2 Revisionen"]),
                    ("Premium", 3, 5, 180, ["2000 Wörter", "Keyword-Recherche", "Meta-Beschreibung", "3 Revisionen"]),
                ],
            },
        ],
    },
    {
        "username": "fotoart_leon",
        "first_name": "Leon",
        "last_name": "Wagner",
        "email": "leon.wagner@fotoart.example",
        "location": "Köln",
        "description": "Produktfotograf für E-Commerce und Social Media.",
        "working_hours": "Mo-Fr 9-16 Uhr",
        "offers": [
            {
                "title": "Produktfotografie für Onlineshops",
                "description": "Professionelle Produktfotos mit neutralem Hintergrund, optimiert für Onlineshops.",
                "details": [
                    ("Basic", 5, 3, 100, ["5 Produktfotos", "1 Revision"]),
                    ("Standard", 15, 4, 250, ["15 Produktfotos", "Freistellung", "2 Revisionen"]),
                    ("Premium", 30, 6, 450, ["30 Produktfotos", "Freistellung", "Bildbearbeitung", "3 Revisionen"]),
                ],
            },
        ],
    },
]

CUSTOMER_USERS = [
    {"username": "kunde_stefan", "first_name": "Stefan", "last_name": "Klein", "email": "stefan.klein@example.com"},
    {"username": "kunde_melanie", "first_name": "Melanie", "last_name": "Neumann", "email": "melanie.neumann@example.com"},
    {"username": "kunde_thomas", "first_name": "Thomas", "last_name": "Schulz", "email": "thomas.schulz@example.com"},
    {"username": "kunde_sarah", "first_name": "Sarah", "last_name": "Vogel", "email": "sarah.vogel@example.com"},
    {"username": "kunde_david", "first_name": "David", "last_name": "Krause", "email": "david.krause@example.com"},
]

REVIEW_TEXTS = [
    "Sehr professionelle Zusammenarbeit, klare Kommunikation und pünktliche Lieferung.",
    "Top Qualität, gerne wieder!",
    "Ergebnis hat meine Erwartungen übertroffen.",
    "Schnelle Umsetzung und faire Preise.",
    "Freundlich, zuverlässig und kreativ - kann ich nur empfehlen.",
    "Gute Arbeit, kleine Verzögerung bei der Lieferung.",
    "Absolut zufrieden mit dem Endergebnis.",
    "Hat alle Wünsche berücksichtigt und war sehr geduldig.",
]

DEFAULT_PASSWORD = "Demo1234!"


class Command(BaseCommand):
    help = "Legt Demo-/Dummy-Daten (Business-User, Angebote, Kunden, Bestellungen, Bewertungen) fuer Portfolio-Praesentationen an."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Loescht zuvor mit diesem Command angelegte Demo-Daten, bevor neue erzeugt werden.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            self._flush_demo_data()

        with transaction.atomic():
            business_users = self._create_business_users()
            customer_users = self._create_customer_users()
            offers = self._create_offers(business_users)
            self._create_orders(business_users, customer_users, offers)
            self._create_reviews(business_users, customer_users)

        self.stdout.write(self.style.SUCCESS("Demo-Daten erfolgreich angelegt."))
        self.stdout.write(f"Business-User Login-Beispiel: {business_users[0].username} / {DEFAULT_PASSWORD}")
        self.stdout.write(f"Kunden-User Login-Beispiel: {customer_users[0].username} / {DEFAULT_PASSWORD}")

    def _flush_demo_data(self):
        all_usernames = [b["username"] for b in BUSINESS_USERS] + [c["username"] for c in CUSTOMER_USERS]
        deleted, _ = User.objects.filter(username__in=all_usernames).delete()
        self.stdout.write(f"{deleted} vorhandene Demo-Datensaetze entfernt.")

    def _create_business_users(self):
        users = []
        for data in BUSINESS_USERS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "type": "business",
                },
            )
            if created:
                user.set_password(DEFAULT_PASSWORD)
                user.save()
                Token.objects.get_or_create(user=user)
                self.stdout.write(f"Business-User angelegt: {user.username}")

            profile = user.profile
            profile.location = data["location"]
            profile.tel = f"+49 {random.randint(100, 999)} {random.randint(1000000, 9999999)}"
            profile.description = data["description"]
            profile.working_hours = data["working_hours"]
            profile.save()

            users.append(user)
        return users

    def _create_customer_users(self):
        users = []
        for data in CUSTOMER_USERS:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "type": "customer",
                },
            )
            if created:
                user.set_password(DEFAULT_PASSWORD)
                user.save()
                Token.objects.get_or_create(user=user)
                self.stdout.write(f"Kunden-User angelegt: {user.username}")
            users.append(user)
        return users

    def _create_offers(self, business_users):
        offers = []
        for business_data, user in zip(BUSINESS_USERS, business_users):
            for offer_data in business_data["offers"]:
                offer, created = Offer.objects.get_or_create(
                    user=user,
                    title=offer_data["title"],
                    defaults={"description": offer_data["description"]},
                )
                if not created:
                    offers.append(offer)
                    continue

                prices = []
                delivery_times = []
                for offer_type, revisions, delivery_time, price, features in offer_data["details"]:
                    OfferDetails.objects.create(
                        offer=offer,
                        title=f"{offer_data['title']} - {offer_type}",
                        revisions=revisions,
                        delivery_time_in_days=delivery_time,
                        price=price,
                        features=features,
                        offer_type=offer_type.lower(),
                    )
                    prices.append(price)
                    delivery_times.append(delivery_time)

                offer.min_price = min(prices)
                offer.min_delivery_time = min(delivery_times)
                offer.save()

                self.stdout.write(f"Angebot angelegt: {offer.title} ({user.username})")
                offers.append(offer)
        return offers

    def _create_orders(self, business_users, customer_users, offers):
        statuses = ["in_progress", "completed", "completed", "cancelled"]
        created_count = 0
        for offer in offers:
            details = list(offer.details.all())
            if not details:
                continue
            for customer in random.sample(customer_users, k=min(2, len(customer_users))):
                detail = random.choice(details)
                order, created = Order.objects.get_or_create(
                    customer_user=customer,
                    business_user=offer.user,
                    title=detail.title,
                    defaults={
                        "revisions": detail.revisions,
                        "delivery_time_in_days": detail.delivery_time_in_days,
                        "price": detail.price,
                        "features": detail.features,
                        "offer_type": detail.offer_type,
                        "status": random.choice(statuses),
                    },
                )
                if created:
                    created_count += 1
        self.stdout.write(f"{created_count} Bestellungen angelegt.")

    def _create_reviews(self, business_users, customer_users):
        created_count = 0
        for business_user in business_users:
            reviewers = random.sample(customer_users, k=min(3, len(customer_users)))
            for reviewer in reviewers:
                _, created = Review.objects.get_or_create(
                    business_user=business_user,
                    reviewer=reviewer,
                    defaults={
                        "rating": random.randint(3, 5),
                        "description": random.choice(REVIEW_TEXTS),
                    },
                )
                if created:
                    created_count += 1
        self.stdout.write(f"{created_count} Bewertungen angelegt.")
