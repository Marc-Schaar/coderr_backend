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
    {
        "username": "designstudio_elena",
        "first_name": "Elena",
        "last_name": "Rossi",
        "email": "elena.rossi@designstudio.example",
        "location": "Mailand, Italien",
        "description": "Brand- und Verpackungsdesignerin mit einem Auge für minimalistische, italienische Ästhetik.",
        "working_hours": "Mo-Fr 9-18 Uhr",
        "offers": [
            {
                "title": "Corporate-Design-Paket",
                "description": "Vollständiges Markenpaket bestehend aus Logo, Farbwelt, Typografie und Geschäftsausstattung.",
                "details": [
                    ("Basic", 2, 6, 180, ["Logo-Redesign", "Farbpalette", "1 Revision"]),
                    ("Standard", 4, 8, 380, ["Logo-Redesign", "Farbpalette", "Typografie-Guide", "3 Revisionen"]),
                    ("Premium", 6, 12, 650, ["Komplettes Brand-Book", "Geschäftsausstattung", "Unbegrenzte Revisionen"]),
                ],
            },
            {
                "title": "Verpackungsdesign",
                "description": "Individuelles Verpackungsdesign für Food- und Beauty-Produkte.",
                "details": [
                    ("Basic", 1, 5, 120, ["1 Verpackungsdesign", "1 Revision"]),
                    ("Standard", 3, 7, 280, ["3 Verpackungsvarianten", "Drucklayout", "2 Revisionen"]),
                    ("Premium", 5, 10, 500, ["5 Verpackungsvarianten", "Drucklayout", "Mockups", "Unbegrenzte Revisionen"]),
                ],
            },
        ],
    },
    {
        "username": "devstudio_carlos",
        "first_name": "Carlos",
        "last_name": "Mendes",
        "email": "carlos.mendes@devstudio.example",
        "location": "Lissabon, Portugal",
        "description": "Backend-Entwickler mit Schwerpunkt auf E-Commerce-Plattformen und Zahlungsanbindungen.",
        "working_hours": "Mo-Fr 8-16 Uhr",
        "offers": [
            {
                "title": "Onlineshop-Einrichtung",
                "description": "Einrichtung eines individuellen Onlineshops inklusive Zahlungsanbindung und Produktimport.",
                "details": [
                    ("Basic", 2, 7, 400, ["Bis zu 20 Produkte", "1 Zahlungsanbieter", "2 Revisionen"]),
                    ("Standard", 4, 12, 900, ["Bis zu 100 Produkte", "2 Zahlungsanbieter", "Versandkonfiguration"]),
                    ("Premium", 8, 18, 1800, ["Unbegrenzte Produkte", "Alle Zahlungsanbieter", "Individuelle Erweiterungen"]),
                ],
            },
        ],
    },
    {
        "username": "wordcraft_amara",
        "first_name": "Amara",
        "last_name": "Okafor",
        "email": "amara.okafor@wordcraft.example",
        "location": "Lagos, Nigeria",
        "description": "Content-Strategin und Copywriterin für internationale Marken und Startups.",
        "working_hours": "Di-Sa 10-16 Uhr",
        "offers": [
            {
                "title": "Website-Copywriting",
                "description": "Überzeugende, konversionsorientierte Texte für Landingpages und Firmenwebsites.",
                "details": [
                    ("Basic", 1, 4, 90, ["Bis zu 3 Seiten", "1 Revision"]),
                    ("Standard", 2, 6, 200, ["Bis zu 6 Seiten", "Tonalitäts-Guide", "2 Revisionen"]),
                    ("Premium", 4, 8, 380, ["Bis zu 12 Seiten", "A/B-Testing-Varianten", "Unbegrenzte Revisionen"]),
                ],
            },
            {
                "title": "E-Mail-Newsletter-Reihe",
                "description": "Aufbau einer mehrteiligen Newsletter-Kampagne inklusive Betreffzeilen-Optimierung.",
                "details": [
                    ("Basic", 3, 3, 70, ["3 Newsletter", "1 Revision"]),
                    ("Standard", 6, 5, 130, ["6 Newsletter", "Betreffzeilen-Varianten", "2 Revisionen"]),
                    ("Premium", 12, 7, 240, ["12 Newsletter", "Automatisierungs-Setup", "3 Revisionen"]),
                ],
            },
        ],
    },
    {
        "username": "pixelworks_yuki",
        "first_name": "Yuki",
        "last_name": "Tanaka",
        "email": "yuki.tanaka@pixelworks.example",
        "location": "Tokio, Japan",
        "description": "Fotografin für Events, Portraits und minimalistische Produktshootings.",
        "working_hours": "Mi-So 10-19 Uhr",
        "offers": [
            {
                "title": "Event-Fotografie",
                "description": "Professionelle Begleitung von Firmenevents, Konferenzen und Produktlaunches.",
                "details": [
                    ("Basic", 0, 5, 220, ["3 Stunden vor Ort", "50 bearbeitete Fotos"]),
                    ("Standard", 1, 5, 420, ["6 Stunden vor Ort", "150 bearbeitete Fotos", "1 Revision"]),
                    ("Premium", 2, 7, 750, ["Ganztägig vor Ort", "Unbegrenzte Fotos", "Highlight-Video"]),
                ],
            },
        ],
    },
    {
        "username": "uxlab_sofia",
        "first_name": "Sofia",
        "last_name": "Lindqvist",
        "email": "sofia.lindqvist@uxlab.example",
        "location": "Stockholm, Schweden",
        "description": "UX/UI-Designerin mit Fokus auf skandinavisches, nutzerzentriertes Interfacedesign.",
        "working_hours": "Mo-Fr 9-17 Uhr",
        "offers": [
            {
                "title": "App-UI/UX-Design",
                "description": "Nutzerzentriertes Interface-Design für mobile Apps, von Wireframe bis High-Fidelity-Prototyp.",
                "details": [
                    ("Basic", 2, 8, 350, ["Wireframes", "5 Screens", "1 Revision"]),
                    ("Standard", 4, 12, 750, ["High-Fidelity-Design", "12 Screens", "Klickbarer Prototyp"]),
                    ("Premium", 8, 18, 1400, ["Komplettes Design-System", "Unbegrenzte Screens", "Usability-Test"]),
                ],
            },
            {
                "title": "Usability-Testing",
                "description": "Strukturierte Usability-Tests mit echten Nutzern inklusive Auswertungsbericht.",
                "details": [
                    ("Basic", 1, 5, 180, ["3 Testpersonen", "Kurzbericht"]),
                    ("Standard", 2, 7, 350, ["6 Testpersonen", "Ausführlicher Bericht", "Handlungsempfehlungen"]),
                    ("Premium", 3, 10, 600, ["10 Testpersonen", "Videoaufzeichnungen", "Workshop zur Auswertung"]),
                ],
            },
        ],
    },
    {
        "username": "videoedit_ahmed",
        "first_name": "Ahmed",
        "last_name": "El-Sayed",
        "email": "ahmed.elsayed@videoedit.example",
        "location": "Kairo, Ägypten",
        "description": "Video-Editor und Motion-Designer für Social-Media-Content und Werbespots.",
        "working_hours": "So-Do 11-19 Uhr",
        "offers": [
            {
                "title": "Social-Media-Video-Schnitt",
                "description": "Dynamischer Videoschnitt für Reels, TikTok und YouTube Shorts inklusive Untertiteln.",
                "details": [
                    ("Basic", 3, 3, 60, ["1 Video bis 60 Sek.", "Untertitel", "1 Revision"]),
                    ("Standard", 5, 4, 150, ["3 Videos bis 60 Sek.", "Untertitel", "Sounddesign"]),
                    ("Premium", 10, 6, 280, ["5 Videos", "Motion-Graphics-Elemente", "Unbegrenzte Revisionen"]),
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
    {"username": "kunde_maria", "first_name": "Maria", "last_name": "Garcia", "email": "maria.garcia@example.com"},
    {"username": "kunde_liam", "first_name": "Liam", "last_name": "O'Brien", "email": "liam.obrien@example.com"},
    {"username": "kunde_priya", "first_name": "Priya", "last_name": "Sharma", "email": "priya.sharma@example.com"},
    {"username": "kunde_wei", "first_name": "Wei", "last_name": "Chen", "email": "wei.chen@example.com"},
    {"username": "kunde_fatima", "first_name": "Fatima", "last_name": "Al-Sayed", "email": "fatima.alsayed@example.com"},
    {"username": "kunde_olga", "first_name": "Olga", "last_name": "Ivanova", "email": "olga.ivanova@example.com"},
    {"username": "kunde_joao", "first_name": "João", "last_name": "Silva", "email": "joao.silva@example.com"},
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
    "Great communication throughout the whole project, would book again.",
    "Sehr kreative Lösungen, die genau zu unserer Marke gepasst haben.",
    "Termintreu und unkompliziert - genau das, was wir gesucht haben.",
    "Die Qualität hat unsere Erwartungen klar übertroffen, sehr empfehlenswert.",
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
            for customer in random.sample(customer_users, k=min(4, len(customer_users))):
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
            reviewers = random.sample(customer_users, k=min(6, len(customer_users)))
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
