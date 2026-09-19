from datetime import date, datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


# ============================================================
# USER REQUEST
# ============================================================

class RecommendationRequest(BaseModel):
    max_calories: Optional[float] = Field(
        default=None,
        ge=0
    )

    min_protein_g: Optional[float] = Field(
        default=None,
        ge=0
    )

    max_carbs_g: Optional[float] = Field(
        default=None,
        ge=0
    )

    max_fat_g: Optional[float] = Field(
        default=None,
        ge=0
    )

    max_sugar_g: Optional[float] = Field(
        default=None,
        ge=0
    )

    dietary_restrictions: list[str] = Field(
        default_factory=list
    )

    allergies: list[str] = Field(
        default_factory=list
    )

    meal_period: Optional[
        Literal[
            "breakfast",
            "lunch",
            "dinner",
            "late_night"
        ]
    ] = None

    # This is the value selected from the frontend dropdown.
    #
    # Examples:
    # "Dietrick Hall"
    # "Ducky's at GLC"
    # "Owens Hall"
    # "Perry Place / Hitt Hall"
    # "Turner Place"
    # "Squires Food Court"
    # "Viva Market"
    # "West End / Cochrane Hall"
    # "Not sure / No preference"
    dining_location: str = "Not sure / No preference"

    priority: Literal[
        "balanced",
        "nutrition",
        "convenience"
    ] = "balanced"

    other_preferences: Optional[str] = None


# ============================================================
# NUTRITION RESPONSE
# ============================================================

class NutritionResponse(BaseModel):
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    sugar_g: Optional[float] = None


# ============================================================
# RECOMMENDATION ITEM
# ============================================================

class RecommendationItem(BaseModel):
    id: str

    food_name: str

    location_name: str

    meal_period: Optional[str] = None

    nutrition: NutritionResponse

    dietary_tags: list[str] = Field(
        default_factory=list
    )

    allergens: list[str] = Field(
        default_factory=list
    )

    availability_status: str = "unknown"

    menu_date: date

    match_explanation: list[str] = Field(
        default_factory=list
    )


# ============================================================
# ADJUSTMENT / NO-EXACT-MATCH OPTION
# ============================================================

class Adjustment(BaseModel):
    id: str

    label: str

    change: dict[str, float]

    matching_option_count: int


# ============================================================
# FINAL RESPONSE
# ============================================================

class RecommendationResponse(BaseModel):
    status: Literal[
        "matches_found",
        "no_exact_matches"
    ]

    data_source: str

    generated_at: datetime

    recommendations: list[
        RecommendationItem
    ] = Field(
        default_factory=list
    )

    adjustments: list[
        Adjustment
    ] = Field(
        default_factory=list
    )