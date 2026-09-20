"use client";

import { useState } from "react";

const mockRecommendations = [
  {
    id: "mock-1",
    foodName: "Grilled Chicken Grain Bowl",
    location: "Turner Place",
    calories: 540,
    protein: 42,
    carbs: 48,
    fat: 18,
    sugar: 8,
    walkingTime: 6,
    dietaryTags: ["High protein"],
    allergens: ["Milk"],
  },
  {
    id: "mock-2",
    foodName: "Tofu & Vegetable Stir-Fry",
    location: "West End Market",
    calories: 490,
    protein: 24,
    carbs: 66,
    fat: 15,
    sugar: 10,
    walkingTime: 8,
    dietaryTags: ["Vegetarian", "Vegan option available"],
    allergens: ["Soy", "Sesame"],
  },
  {
    id: "mock-3",
    foodName: "Turkey Avocado Wrap",
    location: "Owens Food Court",
    calories: 610,
    protein: 38,
    carbs: 59,
    fat: 24,
    sugar: 6,
    walkingTime: 5,
    dietaryTags: ["High protein"],
    allergens: ["Wheat", "Milk"],
  },
];

const mockAdjustments = [
  {
    id: "calories",
    label: "+50 calories",
    description: "4 options",
  },
  {
    id: "walking",
    label: "+2 minutes walking",
    description: "6 options",
  },
  {
    id: "protein",
    label: "-5g protein",
    description: "8 options",
  },
];

export default function ResultsPage() {
  const [showNoMatch, setShowNoMatch] = useState(false);
  const [selectedAdjustment, setSelectedAdjustment] = useState("");

  return (
    <main className="results-page">
      <nav>
        <a className="brand" href="/">
          <span className="brand-mark">VT</span>
          <span>Dining Finder</span>
        </a>

        <a className="sidekick-button" href="/">
          Update preferences
        </a>
      </nav>

      <section className="results-hero">
        <p className="eyebrow">MEAL RECOMMENDATIONS</p>
        <h1>
          {showNoMatch ? "Let’s find your closest match." : "Meals that fit your goals."}
        </h1>
        <p>
          These are temporary prototype recommendations. The app will use
          verified Virginia Tech Dining data once the backend is connected.
        </p>
      </section>

      <section className="results-content">
        <button
          className="demo-toggle"
          onClick={() => {
            setShowNoMatch(!showNoMatch);
            setSelectedAdjustment("");
          }}
        >
          {showNoMatch ? "Show matching options" : "Preview no-match experience"}
        </button>

        {showNoMatch ? (
          <section className="no-match-card">
            <p className="eyebrow">NO EXACT MATCHES</p>
            <h2>Your current filters are very specific.</h2>
            <p>
              Choose one small adjustment, and we’ll search again using your
              updated preferences.
            </p>

            <div className="adjustment-list">
              {mockAdjustments.map((adjustment) => (
                <button
                  className={
                    selectedAdjustment === adjustment.id
                      ? "adjustment-button selected"
                      : "adjustment-button"
                  }
                  key={adjustment.id}
                  onClick={() => setSelectedAdjustment(adjustment.id)}
                >
                  <span>{adjustment.label}</span>
                  <strong>{adjustment.description}</strong>
                </button>
              ))}
            </div>

            {selectedAdjustment && (
              <p className="adjustment-confirmation">
                Adjustment selected. In the finished app, the frontend will
                send the updated preferences to <code>POST /recommend</code>.
              </p>
            )}
          </section>
        ) : (
          <>
            <div className="results-summary">
              <p className="eyebrow">3 OPTIONS FOUND</p>
              <h2>Ranked for nutrition and walking time.</h2>
            </div>

            <div className="recommendation-list">
              {mockRecommendations.map((meal) => (
                <article className="recommendation-card" key={meal.id}>
                  <div className="recommendation-topline">
                    <p>{meal.location}</p>
                    <span>{meal.walkingTime} min walk</span>
                  </div>

                  <h3>{meal.foodName}</h3>

                  <div className="tag-list">
                    {meal.dietaryTags.map((tag) => (
                      <span className="tag" key={tag}>
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className="nutrition-grid">
                    <div>
                      <strong>{meal.calories}</strong>
                      <span>Calories</span>
                    </div>
                    <div>
                      <strong>{meal.protein}g</strong>
                      <span>Protein</span>
                    </div>
                    <div>
                      <strong>{meal.carbs}g</strong>
                      <span>Carbs</span>
                    </div>
                    <div>
                      <strong>{meal.fat}g</strong>
                      <span>Fat</span>
                    </div>
                    <div>
                      <strong>{meal.sugar}g</strong>
                      <span>Sugar</span>
                    </div>
                  </div>

                  <p className="allergen-line">
                    <strong>Allergens:</strong> {meal.allergens.join(", ")}
                  </p>
                </article>
              ))}
            </div>
          </>
        )}
      </section>
    </main>
  );
}