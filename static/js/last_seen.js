try {
  // Listen for navigation events
  window.addEventListener("beforeunload", function (event) {
    $.ajax({
      type: "get",
      url: "/auth/last_seen/update",
    });
  });
} catch (error) {
  console.error(error);
}
