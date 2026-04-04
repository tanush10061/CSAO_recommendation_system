const itemsDb = {
  Biryani: { category: "Main", price: 280, type: "Non-Veg", cuisine: "Indian" },
  "Paneer Tikka": { category: "Main", price: 220, type: "Veg", cuisine: "Indian" },
  "Butter Chicken": { category: "Main", price: 320, type: "Non-Veg", cuisine: "Indian" },
  "Dal Makhani": { category: "Main", price: 180, type: "Veg", cuisine: "Indian" },
  "Chicken Fried Rice": { category: "Main", price: 210, type: "Non-Veg", cuisine: "Chinese" },
  "Hakka Noodles": { category: "Main", price: 190, type: "Veg", cuisine: "Chinese" },
  Raita: { category: "Side", price: 60, type: "Veg", cuisine: "Indian" },
  Salan: { category: "Side", price: 70, type: "Veg", cuisine: "Indian" },
  Naan: { category: "Bread", price: 40, type: "Veg", cuisine: "Indian" },
  Roti: { category: "Bread", price: 30, type: "Veg", cuisine: "Indian" },
  Papad: { category: "Side", price: 25, type: "Veg", cuisine: "Indian" },
  "Gulab Jamun": { category: "Dessert", price: 80, type: "Veg", cuisine: "Indian" },
  Rasgulla: { category: "Dessert", price: 70, type: "Veg", cuisine: "Indian" },
  "Ice Cream": { category: "Dessert", price: 90, type: "Veg", cuisine: "Continental" },
  Brownie: { category: "Dessert", price: 100, type: "Veg", cuisine: "Continental" },
  Coke: { category: "Drink", price: 50, type: "Veg", cuisine: "Beverage" },
  Lassi: { category: "Drink", price: 70, type: "Veg", cuisine: "Indian" },
  "Mineral Water": { category: "Drink", price: 20, type: "Veg", cuisine: "Beverage" },
  "Fresh Lime": { category: "Drink", price: 60, type: "Veg", cuisine: "Beverage" },
  Samosa: { category: "Starter", price: 40, type: "Veg", cuisine: "Indian" },
  "Chicken Wings": { category: "Starter", price: 180, type: "Non-Veg", cuisine: "Continental" },
  "Spring Rolls": { category: "Starter", price: 120, type: "Veg", cuisine: "Chinese" },
  Salad: { category: "Starter", price: 90, type: "Veg", cuisine: "Continental" },
};

const mealRules = {
  Biryani: ["Raita", "Salan", "Gulab Jamun"],
  "Butter Chicken": ["Naan", "Roti", "Raita"],
  "Dal Makhani": ["Roti", "Naan", "Papad"],
  "Paneer Tikka": ["Naan", "Raita", "Coke"],
  "Chicken Fried Rice": ["Spring Rolls", "Coke", "Ice Cream"],
  "Hakka Noodles": ["Spring Rolls", "Coke"],
};

const cityPreferences = {
  Mumbai: ["Butter Chicken", "Paneer Tikka", "Ice Cream"],
  Delhi: ["Butter Chicken", "Naan", "Lassi"],
  Bangalore: ["Biryani", "Coke", "Brownie"],
  Kolkata: ["Biryani", "Rasgulla", "Lassi"],
  Hyderabad: ["Biryani", "Raita", "Gulab Jamun"],
};

const featureImportance = [
  { feature: "meal_completion_score", importance: 0.3278 },
  { feature: "completes_meal", importance: 0.2893 },
  { feature: "item_price", importance: 0.05 },
  { feature: "item_price_ratio", importance: 0.0383 },
  { feature: "cart_value", importance: 0.0287 },
  { feature: "item_category_main", importance: 0.0246 },
  { feature: "price_sensitivity", importance: 0.0223 },
  { feature: "avg_item_price", importance: 0.021 },
  { feature: "user_avg_order_value", importance: 0.0197 },
  { feature: "rest_avg_cart_value", importance: 0.0165 },
];

const state = {
  selectedItems: new Set(["Biryani"]),
};

const citySelect = document.getElementById("city");
const hourInput = document.getElementById("hour");
const hourValue = document.getElementById("hourValue");
const mealTimeBadge = document.getElementById("mealTimeBadge");
const userSegmentSelect = document.getElementById("userSegment");
const userFrequencySelect = document.getElementById("userFrequency");
const itemCatalog = document.getElementById("itemCatalog");
const selectedItemsWrap = document.getElementById("selectedItems");
const cartEmpty = document.getElementById("cartEmpty");
const cartContent = document.getElementById("cartContent");
const cartSize = document.getElementById("cartSize");
const cartValue = document.getElementById("cartValue");
const avgPrice = document.getElementById("avgPrice");
const aovLift = document.getElementById("aovLift");
const recommendationsEmpty = document.getElementById("recommendationsEmpty");
const recommendationsContent = document.getElementById("recommendationsContent");
const recommendationRows = document.getElementById("recommendationRows");
const recommendationCards = document.getElementById("recommendationCards");
const featureImportanceWrap = document.getElementById("featureImportance");
const resetBtn = document.getElementById("resetBtn");
const detectContextBtn = document.getElementById("detectContextBtn");
const contextStatus = document.getElementById("contextStatus");
const locationDetails = document.getElementById("locationDetails");
const locationCoords = document.getElementById("locationCoords");
const locationAccuracy = document.getElementById("locationAccuracy");
const resolvedPlace = document.getElementById("resolvedPlace");

const supportedCities = {
  Mumbai: { lat: 19.076, lon: 72.8777 },
  Delhi: { lat: 28.6139, lon: 77.209 },
  Bangalore: { lat: 12.9716, lon: 77.5946 },
  Kolkata: { lat: 22.5726, lon: 88.3639 },
  Hyderabad: { lat: 17.385, lon: 78.4867 },
};

function inferMealTime(hour) {
  if (hour < 11) return "breakfast";
  if (hour < 15) return "lunch";
  if (hour < 20) return "dinner";
  return "late_night";
}

function titleCase(text) {
  return text.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function getDistance(lat1, lon1, lat2, lon2) {
  const toRad = (value) => (value * Math.PI) / 180;
  const earthRadiusKm = 6371;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  return 2 * earthRadiusKm * Math.asin(Math.sqrt(a));
}

function getNearestSupportedCity(latitude, longitude) {
  return Object.entries(supportedCities)
    .map(([city, coords]) => ({
      city,
      distance: getDistance(latitude, longitude, coords.lat, coords.lon),
    }))
    .sort((left, right) => left.distance - right.distance)[0];
}

function getProfile(selectedItems) {
  const items = Array.from(selectedItems);
  const cartValueTotal = items.reduce((total, item) => total + itemsDb[item].price, 0);
  const categories = items.map((item) => itemsDb[item].category);
  const cuisines = items.map((item) => itemsDb[item].cuisine);

  return {
    items,
    cartValue: cartValueTotal,
    cartSize: items.length,
    avgPrice: items.length ? cartValueTotal / items.length : 0,
    hasMain: categories.some((category) => category === "Main"),
    hasSide: categories.some((category) => category === "Side" || category === "Bread"),
    hasDrink: categories.some((category) => category === "Drink"),
    hasDessert: categories.some((category) => category === "Dessert"),
    cuisines,
  };
}

function buildReasonTags(candidate, profile, city, mealTime, userSegment) {
  const item = itemsDb[candidate];
  const tags = [];

  if (profile.items.some((cartItem) => (mealRules[cartItem] || []).includes(candidate))) {
    tags.push("Completes the current meal");
  }
  if (profile.cuisines.includes(item.cuisine)) {
    tags.push("Matches your current cart cuisine");
  }
  if ((cityPreferences[city] || []).includes(candidate)) {
    tags.push(`Popular choice in ${city}`);
  }
  if (mealTime === "late_night" && (item.category === "Dessert" || item.category === "Drink")) {
    tags.push("Fits late-night ordering behavior");
  }
  if (userSegment === "budget" && item.price <= 80) {
    tags.push("Budget-friendly add-on");
  } else if (userSegment === "premium" && item.price >= 90) {
    tags.push("Works well for premium baskets");
  }
  if (!tags.length) {
    tags.push("Balanced complementary recommendation");
  }

  return tags.slice(0, 3);
}

function scoreCandidate(candidate, profile, city, mealTime, userSegment, userFrequency) {
  const item = itemsDb[candidate];
  let score = 0.2;

  const mealCompletionScore = profile.items.reduce((total, cartItem) => {
    return total + ((mealRules[cartItem] || []).includes(candidate) ? 1 : 0);
  }, 0);

  score += mealCompletionScore * 0.28;

  if (profile.cuisines.includes(item.cuisine)) score += 0.12;
  if ((cityPreferences[city] || []).includes(candidate)) score += 0.08;
  if (!profile.hasDrink && item.category === "Drink") score += 0.14;
  if (!profile.hasDessert && item.category === "Dessert") score += 0.14;
  if (!profile.hasSide && (item.category === "Side" || item.category === "Bread")) score += 0.15;
  if (mealTime === "lunch" && (item.category === "Drink" || item.category === "Side")) score += 0.06;
  if (mealTime === "dinner" && ["Dessert", "Bread", "Side"].includes(item.category)) score += 0.06;
  if (mealTime === "late_night" && ["Dessert", "Drink"].includes(item.category)) score += 0.09;

  if (userSegment === "budget") {
    if (item.price <= 80) score += 0.08;
    else if (item.price >= 200) score -= 0.04;
  } else if (userSegment === "premium" && item.price >= 90) {
    score += 0.06;
  }

  if (userFrequency === "new" && mealCompletionScore > 0) score += 0.05;
  if (userFrequency === "power" && ["Starter", "Dessert"].includes(item.category)) score += 0.04;

  const ratio = item.price / Math.max(profile.cartValue, 1);
  if (ratio >= 0.08 && ratio <= 0.35) score += 0.08;
  else if (ratio > 0.7) score -= 0.06;

  return Math.max(0, Math.min(score, 0.99));
}

function getRecommendations(profile, city, hour, userSegment, userFrequency) {
  const mealTime = inferMealTime(hour);
  return Object.keys(itemsDb)
    .filter((item) => !state.selectedItems.has(item))
    .map((item) => ({
      item,
      ...itemsDb[item],
      score: scoreCandidate(item, profile, city, mealTime, userSegment, userFrequency),
      reasons: buildReasonTags(item, profile, city, mealTime, userSegment),
    }))
    .sort((left, right) => right.score - left.score)
    .slice(0, 8);
}

function renderCityOptions() {
  Object.keys(cityPreferences).forEach((city) => {
    const option = document.createElement("option");
    option.value = city;
    option.textContent = city;
    citySelect.append(option);
  });
  citySelect.value = "Mumbai";
}

function renderItemCatalog() {
  itemCatalog.innerHTML = "";
  Object.entries(itemsDb).forEach(([name, details]) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "item-card";
    if (state.selectedItems.has(name)) {
      card.classList.add("selected");
    }
    card.innerHTML = `
      <div class="item-card-top">
        <div>
          <strong>${name}</strong>
          <div class="card-meta">${details.category} | ${details.type}</div>
        </div>
        <strong>INR ${details.price}</strong>
      </div>
      <div class="chip-row">
        <span class="mini-chip">${details.cuisine}</span>
        <span class="mini-chip">${state.selectedItems.has(name) ? "In cart" : "Add item"}</span>
      </div>
    `;
    card.addEventListener("click", () => {
      if (state.selectedItems.has(name)) state.selectedItems.delete(name);
      else state.selectedItems.add(name);
      updateUI();
    });
    itemCatalog.append(card);
  });
}

function renderSelectedItems(profile) {
  selectedItemsWrap.innerHTML = "";
  profile.items.forEach((item) => {
    const chip = document.createElement("div");
    chip.className = "selected-chip";
    chip.innerHTML = `${item} <button type="button" aria-label="Remove ${item}">x</button>`;
    chip.querySelector("button").addEventListener("click", () => {
      state.selectedItems.delete(item);
      updateUI();
    });
    selectedItemsWrap.append(chip);
  });
}

function renderRecommendations(recommendations) {
  recommendationRows.innerHTML = "";
  recommendationCards.innerHTML = "";

  recommendations.forEach((row, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${row.item}</td>
      <td>${row.category}</td>
      <td>${row.type}</td>
      <td>INR ${row.price}</td>
      <td><span class="score-pill">${row.score.toFixed(2)}</span></td>
    `;
    recommendationRows.append(tr);

    const card = document.createElement("article");
    card.className = "recommendation-card";
    card.innerHTML = `
      <h3>${row.item}</h3>
      <div class="card-meta">${row.category} | ${row.type} | INR ${row.price}</div>
      <div class="card-tags">
        ${row.reasons.map((reason) => `<span class="reason-tag">${reason}</span>`).join("")}
      </div>
    `;
    recommendationCards.append(card);
  });
}

function renderFeatureImportance() {
  featureImportanceWrap.innerHTML = "";
  const maxValue = featureImportance[0].importance;

  featureImportance.forEach((row) => {
    const wrapper = document.createElement("div");
    wrapper.className = "feature-row";
    wrapper.innerHTML = `
      <strong>${row.feature}</strong>
      <div class="feature-bar">
        <div class="feature-bar-fill" style="width: ${(row.importance / maxValue) * 100}%"></div>
      </div>
      <span>${row.importance.toFixed(3)}</span>
    `;
    featureImportanceWrap.append(wrapper);
  });
}

function updateTimeUI() {
  const hour = Number(hourInput.value);
  const mealTime = inferMealTime(hour);
  hourValue.textContent = `${hour}:00`;
  mealTimeBadge.textContent = titleCase(mealTime);
}

function applyDeviceTime() {
  const now = new Date();
  const localHour = now.getHours();
  hourInput.value = String(localHour);
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  return { localHour, timezone };
}

async function reverseGeocode(latitude, longitude) {
  const url = new URL("https://nominatim.openstreetmap.org/reverse");
  url.searchParams.set("format", "jsonv2");
  url.searchParams.set("lat", String(latitude));
  url.searchParams.set("lon", String(longitude));
  url.searchParams.set("zoom", "18");
  url.searchParams.set("addressdetails", "1");

  const response = await fetch(url.toString(), {
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Reverse geocoding failed with status ${response.status}`);
  }

  return response.json();
}

function updateLocationCard({ latitude, longitude, accuracy, placeLabel }) {
  locationDetails.classList.remove("hidden");
  locationCoords.textContent = `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
  locationAccuracy.textContent = `${Math.round(accuracy)} meters`;
  resolvedPlace.textContent = placeLabel || "Not resolved";
}

function detectDeviceContext() {
  const timeInfo = applyDeviceTime();
  contextStatus.textContent = `Using device time from ${timeInfo.timezone}. Detecting current device location...`;
  updateUI();

  if (!navigator.geolocation) {
    contextStatus.textContent = `Using device time from ${timeInfo.timezone}. Browser location is not supported here.`;
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;
      const nearest = getNearestSupportedCity(latitude, longitude);
      let placeLabel = `Nearest supported city: ${nearest.city}`;

      try {
        const geocodeData = await reverseGeocode(latitude, longitude);
        const address = geocodeData.address || {};
        const actualCity =
          address.city ||
          address.town ||
          address.village ||
          address.municipality ||
          address.county ||
          geocodeData.name;
        const state = address.state;
        const country = address.country;
        placeLabel = [actualCity, state, country].filter(Boolean).join(", ") || geocodeData.display_name || placeLabel;

        if (actualCity) {
          const matchingCity = Object.keys(supportedCities).find(
            (city) => city.toLowerCase() === actualCity.toLowerCase()
          );
          citySelect.value = matchingCity || nearest.city;
        } else {
          citySelect.value = nearest.city;
        }
      } catch (error) {
        citySelect.value = nearest.city;
        placeLabel = `${placeLabel} (address lookup unavailable)`;
      }

      updateLocationCard({
        latitude,
        longitude,
        accuracy: position.coords.accuracy,
        placeLabel,
      });

      contextStatus.textContent = `Using device time from ${timeInfo.timezone}. Current coordinates captured from the browser. Recommendations are mapped to ${citySelect.value} because your app supports a fixed city set.`;
      updateUI();
    },
    (error) => {
      const fallbackMessage =
        error.code === error.PERMISSION_DENIED
          ? "Location permission was denied."
          : "Location could not be determined.";
      contextStatus.textContent = `Using device time from ${timeInfo.timezone}. ${fallbackMessage} Keeping your selected city.`;
      updateUI();
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  );
}

function updateUI() {
  updateTimeUI();
  renderItemCatalog();

  const profile = getProfile(state.selectedItems);
  const hasItems = profile.items.length > 0;

  cartEmpty.classList.toggle("hidden", hasItems);
  cartContent.classList.toggle("hidden", !hasItems);
  recommendationsEmpty.classList.toggle("hidden", hasItems);
  recommendationsContent.classList.toggle("hidden", !hasItems);

  if (!hasItems) return;

  renderSelectedItems(profile);
  cartSize.textContent = profile.cartSize;
  cartValue.textContent = `INR ${profile.cartValue}`;
  avgPrice.textContent = `INR ${Math.round(profile.avgPrice)}`;

  const recommendations = getRecommendations(
    profile,
    citySelect.value,
    Number(hourInput.value),
    userSegmentSelect.value,
    userFrequencySelect.value
  );

  const projectedAddonValue =
    recommendations.slice(0, 3).reduce((total, row) => total + row.price, 0) /
    Math.max(recommendations.slice(0, 3).length, 1);
  const lift = (projectedAddonValue / Math.max(profile.cartValue, 1)) * 100;
  aovLift.textContent = `${lift.toFixed(1)}%`;

  renderRecommendations(recommendations);
}

renderCityOptions();
renderFeatureImportance();
updateUI();

hourInput.addEventListener("input", updateUI);
citySelect.addEventListener("change", updateUI);
userSegmentSelect.addEventListener("change", updateUI);
userFrequencySelect.addEventListener("change", updateUI);
resetBtn.addEventListener("click", () => {
  state.selectedItems = new Set();
  updateUI();
});
detectContextBtn.addEventListener("click", detectDeviceContext);
