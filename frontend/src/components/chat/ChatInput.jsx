import { useState } from "react";
import { ArrowUp } from "lucide-react";

export default function ChatInput({ onSend, disabled = false }) {
    const [question, setQuestion] = useState("");

    function handleSubmit(event) {
        event.preventDefault();

        const trimmed = question.trim();

        if (!trimmed || disabled) return;

        onSend(trimmed);
        setQuestion("");
    }

    return (
        <form onSubmit={handleSubmit} className="w-full">
            <div className="flex items-end gap-3 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm transition focus-within:border-violet-300 focus-within:ring-2 focus-within:ring-violet-100">
                <textarea
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    onKeyDown={(event) => {
                        if (event.key === "Enter" && !event.shiftKey) {
                            event.preventDefault();
                            handleSubmit(event);
                        }
                    }}
                    placeholder="Ask a question about your documents..."
                    rows={1}
                    maxLength={2000}
                    disabled={disabled}
                    aria-label="Your question"
                    className="max-h-36 min-h-11 flex-1 resize-none bg-transparent px-2 py-3 text-sm text-slate-800 outline-none placeholder:text-slate-400"
                />

                <button
                    type="submit"
                    disabled={!question.trim() || disabled}
                    aria-label="Send message"
                    className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-violet-700 text-white transition hover:bg-violet-800 disabled:cursor-not-allowed disabled:opacity-40"
                >
                    <ArrowUp size={19} />
                </button>
            </div>

            <p className="mt-3 text-center text-[11px] text-slate-400">
                Answers are generated from available company documentation.
            </p>
        </form>
    );
}