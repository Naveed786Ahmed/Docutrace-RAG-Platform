import { BookOpen, PanelLeft } from "lucide-react";

export default function Header({ onMenuClick, activePage }) {
    const isKnowledgePage = activePage === "knowledge";

    return (
        <header className="flex min-h-20 shrink-0 items-center justify-between gap-4 border-b border-slate-200 bg-white px-4 sm:px-6 lg:px-10">
            <div className="flex min-w-0 items-center gap-3">
                <button
                    type="button"
                    onClick={onMenuClick}
                    aria-label="Open navigation"
                    className="shrink-0 rounded-lg p-2 text-slate-600 transition hover:bg-slate-100 lg:hidden"
                >
                    <PanelLeft size={21} />
                </button>

                <div className="min-w-0">
                    <h2 className="text-sm font-semibold text-slate-900">
                        {isKnowledgePage
                            ? "Knowledge Base"
                            : "Knowledge Assistant"}
                    </h2>

                    <p className="mt-1 truncate text-xs text-slate-400">
                        {isKnowledgePage
                            ? "Browse and explore enterprise documents"
                            : "AcmeTech Solutions / Internal Knowledge Base"}
                    </p>
                </div>
            </div>

            <div className="hidden shrink-0 items-center gap-2 rounded-full border border-slate-200 px-3 py-2 text-xs font-medium text-slate-600 md:flex">
                <BookOpen size={14} className="text-violet-700" />
                AcmeTech Knowledge Base
            </div>
        </header>
    );
}