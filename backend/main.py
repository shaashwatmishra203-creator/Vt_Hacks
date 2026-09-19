from datetime import date, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)

from services.vt_dining import (
    VTDiningConnector,
)

from services.recommendation import (
    RecommendationService,
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="VT Dining AI",
    description=(
        "Virginia Tech student dining "
        "recommendation backend"
    ),
    version="0.2.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "project": "VT Dining AI",
        "version": "0.2.0",
        "message": (
            "Backend is working"
        )
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "timestamp": (
            datetime.now().isoformat()
        )
    }


# ============================================================
# API TEST
# ============================================================

@app.get("/api/test")
def test():

    return {
        "message": (
            "API connection successful"
        )
    }


# ============================================================
# DINING LOCATIONS
# ============================================================

@app.get("/dining-locations")
def get_dining_locations():

    connector = VTDiningConnector()

    return {
        "locations": (
            connector.get_dining_locations()
        )
    }


# ============================================================
# MENU TEST ENDPOINT
# ============================================================

@app.get("/api/menu")
def get_menu():

    connector = VTDiningConnector()

    return connector.get_all_foods(
        "15",
        "9/19/2026",
        "D2"
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

@app.post(
    "/recommend",
    response_model=RecommendationResponse
)
def recommend(
    request: RecommendationRequest
):

    connector = VTDiningConnector()

    # --------------------------------------------------------
    # REAL VT DINING DATA
    # --------------------------------------------------------
    #
    # The connector retrieves the current menu and
    # nutrition data from the official VT Dining API.
    #
    # Future Databricks processing can be inserted between
    # this data retrieval step and the recommendation service.
    # --------------------------------------------------------

    foods = connector.get_foods_for_group(
        dining_location=(
            request.dining_location
        ),
        date=(
            date.today().strftime(
                "%-m/%-d/%Y"
            )
            if False
            else (
                f"{date.today().month}/"
                f"{date.today().day}/"
                f"{date.today().year}"
            )
        )
    )

    # --------------------------------------------------------
    # DETERMINISTIC RECOMMENDATION ENGINE
    # --------------------------------------------------------
    #
    # AI is NOT used to select food.
    # --------------------------------------------------------

    service = RecommendationService()

    return service.recommend(
        request=request,
        foods=foods
    )