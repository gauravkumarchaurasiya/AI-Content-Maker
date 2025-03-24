const form = document.getElementById("video-form");
const outputDiv = document.getElementById("output");
const videoElement = document.getElementById("generated-video");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const topic = document.getElementById("topic").value;

    const formData = new FormData();
    formData.append("topic", topic);

    const response = await fetch("/generate_video/", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        const blob = await response.blob();
        const videoUrl = URL.createObjectURL(blob);
        videoElement.src = videoUrl;
        outputDiv.style.display = "block";
    } else {
        alert("Error generating video.");
    }
});

