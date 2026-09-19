from datetime import datetime
from typing import Any

from models.recommendation import (
    Adjustment,
    NutritionResponse,
    RecommendationItem,
    RecommendationRequest,
    RecommendationResponse,
)


class RecommendationService:
    """
    Deterministic recommendation engine.

    AI does NOT choose the food recommendations.

    This service:
    1. Applies the student's hard constraints.
    2. Filters by dining location.
    3. Filters dietary restrictions.
    4. Filters allergies.
    5. Filters meal period.
    6. Ranks the remaining foods.
    7. Generates explanations.
    8. Suggests constraint adjustments when
       no exact matches exist.
    """

    NO_PREFERENCE = (
        "Not sure / No preference"
    )

    # ========================================================
    # MAIN RECOMMENDATION FUNCTION
    # ========================================================

    def recommend(
        self,
        request: RecommendationRequest,
        foods: list[dict[str, Any]],
    ) -> RecommendationResponse:

        exact_matches = []

        for food in foods:

            if not self._matches(
                request,
                food
            ):
                continue

            exact_matches.append(
                self._build_recommendation_item(
                    request,
                    food
                )
            )

        exact_matches = self._rank_matches(
            request,
            exact_matches
        )

        # ----------------------------------------------------
        # Exact matches found
        # ----------------------------------------------------

        if exact_matches:

            return RecommendationResponse(
                status="matches_found",

                data_source="vt_dining",

                generated_at=datetime.now(),

                recommendations=(
                    exact_matches[:20]
                ),

                adjustments=[]
            )

        # ----------------------------------------------------
        # No exact matches
        # ----------------------------------------------------

        return RecommendationResponse(
            status="no_exact_matches",

            data_source="vt_dining",

            generated_at=datetime.now(),

            recommendations=[],

            adjustments=(
                self._build_adjustments(
                    request,
                    foods
                )
            )
        )

    # ========================================================
    # HARD FILTERS
    # ========================================================

    def _matches(
        self,
        request: RecommendationRequest,
        food: dict[str, Any]
    ) -> bool:

        # ----------------------------------------------------
        # Calories
        # ----------------------------------------------------

        if (
            request.max_calories is not None
            and self._number(
                food.get("calories")
            ) > request.max_calories
        ):
            return False

        # ----------------------------------------------------
        # Protein
        # ----------------------------------------------------

        if (
            request.min_protein_g is not None
            and self._number(
                food.get("protein")
            ) < request.min_protein_g
        ):
            return False

        # ----------------------------------------------------
        # Carbs
        # ----------------------------------------------------

        if (
            request.max_carbs_g is not None
            and self._number(
                food.get("carbs")
            ) > request.max_carbs_g
        ):
            return False

        # ----------------------------------------------------
        # Fat
        # ----------------------------------------------------

        if (
            request.max_fat_g is not None
            and self._number(
                food.get("fat")
            ) > request.max_fat_g
        ):
            return False

        # ----------------------------------------------------
        # Sugar
        # ----------------------------------------------------

        if (
            request.max_sugar_g is not None
            and self._number(
                food.get("sugar")
            ) > request.max_sugar_g
        ):
            return False

        # ----------------------------------------------------
        # Meal period
        # ----------------------------------------------------

        if request.meal_period is not None:

            if not self._meal_matches(
                request.meal_period,
                food.get("meal", "")
            ):
                return False

        # ----------------------------------------------------
        # Dietary restrictions
        # ----------------------------------------------------

        food_tags = [
            str(tag).lower()
            for tag in food.get(
                "dietary_tags",
                []
            )
        ]

        for restriction in (
            request.dietary_restrictions
        ):

            restriction_lower = (
                restriction.lower()
            )

            if restriction_lower not in food_tags:
                return False

        # ----------------------------------------------------
        # Allergies
        # ----------------------------------------------------

        food_allergens = str(
            food.get(
                "allergens",
                ""
            )
        ).lower()

        for allergy in request.allergies:

            if (
                allergy.lower()
                in food_allergens
            ):
                return False

        return True

    # ========================================================
    # MEAL MATCHING
    # ========================================================

    def _meal_matches(
        self,
        requested_meal: str,
        actual_meal: str
    ) -> bool:

        requested = (
            requested_meal
            .lower()
            .replace("_", " ")
        )

        actual = (
            actual_meal
            .lower()
        )

        return (
            requested in actual
            or actual in requested
        )

    # ========================================================
    # RANKING
    # ========================================================

    def _rank_matches(
        self,
        request: RecommendationRequest,
        matches: list[RecommendationItem]
    ) -> list[RecommendationItem]:

        # ----------------------------------------------------
        # Nutrition priority
        #
        # Higher protein first, then lower calories.
        # ----------------------------------------------------

        if request.priority == "nutrition":

            return sorted(
                matches,
                key=lambda item: (
                    -(
                        item.nutrition.protein_g
                        or 0
                    ),

                    item.nutrition.calories
                    if item.nutrition.calories
                    is not None
                    else float("inf")
                )
            )

        # ----------------------------------------------------
        # Convenience priority
        #
        # There is currently no walking-distance
        # calculation, so convenience uses simpler
        # menu relevance rather than fabricated distance.
        # ----------------------------------------------------

        if request.priority == "convenience":

            return sorted(
                matches,
                key=lambda item: (
                    item.location_name.lower(),
                    item.food_name.lower()
                )
            )

        # ----------------------------------------------------
        # Balanced priority
        #
        # Prefer higher protein and lower calories.
        # ----------------------------------------------------

        return sorted(
            matches,
            key=lambda item: (
                -(
                    item.nutrition.protein_g
                    or 0
                ),

                item.nutrition.calories
                if item.nutrition.calories
                is not None
                else float("inf")
            )
        )

    # ========================================================
    # BUILD RESPONSE ITEM
    # ========================================================

    def _build_recommendation_item(
        self,
        request: RecommendationRequest,
        food: dict[str, Any]
    ) -> RecommendationItem:

        nutrition = NutritionResponse(
            calories=self._number(
                food.get("calories")
            ),

            protein_g=self._number(
                food.get("protein")
            ),

            carbs_g=self._number(
                food.get("carbs")
            ),

            fat_g=self._number(
                food.get("fat")
            ),

            sugar_g=self._number(
                food.get("sugar")
            )
        )

        return RecommendationItem(
            id=str(
                food.get(
                    "recipe_id",
                    ""
                )
            ),

            food_name=str(
                food.get(
                    "name",
                    ""
                )
            ),

            location_name=str(
                food.get(
                    "location_name",
                    "Unknown"
                )
            ),

            meal_period=food.get(
                "meal"
            ),

            nutrition=nutrition,

            dietary_tags=[
                str(tag)
                for tag in food.get(
                    "dietary_tags",
                    []
                )
            ],

            allergens=self._parse_allergens(
                food.get(
                    "allergens",
                    ""
                )
            ),

            availability_status=(
                "available"
            ),

            menu_date=food.get(
                "menu_date"
            ),

            match_explanation=(
                self._build_explanation(
                    request,
                    food
                )
            )
        )

    # ========================================================
    # EXPLANATIONS
    # ========================================================

    def _build_explanation(
        self,
        request: RecommendationRequest,
        food: dict[str, Any]
    ) -> list[str]:

        explanations = []

        calories = self._number(
            food.get("calories")
        )

        protein = self._number(
            food.get("protein")
        )

        carbs = self._number(
            food.get("carbs")
        )

        fat = self._number(
            food.get("fat")
        )

        sugar = self._number(
            food.get("sugar")
        )

        if request.max_calories is not None:

            explanations.append(
                f"{calories:g} calories, "
                f"within your "
                f"{request.max_calories:g}-calorie limit"
            )

        if request.min_protein_g is not None:

            explanations.append(
                f"{protein:g}g protein, "
                f"meeting your "
                f"{request.min_protein_g:g}g minimum"
            )

        if request.max_carbs_g is not None:

            explanations.append(
                f"{carbs:g}g carbs, "
                f"within your limit"
            )

        if request.max_fat_g is not None:

            explanations.append(
                f"{fat:g}g fat, "
                f"within your limit"
            )

        if request.max_sugar_g is not None:

            explanations.append(
                f"{sugar:g}g sugar, "
                f"within your limit"
            )

        if request.dining_location != (
            self.NO_PREFERENCE
        ):

            explanations.append(
                f"Available at "
                f"{food.get('location_name')}"
            )

        return explanations

    # ========================================================
    # NO-MATCH ADJUSTMENTS
    # ========================================================

    def _build_adjustments(
        self,
        request: RecommendationRequest,
        foods: list[dict[str, Any]]
    ) -> list[Adjustment]:

        adjustments = []

        # ----------------------------------------------------
        # Increase calories
        # ----------------------------------------------------

        if request.max_calories is not None:

            increase = 50

            modified_request = (
                request.model_copy(
                    update={
                        "max_calories": (
                            request.max_calories
                            + increase
                        )
                    }
                )
            )

            count = sum(
                self._matches(
                    modified_request,
                    food
                )
                for food in foods
            )

            if count > 0:

                adjustments.append(
                    Adjustment(
                        id=(
                            "increase_calories_50"
                        ),

                        label="+50 calories",

                        change={
                            "max_calories": 50
                        },

                        matching_option_count=count
                    )
                )

        # ----------------------------------------------------
        # Reduce protein requirement
        # ----------------------------------------------------

        if request.min_protein_g is not None:

            decrease = 5

            modified_request = (
                request.model_copy(
                    update={
                        "min_protein_g": max(
                            0,
                            request.min_protein_g
                            - decrease
                        )
                    }
                )
            )

            count = sum(
                self._matches(
                    modified_request,
                    food
                )
                for food in foods
            )

            if count > 0:

                adjustments.append(
                    Adjustment(
                        id=(
                            "reduce_protein_5"
                        ),

                        label="-5g protein",

                        change={
                            "min_protein_g": -5
                        },

                        matching_option_count=count
                    )
                )

        # ----------------------------------------------------
        # Increase carb limit
        # ----------------------------------------------------

        if request.max_carbs_g is not None:

            increase = 10

            modified_request = (
                request.model_copy(
                    update={
                        "max_carbs_g": (
                            request.max_carbs_g
                            + increase
                        )
                    }
                )
            )

            count = sum(
                self._matches(
                    modified_request,
                    food
                )
                for food in foods
            )

            if count > 0:

                adjustments.append(
                    Adjustment(
                        id=(
                            "increase_carbs_10"
                        ),

                        label="+10g carbs",

                        change={
                            "max_carbs_g": 10
                        },

                        matching_option_count=count
                    )
                )

        # ----------------------------------------------------
        # Increase fat limit
        # ----------------------------------------------------

        if request.max_fat_g is not None:

            increase = 5

            modified_request = (
                request.model_copy(
                    update={
                        "max_fat_g": (
                            request.max_fat_g
                            + increase
                        )
                    }
                )
            )

            count = sum(
                self._matches(
                    modified_request,
                    food
                )
                for food in foods
            )

            if count > 0:

                adjustments.append(
                    Adjustment(
                        id=(
                            "increase_fat_5"
                        ),

                        label="+5g fat",

                        change={
                            "max_fat_g": 5
                        },

                        matching_option_count=count
                    )
                )

        return adjustments

    # ========================================================
    # HELPERS
    # ========================================================

    @staticmethod
    def _number(
        value: Any
    ) -> float:

        if value is None:
            return 0.0

        try:
            return float(value)

        except (
            TypeError,
            ValueError
        ):
            return 0.0

    @staticmethod
    def _parse_allergens(
        value: Any
    ) -> list[str]:

        if not value:
            return []

        if isinstance(
            value,
            list
        ):
            return [
                str(item)
                for item in value
            ]

        return [
            item.strip()
            for item in str(value).split(",")
            if item.strip()
        ]