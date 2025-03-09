const RECT_WIDTH = 100;
const RECT_HEIGHT = 60;
const SNAP_DISTANCE = 60;
const VERTICAL_GAP = 40; // Gap between boxes for arrows
const MAX_POSITIONS = 10; // Or any maximum limit you want to set

// Initialize stage and layers
const stage = new Konva.Stage({
  container: "container",
  width: window.innerWidth - 400,
  height: window.innerHeight,
});

const mainLayer = new Konva.Layer();
const leftMenuStage = new Konva.Stage({
  container: "left-menu",
  width: 200,
  height: window.innerHeight,
});

const leftMenuLayer = new Konva.Layer();

// Create drop zones
const dropZones = [
  { x: (stage.width() - RECT_WIDTH) / 2, y: 100 }, // Center horizontally
  { x: (stage.width() - RECT_WIDTH) / 2, y: 200 },
  { x: (stage.width() - RECT_WIDTH) / 2, y: 300 },
  { x: (stage.width() - RECT_WIDTH) / 2, y: 400 },
  { x: (stage.width() - RECT_WIDTH) / 2, y: 500 },
];

const droppedRects = new Array(dropZones.length).fill(null);

// Create source rectangles in left menu
const sourceRects = [
  { id: "pipette", color: "#FF6961", text: "Pipette" },
  { id: "pick-and-place", color: "#B3EBF2", text: "Pick and Place" },
  { id: "use-equipment", color: "#80EF80", text: "Use Equipment" },
];

// Draw drop zones and arrows
dropZones.forEach((zone, i) => {
  // Create dotted rectangle
  const dropZone = new Konva.Rect({
    x: zone.x,
    y: zone.y,
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    stroke: "#999",
    strokeWidth: 2,
    dash: [5, 5],
  });
  mainLayer.add(dropZone);

  // Create arrow if not last zone
  if (i < dropZones.length - 1) {
    const nextZone = dropZones[i + 1];
    const arrow = new Konva.Arrow({
      points: [
        zone.x + RECT_WIDTH / 2, // start x (middle of current box)
        zone.y + RECT_HEIGHT, // start y (bottom of current box)
        zone.x + RECT_WIDTH / 2, // end x (middle of next box)
        nextZone.y, // end y (top of next box)
      ],
      stroke: "#999",
      strokeWidth: 2,
      fill: "#999",
      pointerLength: 10,
      pointerWidth: 10,
    });
    mainLayer.add(arrow);
  }
});

// Create draggable rectangles in left menu
sourceRects.forEach((rect, i) => {
  // Create a group to combine the rectangle and text
  const group = new Konva.Group({
    x: 50, // Center horizontally in the left menu
    y: 20 + i * 100, // Spacing between rectangles
    draggable: false, // Prevent dragging the original rectangle
    id: rect.id,
    name: "source", // Add a name to identify source rectangles
  });

  // Create the rectangle
  const rectangle = new Konva.Rect({
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    fill: rect.color,
    stroke: "#000",
    strokeWidth: 1,
  });

  // Create the text
  const text = new Konva.Text({
    text: rect.text,
    fontSize: 14,
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    align: "center",
    verticalAlign: "middle",
    fill: "#000",
  });

  // Add the rectangle and text to the group
  group.add(rectangle);
  group.add(text);

  // Listen for mousedown to create a clone
  group.on("mousedown", function (e) {
    const pointerPosition = stage.getPointerPosition();

    // Create a new clone at the cursor's position, offset to center the rectangle
    const clone = group.clone({
      x: pointerPosition.x - RECT_WIDTH / 2,
      y: pointerPosition.y - RECT_HEIGHT / 2,
      draggable: true,
      name: "clone", // Add a name to identify clones
    });

    // Add the clone to the main layer
    mainLayer.add(clone);
    clone.moveToTop();
    clone.startDrag(); // Start dragging the clone immediately
    setupDragHandlers(clone); // Set up drag-and-drop behavior for the clone
  });

  leftMenuLayer.add(group);
});

// Add button for new position
function addNewPosition() {
  if (dropZones.length >= MAX_POSITIONS) return;

  const lastZone = dropZones[dropZones.length - 1];
  const newY = lastZone.y + 100; // Space for new position
  const newX = lastZone.x;

  // Add new drop zone
  const newZone = { x: newX, y: newY };
  dropZones.push(newZone);
  droppedRects.push(null);

  // Create new dotted rectangle
  const dropZone = new Konva.Rect({
    x: newZone.x,
    y: newZone.y,
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    stroke: "#999",
    strokeWidth: 2,
    dash: [5, 5],
  });
  mainLayer.add(dropZone);

  // Add arrow from previous last position to new position
  const arrow = new Konva.Arrow({
    points: [
      lastZone.x + RECT_WIDTH / 2,
      lastZone.y + RECT_HEIGHT,
      newZone.x + RECT_WIDTH / 2,
      newZone.y,
    ],
    stroke: "#999",
    strokeWidth: 2,
    fill: "#999",
    pointerLength: 10,
    pointerWidth: 10,
  });
  mainLayer.add(arrow);

  // Update add button position
  addButton.y(newY + RECT_HEIGHT + 20);

  // Dynamically resize the stage if the new position exceeds the current height
  const requiredHeight = newY + RECT_HEIGHT + 60; // Add some padding
  if (requiredHeight > stage.height()) {
    stage.height(requiredHeight); // Increase the stage height
  }

  mainLayer.batchDraw();
}

// Create add button
const addButton = new Konva.Label({
  x: dropZones[dropZones.length - 1].x,
  y: dropZones[dropZones.length - 1].y + RECT_HEIGHT + 20,
});

addButton.add(
  new Konva.Tag({
    fill: "#ddd",
    stroke: "#999",
    strokeWidth: 1,
    padding: 10,
    cornerRadius: 5,
  })
);

addButton.add(
  new Konva.Text({
    text: "+ Add",
    padding: 5,
    fontSize: 14,
    fill: "#333",
  })
);

addButton.on("click", addNewPosition);
mainLayer.add(addButton);

function setupDragHandlers(group) {
  // Remove any existing mousedown listeners to prevent cloning
  group.off("mousedown");

  group.on("dragend", function () {
    const pos = this.position();
    let snapped = false;

    // Find the current index of this rectangle in the droppedRects array
    const currentIndex = droppedRects.indexOf(this);

    // Check if the rectangle is within the snap range of any drop zone
    for (let i = 0; i < dropZones.length; i++) {
      const zone = dropZones[i];
      const distance = Math.sqrt(
        Math.pow(pos.x - zone.x, 2) + Math.pow(pos.y - zone.y, 2)
      );

      if (distance < SNAP_DISTANCE) {
        // If there's already a rectangle in this drop zone, replace it
        if (droppedRects[i] && droppedRects[i] !== this) {
          droppedRects[i].destroy(); // Remove the existing rectangle
        }

        // Snap the rectangle to the drop zone
        this.position({
          x: zone.x,
          y: zone.y,
        });

        // Update the droppedRects array
        if (currentIndex !== -1) {
          droppedRects[currentIndex] = null; // Clear the old position
        }
        droppedRects[i] = this; // Set the new position
        snapped = true;
        break;
      }
    }

    if (!snapped) {
      // If the rectangle is not snapped to any drop zone, delete it
      if (currentIndex !== -1) {
        droppedRects[currentIndex] = null; // Clear the old position
      }
      this.destroy();
    }

    mainLayer.batchDraw();
  });
}

// Add layers to stages
stage.add(mainLayer);
leftMenuStage.add(leftMenuLayer);

// Menu collapse functionality
function toggleLeftMenu() {
  const leftMenu = document.getElementById("left-menu");
  leftMenu.classList.toggle("collapsed");
  const button = leftMenu.querySelector("button");
  button.textContent = leftMenu.classList.contains("collapsed") ? "→" : "←";
  updateStageSize();
}

function toggleRightMenu() {
  const rightMenu = document.getElementById("right-menu");
  const button = rightMenu.querySelector("button");
  const menuButtons = document.getElementById("menu-buttons");

  rightMenu.classList.toggle("collapsed");
  button.textContent = rightMenu.classList.contains("collapsed") ? "←" : "→";

  // Show or hide the buttons based on the menu state
  if (rightMenu.classList.contains("collapsed")) {
    menuButtons.style.display = "none";
  } else {
    menuButtons.style.display = "flex";
  }

  updateStageSize();
}

function updateStageSize() {
  const leftMenu = document.getElementById("left-menu");
  const rightMenu = document.getElementById("right-menu");
  const leftWidth = leftMenu.classList.contains("collapsed") ? 50 : 200;
  const rightWidth = rightMenu.classList.contains("collapsed") ? 50 : 200;

  stage.width(window.innerWidth - leftWidth - rightWidth);

  stage.batchDraw();
}

// Handle window resize
window.addEventListener("resize", () => {
  updateStageSize();
});
