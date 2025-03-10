const RECT_WIDTH = 150;
const RECT_HEIGHT = 100;
const SNAP_DISTANCE = 60;
const MATRIX_SIZE = 4; // 4x4 matrix

// Initialize stage and layers
const stage = new Konva.Stage({
  container: "container",
  width: window.innerWidth - 600,
  height: window.innerHeight,
});

const mainLayer = new Konva.Layer();
const leftMenuStage = new Konva.Stage({
  container: "left-menu",
  width: 400,
  height: window.innerHeight,
});

const leftMenuLayer = new Konva.Layer();

// Create a 4x4 matrix of drop zones
const dropZones = [];
const totalHeight = MATRIX_SIZE * (RECT_HEIGHT + 40) - 20; // Total height of the matrix
const startY = (stage.height() - totalHeight) / 2; // Calculate starting Y position to center vertically

for (let row = 0; row < MATRIX_SIZE; row++) {
  for (let col = 0; col < MATRIX_SIZE; col++) {
    dropZones.push({
      x:
        col * (RECT_WIDTH + 40) +
        (stage.width() - MATRIX_SIZE * (RECT_WIDTH + 40)) / 2, // Center horizontally
      y: startY + row * (RECT_HEIGHT + 40), // Center vertically
    });
  }
}
// Array to track dropped rectangles
const droppedRects = new Array(dropZones.length).fill(null);

// Create source rectangles in left menu
const sourceRects = [
  { id: "pipette", color: "#FF6961", text: "96 Well Plate" },
  { id: "pick-and-place", color: "#B3EBF2", text: "1000 uL Pipette Tip" },
  { id: "use-equipment", color: "#80EF80", text: "2.5 mL Vial" },
];

// Draw drop zones
dropZones.forEach((zone, i) => {
  const dropZone = new Konva.Rect({
    x: zone.x,
    y: zone.y,
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    stroke: "#999",
    strokeWidth: 2,
    dash: [5, 5],
    id: `dropZone-${i}`, // Assign an ID for later reference
  });
  mainLayer.add(dropZone);
});

// Create draggable rectangles in left menu
sourceRects.forEach((rect, i) => {
  const group = new Konva.Group({
    x: 50, // Center horizontally in the left menu
    y: 20 + i * 120, // Spacing between rectangles
    draggable: false, // Prevent dragging the original rectangle
    id: rect.id,
    name: "source",
  });

  const rectangle = new Konva.Rect({
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    fill: rect.color,
    stroke: "#000",
    strokeWidth: 1,
  });

  const text = new Konva.Text({
    text: rect.text,
    fontSize: 14,
    width: RECT_WIDTH,
    height: RECT_HEIGHT,
    align: "center",
    verticalAlign: "middle",
    fill: "#000",
  });

  group.add(rectangle);
  group.add(text);

  // Listen for mousedown to create a clone
  group.on("mousedown", function (e) {
    const pointerPosition = stage.getPointerPosition();

    const clone = group.clone({
      x: pointerPosition.x - RECT_WIDTH / 2,
      y: pointerPosition.y - RECT_HEIGHT / 2,
      draggable: true,
      name: "clone",
    });

    mainLayer.add(clone);
    clone.moveToTop();
    clone.startDrag();
    setupDragHandlers(clone);
  });

  leftMenuLayer.add(group);
});

// Function to handle dragging and dropping
function setupDragHandlers(rect) {
  rect.off("mousedown");

  rect.on("dragmove", function () {
    const pos = this.position();
    let isSnapping = false;

    // Check if the rectangle is within the snap range of any drop zone
    for (let i = 0; i < dropZones.length; i++) {
      const zone = dropZones[i];
      const distance = Math.sqrt(
        Math.pow(pos.x - zone.x, 2) + Math.pow(pos.y - zone.y, 2)
      );

      const dropZone = mainLayer.findOne(`#dropZone-${i}`); // Get the drop zone

      if (distance < SNAP_DISTANCE) {
        // Highlight the drop zone to indicate snapping
        dropZone.fill("	rgb(211, 211, 211)"); // Light green fill for snapping
        dropZone.strokeWidth(4); // Make the border thicker
        isSnapping = true;

        if (droppedRects[i] && droppedRects[i] !== this) {
          this.moveToTop();
        }
      } else {
        // Reset the drop zone style if not snapping
        dropZone.fill(null); // Reset fill
        dropZone.stroke("#999"); // Reset stroke color
        dropZone.strokeWidth(2); // Reset stroke width
      }
    }

    mainLayer.batchDraw(); // Redraw the layer to apply changes
  });

  rect.on("dragend", function () {
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

    // Reset drop zone styles after dragging ends
    dropZones.forEach((zone, i) => {
      const dropZone = mainLayer.findOne(`#dropZone-${i}`);
      dropZone.fill(null); // Reset fill
      dropZone.stroke("#999"); // Reset stroke color
      dropZone.strokeWidth(2); // Reset stroke width
    });

    mainLayer.batchDraw(); // Redraw the layer to apply changes
  });

  rect.on("click", function () {
    handleBlockClick(this);
  });
}

function handleBlockClick(group) {
  const blockId = group.attrs.id;
  const pipetteForm = document.getElementById("pipette-form");
  const pickAndPlaceForm = document.getElementById("pick-and-place-form");
  const useEquipmentForm = document.getElementById("use-equipment-form");

  if (blockId == "pipette") {
    pipetteForm.style.display = "flex";
    pickAndPlaceForm.style.display = "none";
    useEquipmentForm.style.display = "none";
  } else if (blockId == "pick-and-place") {
    pipetteForm.style.display = "none";
    pickAndPlaceForm.style.display = "flex";
    useEquipmentForm.style.display = "none";
  } else if (blockId == "use-equipment") {
    pipetteForm.style.display = "none";
    pickAndPlaceForm.style.display = "none";
    useEquipmentForm.style.display = "flex";
  }
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
  rightMenu.classList.toggle("collapsed");
  button.textContent = rightMenu.classList.contains("collapsed") ? "←" : "→";

  // Show or hide the rectangle info based on the menu state
  const rectangleInfo = document.getElementById("rectangle-info");
  if (rightMenu.classList.contains("collapsed")) {
    rectangleInfo.style.display = "none"; // Hide info
  } else {
    rectangleInfo.style.display = "block"; // Show info
  }

  updateStageSize();
}

function updateStageSize() {
  const leftMenu = document.getElementById("left-menu");
  const rightMenu = document.getElementById("right-menu");
  const leftWidth = leftMenu.classList.contains("collapsed") ? 50 : 200;
  const rightWidth = rightMenu.classList.contains("collapsed") ? 50 : 250;

  stage.width(window.innerWidth - leftWidth - rightWidth);
  stage.batchDraw();
}

window.addEventListener("resize", () => {
  updateStageSize();
});
