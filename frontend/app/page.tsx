"use client";

import { useState } from "react";

export default function Home() {
  const [showSidekick, setShowSidekick] = useState(false);
const [chatMessage, setChatMessage] = useState("");
const [chatSubmitted, setChatSubmitted] = useState(false);
  return (
    <main>
      <nav>
        <div className="brand">
          <span className="brand-mark">VT</span>
          <span>Dining Finder</span>
        </div>

        <button
          className="sidekick-button"
          onClick={() => setShowSidekick(!showSidekick)}
        >
          Ask HokieFuel
        </button>
      </nav>

      <section className="hero">
        <p className="eyebrow">VIRGINIA TECH DINING</p>
        <h1>Find a meal that fits your day.</h1>
        <p className="hero-text">
          Filter Virginia Tech dining options by nutrition, dietary needs, and
          walking time.
        </p>

        <a className="primary-button" href="#preferences">
          Find My Meal
        </a>
      </section>

      <section className="intro" id="preferences">
        <div>
          <p className="eyebrow">START HERE</p>
          <h2>Tell us what matters today.</h2>
        </div>
        <p>
          Set your nutrition goals, dietary restrictions, preferred locations,
          and walking limit. We’ll use this information to rank dining options.
        </p>
      </section>

            <section className="preference-form">
        <div className="form-heading">
          <p className="eyebrow">MEAL PREFERENCES</p>
          <h2>Build your meal search.</h2>
          <p>
            Add only the details that matter today. You can leave any field
            empty.
          </p>
        </div>

        <form>
          <fieldset>
            <legend>Nutrition goals</legend>

            <div className="form-grid">
              <label>
                Maximum calories
                <input type="number" placeholder="Example: 650" />
              </label>

              <label>
                Minimum protein (g)
                <input type="number" placeholder="Example: 30" />
              </label>

              <label>
                Maximum carbs (g)
                <input type="number" placeholder="Example: 75" />
              </label>

              <label>
                Maximum fat (g)
                <input type="number" placeholder="Example: 25" />
              </label>

              <label>
                Maximum sugar (g)
                <input type="number" placeholder="Example: 20" />
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>Dining needs</legend>

            <div className="form-grid">
              <label>
                Dietary restriction
                <select defaultValue="">
                  <option value="" disabled>
                    Select one
                  </option>
                  <option>None</option>
                  <option>Vegetarian</option>
                  <option>Vegan</option>
                  <option>Halal</option>
                  <option>Gluten-free</option>
                </select>
              </label>

              <label>
                Allergies or ingredients to avoid
                <input type="text" placeholder="Example: peanuts, dairy" />
              </label>

              <label>
                Meal period
                <select defaultValue="">
                  <option value="" disabled>
                    Select one
                  </option>
                  <option>Breakfast</option>
                  <option>Lunch</option>
                  <option>Dinner</option>
                  <option>Late night</option>
                </select>
              </label>

              <label>
  Which dining location are you closest to?
  <select defaultValue="">
    <option value="" disabled>
      Choose a location
    </option>
    <option>Turner Place</option>
    <option>Owens Food Court</option>
    <option>D2</option>
    <option>West End Market</option>
    <option>Hokie Grill</option>
    <option>Not sure</option>
  </select>
</label>

              <label>
                Maximum walking time (minutes)
                <input type="number" placeholder="Example: 8" />
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>What should matter most?</legend>

            <div className="priority-options">
              <label>
                <input type="radio" name="priority" defaultChecked />
                Balanced nutrition and convenience
              </label>
              <label>
                <input type="radio" name="priority" />
                Better nutrition
              </label>
              <label>
                <input type="radio" name="priority" />
                Shorter walking time
              </label>
            </div>
          </fieldset>

          <a className="primary-button" href="/results">
  See meal options
</a>

          <p className="mock-note">
            Prototype mode: recommendations will use temporary mock data until
            your backend is connected.
          </p>
        </form>
      </section>
      {showSidekick && (
        <aside className="sidekick-panel">
          <div className="sidekick-header">
            <div>
              <p className="eyebrow">AI SIDEKICK</p>
              <h2>HokieFuel</h2>
            </div>
            <button
              className="close-button"
              onClick={() => setShowSidekick(false)}
              aria-label="Close HokieFuel"
            >
              ×
            </button>
          </div>

          <p>
            Tell HokieFuel what you need. Soon it will help update your meal
            preferences using real dining data.
          </p>

          <div className="chat-placeholder">
            I care more about protein than walking distance.
          </div>

          <form
  className="chat-form"
  onSubmit={(event) => {
    event.preventDefault();
    if (chatMessage.trim()) {
      setChatSubmitted(true);
    }
  }}
>
  <input
    aria-label="Message HokieFuel"
    placeholder="Ask HokieFuel about your meal..."
    value={chatMessage}
    onChange={(event) => setChatMessage(event.target.value)}
  />
  <button type="submit">Send</button>
</form>

{chatSubmitted && (
  <div className="sidekick-response">
    <strong>Prototype response</strong>
    <p>
      Your message will eventually be sent to HokieFuel, which will return
      structured preferences for the real dining-data search.
    </p>
  </div>
)}
        </aside>
      )}
    </main>
  );
}