
const startBtn = document.getElementById("startBtn");
const questSection = document.getElementById("quest-section");
const activityButtons = document.querySelectorAll(".activity-card");
const selectedActivity = document.getElementById("selectedActivity");
const generateBtn = document.getElementById("generateBtn");
const durationSelect = document.getElementById("duration");
const moodSelect = document.getElementById("mood");
const result = document.getElementById("result");

let activity = "";

startBtn.addEventListener("click", () => {
  questSection.scrollIntoView({ behavior: "smooth" });
});

activityButtons.forEach((button) => {
  button.addEventListener("click", () => {
    activityButtons.forEach((item) => {
      item.classList.remove("selected");
      item.setAttribute("aria-pressed", "false");
    });

    button.classList.add("selected");
    button.setAttribute("aria-pressed", "true");
    activity = button.dataset.activity;

    selectedActivity.textContent =
      `Lovely choice! Your adventure vibe: ${activity} 🌿`;
  });
});

function addTextElement(parent, tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  element.textContent = text;
  parent.appendChild(element);
  return element;
}

function renderQuest(quest) {
  result.replaceChildren();
  result.hidden = false;

  const topLine = document.createElement("div");
  topLine.className = "result-topline";

  addTextElement(topLine, "span", "result-label", "✦ YOUR OUTDOOR QUEST");
  addTextElement(topLine, "span", "result-duration", `◷ ${quest.duration}`);
  result.appendChild(topLine);

  addTextElement(result, "h3", "", quest.title);
  addTextElement(result, "p", "result-intro", quest.intro);
  addTextElement(result, "h4", "result-subheading", "Your little adventure");

  const stepsList = document.createElement("ol");
  stepsList.className = "quest-steps";

  quest.activities.forEach((step) => {
    const item = document.createElement("li");
    const content = document.createElement("div");

    addTextElement(
  content,
  "span",
  "step-title",
  step.title.replace(/^\s*(?:step\s*)?\d+[.)\-:]*\s*/i, "")
);
    addTextElement(content, "span", "step-detail", step.detail);

    item.appendChild(content);
    stepsList.appendChild(item);
  });

  result.appendChild(stepsList);

  const tipsPanel = document.createElement("div");
  tipsPanel.className = "tips-panel";

  addTextElement(tipsPanel, "h4", "", "🌿 Little tips for a better day");

  const tipsList = document.createElement("ul");
  tipsList.className = "tips-list";

  quest.tips.forEach((tip) => {
    addTextElement(tipsList, "li", "", tip);
  });

  tipsPanel.appendChild(tipsList);
  result.appendChild(tipsPanel);

  addTextElement(
    result,
    "p",
    "safety-note",
    `💚 ${quest.safety_note}`
  );

  const actions = document.createElement("div");
  actions.className = "result-actions";

  const copyButton = document.createElement("button");
  copyButton.className = "secondary-btn";
  copyButton.type = "button";
  copyButton.textContent = "Copy my quest ↗";

  copyButton.addEventListener("click", async () => {
    const text = [
      quest.title,
      `Duration: ${quest.duration}`,
      "",
      ...quest.activities.map(
        (step, i) => `${i + 1}. ${step.title} — ${step.detail}`
      ),
      "",
      "Tips:",
      ...quest.tips.map((tip) => `- ${tip}`),
      "",
      quest.safety_note
    ].join("\n");

    try {
      await navigator.clipboard.writeText(text);
      copyButton.textContent = "Copied! ✓";
    } catch {
      copyButton.textContent = "Clipboard unavailable";
    }
  });

  actions.appendChild(copyButton);
  result.appendChild(actions);

  result.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

generateBtn.addEventListener("click", async () => {
  if (!activity) {
    selectedActivity.textContent =
      "Choose one of the four activity cards first 🌱";
    activityButtons[0].focus();
    return;
  }

  generateBtn.disabled = true;
  generateBtn.textContent = "Planning your adventure... 🌿";

  result.hidden = false;
  result.setAttribute("aria-busy", "true");
  result.replaceChildren();

  addTextElement(
    result,
    "p",
    "result-intro",
    "Finding a little adventure to match your mood..."
  );

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/generate-quest",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          activity,
          duration: durationSelect.value,
          mood: moodSelect.value
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      const message = Array.isArray(data.detail)
        ? data.detail.map((item) => item.msg).join(", ")
        : data.detail || data.error || `Server returned ${response.status}`;

      throw new Error(message);
    }

    renderQuest(data);
  } catch (error) {
    console.error("Quest generation error:", error);

    result.replaceChildren();
    addTextElement(result, "h3", "", "Your adventure is on pause 🌱");
    addTextElement(
      result,
      "p",
      "result-intro",
      "We couldn't connect to OuttaDoor. Check that the FastAPI server is running at http://127.0.0.1:8000, then try again."
    );
  } finally {
    generateBtn.disabled = false;
    generateBtn.innerHTML = 'Create my outdoor quest <span aria-hidden="true">✦</span>';
    result.setAttribute("aria-busy", "false");
  }
});