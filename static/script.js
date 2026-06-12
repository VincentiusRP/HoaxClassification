async function predictHoax() {
  const title = document.getElementById("titleInput").value.trim();
  const resultDiv = document.getElementById("result");
  const errorDiv = document.getElementById("errorMsg");
  const btn = document.getElementById("predictBtn");

  errorDiv.classList.add("hidden");
  resultDiv.classList.add("hidden");

  if (!title) {
    errorDiv.textContent = "Mohon masukkan judul artikel.";
    errorDiv.classList.remove("hidden");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Memproses...";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Terjadi kesalahan");
    }

    document.getElementById("resultLabel").textContent =
      data.label_id === 1 ? "⚠️ HOAX" : "✅ NON-HOAX (VALID)";
    document.getElementById("resultConfidence").textContent =
      `Tingkat keyakinan: ${data.confidence}%`;

    document.getElementById("probValid").textContent = data.probabilities["Non-Hoax (Valid)"] + "%";
    document.getElementById("probHoax").textContent = data.probabilities["Hoax"] + "%";

    document.getElementById("barValid").style.width = data.probabilities["Non-Hoax (Valid)"] + "%";
    document.getElementById("barHoax").style.width = data.probabilities["Hoax"] + "%";

    resultDiv.classList.remove("hidden", "hoax", "valid");
    resultDiv.classList.add(data.label_id === 1 ? "hoax" : "valid");

  } catch (err) {
    errorDiv.textContent = err.message;
    errorDiv.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    btn.textContent = "Prediksi";
  }
}
