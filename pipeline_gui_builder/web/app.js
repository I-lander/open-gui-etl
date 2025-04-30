let pipeline = [];

function addBlock(value, code) {
  if (value) {
    pipeline.push({ type: value, code: code ?? "" });
    renderPipeline();
  }
}

function removeBlock(index) {
  pipeline.splice(index, 1);
  renderPipeline();
}

let draggedIndex = null;

function renderPipeline() {
  const list = document.getElementById("pipelineList");
  list.innerHTML = "";

  pipeline.forEach((block, index) => {
    const li = document.createElement("li");
    li.textContent = block.type + " ";
    li.draggable = true;

    li.addEventListener("dragstart", () => {
      draggedIndex = index;
    });

    li.addEventListener("dragover", (e) => {
      e.preventDefault();
      li.style.borderTop = "2px solid #000";
    });

    li.addEventListener("dragleave", () => {
      li.style.borderTop = "";
    });

    li.addEventListener("drop", () => {
      if (draggedIndex !== null && draggedIndex !== index) {
        const draggedItem = pipeline[draggedIndex];
        pipeline.splice(draggedIndex, 1);
        pipeline.splice(index, 0, draggedItem);
        renderPipeline();
      }
      li.style.borderTop = "";
    });

    const btnContainer = document.createElement("div");

    const upBtn = document.createElement("button");
    const upIcon = document.createElement("span");
    upIcon.className = "icon-up";
    upBtn.appendChild(upIcon);

    upBtn.onclick = () => {
      if (index > 0) {
        [pipeline[index - 1], pipeline[index]] = [
          pipeline[index],
          pipeline[index - 1],
        ];
        renderPipeline();
      }
    };
    btnContainer.appendChild(upBtn);

    const downBtn = document.createElement("button");
    const downIcon = document.createElement("span");
    downIcon.className = "icon-down";
    downBtn.appendChild(downIcon);
    downBtn.onclick = () => {
      if (index < pipeline.length - 1) {
        [pipeline[index + 1], pipeline[index]] = [
          pipeline[index],
          pipeline[index + 1],
        ];
        renderPipeline();
      }
    };
    btnContainer.appendChild(downBtn);

    const delBtn = document.createElement("button");
    const delIcon = document.createElement("span");
    delIcon.className = "icon-close";
    delBtn.appendChild(delIcon);
    delBtn.onclick = () => removeBlock(index);
    btnContainer.appendChild(delBtn);

    li.appendChild(btnContainer);
    list.appendChild(li);
  });
}

function generate() {
  if (window.pywebview) {
    const generateLocalFiles =
      document.getElementById("generateLocalFiles").checked;

    window.pywebview.api.choose_output_path().then((path) => {
      if (path) {
        window.pywebview.api
          .generate_script(pipeline, path, generateLocalFiles)
          .then((savedPath) => {
            alert("Script saved at: " + savedPath);
          });
      }
    });
  } else {
    alert("pywebview not available");
  }
}

window.addEventListener("pywebviewready", () => {
  window.pywebview.api.get_block_categories().then((categories) => {
    buildSidebarFromCategories(categories);
  });
});

function buildSidebarFromCategories(categories) {
  const container = document.getElementById("dynamic-categories");
  container.innerHTML = "";

  for (const categoryName in categories) {
    const blocks = categories[categoryName];

    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category";

    const title = document.createElement("h3");
    title.textContent = categoryName;
    title.style.cursor = "pointer";

    const buttonsDiv = document.createElement("div");
    buttonsDiv.className = "buttons";
    buttonsDiv.style.display = "none";

    title.onclick = () => {
      buttonsDiv.style.display =
        buttonsDiv.style.display === "block" ? "none" : "block";
    };

    blocks.forEach((block) => {
      const btnContainer = document.createElement("div");
      const btn = document.createElement("button");
      btn.textContent = block.label;
      btn.onclick = () => addBlock(block.id, block.code);
      const descrition = document.createElement("p");
      descrition.innerHTML = block.description;
      btnContainer.appendChild(btn);
      btnContainer.appendChild(descrition);
      btnContainer.className = "button-container";
      buttonsDiv.appendChild(btnContainer);
    });

    categoryDiv.appendChild(title);
    categoryDiv.appendChild(buttonsDiv);
    container.appendChild(categoryDiv);
  }
}
