\# Changelog



\## v0.3-recommendation-engine

\*\*Status:\*\* Working checkpoint



\### Completed

\- Connected backend to the live Virginia Tech Dining API.

\- Retrieved real menu data from VT Dining.

\- Retrieved nutrition data for menu items.

\- Added deterministic nutrition filtering:

&#x20; - Maximum calories

&#x20; - Minimum protein

&#x20; - Maximum carbohydrates

&#x20; - Maximum fat

&#x20; - Maximum sugar

\- Added meal-period filtering.

\- Added dietary-restriction filtering.

\- Added structured allergen exclusion.

\- Added dining-location selection.

\- Added "Not sure / No preference" location option.

\- Added deterministic recommendation ranking.

\- Added nutrition-priority ranking.

\- Added convenience-priority ranking.

\- Added match explanations.

\- Added no-exact-match responses.

\- Added constraint-relaxation suggestions.

\- Added FastAPI `/recommend` endpoint.

\- Added FastAPI `/dining-locations` endpoint.

\- Added `/docs` OpenAPI documentation.

\- Added Pydantic request/response validation.

\- Added CORS configuration for the frontend.

\- Added `.gitignore`.

\- Created Git repository and pushed checkpoint to the team GitHub repository.



\### Verified

\- Real VT Dining menu retrieval works.

\- Nutrition filtering works.

\- Allergen exclusion works.

\- Dietary filtering works.

\- Meal-period filtering works.

\- Dining-location filtering works.

\- No-match handling works.

\- Constraint-relaxation suggestions work.



\### Known limitations

\- The current connector has only been mapped to the VT Dining location data currently needed for the prototype.

\- Databricks integration has not yet been added.

\- Frontend integration has not yet been added.

\- HokieFuel natural-language preference parsing has not yet been added.

\- Database persistence has not yet been added.



\## v0.4

\*\*Status:\*\* Planned



\### Planned

\- Clean backend/frontend integration contract.

\- Databricks ingestion and normalized data handoff.

\- Expanded VT Dining location coverage.

\- API documentation and example requests.

\- Additional automated tests.

\- Stable interfaces for the recommendation frontend.

