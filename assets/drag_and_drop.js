function handleDragStart(e) {
  e.dataTransfer.setData("text/plain", e.target.id);
}
function handleDrop(e) {
  e.preventDefault();
  const shapeId = e.dataTransfer.getData("text/plain");
  const grid = document.getElementById("grid");
  const rect = grid.getBoundingClientRect();
  const offsetX = e.clientX - rect.left;
  const offsetY = e.clientY - rect.top;

  const newShape = document.createElement("div");
  newShape.classList.add("shape", shapeId);
  newShape.style.position = "absolute";
  newShape.style.left = offsetX + "px";
  newShape.style.top = offsetY + "px";

  grid.appendChild(newShape);
}
function handleDragOver(e) {
  e.preventDefault();
}
document.querySelectorAll(".shape").forEach((el) => {
  el.addEventListener("dragstart", handleDragStart);
});
const grid = document.getElementById("grid");
grid.addEventListener("drop", handleDrop);
grid.addEventListener("dragover", handleDragOver);
