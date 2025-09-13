const out = document.getElementById("out");
document.getElementById("search").onclick = async () => {
  const city = document.getElementById("city").value.trim();
  if (!city) { out.textContent = "Enter a city"; return; }
  out.textContent = "Loading...";
  const r = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
  out.textContent = await r.text();
};
document.getElementById("geo").onclick = () => {
  out.textContent = "Getting location...";
  navigator.geolocation.getCurrentPosition(async pos => {
    const { latitude, longitude } = pos.coords;
    const r = await fetch(`/api/weather?lat=${latitude}&lon=${longitude}`);
    out.textContent = await r.text();
  }, err => out.textContent = "Geolocation denied");
};