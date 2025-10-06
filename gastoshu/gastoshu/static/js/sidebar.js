/*document.addEventListener('DOMContentLoaded', function () {
  toggleSidebar();
})*/

function toggleSidebar() {
  //Variables del conteido y el id
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");
  //Cancelar si no se encuentran
  if (!sidebar || !content) return; // Salir si no existe el sidebar

  const labels = document.querySelectorAll(".sidebar-label");
  const title = document.getElementById("sidebar-title");
  const isExpanded = sidebar.getAttribute("data-expanded") === "true";
  const esMobil = window  .innerwidth < 800;
  const toggle = document.getElementById("toggle");

  // Alternar clases y atributos
  if (esMobil) {
    if (!isExpanded) {
      sidebar.style.backgroundColor = "background: rgba(255, 255, 255, 0);";
    }
  } else {
    if (isExpanded) {
      sidebar.classList.replace("w-64", "w-16");
      labels.forEach((label) => label.classList.add("hidden"));
      if (title) title.classList.add("hidden");
      content.classList.replace("md:ml-64", "md:ml-16");
    } else {
      sidebar.classList.replace("w-16", "w-64");
      labels.forEach((label) => label.classList.remove("hidden"));
      if (title) title.classList.remove("hidden");
      content.classList.replace("md:ml-16", "md:ml-64");
    }
  }

  // Actualizar estado
  sidebar.setAttribute("data-expanded", String(!isExpanded));
}
