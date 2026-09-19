import requests


class VTDiningConnector:
    """
    Connector for the official Virginia Tech Dining menu API.

    The frontend uses human-readable dining groups.
    This connector handles the underlying VT Dining
    location IDs internally.
    """

    BASE_URL = (
        "https://foodpro.students.vt.edu/menus/API"
    )

    # ========================================================
    # USER-FACING LOCATION GROUPS
    # ========================================================
    #
    # Each frontend option can correspond to one or more
    # actual VT Dining locations.
    #
    # These are internal implementation details.
    # The frontend does NOT need to know the API numbers.
    #
    LOCATION_GROUPS = {
        "Dietrick Hall": [
            "D2",
            "Deet's Place",
            "DX",
            "Future Bites at Xpress Lane",
        ],

        "Ducky's at GLC": [
            "Ducky's at GLC",
        ],

        "Owens Hall": [
            "Hokie Grill at Owens",
            "Owens Food Court",
        ],

        "Perry Place / Hitt Hall": [
            "Perry Place at HITT Hall",
        ],

        "Turner Place": [
            "Turner Place at Lavery Hall",
        ],

        "Squires Food Court": [
            "Squires Food Court",
        ],

        "Viva Market": [
            "Viva Market - Johnston Student Center & Viva Too - Goodwin Hall",
        ],

        "West End / Cochrane Hall": [
            "West End at Cochrane Hall",
        ],
    }

    NO_PREFERENCE = "Not sure / No preference"

    # ========================================================
    # INTERNAL VT API LOCATION IDs
    # ========================================================
    #
    # These are NOT exposed to the frontend.
    #
    # We will continue expanding this mapping as we verify
    # the corresponding VT API locations.
    #
    # 15 is confirmed as D2 from our direct API testing.
    #
    LOCATION_IDS = {
        "D2": "15",
    }

    # ========================================================
    # HTTP HELPER
    # ========================================================

    def _get(
        self,
        endpoint,
        params
    ):
        response = requests.get(
            f"{self.BASE_URL}/{endpoint}",
            params=params,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    # ========================================================
    # MENU API
    # ========================================================

    def get_menu(
        self,
        location_id,
        date
    ):
        return self._get(
            "MenuAtLocation.aspx",
            {
                "locationNum": location_id,
                "dtdate": date
            }
        )

    # ========================================================
    # NUTRITION API
    # ========================================================

    def get_nutrition(
        self,
        location_id,
        date,
        recipe_id,
        portion="1"
    ):
        return self._get(
            "Label.aspx",
            {
                "locationNum": location_id,
                "dtdate": date,
                "recNumAndPort": (
                    f"{recipe_id}*{portion}"
                )
            }
        )

    # ========================================================
    # SINGLE LOCATION
    # ========================================================

    def get_all_foods(
        self,
        location_id,
        date,
        location_name=None
    ):
        """
        Retrieve all menu items and nutrition information
        for one actual VT Dining API location.
        """

        menu = self.get_menu(
            location_id,
            date
        )

        foods = []

        if location_name is None:
            location_name = (
                f"VT Dining Location {location_id}"
            )

        for meal in menu.get(
            "meals",
            []
        ):

            meal_name = meal.get(
                "mealName",
                ""
            )

            for section in meal.get(
                "sections",
                []
            ):

                section_name = section.get(
                    "sectionName",
                    ""
                )

                for recipe in section.get(
                    "recipes",
                    []
                ):

                    recipe_id = recipe.get(
                        "recipeId"
                    )

                    if not recipe_id:
                        continue

                    nutrition = self.get_nutrition(
                        location_id,
                        date,
                        recipe_id,
                        recipe.get(
                            "portionSize",
                            "1"
                        )
                    )

                    foods.append({
                        "recipe_id": recipe_id,

                        "name": recipe.get(
                            "name",
                            ""
                        ),

                        "location_name": (
                            location_name
                        ),

                        "meal": meal_name,

                        "section": section_name,

                        "menu_date": (
                            self._convert_date(
                                date
                            )
                        ),

                        "description": recipe.get(
                            "description",
                            ""
                        ),

                        "portion_size": recipe.get(
                            "portionSize",
                            ""
                        ),

                        "portion_unit": recipe.get(
                            "portionUnit",
                            ""
                        ),

                        "allergens": recipe.get(
                            "allergens",
                            ""
                        ),

                        "dietary_tags": recipe.get(
                            "legendImages",
                            []
                        ),

                        "calories": nutrition.get(
                            "calories"
                        ),

                        "protein": nutrition.get(
                            "proteinGrams"
                        ),

                        "carbs": nutrition.get(
                            "totalCarbohydratesGrams"
                        ),

                        "fat": nutrition.get(
                            "totalFatGrams"
                        ),

                        "sugar": nutrition.get(
                            "sugarsGrams"
                        ),

                        "fiber": nutrition.get(
                            "dietaryFiberGrams"
                        ),

                        "sodium": nutrition.get(
                            "sodiumMilligrams"
                        )
                    })

        return foods

    # ========================================================
    # LOCATION GROUP
    # ========================================================

    def get_foods_for_group(
        self,
        dining_location,
        date
    ):
        """
        Retrieve foods for one frontend dining-location
        selection.

        If the user chooses "Not sure / No preference",
        foods from every verified location are returned.
        """

        # ----------------------------------------------------
        # Determine actual location names
        # ----------------------------------------------------

        if (
            dining_location
            == self.NO_PREFERENCE
        ):
            location_names = []

            for names in self.LOCATION_GROUPS.values():
                location_names.extend(names)

        else:
            location_names = (
                self.LOCATION_GROUPS.get(
                    dining_location,
                    []
                )
            )

        foods = []

        # ----------------------------------------------------
        # Fetch each verified API location
        # ----------------------------------------------------

        for location_name in location_names:

            location_id = self.LOCATION_IDS.get(
                location_name
            )

            # Skip locations whose API ID has not yet
            # been verified.
            #
            # This prevents the backend from guessing
            # API location numbers.
            if location_id is None:
                continue

            try:

                location_foods = (
                    self.get_all_foods(
                        location_id,
                        date,
                        location_name
                    )
                )

                foods.extend(
                    location_foods
                )

            except requests.RequestException:
                # One unavailable location should not
                # crash the entire recommendation request.
                continue

        return foods

    # ========================================================
    # LOCATION LIST FOR FRONTEND
    # ========================================================

    def get_dining_locations(self):
        """
        Return the human-readable dropdown options.
        """

        return [
            "Dietrick Hall",
            "Ducky's at GLC",
            "Owens Hall",
            "Perry Place / Hitt Hall",
            "Turner Place",
            "Squires Food Court",
            "Viva Market",
            "West End / Cochrane Hall",
            self.NO_PREFERENCE,
        ]

    # ========================================================
    # DATE HELPER
    # ========================================================

    @staticmethod
    def _convert_date(
        date_string
    ):
        """
        Convert M/D/YYYY into YYYY-MM-DD.
        """

        month, day, year = (
            date_string.split("/")
        )

        return (
            f"{year}-"
            f"{int(month):02d}-"
            f"{int(day):02d}"
        )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    connector = VTDiningConnector()

    foods = connector.get_foods_for_group(
        "Dietrick Hall",
        "9/19/2026"
    )

    print(
        "Foods retrieved:",
        len(foods)
    )

    for food in foods[:10]:

        print(
            food["name"],
            "| Location:",
            food["location_name"],
            "| Calories:",
            food["calories"],
            "| Protein:",
            food["protein"],
            "| Tags:",
            food["dietary_tags"]
        )