const $ = id => document.getElementById(id);
let sid = null, running = false, prevUrl = null, stream = null;

async function start() {
  $("btn-start").disabled = true;
  $("status").textContent = "Membuka kamera...";
  try {
    stream = await navigator.mediaDevices.getUserMedia(
      { video: { width: 1280, height: 720 }, audio: false });
    $("video").srcObject = stream;
  } catch (e) {
    $("status").textContent = "Kamera tidak bisa dibuka: " + e.message +
      " (butuh HTTPS atau localhost, dan izin kamera).";
    $("btn-start").disabled = false;
    return;
  }
  const res = await fetch("/api/start", { method: "POST" });
  const data = await res.json();
  if (!res.ok) {
    $("status").textContent = data.error;
    stopCamera();
    $("btn-start").disabled = false;
    return;
  }
  sid = data.sid; running = true;
  $("btn-start").hidden = true;
  ["btn-y", "btn-n", "btn-q"].forEach(id => $(id).hidden = false);
  $("view").hidden = false;
  $("status").textContent = "Menyambungkan...";
  loop();
}

async function loop() {
  const cv = $("canvas"), ctx = cv.getContext("2d");
  while (running) {
    ctx.drawImage($("video"), 0, 0, cv.width, cv.height);
    const blob = await new Promise(r => cv.toBlob(r, "image/jpeg", 0.7));
    let resp;
    try {
      resp = await fetch(`/api/frame/${sid}`, { method: "POST", body: blob,
                         headers: { "Content-Type": "image/jpeg" } });
    } catch (e) { $("status").textContent = "Koneksi terputus."; break; }
    if (!resp.ok) { $("status").textContent = "Sesi berakhir (tidak aktif terlalu lama atau server dimulai ulang)."; break; }

    const url = URL.createObjectURL(await resp.blob());
    $("view").src = url;
    if (prevUrl) URL.revokeObjectURL(prevUrl);
    prevUrl = url;
    $("status").textContent = "";

    if (resp.headers.get("X-Done") === "1") {
      const err = resp.headers.get("X-Error");
      $("status").textContent = err ? "Program berhenti karena error: " + err : "Selesai.";
      break;
    }
  }
  finish();
}

function finish() {
  running = false;
  stopCamera();
  ["btn-y", "btn-n", "btn-q"].forEach(id => $(id).hidden = true);
  $("btn-start").hidden = false; $("btn-start").disabled = false;
  $("btn-start").textContent = "Mulai lagi";
  if (sid) { fetch(`/api/stop/${sid}`, { method: "POST" }); sid = null; }
}

function stopCamera() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
}

function sendKey(k) {
  if (!sid) return;
  fetch(`/api/key/${sid}`, { method: "POST", headers: { "Content-Type": "application/json" },
                             body: JSON.stringify({ key: k }) });
}

$("btn-start").onclick = start;
$("btn-y").onclick = () => sendKey("y");
$("btn-n").onclick = () => sendKey("n");
$("btn-q").onclick = () => sendKey("q");
document.addEventListener("keydown", e => {
  if (["y", "n", "q"].includes(e.key.toLowerCase())) sendKey(e.key.toLowerCase());
});
window.addEventListener("pagehide", () => { if (sid) navigator.sendBeacon(`/api/stop/${sid}`); });
