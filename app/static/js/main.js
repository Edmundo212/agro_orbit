async function getJSON(url, opts) {
  const r = await fetch(url, opts);
  if (!r.ok) throw new Error("Error " + r.status);
  return r.json();
}
function postJSON(url, body) {
  return getJSON(url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
}
const fmtFecha = s => new Date(s).toLocaleString("es-PE", {dateStyle: "short", timeStyle: "short"});
