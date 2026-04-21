const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const messages = document.getElementById("messages");
const statusText = document.getElementById("statusText");
const resetBtn = document.getElementById("resetBtn");
const minBtn = document.getElementById("minBtn");
const chatWidget = document.getElementById("chatWidget");
const chatLauncher = document.getElementById("chatLauncher");
const quickChips = document.querySelectorAll(".quick-chip");

let lastTicketSummary = "";

function timeLabel() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

function scrollToBottom() {
  const chatBody = document.getElementById("chatBody");
  chatBody.scrollTop = chatBody.scrollHeight;
}

function createMessageRow(type = "assistant") {
  const row = document.createElement("div");
  row.className = `message-row ${type === "user" ? "user-row" : "assistant-row"}`;

  const time = document.createElement("div");
  time.className = "message-time";
  time.textContent = timeLabel();

  return { row, time };
}

function toggleChips() {
  const chipSection = document.querySelector(".chip-section");
  if (!chipSection) return;

  chipSection.classList.toggle("collapsed");
}

function normalizeAssistantText(text) {
  if (!text) return "No answer returned.";

  const rawLines = text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line !== "");

  const lines = [];
  let reachedActionableContent = false;

  for (const line of rawLines) {
    const lower = line.toLowerCase();

    if (lower === "title:" || lower.startsWith("title:")) continue;
    if (lower === "problem:" || lower.startsWith("problem:")) continue;
    if (lower === "applies to:" || lower.startsWith("applies to:")) continue;

    if (
      lower === "answer:" ||
      lower === "steps:" ||
      lower === "troubleshooting:" ||
      lower === "escalation:" ||
      /^\d+\.\s/.test(line) ||
      lower.startsWith("- ")
    ) {
      reachedActionableContent = true;
    }

    lines.push(line);
  }

  const output = [];
  let currentSection = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lower = line.toLowerCase();

    if (lower === "answer:") {
      currentSection = "answer";
      continue;
    }

    if (lower === "steps:") {
      currentSection = "steps";
      if (output.length) output.push("");
      output.push("**Try these steps:**");
      continue;
  }

    if (lower === "troubleshooting:") {
      currentSection = "troubleshooting";
      if (output.length) output.push("");
      output.push("**Troubleshooting:**");
      continue;
    }

    if (lower === "escalation:") {
      currentSection = "escalation";
      if (output.length) output.push("");
      output.push("**If this still doesn’t work:**");
      continue;
    }

    if (!currentSection) {
      const nextHasStructuredSection = lines.some((l, idx) => {
        if (idx <= i) return false;
        const ll = l.toLowerCase();
        return (
          ll === "steps:" ||
          ll === "troubleshooting:" ||
          ll === "escalation:" ||
          ll === "answer:"
        );
      });

      if (nextHasStructuredSection) {
        continue;
      }
    }

    if (currentSection === "answer") {
      output.push(line);
      continue;
    }

    if (currentSection === "steps") {
      output.push(line.replace(/^\d+\.\s*/, (match) => match));
      continue;
    }

    if (currentSection === "troubleshooting") {
      output.push(line.replace(/^-+\s*/, "- "));
      continue;
    }

    if (currentSection === "escalation") {
      output.push(line);
      continue;
    }

    output.push(line);
  }

  return output.join("\n");
}

function addTextMessage(text, type = "assistant") {
  const { row, time } = createMessageRow(type);

  const bubble = document.createElement("div");
  if (type === "user") {
    bubble.className = "bubble user-bubble";
    bubble.textContent = text;
  } else if (type === "refusal") {
    bubble.className = "bubble refusal-bubble";
    bubble.textContent = text;
  } else {
    bubble.className = "bubble assistant-bubble";
    bubble.innerHTML = normalizeAssistantText(text)
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");
  }

  row.appendChild(bubble);
  row.appendChild(time);
  messages.appendChild(row);
  scrollToBottom();
}

function addPanelMessage(html) {
  const row = document.createElement("div");
  row.className = "panel-row";

  const panel = document.createElement("div");
  panel.className = "panel-card";
  panel.innerHTML = html;

  const time = document.createElement("div");
  time.className = "message-time";
  time.textContent = timeLabel();

  row.appendChild(panel);
  row.appendChild(time);
  messages.appendChild(row);
  scrollToBottom();
}

function addTypingBubble() {
  const row = document.createElement("div");
  row.className = "message-row assistant-row";
  row.id = "typingRow";

  const bubble = document.createElement("div");
  bubble.className = "bubble assistant-bubble typing-bubble";
  bubble.innerHTML = `
    <div class="typing-dots">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  `;

  const time = document.createElement("div");
  time.className = "message-time";
  time.textContent = "AI writing…";

  row.appendChild(bubble);
  row.appendChild(time);
  messages.appendChild(row);
  scrollToBottom();
}

function removeTypingBubble() {
  const typingRow = document.getElementById("typingRow");
  if (typingRow) typingRow.remove();
}

function setStatus(text) {
  statusText.textContent = text || "";
}

function escapeHtml(text) {
  return (text || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function formatTicketSummary(summary) {
  if (!summary) return "";

  const escaped = escapeHtml(summary.trim());
  const sections = escaped.split("\n\n");

  return sections
    .map((section) => {
      const lines = section.split("\n");
      const first = lines[0] || "";
      const rest = lines.slice(1);

      if (first === "Ticket Summary") {
        return `<div class="ticket-section-title">${first}</div>`;
      }

      if (
        first.startsWith("User:") ||
        first.startsWith("Email:") ||
        first.startsWith("Issue:") ||
        first.startsWith("Steps Attempted:") ||
        first.startsWith("Requested Action:")
      ) {
        const body = rest.length
          ? `<div class="ticket-section-body">${rest.join("<br>")}</div>`
          : "";

        return `
          <div class="ticket-section">
            <div class="ticket-section-label">${first}</div>
            ${body}
          </div>
        `;
      }

      return `<div class="ticket-section-body">${lines.join("<br>")}</div>`;
    })
    .join("");
}

function compactVideoHtml(videos) {
  if (!videos || !videos.length) return "";

  return `
    <div class="helper-links-wrap">
      <div class="helper-links-title">Helpful training videos</div>
      <div class="helper-links-subtitle">These short walkthroughs may help you complete the steps.</div>
      <div class="helper-links">
        ${videos
          .map(
            (video) => `
          <a class="helper-link" href="${video.url}" target="_blank" rel="noopener noreferrer">
            ${
              video.thumbnail
                ? `<img class="helper-thumb" src="${video.thumbnail}" alt="${video.title} thumbnail" />`
                : ""
            }
            <div class="helper-link-text">
              <div class="helper-link-title">${video.title}</div>
              <div class="helper-link-meta">Open video guide</div>
            </div>
          </a>
        `
          )
          .join("")}
      </div>
    </div>
  `;
}

function renderResolutionPrompt(ticketSummary, videos) {
  lastTicketSummary = ticketSummary || "";

  const html = `
    ${compactVideoHtml(videos)}
    <div class="resolution-box">
      <div class="resolution-question">Did this solve your issue?</div>
      <div class="action-row">
        <button class="secondary-button" onclick="markResolved(this)">Yes</button>
        <button class="primary-button" onclick="showEscalation(this)">No, escalate</button>
      </div>
    </div>
  `;

  addPanelMessage(html);
}

window.markResolved = function (button) {
  const box = button.closest(".resolution-box");
  if (!box) return;

  box.innerHTML = `<div class="ticket-success">Glad that helped.</div>`;
  scrollToBottom();
};

window.copyTicket = async function () {
  if (!lastTicketSummary) return;

  try {
    await navigator.clipboard.writeText(lastTicketSummary);
    setStatus("Ticket summary copied to clipboard.");
    setTimeout(() => setStatus(""), 1800);
  } catch {
    setStatus("Unable to copy summary on this device.");
    setTimeout(() => setStatus(""), 1800);
  }
};

window.toggleTicketDetails = function (button) {
  const parent = button.parentElement;
  const box = parent.querySelector(".ticket-box");
  if (!box) return;

  const isHidden = box.style.display === "none";
  box.style.display = isHidden ? "block" : "none";
  button.textContent = isHidden ? "Hide ticket details" : "See what was sent to IT";
  scrollToBottom();
};

window.showEscalation = function (button) {
  const box = button.closest(".resolution-box");
  if (!box) return;

  box.innerHTML = `
    <div class="ticket-success">Your ticket has been submitted to IT. A team member will review it shortly.</div>
    <div class="ticket-actions">
      <button class="secondary-button" onclick="copyTicket()">Copy summary</button>
      <button class="secondary-button" onclick="toggleTicketDetails(this)">See what was sent to IT</button>
      <div class="ticket-box" style="display:none;">
        ${formatTicketSummary(lastTicketSummary)}
      </div>
    </div>
  `;
  scrollToBottom();
};

async function askQuestion(promptOverride = null) {
  const query = (promptOverride || questionInput.value).trim();
  if (!query) {
    setStatus("Please enter an IT support question first.");
    return;
  }

  if (!promptOverride) questionInput.value = "";

  addTextMessage(query, "user");
  setStatus("AI analyzing…");

  try {
    await new Promise((resolve) => setTimeout(resolve, 450));
    setStatus("AI writing…");
    addTypingBubble();

    const userContext = {
      name: "Skyler Blood",
      email: "skyler@skylab.com"
    };

    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        query,
        user: userContext
      })
    });

    const data = await response.json();

    removeTypingBubble();
    setStatus("");

    if (data.blocked) {
      addTextMessage(data.answer || "That request was blocked.", "refusal");
    } else {
      addTextMessage(data.answer || "No answer returned.", "assistant");
    }

    renderResolutionPrompt(data.ticket_summary || "", data.videos || []);
  } catch (error) {
    removeTypingBubble();
    setStatus("");
    addTextMessage(
      "Something went wrong while contacting the help desk service. Please try again or escalate the issue.",
      "assistant"
    );
  }
}

askBtn.addEventListener("click", () => askQuestion());

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") askQuestion();
});

quickChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    askQuestion(chip.dataset.prompt || "");

    const chipSection = document.querySelector(".chip-section");
    if (chipSection) {
      chipSection.classList.add("collapsed");
    }
  });
});

resetBtn.addEventListener("click", () => {
  questionInput.value = "";
  setStatus("");
  lastTicketSummary = "";
  messages.innerHTML = "";

  const chipSection = document.querySelector(".chip-section");
  if (chipSection) {
    chipSection.classList.remove("collapsed");
  }

  addTextMessage(
    "Hi — I can help with common work device, email, login, and mobile access issues.",
    "assistant"
  );
});

minBtn.addEventListener("click", () => {
  chatWidget.classList.add("hidden");
  chatLauncher.classList.remove("hidden");
});

chatLauncher.addEventListener("click", () => {
  chatWidget.classList.remove("hidden");
  chatLauncher.classList.add("hidden");
});

addTextMessage(
  "Hi — I can help with common work device, email, login, and mobile access issues.",
  "assistant"
);

scrollToBottom();