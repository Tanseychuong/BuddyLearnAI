const uploadForm = document.querySelector("#upload-form");
const uploadResult = document.querySelector("#upload-result");
const output = document.querySelector("#tool-output");
const roleSummary = document.querySelector("#role-summary");
const roleAction = document.querySelector("#role-action");
const workspaceEyebrow = document.querySelector("#workspace-eyebrow");
const workspaceTitle = document.querySelector("#workspace-title");
const workspaceCopy = document.querySelector("#workspace-copy");

const roleContent = {
  student: {
    summary: "Student workspace",
    action: "Student mode",
    eyebrow: "Student dashboard",
    title: "Turn course files into focused study sessions.",
    copy: "Upload notes, generate quizzes, create flashcards, and review exam patterns from one calm workspace.",
  },
  teacher: {
    summary: "Teacher workspace",
    action: "Teacher mode",
    eyebrow: "Teacher dashboard",
    title: "Prepare smarter practice from your class materials.",
    copy: "Organize course documents, create guided revision, and shape practice sessions around the topics students need most.",
  },
  admin: {
    summary: "Admin workspace",
    action: "Admin mode",
    eyebrow: "Admin dashboard",
    title: "Manage the learning platform without exposing tools to learners.",
    copy: "Review system health, verify routes, and keep backend controls separate from the student and teacher experience.",
  },
};

const endpoints = {
  "study-guide": {
    path: "/study-guides/generate",
    payload: { course_id: 1, topic: "Algorithms" },
  },
  quiz: {
    path: "/quizzes/generate",
    payload: { course_id: 1, question_types: ["mcq"], difficulty: "mixed", question_count: 5 },
  },
  flashcards: {
    path: "/flashcards/generate",
    payload: { course_id: 1, topic: "Dynamic programming", count: 5 },
  },
  recommendations: {
    path: "/recommendations",
    payload: { course_id: 1 },
  },
};

async function postJson(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Request failed with ${response.status}`);
  }

  return response.json();
}

function setRole(role) {
  const content = roleContent[role];

  roleSummary.textContent = content.summary;
  roleAction.textContent = content.action;
  workspaceEyebrow.textContent = content.eyebrow;
  workspaceTitle.textContent = content.title;
  workspaceCopy.textContent = content.copy;

  document.querySelectorAll(".role-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.role === role);
  });

  document.querySelectorAll("[data-admin-only]").forEach((element) => {
    element.hidden = role !== "admin";
  });
}

function renderStudyResult(action, data) {
  const renderers = {
    "study-guide": () => `
      <strong>${data.title}</strong>
      <span>${data.status.replaceAll("_", " ")}</span>
      <ul>${data.sections.map((section) => `<li>${section}</li>`).join("")}</ul>
    `,
    quiz: () => `
      <strong>Quiz generated</strong>
      <span>${data.difficulty} difficulty for course ${data.course_id}</span>
      <ul>${data.questions.map((question) => `<li>${question.prompt}</li>`).join("")}</ul>
    `,
    flashcards: () => `
      <strong>Flashcards ready</strong>
      <ul>${data.flashcards.map((card) => `<li>${card.front} ${card.back}</li>`).join("")}</ul>
    `,
    recommendations: () => `
      <strong>Recommended next steps</strong>
      <ul>${data.recommendations.map((item) => `<li>${item.title}: ${item.reason}</li>`).join("")}</ul>
    `,
  };

  output.innerHTML = renderers[action]();
}

document.querySelectorAll(".role-button").forEach((button) => {
  button.addEventListener("click", () => setRole(button.dataset.role));
});

document.querySelectorAll("[data-action]").forEach((button) => {
  button.addEventListener("click", async () => {
    const action = button.dataset.action;
    const endpoint = endpoints[action];

    output.textContent = "Preparing study result...";
    try {
      const data = await postJson(endpoint.path, endpoint.payload);
      renderStudyResult(action, data);
    } catch (error) {
      output.textContent = error.message;
    }
  });
});

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(uploadForm);
  uploadResult.textContent = "Uploading...";

  try {
    const response = await fetch("/uploads", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed with ${response.status}`);
    }

    const data = await response.json();
    uploadResult.textContent = `${data.filename} queued for processing.`;
  } catch (error) {
    uploadResult.textContent = error.message;
  }
});

setRole("student");
