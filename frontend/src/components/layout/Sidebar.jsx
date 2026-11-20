import {
    BookOpen,
    MessageSquare,
    Plus,
    ShieldCheck,
    X,
} from "lucide-react";

export default function Sidebar({
    isOpen,
    onClose,
    onNewConversation,
    activePage,
    onNavigate,
}) {
    return (
        <>
            {isOpen && (
                <button
                    type="button"
                    aria-label="Close navigation"
                    onClick={onClose}
                    className="fixed inset-0 z-40 bg-slate-950/40 lg:hidden"
                />
            )}

            <aside
                className={`
          fixed inset-y-0 left-0 z-50
          flex w-72 flex-col
          border-r border-slate-200 bg-white
          transition-transform duration-200 ease-out
          lg:sticky lg:top-0 lg:h-dvh lg:w-64 lg:translate-x-0
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
            >
                <div className="flex h-20 shrink-0 items-center justify-between border-b border-slate-100 px-6">
                    <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-700 text-white">
                            <BookOpen size={21} />
                        </div>

                        <div>
                            <h1 className="text-lg font-bold tracking-tight text-slate-900">
                                DocuTrace
                            </h1>

                            <p className="text-[10px] font-medium tracking-wide text-slate-400">
                                KNOWLEDGE INTELLIGENCE
                            </p>
                        </div>
                    </div>

                    <button
                        type="button"
                        onClick={onClose}
                        aria-label="Close sidebar"
                        className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
                    >
                        <X size={20} />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto px-4 py-6">
                    <button onClick={onNewConversation} className="flex w-full items-center justify-center gap-2 rounded-xl bg-violet-700 px-4 py-3 text-sm font-semibold text-white transition hover:bg-violet-800">
                        <Plus size={17} />
                        New conversation
                    </button>

                    <p className="mb-3 mt-8 px-3 text-[11px] font-semibold uppercase tracking-widest text-slate-400">
                        Workspace
                    </p>

                    <nav className="space-y-1">
                        <button
                            type="button"
                            onClick={() => onNavigate("chat")}
                            aria-current={activePage === "chat" ? "page" : undefined}
                            className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left text-sm transition ${activePage === "chat"
                                    ? "bg-violet-50 font-semibold text-violet-700"
                                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                                }`}
                        >
                            <MessageSquare size={18} />
                            AI Assistant
                        </button>

                        <button
                            type="button"
                            onClick={() => onNavigate("knowledge")}
                            aria-current={activePage === "knowledge" ? "page" : undefined}
                            className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left text-sm transition ${activePage === "knowledge"
                                    ? "bg-violet-50 font-semibold text-violet-700"
                                    : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                                }`}
                        >
                            <BookOpen size={18} />
                            Knowledge Base
                        </button>
                    </nav>

                </div>

                <div className="shrink-0 border-t border-slate-100 p-5">
                    <div className="flex items-start gap-3 rounded-xl bg-slate-50 p-3">
                        <ShieldCheck
                            size={19}
                            className="mt-0.5 shrink-0 text-emerald-600"
                        />

                        <div>
                            <p className="text-xs font-semibold text-slate-800">
                                Evidence-grounded AI
                            </p>

                            <p className="mt-1 text-[11px] leading-relaxed text-slate-500">
                                Answers backed by company documents.
                            </p>
                        </div>
                    </div>
                </div>
            </aside>
        </>
    );
}