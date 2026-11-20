import {
    ArrowUpRight,
    BookOpenText,
    FileSearch,
    ShieldCheck,
    Sparkles,
} from "lucide-react";

const suggestions = [
    {
        id: "Q096",
        icon: FileSearch,
        title: "Support Operations",
        category: "CUSTOMER SUPPORT",
        question:
            "After how long should an unresolved P1 ticket be escalated to Tier 2?",
    },
    {
        id: "Q045",
        icon: ShieldCheck,
        title: "Security & Compliance",
        category: "SECURITY",
        question:
            "What multi-factor authentication methods are permitted at AcmeTech, and which is explicitly not allowed?",
    },
    {
        id: "Q001",
        icon: BookOpenText,
        title: "People & Policies",
        category: "HUMAN RESOURCES",
        question:
            "How long is the probationary period for new hires at AcmeTech?",
    },
];

export default function WelcomeScreen({ onSuggestionClick }) {
    return (
        <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-5 py-10 sm:px-8 sm:py-14 lg:px-12">
            <div className="mb-7 flex h-14 w-14 items-center justify-center rounded-2xl border border-violet-100 bg-violet-50 text-violet-700">
                <Sparkles size={26} strokeWidth={1.7} />
            </div>

            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-violet-700">
                Enterprise Knowledge Intelligence
            </p>

            <h1 className="max-w-2xl text-3xl font-semibold leading-tight tracking-tight text-slate-900 sm:text-4xl lg:text-[42px]">
                Find answers across your company knowledge.
            </h1>

            <p className="mt-5 max-w-2xl text-sm leading-7 text-slate-500 sm:text-base">
                Ask questions about internal policies, operational procedures, and
                product documentation. Get answers grounded in your knowledge base,
                with references to the original documents.
            </p>

            <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
                {suggestions.map(({ id, icon: Icon, title, category, question }) => (
                    <button
                        key={id}
                        type="button"
                        onClick={() => onSuggestionClick(question)}
                        className="group flex min-h-56 min-w-0 flex-col rounded-2xl border border-slate-200 bg-white p-5 text-left transition-all duration-200 hover:-translate-y-0.5 hover:border-violet-300 hover:shadow-md hover:shadow-slate-200/50 focus-visible:outline-2 focus-visible:outline-violet-600"
                    >
                        <div className="mb-6 flex items-center justify-between">
                            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-700">
                                <Icon size={20} strokeWidth={1.8} />
                            </div>

                            <ArrowUpRight
                                size={17}
                                className="text-slate-400 transition group-hover:text-violet-700"
                            />
                        </div>

                        <p className="text-[10px] font-semibold tracking-widest text-slate-400">
                            {category}
                        </p>

                        <h3 className="mt-2 text-sm font-semibold text-slate-900">
                            {title}
                        </h3>

                        <p className="mt-2 text-xs leading-5 text-slate-500">
                            {question}
                        </p>
                    </button>
                ))}
            </div>
        </div>
    );
}