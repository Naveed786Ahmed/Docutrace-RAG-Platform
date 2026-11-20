const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function sendChatMessage(question, signal) {
    const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
        signal,
    });

    if (!response.ok) {
        throw new Error(`Chat request failed: ${response.status}`);
    }

    return response.json();
}