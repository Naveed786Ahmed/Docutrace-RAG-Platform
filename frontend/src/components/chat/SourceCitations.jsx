import { FileText, BookOpen } from "lucide-react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getDocumentUrl(citation) {
    const department = encodeURIComponent(citation.department);
    const filename = encodeURIComponent(citation.source_file);

    return (
        `${API_BASE_URL}/documents/${department}/${filename}` +
        `#page=${citation.page_number}`
    );
}

export default function SourceCitations({ citations = [] }) {
    if (!citations.length) return null;

    return (
        <section className="mt-6 border-t border-slate-200 pt-5">
            <div className="mb-4 flex items-center gap-2">
                <BookOpen size={16} className="text-violet-600" />

                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    Supporting Sources
                </h4>

                <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-500">
                    {citations.length}
                </span>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
                {citations.map((citation) => (
                    <a
                        key={`${citation.source_id}-${citation.source_file}-${citation.page_number}`}
                        href={getDocumentUrl(citation)}
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label={`Open ${citation.source_file} at page ${citation.page_number}`}
                        className="block rounded-xl border border-slate-200 bg-white p-4 transition hover:border-violet-300 hover:shadow-sm focus-visible:outline-2 focus-visible:outline-violet-600"
                    >
                        <div className="flex items-start gap-3">
                            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-violet-50 text-violet-700">
                                <FileText size={19} />
                            </div>

                            <div className="min-w-0 flex-1">
                                <p className="mb-1 text-[11px] font-semibold text-violet-700">
                                    Source {citation.source_id}
                                </p>

                                <p
                                    title={citation.source_file}
                                    className="truncate text-sm font-semibold text-slate-900"
                                >
                                    {citation.source_file}
                                </p>

                                <p className="mt-1 text-xs text-slate-500">
                                    {citation.department?.replaceAll("_", " ")}
                                </p>

                                <p className="mt-3 text-xs font-medium text-slate-600">
                                    Page {citation.page_number}
                                </p>
                            </div>
                        </div>
                    </a>
                ))}
            </div>
        </section>
    );
}