
  const day = document.getElementById("today");

  const date = new Date();
  const month = date.toLocaleString("default", {
    month: "short",
  });
  
  const weekday = date.toLocaleDateString("default", { weekday: "short" });
  const year = date.getFullYear();

  day.innerText = `${date.getDate()} ${month} ${year}`;

  const active = document.getElementById("weekdaybadge");
  let closedTime = document.getElementById("time-closed");

  if (!(weekday === "Sun")) {
    active.innerText = "open now";
  } else {
    active.classList.remove("bg-success-light");
    active.classList.add("bg-danger-light");
    active.innerText = "closed";
    closedTime.innerText = "";
  }
